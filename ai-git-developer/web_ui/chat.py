from flask import Flask, render_template, request, jsonify
from embedding_manager import store_memory, retrieve_memory
from deepseek_model import DeepSeek
import os
import json

# Config
MODEL_PATH = os.getenv("DEEPSEEK_MODEL_PATH", "C:\\DeepSeekAINonGit\\models\\small_models\\initializer.gguf")
GIT_REPO_PATH = "C:\\DeepSeekAI"
FRONTEND_PATH = os.path.join(GIT_REPO_PATH, "frontend", "angular-ui")

# Initialize DeepSeek model
AI_MODEL = DeepSeek(
    model_path=MODEL_PATH,
    n_ctx=131072,
    use_mmap=True,
    use_mlock=True,
    verbose=True
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")

    # Store user input
    store_memory("user", user_message)

    # Pass prompt to DeepSeek
    prompt = f"""
You are an expert AI full-stack engineer.
Generate an Angular frontend hosted on IIS that connects to our Flask API server (port 5000) and uses our SQLite database at DEEPSEEK_DB_PATH.
Write the frontend code to: {FRONTEND_PATH}
Your response should include:
- Angular component structure
- IIS web.config for routing
- frontend/index.html with axios or fetch to call API
- Link data visually to the backend chat & memory

Only write real usable source code files.
"""
    result = AI_MODEL.create_completion(prompt=prompt, max_tokens=4096)
    ai_response = result['choices'][0]['text'].strip()

    # Save AI response and embed it
    store_memory("DeepSeek", ai_response)

    # Write generated code to local repo (if directory exists)
    os.makedirs(FRONTEND_PATH, exist_ok=True)
    with open(os.path.join(FRONTEND_PATH, "deepseek_ui_generated.md"), "w", encoding="utf-8") as f:
        f.write(ai_response)

    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(port=8081)
