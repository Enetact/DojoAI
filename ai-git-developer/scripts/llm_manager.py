import os
import json
import torch
from llama_cpp import Llama

MODEL_PATH = os.getenv("DEEPSEEK_MODEL_PATH", "C:/DeepSeekAINonGit/models/small_models/initializer.gguf")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize DeepSeek-compatible model for embeddings
LLM = Llama(
    model_path=MODEL_PATH,
    n_ctx=131072,
    use_mmap=True,
    use_mlock=True,
    embedding=True,  # Required to use .create_embedding
    verbose=False
)

def get_embeddings(text):
    """Returns an embedding vector (list of floats) for a given input string."""
    if not text.strip():
        return []
    result = LLM.create_embedding(text)
    return result["data"][0]["embedding"]
