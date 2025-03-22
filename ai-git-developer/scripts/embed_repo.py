import os
import sqlite3
import json
import torch
from llm_manager import get_embeddings  # Reuse existing embedding function

REPO_PATH = "C:/DeepSeekAI"
DB_PATH = "C:/DeepSeekAINonGit/ai-git-developer/ai_memory.db"

SUPPORTED_EXTENSIONS = [".py", ".md", ".txt", ".json", ".html", ".css", ".js"]

def connect_db():
    return sqlite3.connect(DB_PATH)

def clean_text(text):
    return ' '.join(text.split())

def store_embedding(conn, agent_id, message, embedding, metadata_type):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversations (agent_id, message) VALUES (?, ?)", (agent_id, message))
    cursor.execute("INSERT INTO embeddings (vector, metadata) VALUES (?, ?)", (json.dumps(embedding), json.dumps({"type": metadata_type})))
    conn.commit()

def ensure_agent(conn, name="code_trainer"):
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO agents (name) VALUES (?)", (name,))
    cursor.execute("SELECT id FROM agents WHERE name=?", (name,))
    return cursor.fetchone()[0]

def extract_code_chunks(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    content = clean_text(content)
    chunks = [content[i:i+1024] for i in range(0, len(content), 1024)]
    return chunks

def process_repo():
    conn = connect_db()
    agent_id = ensure_agent(conn, "code_trainer")

    for root, _, files in os.walk(REPO_PATH):
        for file in files:
            if any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                full_path = os.path.join(root, file)
                try:
                    print(f"Embedding: {full_path}")
                    for chunk in extract_code_chunks(full_path):
                        if chunk.strip():
                            embedding = get_embeddings(chunk)
                            store_embedding(conn, agent_id, chunk, embedding, "repo_code")
                except Exception as e:
                    print(f"Error processing {full_path}: {e}")

    conn.close()
    print("Repository embedding complete.")

if __name__ == "__main__":
    process_repo()
