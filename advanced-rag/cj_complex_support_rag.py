import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
import json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from sklearn.decomposition import PCA
import time

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SimpleRAGComparison:
    def __init__(self, pdf_path: str):
        """Initialize the RAG comparison system."""
        print("📚 Setting up RAG comparison system...")
        self.setup_document_processing(pdf_path)
        self.setup_vector_store()
        
    def setup_document_processing(self, pdf_path: str):
        """Set up document processing pipeline."""
        reader = PdfReader(pdf_path)
        pdf_texts = [p.extract_text().strip() for p in reader.pages]
        pdf_texts = [text for text in pdf_texts if text]
        
        # Text splitting configuration
        character_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ". ", " ", ""],
            chunk_size=1000,
            chunk_overlap=0
        )
        character_split_texts = character_splitter.split_text("\n\n".join(pdf_texts))
        
        token_splitter = SentenceTransformersTokenTextSplitter(
            chunk_overlap=0,
            tokens_per_chunk=256
        )
        
        self.token_split_texts = []
        for text in character_split_texts:
            self.token_split_texts += token_splitter.split_text(text)
        
        print(f"✅ Processed {len(self.token_split_texts)} text chunks")
            
    def setup_vector_store(self):
        """Set up the vector store with ChromaDB."""
        self.embedding_function = SentenceTransformerEmbeddingFunction()
        self.chroma_client = chromadb.Client()
        self.chroma_collection = self.chroma_client.create_collection(
            f"cj-complex-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            embedding_function=self.embedding_function
        )
        
        ids = [str(i) for i in range(len(self.token_split_texts))]
        self.chroma_collection.add(ids=ids, documents=self.token_split_texts)
        print(f"✅ Added {len(self.token_split_texts)} documents to vector store")

    def generate_multi_query(self, query: str, model: str = "o4-mini") -> List[str]:
        """Generate multiple related queries."""
        prompt = """Du er en AI-kundeservicemedarbejder hos CJ Complex, et marketing servicefirma.
        Givet en kundes spørgsmål, generer 3-4 relaterede spørgsmål, der vil hjælpe med at give
        omfattende information fra vores vidensbase. Fokuser på spørgsmål der:
        
       1. Være klart, kortfattet og professionelt
        2. Kun bruge information fra den givne kontekst
        3. Opretholde CJ Complex's professionelle tone
        4. Inkludere specifikke detaljer når de er tilgængelige
        5. Anerkende hvis bestemt information ikke er tilgængelig i konteksten
        
        Formater hvert spørgsmål på en separat linje uden nummerering.
        Hold spørgsmålene korte og fokuserede på enkelte emner."""

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": query}
        ]

        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        expanded_queries = [q.strip() for q in response.choices[0].message.content.split('\n') if q.strip()]
        return expanded_queries[:4]

    def generate_support_response(self, context: List[str], question: str, model: str = "o4-mini") -> str:
        """Generate response using retrieved context."""
        limited_context = context[:2]
        context_text = "\n\n".join(limited_context)
        
        prompt = f"""Du er en AI-kundeservicemedarbejder hos CJ Complex. Brug den givne kontekst til at besvare
        kundens spørgsmål professionelt og præcist. Vær kortfattet og direkte.
        
        Kontekst:
        {context_text}
        
        Spørgsmål: {question}"""

        messages = [{"role": "system", "content": prompt}]
        response = client.chat.completions.create(model=model, messages=messages)
        return response.choices[0].message.content

    def get_all_similarities(self, question: str) -> List[float]:
        """Get all similarity scores for a question (for analysis)."""
        results = self.chroma_collection.query(
            query_texts=[question],
            n_results=len(self.token_split_texts),
            include=["distances"]
        )
        similarities = [1 - d for d in results["distances"][0]]
        return similarities

    def naive_rag(self, question: str, relevance_threshold: float = 0.3) -> Dict:
        """Implement naive RAG - single query retrieval."""
        results = self.chroma_collection.query(
            query_texts=[question],
            n_results=50,
            include=["documents", "distances", "embeddings"]
        )
        
        # Filter by relevance threshold
        relevant_documents = []
        relevant_similarities = []
        relevant_embeddings = []
        
        for doc, distance, embedding in zip(results["documents"][0], results["distances"][0], results["embeddings"][0]):
            similarity = 1 - distance
            if similarity >= relevance_threshold:
                relevant_documents.append(doc)
                relevant_similarities.append(similarity)
                relevant_embeddings.append(embedding)
        
        response = self.generate_support_response(relevant_documents, question) if relevant_documents else "Ingen relevant information fundet."
        
        return {
            "method": "Naive RAG",
            "original_question": question,
            "retrieved_documents": relevant_documents,
            "similarities": relevant_similarities,
            "embeddings": relevant_embeddings,
            "response": response,
            "num_unique_documents": len(relevant_documents),
            "all_similarities": self.get_all_similarities(question)
        }
    
    def naive_rag_no_llm(self, question: str, relevance_threshold: float = 0.3) -> Dict:
        """Naive RAG without LLM call - for threshold testing."""
        results = self.chroma_collection.query(
            query_texts=[question],
            n_results=50,
            include=["documents", "distances"]
        )
        
        relevant_documents = []
        for doc, distance in zip(results["documents"][0], results["distances"][0]):
            similarity = 1 - distance
            if similarity >= relevance_threshold:
                relevant_documents.append(doc)
        
        return {"num_unique_documents": len(relevant_documents)}

    def advanced_rag(self, question: str, relevance_threshold: float = 0.3) -> Dict:
        """Implement advanced RAG with query expansion."""
        # Generate expanded queries
        expanded_queries = self.generate_multi_query(question)
        all_queries = [question] + expanded_queries
        
        # Retrieve from all queries
        all_docs_with_similarity = []
        
        for query in all_queries:
            results = self.chroma_collection.query(
                query_texts=[query],
                n_results=50,
                include=["documents", "distances", "embeddings"]
            )
            
            for doc, distance, embedding in zip(results["documents"][0], results["distances"][0], results["embeddings"][0]):
                similarity = 1 - distance
                if similarity >= relevance_threshold:
                    all_docs_with_similarity.append({
                        'document': doc,
                        'similarity': similarity,
                        'embedding': embedding
                    })
        
        # Deduplicate and sort by similarity
        seen_docs = set()
        relevant_documents = []
        relevant_similarities = []
        relevant_embeddings = []
        
        sorted_docs = sorted(all_docs_with_similarity, key=lambda x: x['similarity'], reverse=True)
        for item in sorted_docs:
            if item['document'] not in seen_docs:
                relevant_documents.append(item['document'])
                relevant_similarities.append(item['similarity'])
                relevant_embeddings.append(item['embedding'])
                seen_docs.add(item['document'])
        
        response = self.generate_support_response(relevant_documents, question) if relevant_documents else "Ingen relevant information fundet."
        
        return {
            "method": "Advanced RAG",
            "original_question": question,
            "expanded_queries": expanded_queries,
            "retrieved_documents": relevant_documents,
            "similarities": relevant_similarities,
            "embeddings": relevant_embeddings,
            "response": response,
            "num_unique_documents": len(relevant_documents)
        }

    def compare_methods(self, questions: List[str]) -> Dict:
        """Compare naive and advanced RAG methods."""
        results = {
            "naive_rag": [],
            "advanced_rag": [],
            "metrics": []
        }
        
        print(f"\n🔄 Processing {len(questions)} questions...")
        
        for i, question in enumerate(questions, 1):
            print(f"\nQuestion {i}/{len(questions)}: {question[:50]}...")
            
            naive_result = self.naive_rag(question)
            advanced_result = self.advanced_rag(question)
            
            metrics = {
                "question": question,
                "naive_docs": naive_result["num_unique_documents"],
                "advanced_docs": advanced_result["num_unique_documents"],
                "improvement": advanced_result["num_unique_documents"] - naive_result["num_unique_documents"],
                "expanded_queries": len(advanced_result["expanded_queries"])
            }
            
            results["naive_rag"].append(naive_result)
            results["advanced_rag"].append(advanced_result)
            results["metrics"].append(metrics)
            
            print(f"  ✓ Naive: {naive_result['num_unique_documents']} docs")
            print(f"  ✓ Advanced: {advanced_result['num_unique_documents']} docs (+{metrics['improvement']})")
        
        # Calculate summary statistics
        results["summary"] = self.calculate_summary(results["metrics"])
        return results
    
    def calculate_summary(self, metrics: List[Dict]) -> Dict:
        """Calculate summary statistics."""
        total_questions = len(metrics)
        naive_docs = [m["naive_docs"] for m in metrics]
        advanced_docs = [m["advanced_docs"] for m in metrics]
        improvements = [m["improvement"] for m in metrics]
        
        return {
            "total_questions": total_questions,
            "average_documents_naive": np.mean(naive_docs),
            "average_documents_advanced": np.mean(advanced_docs),
            "average_improvement": np.mean(improvements),
            "total_naive_docs": sum(naive_docs),
            "total_advanced_docs": sum(advanced_docs),
            "questions_with_improvement": sum(1 for imp in improvements if imp > 0),
            "improvement_rate": sum(1 for imp in improvements if imp > 0) / total_questions * 100,
            "total_expanded_queries": sum(m["expanded_queries"] for m in metrics),
            "average_expanded_queries": np.mean([m["expanded_queries"] for m in metrics])
        }
    
    def create_thesis_visualizations(self, results: Dict, prefix: str = "thesis_rag"):
        """Create improved thesis visualizations."""
        # Set matplotlib parameters
        plt.rcParams['font.size'] = 12
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['figure.dpi'] = 300
        
        print("\n📊 Creating thesis visualizations...")
        
        # 1. Document Retrieval Comparison
        print("Creating retrieval comparison...")
        self.create_retrieval_comparison(results, prefix)
        
        # 2. Similarity Distribution
        print("Creating similarity distribution...")
        self.create_similarity_distribution(results, prefix)
        
        # 3. Query Expansion Visualization
        print("Creating query expansion visualization...")
        self.create_query_expansion_viz(results, prefix)
        
        # 4. Semantic Space
        print("Creating semantic space...")
        self.create_semantic_space(results, prefix)
        
        # 5. Performance Summary
        print("Creating performance summary...")
        self.create_performance_summary(results, prefix)
        
        print("✅ All visualizations created!")
    
    def create_retrieval_comparison(self, results, prefix):
        """Create document retrieval comparison."""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        questions = [f'Q{i+1}' for i in range(len(results["metrics"]))]
        naive_docs = [m["naive_docs"] for m in results["metrics"]]
        advanced_docs = [m["advanced_docs"] for m in results["metrics"]]
        
        x = np.arange(len(questions))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, naive_docs, width, label='Naive RAG',
                        color='#E74C3C', alpha=0.8, edgecolor='black')
        bars2 = ax.bar(x + width/2, advanced_docs, width, label='Advanced RAG',
                        color='#2ECC71', alpha=0.8, edgecolor='black')
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height,
                        f'{int(height)}', ha='center', va='bottom')
        
        # Add improvement indicators
        for i, (n, a) in enumerate(zip(naive_docs, advanced_docs)):
            if a > n:
                ax.text(i, max(n, a) + 0.5, f'+{a-n}', ha='center', 
                       fontsize=10, color='green', fontweight='bold')
        
        ax.set_xlabel('Questions')
        ax.set_ylabel('Documents Retrieved')
        ax.set_title('Document Retrieval: Naive vs Advanced RAG', fontsize=16, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(questions)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(f'{prefix}_retrieval_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_similarity_distribution(self, results, prefix):
        """Show similarity distribution and why low threshold is needed."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Get all similarities from first question
        example = results["naive_rag"][0]
        all_sims = example["all_similarities"]
        
        # Distribution plot
        ax1.hist(all_sims, bins=50, alpha=0.7, color='#3498DB', edgecolor='black')
        ax1.axvline(x=0.3, color='red', linestyle='--', linewidth=2, label='Used threshold (0.3)')
        ax1.axvline(x=0.5, color='orange', linestyle='--', linewidth=2, label='Typical threshold (0.5)')
        ax1.set_xlabel('Similarity Score')
        ax1.set_ylabel('Number of Documents')
        ax1.set_title('Similarity Distribution: All Documents')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Statistics
        above_03 = sum(1 for s in all_sims if s >= 0.3)
        above_05 = sum(1 for s in all_sims if s >= 0.5)
        ax1.text(0.02, 0.98, f'Documents above 0.3: {above_03}\nDocuments above 0.5: {above_05}', 
                transform=ax1.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Threshold impact on different questions
        thresholds = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
        question_counts = []
        
        for threshold in thresholds:
            counts = []
            for naive_result in results["naive_rag"][:5]:  # First 5 questions
                count = sum(1 for sim in naive_result["all_similarities"] if sim >= threshold)
                counts.append(count)
            question_counts.append(counts)
        
        # Plot lines for each question
        for i in range(5):
            counts_per_threshold = [qc[i] for qc in question_counts]
            ax2.plot(thresholds, counts_per_threshold, 'o-', label=f'Q{i+1}', alpha=0.7)
        
        ax2.axvline(x=0.3, color='red', linestyle='--', alpha=0.5)
        ax2.set_xlabel('Similarity Threshold')
        ax2.set_ylabel('Documents Above Threshold')
        ax2.set_title('Impact of Threshold on Retrieval')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{prefix}_similarity_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_query_expansion_viz(self, results, prefix):
        """Create query expansion visualization."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Find good example
        example_idx = 0
        for i, result in enumerate(results["advanced_rag"]):
            if result["num_unique_documents"] > results["naive_rag"][i]["num_unique_documents"]:
                example_idx = i
                break
        
        example = results["advanced_rag"][example_idx]
        
        # Setup
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'Query Expansion Mechanism', fontsize=16, fontweight='bold', ha='center')
        
        # Original query
        center_x, center_y = 5, 5
        circle = plt.Circle((center_x, center_y), 1, color='#3498DB', alpha=0.9)
        ax.add_patch(circle)
        ax.text(center_x, center_y, 'Original\nQuery', ha='center', va='center', 
                fontweight='bold', fontsize=12, color='white')
        
        # Expanded queries
        n_expanded = len(example["expanded_queries"])
        if n_expanded > 0:
            angles = np.linspace(0, 2*np.pi, n_expanded, endpoint=False)
            radius = 3
            colors = ['#E74C3C', '#F39C12', '#9B59B6', '#1ABC9C']
            
            for i, angle in enumerate(angles):
                x = center_x + radius * np.cos(angle)
                y = center_y + radius * np.sin(angle)
                
                # Query circle
                exp_circle = plt.Circle((x, y), 0.7, color=colors[i % len(colors)], alpha=0.9)
                ax.add_patch(exp_circle)
                ax.text(x, y, f'Q{i+1}', ha='center', va='center', 
                       fontweight='bold', fontsize=11, color='white')
                
                # Connection
                ax.plot([center_x, x], [center_y, y], 'k--', alpha=0.5, linewidth=2)
        
        # Results
        naive_docs = results["metrics"][example_idx]["naive_docs"]
        advanced_docs = results["metrics"][example_idx]["advanced_docs"]
        
        ax.text(1, 1, f'Single Query:\n{naive_docs} documents', fontsize=12, 
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFE5E5'),
               ha='center')
        
        ax.text(9, 1, f'Multi-Query:\n{advanced_docs} documents\n(+{advanced_docs-naive_docs})', 
               fontsize=12, ha='center',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#E5FFE5'))
        
        plt.tight_layout()
        plt.savefig(f'{prefix}_query_expansion.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_semantic_space(self, results, prefix):
        """Create semantic space visualization."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        # Get embeddings
        all_data = self.chroma_collection.get(include=["embeddings"])
        all_embeddings = np.array(all_data["embeddings"])
        
        # PCA
        pca = PCA(n_components=2, random_state=42)
        all_embeddings_2d = pca.fit_transform(all_embeddings)
        
        # Example
        example_idx = 3
        naive_result = results["naive_rag"][example_idx]
        advanced_result = results["advanced_rag"][example_idx]
        
        for ax, result, title in [(ax1, naive_result, 'Naive RAG'),
                                   (ax2, advanced_result, 'Advanced RAG')]:
            # All documents
            ax.scatter(all_embeddings_2d[:, 0], all_embeddings_2d[:, 1], 
                      c='lightgray', s=20, alpha=0.5)
            
            # Retrieved documents
            if result["embeddings"]:
                retrieved_embeddings_2d = pca.transform(result["embeddings"])
                scatter = ax.scatter(retrieved_embeddings_2d[:, 0], retrieved_embeddings_2d[:, 1], 
                                   c=result["similarities"], s=200, alpha=0.8, 
                                   cmap='Reds', vmin=0.3, vmax=0.5,
                                   edgecolors='black', linewidth=1)
                plt.colorbar(scatter, ax=ax, label='Similarity')
            
            # Query
            query_embedding = self.embedding_function([result["original_question"]])[0]
            query_2d = pca.transform([query_embedding])[0]
            ax.scatter(query_2d[0], query_2d[1], c='blue', s=500, marker='*',
                      edgecolors='black', linewidth=2, zorder=100)
            
            ax.set_xlabel('Dimension 1')
            ax.set_ylabel('Dimension 2')
            ax.set_title(f'{title}: {result["num_unique_documents"]} documents')
            ax.grid(True, alpha=0.2)
        
        plt.suptitle('Semantic Search Space', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{prefix}_semantic_space.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_performance_summary(self, results, prefix):
        """Create performance summary."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        summary = results["summary"]
        
        # 1. Average performance
        methods = ['Naive RAG', 'Advanced RAG']
        averages = [summary['average_documents_naive'], 
                   summary['average_documents_advanced']]
        
        bars = ax1.bar(methods, averages, color=['#E74C3C', '#2ECC71'], alpha=0.8)
        for bar, avg in zip(bars, averages):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    f'{avg:.1f}', ha='center', va='bottom', fontweight='bold')
        
        ax1.set_ylabel('Average Documents/Query')
        ax1.set_title('Average Retrieval Performance')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 2. Success rate
        improvement_rate = summary['improvement_rate']
        wedges, _ = ax2.pie([improvement_rate, 100-improvement_rate], 
                           colors=['#2ECC71', '#E0E0E0'], 
                           startangle=90,
                           wedgeprops=dict(width=0.3))
        ax2.text(0, 0, f'{improvement_rate:.0f}%', 
                ha='center', va='center', fontsize=24, fontweight='bold')
        ax2.text(0, -0.4, 'Success Rate', ha='center', fontsize=12)
        
        # 3. Improvement distribution
        improvements = [m["improvement"] for m in results["metrics"]]
        ax3.hist(improvements, bins=range(min(improvements), max(improvements)+2),
                color='#3498DB', alpha=0.8, edgecolor='black')
        ax3.set_xlabel('Additional Documents')
        ax3.set_ylabel('Number of Questions')
        ax3.set_title('Improvement Distribution')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Summary text
        ax4.axis('off')
        summary_text = f"""Key Findings:
        
• Average improvement: +{summary['average_improvement']:.1f} docs/query
• Success rate: {summary['improvement_rate']:.0f}%
• Total additional docs: {summary['total_advanced_docs'] - summary['total_naive_docs']}

Low similarity threshold (0.3) reveals 
semantic gap between queries and documents.
Query expansion bridges this gap."""
        
        ax4.text(0.1, 0.9, summary_text, transform=ax4.transAxes, fontsize=12,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig(f'{prefix}_performance_summary.png', dpi=300, bbox_inches='tight')
        plt.close()

def main():
    """Main function to run the RAG comparison study."""
    # Same 10 test questions from thesis
    test_questions = [
        "Hvordan fungerer jeres AI-coaching og hvad lærer jeg konkret?",
        "Kan I hjælpe mig med at automatisere mine arbejdsgange med AI og i så fald hvordan?",
        "Hvilke AI-tools anbefaler I til contentproduktion og kundeservice og kan jeg lære dem via jer?",
        "Hvordan adskiller jeres AI-løsninger sig fra andre bureauers?",
        "Er det muligt at få skræddersyet AI-setup eller undervisning kun til min branche eller arbejdsproces?",
        "Hvilket annonceringsbudget skal jeg minimum regne med for at få resultater?",
        "Hvordan foregår et typisk samarbejde med jer fra start til slut?",
        "Kan I hjælpe med alt hvis jeg ikke har nogen marketingopsætning i forvejen?",
        "Hvad sker der hvis jeg ikke er tilfreds med jeres arbejde?",
        "Hvilke resultater har I tidligere skabt og hvad kan jeg realistisk forvente?"
    ]
    
    print("🚀 Starting RAG Comparison Analysis")
    print(f"Model: o4-mini")
    print(f"Relevance threshold: 0.3")
    print(f"Test questions: {len(test_questions)}")
    
    # Initialize system
    rag_comparison = SimpleRAGComparison("data/Full CJ COMPLEX knowlegdebase.pdf")
    
    # Run comparison
    results = rag_comparison.compare_methods(test_questions)
    
    # Create visualizations
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rag_comparison.create_thesis_visualizations(results, f"thesis_rag_{timestamp}")
    
    # Save results
    with open(f"rag_comparison_{timestamp}.json", "w", encoding='utf-8') as f:
        json.dump({
            "timestamp": timestamp,
            "model": "o4-mini",
            "relevance_threshold": 0.3,
            "summary": results["summary"],
            "metrics": results["metrics"]
        }, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n📊 FINAL SUMMARY")
    print("="*50)
    summary = results["summary"]
    print(f"Naive RAG average: {summary['average_documents_naive']:.1f} docs/query")
    print(f"Advanced RAG average: {summary['average_documents_advanced']:.1f} docs/query")
    print(f"Improvement: +{summary['average_improvement']:.1f} docs/query")
    print(f"Success rate: {summary['improvement_rate']:.0f}%")
    
    print("\n✅ Analysis complete! Check the visualizations.")

if __name__ == "__main__":
    main()
