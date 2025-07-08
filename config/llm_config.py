import os
from langchain_ollama.chat_models import ChatOllama
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LlamaConfig:
    """Configuration for Llama models via Ollama"""

    def __init__(self):
        self.model_name = os.getenv("LLAMA_MODEL", "llama3.2")
        self.temperature = float(os.getenv("LLAMA_TEMPERATURE", "0.1"))
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    def get_llm(self) -> ChatOllama:
        """Returns configured Llama model instance"""
        try:
            llm = ChatOllama(
                model=self.model_name,
                temperature=self.temperature,
                base_url=self.base_url,
            )
            print(f"✅ Loaded Llama model: {self.model_name}")
            return llm
        except Exception as e:
            print(f"❌ Error loading Llama model: {e}")
            raise RuntimeError(
                f"Failed to load Llama model '{self.model_name}'. "
                f"Please ensure Ollama is running and the model is available. "
                f"Original error: {e}"
            )


# Global configuration instance
config = LlamaConfig()
llm = config.get_llm()
