# roshi-rag
RAG agent for Roshi-AI (In progress)

Setup environment:

1. Have Python installed (3.13 preferrably)
2. Run `pip install -r requirements.txt`
3. Setup your LLM in `config/llm_config.py`, this project is currently using an Ollama model, which you would need to have the `llama3.2` model and the (CLI)[https://ollama.com] installed.
4. Run the project with `fastapi dev main.py` or with uvicorn `uvicorn main:app --reload`