import sqlite3
import json
import torch
from llama_cpp import Llama

DB_PATH = "C:/DeepSeekAI/memory/ai_memory.db"
MODEL_PATH = "C:/DeepSeekAI/models/small_models/initializer.gguf"

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Training using device: {device.upper()}")

# Load AI model
AGENTS = {
    "trainer": Llama(
        model_path=MODEL_PATH,
        n_ctx=131072,
        use_mmap=True,
        use_mlock=True,
        verbose=True
    )
}

def connect_db():
    """Connect to SQLite database."""
    return sqlite3.connect(DB_PATH)

def fetch_embeddings():
    """Retrieve embeddings from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT vector FROM embeddings")
    embeddings = [json.loads(row[0]) for row in cursor.fetchall()]
    conn.close()
    return embeddings

def train_model():
    """Train the AI model with stored embeddings."""
    embeddings = fetch_embeddings()
    if not embeddings:
        print("No embeddings found for training.")
        return

    # Simulating AI Training (replace with actual fine-tuning logic)
    print(f"Training AI model with {len(embeddings)} embeddings...")

    # TODO: Implement actual fine-tuning

if __name__ == "__main__":
    train_model()
