# RAG Customer Service Assistant

A Retrieval-Augmented Generation (RAG) application that provides intelligent customer service responses in Danish. The system uses ChromaDB for vector storage and OpenAI's GPT and embedding models to deliver contextually relevant answers based on a company knowledge base.

## Overview

This application demonstrates a complete RAG pipeline that:

- Loads documents from a knowledge base directory
- Splits documents into chunks for better semantic search
- Generates embeddings using OpenAI's text-embedding-3-small model
- Stores embeddings in ChromaDB with persistent storage
- Retrieves relevant context based on user queries
- Generates responses using OpenAI's GPT model with Danish language prompts

## Features

- **Document Processing**: Automatically loads and processes `.txt` files from the knowledge base
- **Text Chunking**: Intelligent text splitting with configurable chunk size and overlap
- **Vector Storage**: Persistent ChromaDB storage for embeddings
- **Semantic Search**: Retrieves most relevant document chunks for queries
- **Danish Customer Service**: Optimized prompts for professional Danish customer service responses
- **Contextual Responses**: Uses retrieved chunks to provide accurate, contextual answers

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Virtual environment (recommended)

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd rag
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Project Structure

```
rag/
├── app.py                          # Main application file
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (create this)
├── knowledge_base/                # Directory containing knowledge documents
│   └── Full CJ COMPLEX knowlegdebase.txt
├── chroma_persistent_storage/     # ChromaDB persistent storage (auto-created)
└── README.md                      # This file
```

## Usage

### Running the Application

1. **Ensure your knowledge base is populated**

   - Place your `.txt` files in the `knowledge_base/` directory
   - The application will automatically process all `.txt` files

2. **Run the application**

   ```bash
   python app.py
   ```

3. **Modify queries**
   - Edit the `question` variable at the bottom of `app.py` to test different queries
   - Example queries are provided in the comments

### Example Queries (in Danish)

The application includes several example queries you can test:

- "Hvordan fungerer jeres AI-coaching og hvad lærer jeg konkret?"
- "Kan I hjælpe mig med at automatisere mine arbejdsgange med AI og i så fald hvordan?"
- "Hvilke AI-tools anbefaler I til contentproduktion og kundeservice og kan jeg lære dem via jer?"
- "Hvordan adskiller jeres AI-løsninger sig fra andre bureauers?"

### Configuration

You can modify several parameters in `app.py`:

- **Chunk size**: Change `chunk_size` parameter in `split_text()` function (default: 1000)
- **Chunk overlap**: Change `chunk_overlap` parameter (default: 20)
- **Number of results**: Change `n_results` in `query_documents()` function (default: 2)
- **OpenAI model**: Change the model in `generate_response()` function (default: "o4-mini")

## How It Works

1. **Document Loading**: The system scans the `knowledge_base/` directory for `.txt` files
2. **Text Preprocessing**: Documents are split into overlapping chunks for better semantic search
3. **Embedding Generation**: Each chunk is converted to embeddings using OpenAI's embedding model
4. **Vector Storage**: Embeddings are stored in ChromaDB with persistent storage
5. **Query Processing**: User questions are converted to embeddings and matched against stored chunks
6. **Response Generation**: Relevant chunks are used as context for GPT to generate responses

## Technical Details

- **Embedding Model**: text-embedding-3-small
- **Chat Model**: o4-mini
- **Vector Database**: ChromaDB with persistent storage
- **Language**: Danish-optimized prompts
- **Chunk Strategy**: Overlapping chunks for better context preservation

## Troubleshooting

### Common Issues

1. **Missing OpenAI API Key**

   - Ensure your `.env` file contains a valid `OPENAI_API_KEY`
   - Verify the API key has sufficient credits

2. **Empty Knowledge Base**

   - Ensure `.txt` files are present in the `knowledge_base/` directory
   - Check file encoding (should be UTF-8)

3. **ChromaDB Issues**
   - Delete the `chroma_persistent_storage/` directory to reset the database
   - Ensure sufficient disk space for vector storage

### Debug Mode

The application includes debug print statements that show:

- Document loading progress
- Chunk creation process
- Embedding generation status
- Database insertion progress

## License

This project is for educational purposes. Please ensure you comply with OpenAI's usage policies when using their API.

## Contributing

This is an educational project for examination purposes. For questions or issues, please contact the project maintainer.
