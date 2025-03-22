import sqlite3
from flask import Flask, request, jsonify
from deepseek_model import DeepSeek

# Paths
DB_PATH = "C:/DeepSeekAINonGit/ai-git-developer/ai_memory.db"
MODEL_PATH = "C:/DeepSeekAINonGit/models/small_models/initializer.gguf"

# Initialize DeepSeek (which wraps Llama)
deepseek_instance = DeepSeek(
    model_path=MODEL_PATH,
    n_ctx=131072,
    use_mmap=True,
    use_mlock=True,
    embedding=True,
    verbose=True
)

# Access the underlying llama model (llama_cpp.Llama instance)
llm = deepseek_instance.model if hasattr(deepseek_instance, "model") else deepseek_instance

app = Flask(__name__)

def store_conversation(agent, message, response):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id INTEGER,
                message TEXT,
                response TEXT
            )
        """)
        agent_id = ensure_agent_exists(conn, agent)
        cursor.execute("INSERT INTO conversations (agent_id, message, response) VALUES (?, ?, ?)",
                       (agent_id, message, response))
        conn.commit()

def ensure_agent_exists(conn, name="initializer"):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM agents WHERE name = ?", (name,))
    row = cursor.fetchone()
    if not row:
        cursor.execute("INSERT INTO agents (name) VALUES (?)", (name,))
        return cursor.lastrowid
    return row[0]

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")
    agent = data.get("agent", "initializer")

    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400

    #  Call create_completion on llama_cpp.Llama instance
    result = llm.create_completion(
        prompt=prompt,
        max_tokens=2048,
        temperature=0.7,
        stop=["<|EOT|>"]
    )
    answer = result["choices"][0]["text"].strip()
    store_conversation(agent, prompt, answer)
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
