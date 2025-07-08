"""
Utility for Llama model configuration and management
"""

import os
from config.llm_config import LlamaConfig


class LlamaManager:
    """Utility for managing Llama model configuration"""

    @staticmethod
    def set_model(model: str, temperature: float = None, base_url: str = None):
        """
        Set Llama model configuration

        Args:
            model: Llama model name (e.g., 'llama3.2', 'llama3.1')
            temperature: Model temperature (0.0 to 1.0)
            base_url: Ollama base URL
        """
        os.environ["LLAMA_MODEL"] = model

        if temperature is not None:
            os.environ["LLAMA_TEMPERATURE"] = str(temperature)

        if base_url is not None:
            os.environ["OLLAMA_BASE_URL"] = base_url

        print(f"✅ Set Llama model: {model}")
        if temperature is not None:
            print(f"🌡️ Temperature: {temperature}")
        if base_url is not None:
            print(f"🔗 Base URL: {base_url}")

    @staticmethod
    def get_current_config():
        """Returns current Llama configuration"""
        return {
            "model": os.getenv("LLAMA_MODEL", "llama3.2"),
            "temperature": float(os.getenv("LLAMA_TEMPERATURE", "0.1")),
            "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        }

    @staticmethod
    def get_llm():
        """Returns new Llama LLM instance with current configuration"""
        config = LlamaConfig()
        return config.get_llm()


# Convenience functions
def set_llama_model(
    model: str = "llama3.2", temperature: float = 0.1, base_url: str = None
):
    """Set Llama model configuration"""
    LlamaManager.set_model(model, temperature, base_url)


def get_current_llama():
    """Returns current Llama LLM instance"""
    return LlamaManager.get_llm()


def show_llama_config():
    """Shows current Llama configuration"""
    config = LlamaManager.get_current_config()
    print("🦙 Current Llama Configuration:")
    print(f"   Model: {config['model']}")
    print(f"   Temperature: {config['temperature']}")
    print(f"   Base URL: {config['base_url']}")


def list_available_models():
    """Lists commonly available Llama models"""
    models = [
        "llama3.2",
        "llama3.1",
        "llama3.1:8b",
        "llama3.1:70b",
        "llama3.2:1b",
        "llama3.2:3b",
        "codellama",
        "codellama:7b",
        "codellama:13b",
    ]

    print("🦙 Available Llama Models:")
    for model in models:
        print(f"   - {model}")

    print("\n💡 To pull a model: ollama pull <model_name>")
    print("💡 To list installed models: ollama list")
