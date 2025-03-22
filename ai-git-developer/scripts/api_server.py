from flask import Flask, request, jsonify
import sqlite3
import json
import torch
from llm_manager import ask_agent, get_embeddings

app = Flask(__name__)

DB_PATH = "C:/DeepSeekAINonGit/ai-git-developer/ai_memory.db"


# Auto-detect GPU or use CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device.upper()}")

def connect_db():
    """Connect to SQLite database."""
    return sqlite3.connect(DB_PATH)

def store_conversation(agent, user_message, ai_response):
    """Stores user messages and AI responses in the database."""
    conn = connect_db()
    cursor = conn.cursor()

    # Ensure agent exists
    cursor.execute("INSERT OR IGNORE INTO agents (name) VALUES (?)", (agent,))
    cursor.execute("SELECT id FROM agents WHERE name=?", (agent,))
    agent_id = cursor.fetchone()[0]

    # Generate embedding for the message
    user_embedding = json.dumps(get_embeddings(user_message))
    ai_embedding = json.dumps(get_embeddings(ai_response))

    # Store message and response
    cursor.execute(
        "INSERT INTO conversations (agent_id, message) VALUES (?, ?)", (agent_id, user_message)
    )
    cursor.execute(
        "INSERT INTO conversations (agent_id, message) VALUES (?, ?)", (agent_id, ai_response)
    )

    # Store embeddings
    cursor.execute(
        "INSERT INTO embeddings (vector, metadata) VALUES (?, ?)", (user_embedding, json.dumps({"type": "user_message"}))
    )
    cursor.execute(
        "INSERT INTO embeddings (vector, metadata) VALUES (?, ?)", (ai_embedding, json.dumps({"type": "ai_response"}))
    )

    conn.commit()
    conn.close()

@app.route('/query', methods=['POST'])
def query_agents():
    """Handles user queries and generates AI responses."""
    data = request.json
    agent = data.get("agent")
    prompt = data.get("prompt")

    response = ask_agent(agent, prompt)
    
    # Store conversation for learning
    store_conversation(agent, prompt, response)

    return jsonify({"response": response})

@app.route('/store', methods=['POST'])
def store_data():
    """Allows manual storage of conversation data."""
    data = request.json
    agent = data.get("agent")
    user_message = data.get("user_message")
    ai_response = data.get("ai_response")

    store_conversation(agent, user_message, ai_response)

    return jsonify({"message": "Data stored successfully."})

@app.route('/train', methods=['POST'])
def train_ai():
    """Triggers on-demand AI training from stored embeddings."""
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch stored embeddings
    cursor.execute("SELECT vector FROM embeddings")
    embedding_rows = cursor.fetchall()

    if not embedding_rows:
        return jsonify({"error": "No embeddings found for training."})

    embeddings = [json.loads(row[0]) for row in embedding_rows]

    # Send embeddings to the AI model for training (simulated for now)
    # TODO: Implement actual model fine-tuning using embeddings
    print(f"Training AI with {len(embeddings)} embeddings...")

    conn.close()
    return jsonify({"message": "AI training triggered successfully."})

if __name__ == "__main__":
    app.run(port=5000)
