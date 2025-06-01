from langchain_ollama.chat_models import ChatOllama

try:
    llm = ChatOllama(model="llama3.2", temperature=0.1)
    print(f"Loaded model: {llm.model}")
except Exception as e:
    print(f"Error loading model: {e}")
    raise RuntimeError(f"Failed to load the LLM model. Please check your configuration Ollama and the model name. Original error: {e}")