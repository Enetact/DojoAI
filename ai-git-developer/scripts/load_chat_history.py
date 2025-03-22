import sqlite3
import json

DB_PATH = "C:\\DeepSeekAI\\ai-git-developer\\memory\\ai_memory.db"

def load_chat_history():
    """Loads and formats chat history from the database for AI training."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT agent_id, message, embedding_id FROM conversations ORDER BY id ASC")
        chat_data = cursor.fetchall()

        if not chat_data:
            print("No chat history found.")
            return ""

        formatted_chat = []
        for agent_id, message, embedding_id in chat_data:
            cursor.execute("SELECT name FROM agents WHERE id=?", (agent_id,))
            agent_name = cursor.fetchone()[0]

            cursor.execute("SELECT vector FROM embeddings WHERE id=?", (embedding_id,))
            embedding_vector = cursor.fetchone()[0]

            formatted_chat.append(f"{agent_name}: {message} | EMBEDDING: {embedding_vector}")

        return "\n".join(formatted_chat)

if __name__ == "__main__":
    chat_history = load_chat_history()
    if chat_history:
        print(f"Loaded Chat History:\n{chat_history}")
