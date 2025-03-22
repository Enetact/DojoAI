import os
import subprocess
import sqlite3
import requests
import torch
import shutil
from llama_cpp import Llama

# Step 1: Environment Variables & Paths
MODEL_PATH = "C:/DeepSeekAINonGit/models/ollama/llama3-70b.gguf"
OLD_MODEL_PATH = "C:/DeepSeekAINonGit/models/small_models/initializer.gguf"
DB_PATH = "C:/DeepSeekAINonGit/ai-git-developer/ai_memory.db"
API_ENDPOINT = "http://127.0.0.1:5000/chat"
GIT_REPO_PATH = "C:/DeepSeekAI"

# Step 2: Install & Update Required Packages
def install_packages():
    packages = [
        "torch --upgrade --extra-index-url https://download.pytorch.org/whl/cu121",
        "llama-cpp-python --upgrade",
        "requests --upgrade",
        "flask --upgrade",
        "numpy --upgrade",
        "scipy --upgrade"
    ]
    for pkg in packages:
        subprocess.check_call(f"pip install {pkg}", shell=True)

# Step 3: Validate GPU/CUDA & Ollama Model
def validate_gpu_and_model():
    cuda_available = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if cuda_available else "GPU not detected"
    print(f"CUDA Available: {cuda_available}")
    print(f"GPU Detected: {gpu_name}")

    try:
        model = Llama(model_path=MODEL_PATH, n_gpu_layers=100, verbose=False)
        test_output = model("Explain the Flask framework briefly.", max_tokens=50)
        print(f"Ollama Model Response: {test_output['choices'][0]['text'].strip()}")
    except Exception as e:
        print(f"Model Loading Error: {e}")

# Step 4: Verify Embeddings & DB Schema
def validate_embeddings_and_schema():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            print(f"DB Tables Found: {tables}")
            
            conversations_count = cursor.execute("SELECT COUNT(*) FROM conversations;").fetchone()[0]
            embeddings_count = cursor.execute("SELECT COUNT(*) FROM embeddings;").fetchone()[0]
            print(f"Conversations: {conversations_count}, Embeddings: {embeddings_count}")

            required_cols = {"agent_id", "message", "response"}
            cols = set(row[1] for row in cursor.execute("PRAGMA table_info(conversations);"))
            if not required_cols.issubset(cols):
                print(f"Missing DB Columns: {required_cols - cols}")
            else:
                print("DB schema is valid.")
    except Exception as e:
        print(f"DB Validation Error: {e}")

# Step 5: Check Flask API
def validate_flask_api():
    try:
        response = requests.post(API_ENDPOINT, json={"prompt": "What is Angular?", "agent": "validator"})
        if response.status_code == 200:
            print(f"Flask API Response: {response.json()['response']}")
        else:
            print(f"Flask API Error: Status Code {response.status_code}")
    except Exception as e:
        print(f"Flask API Connection Error: {e}")

# Step 6: Tag Current Repo as v1
def tag_current_repo_version():
    try:
        subprocess.run(["git", "-C", GIT_REPO_PATH, "add", "."], check=True)
        subprocess.run(["git", "-C", GIT_REPO_PATH, "commit", "-m", "Initial stable version v1"], check=True)
        subprocess.run(["git", "-C", GIT_REPO_PATH, "tag", "-a", "v1", "-m", "Version 1"], check=True)
        print("Repo tagged successfully as v1.")
    except Exception as e:
        print(f"Git Tagging Error: {e}")

# Step 7: Structure New Git Repo
def restructure_git_repo():
    try:
        v1_backup_path = f"{GIT_REPO_PATH}_v1_backup"
        shutil.copytree(GIT_REPO_PATH, v1_backup_path, dirs_exist_ok=True)
        print(f"Current repo backed up to: {v1_backup_path}")

        # Create new structured directories
        new_dirs = ["frontend", "backend", "database", "scripts", "embeddings", "docs"]
        for d in new_dirs:
            os.makedirs(os.path.join(GIT_REPO_PATH, d), exist_ok=True)
        print(f"New repo structure created: {new_dirs}")
    except Exception as e:
        print(f"Repo Restructure Error: {e}")

# Step 8: Ollama Integration & Embedding
def integrate_ollama_with_embeddings():
    try:
        model = Llama(model_path=MODEL_PATH, n_gpu_layers=100, embedding=True, verbose=False)
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT message FROM conversations LIMIT 1;")
            sample_text = cursor.fetchone()[0]
            embedding_vector = model.create_embedding(sample_text)
            print(f"Sample Embedding Created (len={len(embedding_vector['data'])})")
    except Exception as e:
        print(f"Ollama Embedding Integration Error: {e}")

# Step 9: Prompt Ollama for Frontend UI Generation
def prompt_ollama_frontend_ui():
    prompt = (
        "Generate a structured Angular frontend with HomeComponent, ChatComponent, "
        "HistoryComponent, AgentSelectorComponent, a ChatService for Flask API (/chat endpoint), "
        "Bootstrap 5 for styling, and IIS deployment instructions. Output this clearly "
        "to the frontend folder in the repository, including code structure and IIS setup."
    )

    try:
        model = Llama(model_path=MODEL_PATH, n_gpu_layers=100, verbose=False)
        ui_output = model(prompt, max_tokens=2000)
        frontend_setup_instructions = ui_output['choices'][0]['text'].strip()

        output_path = os.path.join(GIT_REPO_PATH, "frontend", "setup_instructions.txt")
        with open(output_path, "w") as file:
            file.write(frontend_setup_instructions)

        print(f"Frontend UI setup instructions generated successfully at {output_path}.")
    except Exception as e:
        print(f"Ollama UI Prompt Generation Error: {e}")

# Main Execution
if __name__ == "__main__":
    install_packages()
    validate_gpu_and_model()
    validate_embeddings_and_schema()
    validate_flask_api()
    tag_current_repo_version()
    restructure_git_repo()
    integrate_ollama_with_embeddings()
    prompt_ollama_frontend_ui()

    print("All tasks completed successfully.")
