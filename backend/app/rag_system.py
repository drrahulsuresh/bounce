from sqlalchemy.orm import Session
from backend.app.models import SurveyData, engine
from transformers import pipeline


class RAGSystem:
    def __init__(self):
        self.session = Session(bind=engine)
        self.text_generation_model = pipeline("text-generation", model="gpt2")

    def retrieve_data(self, query):
        db_query = f"%{query.lower()}%"  
        result = self.session.query(SurveyData).filter(SurveyData.question.ilike(db_query)).all()

        if result:
            retrieved_data = [f"{row.question}: {row.response_value}" for row in result]
            return retrieved_data
        else:
            return ["No relevant data found in the database."]

    def generate_response(self, query):
        retrieved_data = self.retrieve_data(query)
        combined_data = " ".join(retrieved_data)
        ai_response = self.text_generation_model(f"Here is some information about {query}: {combined_data}", max_length=150)
        return ai_response[0]['generated_text']

# Initialize the RAG system
rag_system = RAGSystem()
