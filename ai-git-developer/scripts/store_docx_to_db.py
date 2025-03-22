import os
import sqlite3
import json
import re
from docx import Document
from deepseek_model import DeepSeek

DOCX_FILE = "C:/DeepSeekAI/ai-git-developer/memory/seed_data/AIDEVCHAT.docx"
DB_PATH = "C:/DeepSeekAINonGit/ai-git-developer/ai_memory.db"

def clean_text(text):
    text = re.sub(r"[^a-zA-Z0-9\s.,!?]", "", text)
    return re.sub(r"\s+", " ", text).strip()

def extract_text_from_docx():
    if not os.path.exists(DOCX_FILE):
        return []
    doc = Document(DOCX_FILE)
    return [clean_text(p.text) for p in doc.paragraphs if p.text.strip()]

def ensure_agent_exists(conn, name="initializer"):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM agents WHERE name=?", (name,))
    agent = cursor.fetchone()
    if agent:
        return agent[0]
    cursor.execute("INSERT INTO agents (name) VALUES (?)", (name,))
    return cursor.lastrowid

def store_messages(messages):
    if not messages:
        return

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

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

        agent_id = ensure_agent_exists(conn)

        for message in messages:
            embedding = DeepSeek.create_embedding(message)["data"][0]["embedding"]
            cursor.execute("INSERT INTO embeddings (vector, metadata) VALUES (?, ?)", 
                           (json.dumps(embedding), json.dumps({"source": "docx"})))
            embedding_id = cursor.lastrowid
            cursor.execute("INSERT INTO conversations (agent_id, message, embedding_id) VALUES (?, ?, ?)",
                           (agent_id, message, embedding_id))

        conn.commit()
        print("Messages from DOCX stored and embedded.")

if __name__ == "__main__":
    store_messages(extract_text_from_docx())
