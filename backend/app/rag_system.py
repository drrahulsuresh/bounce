import spacy
from fuzzywuzzy import fuzz
from sqlalchemy.orm import Session
from transformers import pipeline
from backend.app.models import SurveyData, engine
import redis
from textblob import TextBlob

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize Redis for caching
cache = redis.StrictRedis(host='localhost', port=6379, db=0)

class RAGSystem:
    def __init__(self):
        self.session = Session(bind=engine)
        self.text_generation_model = pipeline("text-generation", model="gpt2")

    def preprocess_query(self, query):
        """ Preprocess the user query using spaCy to lemmatize and remove stopwords. """
        doc = nlp(query)
        preprocessed_query = " ".join([token.lemma_ for token in doc if not token.is_stop])
        return preprocessed_query

    def analyze_sentiment(self, text):
        """ Analyze sentiment of the combined data using TextBlob. """
        analysis = TextBlob(text)
        return analysis.sentiment.polarity

    def retrieve_data(self, query):
        """ Retrieve data from the database based on the processed query, with Redis caching. """
        # Check cache first
        cached_response = cache.get(query)
        if cached_response:
            print("Returning cached response.")
            return cached_response.decode('utf-8')

        # Preprocess the query
        preprocessed_query = self.preprocess_query(query)
        db_query = f"%{preprocessed_query.lower()}%"

        # Query the database
        result = self.session.query(SurveyData).filter(SurveyData.question.ilike(db_query)).all()

        if result:
            # Extract relevant information
            retrieved_data = [f"{row.question}: {row.response_value}" for row in result]
            combined_data = " ".join(retrieved_data)

            # Cache the result
            cache.set(query, combined_data)
            print("Caching result for future queries.")
            
            return combined_data
        else:
            return "No relevant data found in the database."

    def generate_response(self, query):
        """ Generate a response by retrieving data and performing AI text generation with sentiment analysis. """
        # Retrieve the data from the database or cache
        retrieved_data = self.retrieve_data(query)
        
        # Analyze sentiment of the retrieved data
        sentiment_score = self.analyze_sentiment(retrieved_data)
        
        # Generate AI response with GPT-2
        ai_response = self.text_generation_model(f"Here is some information about {query}. Sentiment score: {sentiment_score}: {retrieved_data}", max_length=150)
        
        # Return the generated text response
        return ai_response[0]['generated_text']

# Initialize the RAG system
rag_system = RAGSystem()
