import os
from llama_cpp import Llama
import torch

class DeepSeek:
    def __init__(self,
                 model_path: str = None,
                 n_ctx: int = 16384,
                 embedding: bool = False,
                 use_mmap: bool = True,
                 use_mlock: bool = True,
                 n_gpu_layers: int = -1,
                 verbose: bool = False):

        self.model_path = model_path or os.getenv("DEEPSEEK_MODEL_PATH")
        if not self.model_path or not os.path.exists(self.model_path):
            raise FileNotFoundError(f"DeepSeek GGUF model not found at: {self.model_path}")

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        self.model = Llama(
            model_path=self.model_path,
            n_ctx=n_ctx,
            embedding=embedding,
            use_mmap=use_mmap,
            use_mlock=use_mlock,
            n_gpu_layers=n_gpu_layers,
            verbose=verbose
        )

    def chat(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.7, stop: list = ["<|EOT|>"]) -> str:
        tokens = prompt.split()
        if len(tokens) > self.model.context_params.n_ctx - max_tokens:
            prompt = " ".join(tokens[-(self.model.context_params.n_ctx - max_tokens):])

        result = self.model.create_completion(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=stop
        )

        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["text"].strip()
        else:
            raise ValueError(f"Model response invalid: {result}")

    def create_embedding(self, text: str) -> dict:
        embedding_result = self.model.create_embedding(text)
        if "data" in embedding_result:
            return embedding_result
        else:
            raise ValueError(f"Embedding generation failed: {embedding_result}")
