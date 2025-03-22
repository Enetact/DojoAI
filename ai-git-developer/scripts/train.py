import os
import sqlite3
import json
from deepseek_model import DeepSeek

DB_PATH = "C:/DeepSeekAINonGit/ai-git-developer/ai_memory.db"

def embed_and_store(text, agent="initializer"):
    embedding = DeepSeek.create_embedding(text)["data"][0]["embedding"]
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Ensure tables exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vector BLOB NOT NULL,
                metadata TEXT
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id INTEGER,
                message TEXT,
                embedding_id INTEGER,
                FOREIGN KEY (agent_id) REFERENCES agents(id),
                FOREIGN KEY (embedding_id) REFERENCES embeddings(id)
            );
        """)
        agent_id = ensure_agent_exists(conn, agent)

        # Insert embedding and reference in conversations
        cursor.execute("INSERT INTO embeddings (vector, metadata) VALUES (?, ?)", 
                       (json.dumps(embedding), json.dumps({"source": "train.py"})))
        embedding_id = cursor.lastrowid
        cursor.execute("INSERT INTO conversations (agent_id, message, embedding_id) VALUES (?, ?, ?)",
                       (agent_id, text, embedding_id))
        conn.commit()

def ensure_agent_exists(conn, name="initializer"):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM agents WHERE name = ?", (name,))
    row = cursor.fetchone()
    if not row:
        cursor.execute("INSERT INTO agents (name) VALUES (?)", (name,))
        return cursor.lastrowid
    return row[0]

if __name__ == "__main__":
    sample_texts = [
        "Let's build a frontend using Angular hosted on IIS.",
        "Connect the frontend to the backend API via REST.",
        "Ensure database interaction is secured and logged properly."
    ]

    for text in sample_texts:
        embed_and_store(text)
    
    print("Training data embedded and stored.")
