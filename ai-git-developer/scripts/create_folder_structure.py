import os

# Define base path
BASE_PATH = "C:\\DeepSeekAI\\ai-git-developer"

# Define all required directories
FOLDERS = [
    "memory",
    "memory/conversations",
    "memory/chroma_memory",
    "memory/embeddings",
    "models",
    "models/trained-models",
    "models/small_models",
    "scripts",
    "web_ui",
    "web_ui/static",
    "web_ui/templates",
    "logs",
    "seed_data"
]

def create_folders():
    """Create all necessary folders for DeepSeek"""
    for folder in FOLDERS:
        path = os.path.join(BASE_PATH, folder)
        os.makedirs(path, exist_ok=True)
        print(f"Created: {path}")  

    print("\n All required folders have been set up!")

if __name__ == "__main__":
    create_folders()
