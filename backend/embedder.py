from sentence_transformers import SentenceTransformer

class STEmbeddingFunction:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, docs):
        return self.model.encode(docs).tolist()

    def embed_query(self, query):
        return self.model.encode([query])[0].tolist()
