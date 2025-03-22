import torch

# Check if CUDA (GPU) is available
if torch.cuda.is_available():
    print(f" Using GPU: {torch.cuda.get_device_name(0)}")
    print(f"Memory Allocated: {torch.cuda.memory_allocated(0) / 1e9} GB")
    print(f"Memory Cached: {torch.cuda.memory_reserved(0) / 1e9} GB")
else:
    print(" No GPU available. Running on CPU.")
