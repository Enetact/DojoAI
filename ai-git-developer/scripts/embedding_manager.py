import sqlite3
import json
from datetime import datetime
from llama_cpp import Llama

DB_PATH = "C:\\DeepSeekAINonGit\\ai-git-developer\\ai_memory.db"
MODEL_PATH = "C:\\DeepSeekAINonGit\\models\\small_models\\initializer.gguf"

AI_MODEL = Llama(
    model_path=MODEL_PATH,
    n_ctx=131072,
    embedding=True,
    use_mmap=True,
    use_mlock=True
)

def store_memory(agent, message):
    """Stores chat message and its embedding"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        embedding = AI_MODEL.create_embedding(message)["data"][0]["embedding"]
        embedding_json = json.dumps(embedding)
        cursor.execute("INSERT INTO embeddings (vector, metadata) VALUES (?, ?)", (embedding_json, '{}'))
        embedding_id = cursor.lastrowid
        cursor.execute("SELECT id FROM agents WHERE name=?", (agent,))
        agent_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO conversations (agent_id, message, embedding_id, timestamp) VALUES (?, ?, ?, ?)",
                       (agent_id, message, embedding_id, datetime.utcnow()))
        conn.commit()

def retrieve_memory(limit=10):
    """Returns the latest N chat entries"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.name, c.message
            FROM conversations c
            JOIN agents a ON c.agent_id = a.id
            ORDER BY c.timestamp DESC
            LIMIT ?
        """, (limit,))
        return cursor.fetchall()
