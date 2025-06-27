# 🧠 DojoAI

**DojoAI** is a modular, local-first AI framework that combines large language models (LLMs), vector databases (ChromaDB), SQLite for storage, and a Gradio-based UI to enable secure, private, and powerful Retrieval-Augmented Generation (RAG) pipelines—all running locally on a Windows 11 machine.

---

## 🚀 Features

- 🧩 Modular architecture: Swap or extend models easily
- 💾 Local SQLite & ChromaDB: Lightweight persistence and vector search
- 🧠 LLM Integration: Ollama, OpenAI, DeepSeek support
- 🖥️ Gradio UI: Clean, interactive local web interface
- 📁 Seeded RAG: Populate knowledge base with markdown/documents
- 🔒 Full local setup (No WSL, no cloud dependency)

---

## 🖥️ Requirements

- Windows 11 (No WSL required)
- Miniconda 3 (Python 3.9+)
- Git for Windows
- Optional: GPU support for faster local inference

---

## 📦 Installation Guide

### 1. Install Prerequisites

- [Miniconda 3 (Windows)](https://docs.conda.io/en/latest/miniconda.html#windows-installers)
- [Git for Windows](https://git-scm.com/download/win)
- [Ollama (for local LLMs)](https://ollama.com/)

### 2. Clone the Repository

```bash
git clone https://github.com/Enetact/DojoAI.git
cd DojoAI
```

### 3. Create Python Environment

```bash
conda create -n dojoai python=3.9 -y
conda activate dojoai
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing, manually install:
```bash
pip install torch gradio langchain chromadb tiktoken openai
```

### 5. (Optional) Setup Ollama for Local LLM Inference

Install models like:
```bash
ollama run llama3
ollama run deepseek-coder
```

---

## 🗃️ Database Setup

### 6. Initialize SQLite

Creates a lightweight document store:
```bash
python init_db.py
```
> This creates `dojoai.db` with a `documents` table.

### 7. Initialize Chroma Vector DB

Chroma uses local `duckdb+parquet` setup:
```python
from chromadb import Client
from chromadb.config import Settings

client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db"))
client.create_collection(name="documents")
```

---

## 📥 Seeding RAG Knowledge

Place your markdown or .txt files into the `seed_data/` folder.

Then run:
```bash
python embed_seed_data.py
```

> This script:
> - Reads each file
> - Stores plain text in SQLite
> - Embeds and indexes vectors in ChromaDB using OpenAI embeddings

> 🔑 Make sure your `OPENAI_API_KEY` is set in a `.env` or within `embed_seed_data.py`.

---

## 💻 Running the App

```bash
python web_ui/app.py
```

Then open: [http://127.0.0.1:7860](http://127.0.0.1:7860)

---

## 🧰 Configuration

Edit `config.py` for:
- LLM selection (OpenAI, Ollama, etc.)
- Vector DB path
- Embedding strategy
- API keys

---

## 🧪 Example Workflow

1. Clone repo and install requirements
2. Drop some `.md` files into `seed_data/`
3. Run `embed_seed_data.py`
4. Launch `app.py` and chat with your documents!

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| `No module named chromadb` | Run `pip install chromadb` |
| UI doesn’t load | Ensure Gradio is installed and port 7860 is free |
| Embeddings fail | Check `OPENAI_API_KEY` is correctly set |
| ChromaDB error | Delete `/chroma_db/` folder and reinitialize |

---

