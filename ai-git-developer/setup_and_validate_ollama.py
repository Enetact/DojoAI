import subprocess
import sqlite3
import requests
import shutil
import os
import ollama
import torch

# Paths
DB_PATH = "C:/DeepSeekAINonGit/ai-git-developer/ai_memory.db"
API_ENDPOINT = "http://127.0.0.1:5000/chat"
GIT_REPO_PATH = "C:/DeepSeekAI"

# Step 1: Ensure Ollama installed and model pulled
def ensure_ollama_model():
    subprocess.run("ollama pull llama3:70b", shell=True, check=True)
    subprocess.run("ollama cp llama3:70b localdev", shell=True, check=True)
    print("Ollama llama3:70b ready and tagged as localdev.")

# Step 2: Validate GPU
def validate_gpu():
    cuda_available = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if cuda_available else "No GPU detected"
    print(f"CUDA Available: {cuda_available}, GPU: {gpu_name}")

# Step 3: Validate DB schema and Embeddings
def validate_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        print("DB Tables:", tables)

        conv_count = cursor.execute("SELECT COUNT(*) FROM conversations;").fetchone()[0]
        emb_count = cursor.execute("SELECT COUNT(*) FROM embeddings;").fetchone()[0]
        print(f"Conversations: {conv_count}, Embeddings: {emb_count}")

# Step 4: Validate Flask API
def validate_api():
    try:
        response = requests.post(API_ENDPOINT, json={"prompt": "What is Flask?"})
        if response.ok:
            print("API Response:", response.json()["response"])
        else:
            print("API Error:", response.status_code)
    except Exception as e:
        print("API Connection Error:", e)

# Step 5: Tag current code repo as v1
def tag_git_repo():
    subprocess.run(f"git -C {GIT_REPO_PATH} add .", shell=True, check=True)
    subprocess.run(f'git -C {GIT_REPO_PATH} commit -m "Stable v1"', shell=True, check=True)
    subprocess.run(f'git -C {GIT_REPO_PATH} tag v1', shell=True, check=False)
    print("Repo tagged as v1.")

# Step 6: Backup and restructure repo
def restructure_repo():
    backup_path = f"{GIT_REPO_PATH}_v1_backup"
    shutil.copytree(GIT_REPO_PATH, backup_path, dirs_exist_ok=True)
    print(f"Backup created at {backup_path}")

    dirs = ["frontend", "backend", "database", "scripts", "embeddings", "docs"]
    for d in dirs:
        os.makedirs(os.path.join(GIT_REPO_PATH, d), exist_ok=True)
    print("New repo structure created.")

# Step 7: Ollama embedding example
def ollama_embedding_example():
    response = ollama.embeddings(model='localdev', prompt='Example embedding')
    print("Embedding vector length:", len(response["embedding"]))

# Step 8: Prompt Ollama to Generate UI instructions
def generate_ui_instructions():
    prompt = (
        "Generate detailed instructions to build a full Angular frontend with components: "
        "HomeComponent, ChatComponent, HistoryComponent, AgentSelectorComponent, ChatService "
        "connecting to a Flask API at '/chat', styled with Bootstrap 5, and include IIS setup steps."
    )

    response = ollama.generate(model='localdev', prompt=prompt, options={"temperature":0.7})
    instructions = response['response']

    frontend_path = os.path.join(GIT_REPO_PATH, "frontend", "setup_ui_instructions.txt")
    with open(frontend_path, "w") as f:
        f.write(instructions)

    print(f"UI setup instructions saved at {frontend_path}")

# Main execution
if __name__ == "__main__":
    ensure_ollama_model()
    validate_gpu()
    validate_db()
    validate_api()
    tag_git_repo()
    restructure_repo()
    ollama_embedding_example()
    generate_ui_instructions()

    print("Setup and validation completed.")
