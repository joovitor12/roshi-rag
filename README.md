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
3.  **Setup your LLM in `config/llm_config.py`:** This project is currently using an Ollama model. You would need to have the `llama3.2` model and the Ollama CLI (available at [https://ollama.com](https://ollama.com)) installed.
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
