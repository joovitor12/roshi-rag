"""
Example usage of Llama integration in Roshi-RAG
Demonstrates how to use different Llama models and configurations
"""

import asyncio
from utils.llama_config import (
    set_llama_model,
    get_current_llama,
    show_llama_config,
    list_available_models,
)


async def test_basic_llama():
    """Test basic Llama functionality"""
    print("🦙 TESTING BASIC LLAMA FUNCTIONALITY")
    print("=" * 50)

    # Show current configuration
    print("\n📋 Current configuration:")
    show_llama_config()

    # Test with current model
    print("\n🤖 Testing with current model...")
    try:
        llm = get_current_llama()
        response = await llm.ainvoke("Say 'Hello from Llama!' in English")
        print(f"✅ Response: {response.content}")
    except Exception as e:
        print(f"❌ Error: {e}")


async def test_different_models():
    """Test different Llama models"""
    print("\n" + "=" * 50)
    print("🔄 TESTING DIFFERENT LLAMA MODELS")
    print("=" * 50)

    models_to_test = [("llama3.2", 0.1), ("llama3.1", 0.2), ("codellama", 0.0)]

    for model, temp in models_to_test:
        print(f"\n🦙 Testing model: {model} (temp: {temp})")

        try:
            set_llama_model(model=model, temperature=temp)
            llm = get_current_llama()

            if "code" in model.lower():
                prompt = "Write a simple Python function that adds two numbers"
            else:
                prompt = f"Respond with: 'Working with {model}!'"

            response = await llm.ainvoke(prompt)
            print(f"✅ Response: {response.content[:100]}...")

        except Exception as e:
            print(f"❌ Error with {model}: {e}")


async def test_streaming():
    """Test streaming functionality"""
    print("\n" + "=" * 50)
    print("🌊 TESTING LLAMA STREAMING")
    print("=" * 50)

    llm = get_current_llama()

    print("\n🔄 Streaming response:")
    print("-" * 40)

    try:
        async for chunk in llm.astream(
            "Tell me an interesting fact about llamas in one sentence"
        ):
            print(chunk.content, end="", flush=True)
        print("\n" + "-" * 40)
        print("✅ Streaming completed!")
    except Exception as e:
        print(f"❌ Streaming error: {e}")


def show_configuration_help():
    """Show configuration help"""
    print("\n" + "=" * 50)
    print("⚙️ LLAMA CONFIGURATION GUIDE")
    print("=" * 50)

    print("\n📝 Environment variables:")
    print("   LLAMA_MODEL      = Llama model name")
    print("   LLAMA_TEMPERATURE = Model temperature (0.0-1.0)")
    print("   OLLAMA_BASE_URL  = Ollama server URL")

    print("\n🔧 Programmatic configuration:")
    print("   set_llama_model('llama3.2', temperature=0.1)")
    print("   show_llama_config()")
    print("   get_current_llama()")

    print("\n📦 Available models:")
    list_available_models()


async def main():
    """Main demonstration function"""
    print("🦙 LLAMA INTEGRATION - ROSHI RAG")
    print("Complete demonstration of Llama functionality")

    await test_basic_llama()
    await test_different_models()
    await test_streaming()
    show_configuration_help()

    print("\n" + "=" * 50)
    print("🎉 DEMONSTRATION COMPLETED!")
    print("=" * 50)

    print("\n💡 Next steps:")
    print("   1. Configure your environment variables in .env")
    print("   2. Install dependencies: poetry install --no-root")
    print("   3. Pull Llama models: ollama pull llama3.2")
    print("   4. Run this demo: poetry run python examples/llama_example.py")
    print("   5. Start the API: fastapi dev main.py")

    print("\n📚 Documentation:")
    print("   - README.md: detailed setup instructions")
    print("   - utils/llama_config.py: configuration utilities")
    print("   - test/test_llama.py: automated tests")


if __name__ == "__main__":
    asyncio.run(main())
