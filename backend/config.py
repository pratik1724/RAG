# Configuration for RAG chatbot (Ollama only)

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "rag_collection"

# Embedding model (from SentenceTransformers)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Retrieval
TOP_K = 3                  # number of documents to retrieve
MAX_CONTEXT_CHARS = 1500   # truncate context length

# Ollama model to use
OLLAMA_MODEL = "llama3"    # make sure it's pulled via: ollama pull llama3
