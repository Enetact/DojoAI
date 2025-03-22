import sqlite3
import torch
import json
from llama_cpp import Llama

# Database Path
DB_PATH = "C:\\DeepSeekAI\\memory\\ai_memory.db"

# Model Path
MODEL_PATH = "C:\\DeepSeekAI\\models\\small_models\\initializer.gguf"

# Auto-detect GPU or use CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device.upper()}")

# Load Llama Model with GPU offloading
AGENTS = {
    "initializer": Llama(
        model_path=MODEL_PATH,
        n_ctx=131072,  # Start with 128K tokens
        use_mmap=True,
        use_mlock=True,
        verbose=True
    )
}

def connect_db():
    """Connect to SQLite database."""
    return sqlite3.connect(DB_PATH)

def validate_database():
    """Validate AI database integrity before querying"""
    conn = connect_db()
    cursor = conn.cursor()

    required_tables = ["conversations", "agents", "embeddings", "api_requests"]
    for table in required_tables:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        if not cursor.fetchone():
            print(f"Table '{table}' not found in ai_memory.db")
            conn.close()
            return False

    conn.close()
    return True

def get_chat_history():
    """Retrieve chat history for AI learning"""
    if not validate_database():
        return ""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT agents.name, conversations.message 
        FROM conversations
        LEFT JOIN agents ON conversations.agent_id = agents.id
        ORDER BY conversations.timestamp ASC
    """)
    chat_data = cursor.fetchall()
    conn.close()

    formatted_chat = "\n".join([f"{agent}: {message}" for agent, message in chat_data])
    return formatted_chat

def insert_new_conversation(agent_name, user_message, ai_response):
    """Store new AI conversation in database"""
    conn = connect_db()
    cursor = conn.cursor()

    # Ensure agent exists
    cursor.execute("SELECT id FROM agents WHERE name=?", (agent_name,))
    agent_id = cursor.fetchone()
    if not agent_id:
        cursor.execute("INSERT INTO agents (name) VALUES (?)", (agent_name,))
        agent_id = cursor.lastrowid
    else:
        agent_id = agent_id[0]

    # Insert new conversation
    cursor.execute("""
        INSERT INTO conversations (agent_id, message) 
        VALUES (?, ?)
    """, (agent_id, user_message))
    conversation_id = cursor.lastrowid

    # Insert AI response
    cursor.execute("""
        INSERT INTO conversations (agent_id, message) 
        VALUES (?, ?)
    """, (agent_id, ai_response))

    conn.commit()
    conn.close()
    print(f" Stored new AI conversation with ID {conversation_id}")

def insert_embedding(conversation_id, vector, metadata=None):
    """Store AI embeddings"""
    conn = connect_db()
    cursor = conn.cursor()

    metadata_json = json.dumps(metadata) if metadata else "{}"
    
    cursor.execute("""
        INSERT INTO embeddings (vector, metadata)
        VALUES (?, ?)
    """, (vector, metadata_json))

    embedding_id = cursor.lastrowid

    # Link the embedding to the conversation
    cursor.execute("""
        UPDATE conversations 
        SET embedding_id = ? 
        WHERE id = ?
    """, (embedding_id, conversation_id))

    conn.commit()
    conn.close()
    print(f" Stored new embedding with ID {embedding_id}")

def initialize_setup():
    """AI reads chat history, responds, and stores new data"""
    chat_history = get_chat_history()
    if not chat_history:
        print("No chat history found. Skipping setup.")
        return

    response = AGENTS["initializer"].create_completion(
        prompt=f"Based on this chat history, set up all necessary infrastructure and start development.\n\n{chat_history}",
        max_tokens=16384,  # Avoid OOM errors
    )

    ai_response = response['choices'][0]['text'].strip()

    # Simulating new user input for AI processing
    user_message = "How should we structure the AI pipeline?"
    agent_name = "DeepSeekAI"

    # Store conversation and embedding
    insert_new_conversation(agent_name, user_message, ai_response)
    insert_embedding(1, b"VECTOR_DATA_HERE")  # Replace with actual vector data

    print(f"AI Initializer Response:\n{ai_response}\n")

if __name__ == "__main__":
    initialize_setup()
