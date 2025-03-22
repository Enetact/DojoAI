import os
import sqlite3
from llama_cpp import Llama

# Paths
MODEL_PATH = os.getenv("DEEPSEEK_MODEL_PATH", "C:/DeepSeekAINonGit/models/small_models/initializer.gguf")
DB_PATH = os.getenv("DEEPSEEK_DB_PATH", "C:/DeepSeekAINonGit/ai-git-developer/ai_memory.db")

# Initialize model with safer context
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=8192,              # safer default
    embedding=True,
    use_mmap=True,
    use_mlock=True,
    verbose=True
)

def verify_schema():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(conversations);")
            columns = {col[1] for col in cursor.fetchall()}
            required = {"agent_id", "message", "response"}
            if not required.issubset(columns):
                print(f"WARNING: 'conversations' table is missing one of: {required}")
    except Exception as e:
        print(f"ERROR verifying schema: {e}")

# Safe generator using chat interface
def chat_with_deepseek(user_input: str):
    try:
        messages = [
            {"role": "system", "content": "You are DeepSeek, an expert autonomous AI developer."},
            {"role": "user", "content": user_input}
        ]

        result = llm.create_chat_completion(
            messages=messages,
            max_tokens=2048,
            temperature=0.7,
            stop=["<|EOT|>"]
        )

        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"Generation error: {e}"

def run_console_chat():
    print("DeepSeek Console Chat Ready. Type 'exit' to quit.\n")
    verify_schema()

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        reply = chat_with_deepseek(user_input)
        print(f"\nDeepSeek:\n{reply}\n")

if __name__ == "__main__":
    run_console_chat()
