import spacy
from fuzzywuzzy import fuzz
from sqlalchemy.orm import Session
from transformers import pipeline
from backend.app.models import SurveyData, engine
from textblob import TextBlob
import sqlite3

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to create a new SQLite connection (thread-safe)
def get_sqlite_connection():
    conn = sqlite3.connect('cache.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cache (
            query TEXT PRIMARY KEY,
            response TEXT
        )
    ''')
    conn.commit()
    return conn

# Initialize the RAG system with thread-safe SQLite
class RAGSystem:
    def __init__(self):
        self.session = Session(bind=engine)
        self.text_generation_model = pipeline("text-generation", model="gpt2")
        self.conn = get_sqlite_connection()
        self.cursor = self.conn.cursor()

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
        """ Retrieve data from the database based on the processed query, with SQLite caching. """
        # Check cache first in SQLite
        self.cursor.execute("SELECT response FROM cache WHERE query = ?", (query,))
        cached_response = self.cursor.fetchone()

        if cached_response:
            print("Returning cached response.")
            return cached_response[0]

        # Preprocess the query
        preprocessed_query = self.preprocess_query(query)
        db_query = f"%{preprocessed_query.lower()}%"

        # Query the database
        result = self.session.query(SurveyData).filter(SurveyData.question.ilike(db_query)).all()

        if result:
            # Extract relevant information
            retrieved_data = [f"{row.question}: {row.response_value}" for row in result]
            combined_data = " ".join(retrieved_data)

            # Cache the result in SQLite
            self.cursor.execute("INSERT OR REPLACE INTO cache (query, response) VALUES (?, ?)", (query, combined_data))
            self.conn.commit()
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
