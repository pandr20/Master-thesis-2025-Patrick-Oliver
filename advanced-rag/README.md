# RAG System Comparison: Naive vs Advanced Query Expansion

## Project Overview

This project implements and compares two Retrieval-Augmented Generation (RAG) approaches for customer support question answering:

1. **Naive RAG**: Single query retrieval using direct semantic search
2. **Advanced RAG**: Multi-query retrieval using LLM-generated query expansion

The system is designed for CJ Complex, a Danish marketing services company, and demonstrates how query expansion can improve document retrieval in scenarios with semantic gaps between user questions and document content.

## Key Features

- **Dual RAG Implementation**: Compare naive vs advanced RAG approaches
- **Query Expansion**: LLM-generated related queries to improve retrieval coverage
- **Low Similarity Threshold Analysis**: Demonstrates why low thresholds (0.3) are necessary
- **Comprehensive Visualizations**: 5 detailed analysis charts for thesis documentation
- **Danish Language Support**: Optimized for Danish customer service scenarios
- **Performance Metrics**: Detailed comparison metrics and success rates

## Technical Architecture

### RAG Implementation Details

- **Embedding Model**: SentenceTransformerEmbeddingFunction (all-MiniLM-L6-v2, 384 dimensions)
- **Chunking Strategy**: Two-stage approach:
  - RecursiveCharacterTextSplitter (1000 characters, no overlap)
  - SentenceTransformersTokenTextSplitter (256 tokens, no overlap)
- **Vector Store**: ChromaDB in-memory client with time-stamped collections
- **LLM Integration**: OpenAI o4-mini for query expansion and response generation
- **Similarity Threshold**: 0.3 (chosen to bridge semantic gap between queries and documents)

## Requirements

### System Requirements

- Python 3.8+
- OpenAI API key
- Minimum 4GB RAM (for embeddings processing)

### Dependencies

All dependencies are listed in `requirements.txt`:

```txt
openai>=1.0.0
python-dotenv>=0.19.0
chromadb>=0.4.0
langchain>=0.0.325
sentence-transformers>=2.2.0
pypdf>=3.0.0
numpy>=1.21.0
pandas>=1.3.0
umap-learn>=0.5.0
matplotlib>=3.4.0
typing>=3.7.4
pydantic>=1.8.2
tqdm>=4.62.0
```

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd advanced-rag
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Verify Data File

Ensure the PDF knowledge base is in place:

```
data/Full CJ COMPLEX knowlegdebase.pdf
```

## Usage

### Running the RAG Comparison

Execute the main comparison script:

```bash
python cj_complex_support_rag.py
```

### Expected Output

The system will:

1. Process the PDF knowledge base (chunk into ~256-token segments)
2. Create ChromaDB vector store with embeddings
3. Run 10 test questions through both RAG approaches
4. Generate 5 comprehensive visualization charts
5. Output performance metrics and JSON results

### Test Questions

The system evaluates 10 Danish customer service questions covering:

- AI coaching and automation
- Marketing services and tools
- Pricing and packages
- Training and support
- Results and case studies

## Project Structure

```
advanced-rag/
├── cj_complex_support_rag.py          # Main RAG comparison implementation
├── requirements.txt                    # Python dependencies
├── .env                               # Environment variables (create this)
├── data/
│   └── Full CJ COMPLEX knowlegdebase.pdf  # Knowledge base document
├── README.md                          # This file
└── Generated Output:
    ├── rag_comparison_[timestamp].json    # Performance metrics
    ├── thesis_rag_[timestamp]_*.png       # 5 visualization charts
    └── __pycache__/                       # Python cache files
```

## Generated Outputs

### 1. Performance Metrics (`rag_comparison_[timestamp].json`)

Contains:

- Summary statistics (averages, improvement rates)
- Per-question metrics
- Model configuration details

### 2. Visualization Charts (5 PNG files)

- **Retrieval Comparison**: Bar chart comparing document counts
- **Similarity Distribution**: Analysis of why low threshold is needed
- **Query Expansion**: Mechanism demonstration
- **Semantic Space**: 2D visualization of document retrieval
- **Performance Summary**: Comprehensive metrics dashboard

## Key Findings

The analysis demonstrates:

- **Average Improvement**: +1.4 documents per query (40% increase)
- **Success Rate**: 70% of queries benefit from expansion
- **Semantic Gap**: Low similarity threshold (0.3) necessary due to mismatch between user language and document content
- **Query Expansion Effectiveness**: Multi-query approach finds documents in different semantic areas

## Troubleshooting

### Common Issues

1. **Missing OpenAI API Key**

   ```
   Error: OpenAI API key not found
   Solution: Create .env file with OPENAI_API_KEY
   ```

2. **PDF Not Found**

   ```
   Error: Cannot find PDF file
   Solution: Ensure data/Full CJ COMPLEX knowlegdebase.pdf exists
   ```

3. **Memory Issues**

   ```
   Error: Out of memory during embedding
   Solution: Ensure minimum 4GB RAM available
   ```

4. **Model Name Error**
   ```
   Error: Invalid model 'o4-mini'
   Solution: The code uses 'o4-mini' as configured - ensure OpenAI API supports this model
   ```

## Configuration Options

### Adjustable Parameters

- `relevance_threshold`: Default 0.3 (similarity threshold for retrieval)
- `chunk_size`: Default 1000 characters (initial chunking)
- `tokens_per_chunk`: Default 256 tokens (final chunking)
- `model`: Default "o4-mini" (OpenAI model for LLM calls)

### Modifying Test Questions

Edit the `test_questions` list in the `main()` function to test different scenarios.

## Performance Expectations

### Runtime

- Initial setup: ~30 seconds (PDF processing + embeddings)
- Per question analysis: ~5-10 seconds
- Full analysis (10 questions): ~2-3 minutes
- Visualization generation: ~10-15 seconds

### Resource Usage

- Memory: ~2-4GB during processing
- Storage: ~50MB for outputs
- API Calls: ~40-60 OpenAI API requests per full run

## Academic Context

This implementation serves as a practical demonstration of:

- **RAG Architecture Patterns**: Comparing different retrieval strategies
- **Semantic Search Challenges**: Addressing query-document semantic gaps
- **Query Expansion Techniques**: Using LLMs to improve retrieval coverage
- **Evaluation Methodologies**: Measuring RAG system performance

## Support

For technical issues or questions about the implementation:

1. Check the troubleshooting section above
2. Verify all dependencies are correctly installed
3. Ensure the OpenAI API key has sufficient credits
4. Review the generated error logs for specific issues

## License

This project is developed for academic/educational purposes as part of a thesis evaluation.
