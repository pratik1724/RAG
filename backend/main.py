from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import RAGPipeline

app = FastAPI()

# ✅ Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # includes OPTIONS
    allow_headers=["*"],
)

pipeline = RAGPipeline()

class QueryRequest(BaseModel):
    query: str

@app.post("/chat")
def chat(request: QueryRequest):
    result = pipeline.run(request.query)
    return result
