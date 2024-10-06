from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .rag_system import process_query

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "RAG-powered Survey Analysis"}

@app.post("/query")
def query_rag(request: QueryRequest):
    try:
        response = process_query(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
