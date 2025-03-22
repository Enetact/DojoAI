from flask import Flask, render_template
from memory_store import get_conversation_history

app = Flask(__name__)

@app.route('/')
def index():
    history = get_conversation_history()
    return render_template('dashboard.html', history=history)

if __name__ == "__main__":
    app.run(port=8080)
