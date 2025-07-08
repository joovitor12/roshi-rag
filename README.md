# roshi-rag
RAG agent for Roshi-AI (In progress)

## Setup environment:

1.  **Have Python installed (3.13 preferrably)**
2.  **Install project dependencies:**
    ```bash
    pip install poetry
    poetry install --no-root
    ```
    This file includes all necessary libraries for the project, including `ruff` for linting/formatting and `pre-commit`.
3.  **Configure Llama Models:** This project uses Llama models via Ollama. Configure your preferred model in the `.env` file:

    ```bash
    LLAMA_MODEL=llama3.2
    LLAMA_TEMPERATURE=0.1
    OLLAMA_BASE_URL=http://localhost:11434
    ```

    You'll need to have the Ollama CLI installed ([https://ollama.com](https://ollama.com)) and the model downloaded:
    ```bash
    ollama pull llama3.2
    ```

4.  **Configure Pre-commit Hooks:**
    To ensure code quality and consistency, this project uses pre-commit hooks. After installing the dependencies (which includes `pre-commit`), run the following command once in your local repository to activate the hooks:
    ```bash
    pre-commit install
    ```
    This will run linters (like `Ruff`) and formatters automatically before each commit. If a hook modifies a file, you'll need to `git add` the changes and attempt the commit again.
5.  **Run the project:**
    ```bash
    fastapi dev main.py
    ```
    or with uvicorn:
    ```bash
    poetry run uvicorn main:app --reload
    ```


## For nerds / who's interested in the project's approach

Hi, i recommend testing the application core by using the test file for streaming, by using the command below:

```
poetry run python -m test.test_llm_stream
```

In the future this file will be removed, bc i want to create a front-end application that will integrate with this chatbot, but have fun with this for now.

## Llama Model Configuration

This project uses Llama models via Ollama for local AI inference.

### Using the Llama Configuration Utility

You can programmatically configure Llama models using the utility functions:

```python
from utils.llama_config import set_llama_model, get_current_llama, show_llama_config

# Set Llama model
set_llama_model(model="llama3.2", temperature=0.1)

# Get current LLM instance
llm = get_current_llama()

# Show current configuration
show_llama_config()
```

### Environment Variables

Configure your Llama model in the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `LLAMA_MODEL` | Llama model name | `llama3.2` |
| `LLAMA_TEMPERATURE` | Model temperature (0.0 to 1.0) | `0.1` |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |

### Testing Llama Models

Run the example script to test different Llama models:

```bash
poetry run python examples/llama_example.py
```

### Available Llama Models

**Popular Llama Models:**
- `llama3.2` (default, latest)
- `llama3.1`
- `llama3.1:8b`
- `llama3.1:70b`
- `llama3.2:1b` (lightweight)
- `llama3.2:3b`
- `codellama` (code-focused)
- `codellama:7b`
- `codellama:13b`

### Model Management

```bash
# Pull a specific model
ollama pull llama3.2

# List installed models
ollama list

# Remove a model
ollama rm llama3.1
```

## VS Code Configuration (Recommended)

For an optimal development experience with consistent formatting and linting in VS Code:

1.  **Install Recommended Extensions:**
    * Open the project in VS Code.
    * Go to the Extensions view (`Ctrl+Shift+X`).
    * VS Code should suggest workspace-recommended extensions based on the `.vscode/extensions.json` file in this repository. Please install them, especially:
        * `ms-python.python` (Python by Microsoft)
        * `charliermarsh.ruff` (Ruff by Astral Software/charliermarsh)

2.  **Enable Workspace Settings:**
    * This project includes recommended VS Code settings in `.vscode/settings.json` to automatically format your code with `Ruff` on save and enable other helpful Python features.
    * If prompted by VS Code, "trust" the workspace to apply these settings.

This setup will help ensure your code is automatically formatted and linted by `Ruff` as you save files and before you commit.

## Roadmap

![image](https://github.com/user-attachments/assets/ec3b1967-9faf-4804-8ece-7a3f5950681d)

**Note**: I'll detail more the Milestones in the project issues, I'll won't vomit a lot of text here.
