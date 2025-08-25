from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline import RAGPipeline

app = FastAPI()
pipeline = RAGPipeline()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    result = pipeline.run(query.question)
    return result
