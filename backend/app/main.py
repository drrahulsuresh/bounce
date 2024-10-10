from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_system import rag_system

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "Welcome to the RAG-powered Survey Analysis!"}

@app.post("/query")
def query_rag(request: QueryRequest):
    try:
        # Process the query using the RAG system
        response = rag_system.generate_response(request.query)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}
