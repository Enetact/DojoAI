import os
import subprocess
import sqlite3
import chromadb
import git

# Define project paths
BASE_PATH = "C:\\DeepSeekAI\\ai-git-developer"
DB_PATH = os.path.join(BASE_PATH, "memory", "ai_memory.db")
CHROMA_PATH = os.path.join(BASE_PATH, "memory", "chroma_memory")
REPO_PATH = BASE_PATH

def install_dependencies():
    """Install required Python packages"""
    subprocess.run(["pip", "install", "llama-cpp-python", "chromadb", "faiss-cpu", "flask", "gitpython"], check=True)


def setup_sqlite():
    """Initialize SQLite for structured memory"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS conversations 
                      (id INTEGER PRIMARY KEY, agent TEXT, message TEXT)''')
    conn.commit()
    conn.close()

def setup_chroma_db():
    """Initialize ChromaDB for vector storage"""
    os.makedirs(CHROMA_PATH, exist_ok=True)
    chromadb.PersistentClient(path=CHROMA_PATH)

def setup_git():
    """Initialize a local Git repository for AI development"""
    if not os.path.exists(REPO_PATH):
        os.makedirs(REPO_PATH)
        repo = git.Repo.init(REPO_PATH)
        repo.git.config("user.name", "DeepSeekAI")
        repo.git.config("user.email", "deepseek@local.dev")
        print(f" Git repository initialized at {REPO_PATH}")

        # Commit initial code
        repo.git.add(all=True)
        repo.git.commit("-m", "Initial commit by DeepSeek AI")
        print(" Initial commit completed.")

if __name__ == "__main__":
    install_dependencies()
    setup_sqlite()
    setup_chroma_db()
    setup_git()
    print("\n DeepSeek AI environment is fully set up!")
