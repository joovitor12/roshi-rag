import asyncio
import uuid
import sys

from services.llm_service import LLMService

# Fix for Windows asyncio event loop compatibility with Psycopg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

dash = 30


async def main():
    print("Starting the test chat with POSTGRESQL PERSISTENT MEMORY...")
    print("Type 'exit' or 'quit' to end. Type 'new' to start a new conversation.")
    print("-" * dash)

    # Initialize with PostgreSQL support
    llm_service = LLMService(use_postgres=True)
    conversation_id = None  # Starts without a conversation ID

    try:
        while True:
            try:
                user_message = input("You: ")

                if user_message.lower() in ["exit", "quit"]:
                    print("👋 Ending the chat. See you soon!")
                    break

                if user_message.lower() == "new":
                    conversation_id = None
                    print("\n🔄 Starting a new conversation.\n")
                    continue

                # If it's the first message in a conversation, generate a new ID
                if not conversation_id:
                    conversation_id = str(uuid.uuid4())
                    print(
                        f"(New conversation started with ID: {conversation_id[:8]}...)"
                    )

                print(f"AI (Conv: {conversation_id[:8]}): ", end="", flush=True)

                # Consume the generator from the service, passing the conversation ID
                async for chunk in llm_service.stream_message(
                    user_message, conversation_id
                ):
                    print(chunk, end="", flush=True)

                print("\n")

            except KeyboardInterrupt:
                print("\nEnding the chat. See you soon!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                break
    finally:
        # Close the service properly
        await llm_service.close()


if __name__ == "__main__":
    asyncio.run(main())
