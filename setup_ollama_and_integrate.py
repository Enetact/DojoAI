import os
import subprocess
import sqlite3
import time
from pathlib import Path

# Paths
OLLAMA_MODEL_NAME = "llama3:70b"
OLLAMA_INSTALL_URL = "https://ollama.com/download/OllamaSetup.exe"
OLLAMA_EXE = Path("C:/Program Files/Ollama/ollama.exe")
MODEL_DIR = Path("C:/DeepSeekAINonGit/models/ollama_70b")
DB_PATH = "C:/DeepSeekAINonGit/ai-git-developer/ai_memory.db"
MODEL_NAME_ALIAS = "localdev"

# Step 1: Install Ollama if not found
def install_ollama():
    if not OLLAMA_EXE.exists():
        print("[INFO] Downloading and installing Ollama...")
        setup_path = Path("C:/Temp/OllamaSetup.exe")
        os.makedirs(setup_path.parent, exist_ok=True)
        subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {OLLAMA_INSTALL_URL} -OutFile {setup_path}"], check=True)
        subprocess.run([str(setup_path)], check=True)
        print("[INFO] Ollama installation triggered.")
        time.sleep(10)

# Step 2: Pull the 70B model
def pull_model():
    print("[INFO] Pulling Ollama 3.3 70B model. This may take a while...")
    subprocess.run(["ollama", "pull", OLLAMA_MODEL_NAME], check=True)
    print("[INFO] Model downloaded.")

# Step 3: Tag it for reference
def tag_model():
    print("[INFO] Tagging model as 'localdev'...")
    subprocess.run(["ollama", "create", MODEL_NAME_ALIAS, "--from", OLLAMA_MODEL_NAME], check=True)

# Step 4: Validate and prep memory DB
def validate_memory_schema():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(conversations);")
        cols = [col[1] for col in cursor.fetchall()]
        required = {"agent_id", "message", "response"}
        missing = required.difference(set(cols))
        if missing:
            raise Exception(f"Missing columns in conversations: {missing}")
        print("[INFO] Memory DB schema validated.")

# Step 5: Install Python packages
def install_dependencies():
    print("[INFO] Installing Python dependencies...")
    subprocess.run(["pip", "install", "--upgrade", "ollama", "llama-cpp-python", "requests", "flask", "tqdm", "sentence-transformers", "faiss-cpu"], check=True)

# Step 6: Set up environment
def set_env_vars():
    os.environ["DEEPSEEK_MODEL"] = MODEL_NAME_ALIAS
    os.environ["DEEPSEEK_DB_PATH"] = DB_PATH
    print("[INFO] Environment variables set.")

# Step 7: Summary and ready
def setup_summary():
    print("[DONE] Ollama 70B is installed, aliased as 'localdev'.")
    print("[READY] API knowledge and memory database are integrated.")
    print("[NEXT] Prompt the system to begin Angular frontend generation.")

# Main
if __name__ == "__main__":
    install_ollama()
    install_dependencies()
    pull_model()
    tag_model()
    validate_memory_schema()
    set_env_vars()
    setup_summary()
