import os
import subprocess
import chromadb
from embedder import STEmbeddingFunction
from config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL


class RAGPipeline:
    def __init__(self):
        # Ensure Chroma directory exists
        os.makedirs(CHROMA_DIR, exist_ok=True)

        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=CHROMA_DIR)
        self.collection = self.client.get_or_create_collection(COLLECTION_NAME)
        self.embed_fn = STEmbeddingFunction(EMBEDDING_MODEL)

    def retrieve_context(self, query: str, top_k: int = 3):
        """Retrieve top-k relevant documents from Chroma."""
        query_embedding = self.embed_fn.embed_query(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        if not results["documents"]:
            return ["No relevant documents found."]

        return results["documents"][0]

    def generate_answer(self, query: str, context_docs: list):
        """Generate an answer using Ollama (LLaMA model)."""
        prompt = f"""You are a helpful assistant. Use the context below to answer the question.

Context:
{chr(10).join(context_docs)}

Question: {query}
Answer:"""

        try:
            result = subprocess.run(
                ["ollama", "run", "llama3"],
                input=prompt,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Ollama error: {e.stderr.strip()}"

    def run(self, query: str, top_k: int = 3):
        """Complete RAG flow: retrieve + generate."""
        context_docs = self.retrieve_context(query, top_k)
        answer = self.generate_answer(query, context_docs)
        return {"answer": answer, "context": context_docs}
