import sqlite3
import faiss
import numpy as np

DB_PATH = "C:\\DeepSeekAI\\ai-git-developer\\memory\\ai_memory.db"

def get_existing_features():
    """Retrieve existing features from memory"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT response FROM project_memory WHERE prompt = 'Application Planning'")
    results = cursor.fetchall()
    conn.close()
    
    return [r[0] for r in results]

def predict_future_apps():
    """Predict future applications that could be built"""
    past_features = get_existing_features()
    if not past_features:
        return "No prior knowledge found. Please define project first."
    
    vectorized_features = np.random.rand(len(past_features), 256).astype("float32")
    
    faiss_index = faiss.IndexFlatL2(256)
    faiss_index.add(vectorized_features)
    
    _, suggested_indices = faiss_index.search(np.random.rand(1, 256).astype("float32"), 3)
    predictions = [past_features[i] for i in suggested_indices[0]]
    
    return predictions

# Output next applications to build
next_apps = predict_future_apps()
print("🔮 Predicted Next Applications:", next_apps)
