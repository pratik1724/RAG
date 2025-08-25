import os
import pandas as pd
import chromadb
from chromadb.config import Settings
from embedder import STEmbeddingFunction
from config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL

# Correct path for CSV (always works, no matter where you run the script)
csv_path = os.path.join(os.path.dirname(__file__), "data", "rag_sample_qas_from_kis.csv")
df = pd.read_csv(csv_path)

# Init Chroma client
client = chromadb.PersistentClient(
    path=CHROMA_DIR,
    settings=Settings(anonymized_telemetry=False)
)

# Delete if exists (fresh ingest)
try:
    client.delete_collection(COLLECTION_NAME)
except Exception:
    pass

collection = client.create_collection(name=COLLECTION_NAME)

# Embedding function
embed_fn = STEmbeddingFunction(EMBEDDING_MODEL)

# Combine Q + A for embeddings (better retrieval)
documents = (
    df["sample_question"].astype(str) + " " + df["sample_ground_truth"].astype(str)
).tolist()

embeddings = embed_fn.embed_documents(documents)

# Insert into Chroma
collection.add(
    documents=df["sample_ground_truth"].astype(str).tolist(),   # Store answers
    embeddings=embeddings,
    metadatas=[{"question": q, "topic": t} for q, t in zip(df["sample_question"], df["ki_topic"])],
    ids=[f"doc_{i}" for i in range(len(df))]
)

print(f"✅ Ingested {len(df)} rows into ChromaDB.")
