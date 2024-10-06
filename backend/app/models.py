from sentence_transformers import SentenceTransformer

def get_model():
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'  
    model = SentenceTransformer(model_name)
    return model
