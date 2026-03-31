import os
import faiss
import pickle
import numpy as np

os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'

from sentence_transformers import SentenceTransformer

MODEL = None
INDEX = None
METADATA = None

def init_engine():
    global MODEL, INDEX, METADATA
    
    if MODEL is not None:
        return
        
    base_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(base_dir, "..", "data", "faq.faiss")
    metadata_path = os.path.join(base_dir, "..", "data", "faq_metadata.pkl")
    
    if not os.path.exists(index_path) or not os.path.exists(metadata_path):
        raise FileNotFoundError("Missing AI files in the data folder")
        
    MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    INDEX = faiss.read_index(index_path)
    
    with open(metadata_path, 'rb') as f:
        METADATA = pickle.load(f)

def get_answer(user_query: str) -> dict:
    if MODEL is None:
        init_engine()
        
    query_emb = MODEL.encode([user_query], normalize_embeddings=True, convert_to_numpy=True)
    
    k = 3
    distances, indices = INDEX.search(query_emb, k)
    
    best_dist = float(distances[0][0])
    best_idx = int(indices[0][0])
    
    if best_idx == -1 or best_idx not in METADATA:
        return {
            "answer": "I am not sure about this one. Try checking official NUST guides or contact them directly.",
            "confidence": "Low",
            "note": "No match"
        }
        
    best_match_meta = METADATA[best_idx]
    base_answer = best_match_meta["answer"]
    has_more_info = best_match_meta.get("has_more_info", False)
    
    keywords = best_match_meta.get("keywords", [])
    query_lower = user_query.lower()
    if any(k.lower() in query_lower for k in keywords):
        best_dist = max(0.0, best_dist - 0.1)
    
    if best_dist < 0.4:
        confidence = "High"
        final_answer = base_answer
    elif best_dist < 0.8:
        confidence = "Medium"
        final_answer = "This seems relevant to your query: " + base_answer
    else:
        confidence = "Low"
        final_answer = "I am not sure about this one. Try checking official NUST guides or contact them directly."
        
    if has_more_info and confidence in ["High", "Medium"]:
        final_answer += "\n\nMore details might be in official manuals online."
        
    return {
        "answer": final_answer,
        "confidence": confidence,
        "note": f"Dist: {best_dist:.3f}"
    }

def handle_query(question: str) -> dict:
    result = get_answer(question)
    
    ans = result["answer"]
    conf = result["confidence"]
    
    if conf == "High":
        cred = "This is a direct match from the official student FAQ data."
    elif conf == "Medium":
        cred = "We found a likely match but please double check with NUST offices if you need exactity."
    else:
        cred = "An exact match was not found so I provided a general guideline."
        
    return {
        "answer": ans,
        "credibility": cred
    }
