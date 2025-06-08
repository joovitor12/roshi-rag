# test_llm_stream.py

import asyncio

from services.llm_service import LLMService

dash = 30


async def main():
    """
    Main function to run an interactive test chat in the terminal
    that demonstrates streaming functionality.
    """
    print("Starting the test chat with the LLM Service...")
    print("Type 'exit' or 'quit' to end.")
    print("-" * dash)

    # Instantiate our service, which in turn compiles the graph.
    llm_service = LLMService()

    while True:
        try:
            # Ask for user input.
            user_message = input("You: ")

            if user_message.lower() in ["exit", "quit"]:
                print("Ending the chat. See you soon!")
                break

            print("AI: ", end="", flush=True)

            # Consume the asynchronous generator from the streaming service.
            async for chunk in llm_service.stream_message(user_message):
                # Print each piece of the response immediately.
                # end="" prevents print from adding a newline for each chunk.
                # flush=True forces immediate printing to the terminal.
                print(chunk, end="", flush=True)

            # Add a newline at the end of the complete AI response.
            print("\n")

        except KeyboardInterrupt:
            print("\nEnding the chat. See you soon!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            break


if __name__ == "__main__":
    # Run the async main function.
    asyncio.run(main())
