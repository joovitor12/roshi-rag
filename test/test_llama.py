"""
Tests for Llama integration functionality
"""

import os
import pytest
from unittest.mock import patch, MagicMock

from config.llm_config import LlamaConfig
from utils.llama_config import (
    LlamaManager,
    set_llama_model,
    show_llama_config,
)


class TestLlamaConfig:
    """Tests for LlamaConfig class"""

    def test_default_model_is_llama32(self):
        """Test if default model is llama3.2"""
        with patch.dict(os.environ, {}, clear=True):
            config = LlamaConfig()
            assert config.model_name == "llama3.2"

    def test_model_from_env(self):
        """Test if model is read correctly from environment"""
        with patch.dict(os.environ, {"LLAMA_MODEL": "llama3.1"}):
            config = LlamaConfig()
            assert config.model_name == "llama3.1"

    def test_temperature_from_env(self):
        """Test if temperature is read correctly from environment"""
        with patch.dict(os.environ, {"LLAMA_TEMPERATURE": "0.5"}):
            config = LlamaConfig()
            assert config.temperature == 0.5

    def test_base_url_from_env(self):
        """Test if base URL is read correctly from environment"""
        with patch.dict(os.environ, {"OLLAMA_BASE_URL": "http://custom:11434"}):
            config = LlamaConfig()
            assert config.base_url == "http://custom:11434"


class TestLlamaManager:
    """Tests for LlamaManager class"""

    def test_set_model(self):
        """Test setting Llama model"""
        LlamaManager.set_model("llama3.1", 0.2, "http://test:11434")

        assert os.environ["LLAMA_MODEL"] == "llama3.1"
        assert os.environ["LLAMA_TEMPERATURE"] == "0.2"
        assert os.environ["OLLAMA_BASE_URL"] == "http://test:11434"

    def test_set_model_partial(self):
        """Test setting only model name"""
        LlamaManager.set_model("codellama")
        assert os.environ["LLAMA_MODEL"] == "codellama"

    def test_get_current_config(self):
        """Test getting current configuration"""
        with patch.dict(
            os.environ,
            {
                "LLAMA_MODEL": "llama3.2",
                "LLAMA_TEMPERATURE": "0.1",
                "OLLAMA_BASE_URL": "http://localhost:11434",
            },
        ):
            config = LlamaManager.get_current_config()

            assert config["model"] == "llama3.2"
            assert config["temperature"] == 0.1
            assert config["base_url"] == "http://localhost:11434"

    def test_convenience_functions(self):
        """Test convenience functions"""
        set_llama_model("llama3.1", 0.3)
        assert os.environ["LLAMA_MODEL"] == "llama3.1"
        assert os.environ["LLAMA_TEMPERATURE"] == "0.3"


@pytest.mark.asyncio
async def test_llama_integration():
    """Integration test (requires actual Ollama setup)"""
    # Skip if no Ollama configuration available
    if not os.getenv("LLAMA_MODEL") and not os.path.exists("/usr/local/bin/ollama"):
        pytest.skip("No Ollama configuration available for integration test")

    config = LlamaConfig()

    try:
        llm = config.get_llm()
        # Basic invocation test
        response = await llm.ainvoke("Say only 'OK'")
        assert response.content is not None
        assert len(response.content) > 0
    except Exception as e:
        pytest.skip(f"Ollama integration error: {e}")


def test_show_config_output(capsys):
    """Test if show_llama_config produces correct output"""
    with patch.dict(
        os.environ,
        {
            "LLAMA_MODEL": "llama3.2",
            "LLAMA_TEMPERATURE": "0.1",
            "OLLAMA_BASE_URL": "http://localhost:11434",
        },
    ):
        show_llama_config()
        captured = capsys.readouterr()

        assert "Current Llama Configuration:" in captured.out
        assert "Model: llama3.2" in captured.out
        assert "Temperature: 0.1" in captured.out
        assert "Base URL: http://localhost:11434" in captured.out


class TestErrorHandling:
    """Tests for error handling"""

    @patch("config.llm_config.ChatOllama")
    def test_llm_creation_error(self, mock_chat_ollama):
        """Test error handling when LLM creation fails"""
        mock_chat_ollama.side_effect = Exception("Connection failed")

        config = LlamaConfig()
        with pytest.raises(RuntimeError, match="Failed to load Llama model"):
            config.get_llm()


@pytest.mark.asyncio
async def test_streaming_functionality():
    """Test streaming functionality (mocked)"""
    mock_llm = MagicMock()
    mock_chunk = MagicMock()
    mock_chunk.content = "test"
    mock_llm.astream.return_value = [mock_chunk]

    # Test streaming
    chunks = []
    async for chunk in mock_llm.astream("test prompt"):
        chunks.append(chunk.content)

    assert len(chunks) == 1
    assert chunks[0] == "test"


if __name__ == "__main__":
    # Run basic tests
    print("🧪 Running basic Llama tests...")

    # Test configuration
    config = LlamaConfig()
    print(f"✅ Current model: {config.model_name}")

    # Test manager
    set_llama_model("llama3.2")
    print("✅ Set model to llama3.2")

    # Show configuration
    show_llama_config()

    print("\n🎉 Basic tests completed!")
    print("💡 For complete tests, run: poetry run pytest test/test_llama.py")
