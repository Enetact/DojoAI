
# 🧠 DojoAI

DojoAI is a modular framework designed to integrate and experiment with various Large Language Models (LLMs), facilitating the development of AI-driven applications. It supports seamless integration with models like DeepSeek and Ollama, providing a flexible environment for AI experimentation.

## 📋 Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🚀 Features

- **Modular Architecture**: Easily switch between different LLMs like DeepSeek and Ollama.
- **Web Interface**: Interact with models through a user-friendly web UI.
- **Logging**: Comprehensive logging for monitoring and debugging.
- **Seed Data**: Preloaded data to facilitate initial testing and development.

## 🛠️ Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Enetact/DojoAI.git
   cd DojoAI
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up configuration**:

   Modify `config.py` to configure model settings and other parameters.

## 💡 Usage

1. **Run the application**:

   ```bash
   python main.py
   ```

2. **Access the web interface**:

   Open your browser and navigate to `http://localhost:8000` to interact with the models.

3. **Switching Models**:

   To switch between DeepSeek and Ollama models, use the provided setup scripts:

   - `setup_ollama_and_integrate.py`
   - `setup_ollama_and_replace_deepseek.py`

   Run the desired script to configure the application with the chosen model.

## 📁 Project Structure

```
DojoAI/
├── ai-git-developer/            # Core AI development modules
├── logs/                        # Log files
├── seed_data/                   # Initial data for testing
├── web_ui/                      # Web interface components
├── config.py                    # Configuration settings
├── import_torch.py              # Torch import utilities
├── setup_ollama_and_integrate.py
├── setup_ollama_and_replace_deepseek.py
└── requirements.txt             # Python dependencies
```

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m 'Add YourFeature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Open a pull request.

For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📬 Contact

For questions or suggestions, please open an issue on the [GitHub repository](https://github.com/Enetact/DojoAI/issues).
