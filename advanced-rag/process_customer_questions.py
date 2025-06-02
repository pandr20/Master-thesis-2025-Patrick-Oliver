import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from helper_utils import project_embeddings, word_wrap
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
import json
from datetime import datetime

# Load environment variables
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)

class CustomerSupportRAG:
    def __init__(self, pdf_path: str):
        """Initialize the RAG system with a knowledge base PDF."""
        self.setup_document_processing(pdf_path)
        self.setup_vector_store()
        
    def setup_document_processing(self, pdf_path: str):
        """Set up document processing pipeline."""
        # Initialize PDF reader and extract text
        reader = PdfReader(pdf_path)
        self.pdf_texts = [p.extract_text().strip() for p in reader.pages]
        self.pdf_texts = [text for text in self.pdf_texts if text]
        
        # Set up text splitters
        self.character_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ". ", " ", ""],
            chunk_size=1000,
            chunk_overlap=0
        )
        self.token_splitter = SentenceTransformersTokenTextSplitter(
            chunk_overlap=0,
            tokens_per_chunk=256
        )
        
        # Process the text
        character_split_texts = self.character_splitter.split_text("\n\n".join(self.pdf_texts))
        self.token_split_texts = []
        for text in character_split_texts:
            self.token_split_texts += self.token_splitter.split_text(text)

    def setup_vector_store(self):
        """Set up the vector store with ChromaDB."""
        self.embedding_function = SentenceTransformerEmbeddingFunction()
        self.chroma_client = chromadb.Client()
        self.chroma_collection = self.chroma_client.create_collection(
            "cj-complex-support",
            embedding_function=self.embedding_function
        )
        
        # Add documents to collection
        ids = [str(i) for i in range(len(self.token_split_texts))]
        self.chroma_collection.add(ids=ids, documents=self.token_split_texts)

    def generate_expanded_queries(self, question: str) -> List[str]:
        """Generate expanded queries for a customer question."""
        prompt = """
        Du er en AI-kundeservicemedarbejder hos CJ Complex, en finansiel virksomhed.
        Givet kundens spørgsmål, generer 3-5 relaterede spørgsmål, der vil hjælpe med at give
        omfattende information fra vores vidensbase. Fokuser på spørgsmål der:
        
        1. Afklarer specifikke aspekter af kundens forespørgsel
        2. Adresserer potentielle opfølgende bekymringer
        3. Dækker relaterede emner, der kan være nyttige
        4. Forbliver inden for CJ Complex's services og produkter
        
        Formater hvert spørgsmål på en separat linje uden nummerering.
        Hold spørgsmålene korte og fokuserede på enkelte emner.
        Sørg for at spørgsmålene er direkte relevante for CJ Complex's forretningskontekst.
        """
        
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
        
        response = client.chat.completions.create(
            model="o4-mini",
            messages=messages
        )
        
        return [q.strip() for q in response.choices[0].message.content.split('\n') if q.strip()]

    def generate_response(self, context: List[str], question: str) -> str:
        """Generate a customer support response using retrieved context."""
        prompt = """
        Du er en AI-kundeservicemedarbejder hos CJ Complex. Brug den givne kontekst til at besvare
        kundens spørgsmål professionelt og præcist. Dit svar skal:
        
        1. Være klart, kortfattet og professionelt
        2. Kun bruge information fra den givne kontekst
        3. Opretholde CJ Complex's professionelle tone
        4. Inkludere specifikke detaljer når de er tilgængelige
        5. Anerkende hvis bestemt information ikke er tilgængelig i konteksten
        
        Kontekst:
        {context}
        
        Kundespørgsmål:
        {question}
        """
        
        messages = [
            {
                "role": "system",
                "content": prompt.format(
                    context="\n\n".join(context),
                    question=question
                )
            }
        ]
        
        response = client.chat.completions.create(
            model="o4-mini",
            messages=messages
        )
        
        return response.choices[0].message.content

    def process_question(self, question: str) -> Dict:
        """Process a single customer question."""
        # Generate expanded queries
        expanded_queries = self.generate_expanded_queries(question)
        all_queries = [question] + expanded_queries
        
        # Retrieve relevant documents
        results = self.chroma_collection.query(
            query_texts=all_queries,
            n_results=3,
            include=["documents"]
        )
        
        # Deduplicate retrieved documents
        unique_documents = list(set([
            doc for sublist in results["documents"] for doc in sublist
        ]))
        
        # Generate the response
        response = self.generate_response(unique_documents, question)
        
        return {
            "original_question": question,
            "expanded_queries": expanded_queries,
            "context_used": unique_documents,
            "response": response
        }

    def process_questions(self, questions: List[str]) -> List[Dict]:
        """Process multiple customer questions."""
        results = []
        for question in questions:
            result = self.process_question(question)
            results.append(result)
        return results

    def save_results(self, results: List[Dict], output_file: str = None):
        """Save results to a file."""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"support_responses_{timestamp}.txt"
        
        output = []
        for i, result in enumerate(results, 1):
            output.append(f"\n{'='*80}\n")
            output.append(f"Question {i}: {result['original_question']}\n")
            output.append("\nExpanded Queries:")
            for query in result['expanded_queries']:
                output.append(f"- {query}")
            
            output.append("\nAI Support Agent Response:")
            output.append(word_wrap(result['response']))
            output.append("\n")
        
        # Save formatted output
        with open(output_file, "w") as f:
            f.write("\n".join(output))
        
        # Save raw results as JSON for potential further analysis
        json_file = output_file.replace(".txt", ".json")
        with open(json_file, "w") as f:
            json.dump(results, f, indent=2)

def main():
    # Initialize the RAG system
    rag = CustomerSupportRAG("data/Full CJ COMPLEX knowlegdebase.pdf")
    
    print("Indtast venligst dine kundeservicespørgsmål (et pr. linje).")
    print("Tryk Enter på en tom linje når du er færdig:")
    
    questions = []
    while True:
        question = input().strip()
        if not question:
            break
        questions.append(question)
    
    if not questions:
        print("Ingen spørgsmål indtastet. Afslutter.")
        return
    
    print(f"\nBehandler {len(questions)} spørgsmål...")
    results = rag.process_questions(questions)
    
    # Save results
    rag.save_results(results)
    print(f"\nResultater er gemt i support_responses_<timestamp>.txt")
    print("En JSON-version af resultaterne er også tilgængelig i support_responses_<timestamp>.json")

if __name__ == "__main__":
    main()