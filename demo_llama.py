"""
Demonstration of Llama integration in Roshi-RAG
Shows how to use different Llama models and configurations
"""

import asyncio
from utils.llama_config import (
    set_llama_model,
    get_current_llama,
    show_llama_config,
    list_available_models,
)


async def demo_basic_usage():
    """Basic usage demonstration"""
    print("🦙 LLAMA INTEGRATION - ROSHI RAG")
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


async def demo_model_switching():
    """Model switching demonstration"""
    print("\n" + "=" * 50)
    print("🔄 TESTING DIFFERENT LLAMA MODELS")
    print("=" * 50)

    models_to_test = ["llama3.2", "llama3.1", "codellama"]

    for model in models_to_test:
        print(f"\n🦙 Testing model: {model}")

        try:
            set_llama_model(model=model, temperature=0.1)
            llm = get_current_llama()

            if "code" in model.lower():
                prompt = "Write a simple Python function that adds two numbers"
            else:
                prompt = f"Respond with: 'Working with {model}!'"

            response = await llm.ainvoke(prompt)
            print(f"✅ Response: {response.content[:100]}...")

        except Exception as e:
            print(f"❌ Error with {model}: {e}")


async def demo_streaming():
    """Streaming demonstration"""
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


def show_help():
    """Show configuration help"""
    print("\n" + "=" * 50)
    print("⚙️ LLAMA CONFIGURATION GUIDE")
    print("=" * 50)

    print("\n📝 Environment variables (.env file):")
    print("   LLAMA_MODEL      = llama3.2")
    print("   LLAMA_TEMPERATURE = 0.1")
    print("   OLLAMA_BASE_URL  = http://localhost:11434")

    print("\n🔧 Programmatic configuration:")
    print("   set_llama_model('llama3.2', temperature=0.1)")
    print("   show_llama_config()")
    print("   get_current_llama()")

    print("\n📦 Available models:")
    list_available_models()


async def main():
    """Main demonstration function"""
    await demo_basic_usage()
    await demo_model_switching()
    await demo_streaming()
    show_help()

    print("\n" + "=" * 50)
    print("🎉 DEMONSTRATION COMPLETED!")
    print("=" * 50)

    print("\n💡 Next steps:")
    print("   1. Configure .env file with your preferred model")
    print("   2. Install dependencies: poetry install --no-root")
    print("   3. Pull Llama models: ollama pull llama3.2")
    print("   4. Run this demo: poetry run python demo_llama.py")
    print("   5. Start the API: fastapi dev main.py")


if __name__ == "__main__":
    asyncio.run(main())
