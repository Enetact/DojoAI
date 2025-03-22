from flask import Flask, render_template, request, jsonify
from embedding_manager import store_memory, retrieve_memory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    ai_response = "I am still learning, but I will improve over time!"  # Placeholder response

    # Store chat log in embeddings
    store_memory("user", user_message)
    store_memory("DeepSeek", ai_response)

    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(port=8081)
