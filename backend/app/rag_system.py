import pandas as pd
from sentence_transformers import SentenceTransformer, util
from .data_processing import load_datasets
from .models import get_model

dataset1, dataset2 = load_datasets()
model = get_model()

def process_query(query: str) -> dict:
    query_embedding = model.encode(query)

    results = {}
    for dataset_name, dataset in [("Sustainability", dataset1), ("Christmas", dataset2)]:
        sentences = dataset["Survey Responses"].tolist()
        embeddings = model.encode(sentences)
        similarities = util.pytorch_cos_sim(query_embedding, embeddings)
        top_k = similarities.topk(k=3)

        top_responses = [sentences[i] for i in top_k[1][0].tolist()]
        results[dataset_name] = top_responses

    return results
