import pandas as pd
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from app.data_processing import load_datasets

class RAGSystem:
    def __init__(self):
        # Load datasets
        self.sustainability_df, self.christmas_df = load_datasets()

        # Load models
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.text_generation_model = pipeline("text-generation", model="gpt2")

    def embed_dataset(self, df):
        # Create embeddings for the dataset rows for semantic search
        sentences = df.dropna().astype(str).values.flatten().tolist()
        embeddings = self.embedding_model.encode(sentences, convert_to_tensor=True)
        return sentences, embeddings

    def retrieve_data(self, query):
        # Embed query using Sentence-BERT
        query_embedding = self.embedding_model.encode(query, convert_to_tensor=True)

        # Embed and search both datasets
        sustainability_sentences, sustainability_embeddings = self.embed_dataset(self.sustainability_df)
        christmas_sentences, christmas_embeddings = self.embed_dataset(self.christmas_df)

        # Compute cosine similarity
        sustainability_scores = util.pytorch_cos_sim(query_embedding, sustainability_embeddings).squeeze()
        christmas_scores = util.pytorch_cos_sim(query_embedding, christmas_embeddings).squeeze()

        # Find the best match from each dataset
        max_sus_index = sustainability_scores.argmax().item()
        max_chr_index = christmas_scores.argmax().item()

        # Return the highest scoring match
        if "sustainability" in query.lower():
            return sustainability_sentences[max_sus_index]
        elif "christmas" in query.lower():
            return christmas_sentences[max_chr_index]
        else:
            return "No relevant data found."

    def generate_response(self, query):
        # Retrieve relevant data based on the query
        retrieved_data = self.retrieve_data(query)

        # Generate AI-enhanced response using GPT-2
        ai_response = self.text_generation_model(f"Here is some information about {query}: {retrieved_data}", max_length=150)
        return ai_response[0]['generated_text']

# Initialize RAG system
rag_system = RAGSystem()
