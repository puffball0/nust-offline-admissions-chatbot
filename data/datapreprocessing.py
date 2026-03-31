import json
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

def build_index(data_path, index_path, metadata_path):
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"No {data_path} found")
        
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = []
    metadata = {}
    
    for i, item in enumerate(data):
        question = item.get("question", item.get("Question", "")).strip()
        answer = item.get("answer", item.get("Answer", "")).strip()
        has_more_info = item.get("has_more_info", False)
        keywords = item.get("keywords", [])
        
        if not question or not answer:
            continue
            
        questions.append(question)
        metadata[i] = {
            "question": question,
            "answer": answer,
            "has_more_info": has_more_info,
            "keywords": keywords
        }

    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(questions, normalize_embeddings=True, convert_to_numpy=True)
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    faiss.write_index(index, index_path)
    
    with open(metadata_path, 'wb') as f:
        pickle.dump(metadata, f)

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE = os.path.join(BASE_DIR, "qa.json")
    INDEX_FILE = os.path.join(BASE_DIR, "faq.faiss")
    METADATA_FILE = os.path.join(BASE_DIR, "faq_metadata.pkl")
    
    build_index(DATA_FILE, INDEX_FILE, METADATA_FILE)
