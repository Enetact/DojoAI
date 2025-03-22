import os
from llama_cpp import Llama

class DeepSeek:
    def __init__(self,
                 model_path: str = None,
                 n_ctx: int = 16384,
                 embedding: bool = False,
                 use_mmap: bool = True,
                 use_mlock: bool = True,
                 verbose: bool = False):

        self.model_path = model_path or os.getenv("DEEPSEEK_MODEL_PATH")
        if not self.model_path or not os.path.exists(self.model_path):
            raise FileNotFoundError(f"DeepSeek GGUF model not found at: {self.model_path}")

        self.model = Llama(
            model_path=self.model_path,
            n_ctx=n_ctx,
            embedding=embedding,
            use_mmap=use_mmap,
            use_mlock=use_mlock,
            verbose=verbose
        )

    def chat(self, prompt: str, max_tokens: int = 2048) -> str:
        result = self.model.create_completion(prompt=prompt, max_tokens=max_tokens)
        return result["choices"][0]["text"].strip()

    def create_embedding(self, text: str) -> dict:
        return self.model.create_embedding(text)
