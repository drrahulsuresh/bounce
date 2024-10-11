from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.app.rag_system import rag_system


app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "Welcome to the RAG-powered Survey Analysis API!"}

@app.post("/query")
def query_rag(request: QueryRequest):
    try:
        response = rag_system.generate_response(request.query)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}
