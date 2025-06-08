from typing import AsyncGenerator

from langchain_core.messages import HumanMessage

from agents.graph.agents_graph import graph_builder
from config.llm_config import llm


class LLMService:
    """
    Service for processing user messages using a state graph.
    """

    def __init__(self):
        self.graph = graph_builder.compile()

    async def stream_message(self, user_message: str) -> AsyncGenerator[str, None]:
        """
        Now in two steps:
        1. Invokes the graph to obtain the final prompt.
        2. Streams the LLM response using this prompt.
        """
        # Step 1: Execute the graph to obtain the final state
        # We use `ainvoke` to run the graph asynchronously
        final_state = await self.graph.ainvoke(
            {"messages": [HumanMessage(content=user_message)], "results": []}
        )

        # Extracts the final prompt prepared by the synthesizer
        final_prompt = final_state.get("results", [])[-1]

        if not final_prompt or not isinstance(final_prompt, str):
            print("[SERVICE] The graph did not produce a final prompt for streaming.")
            return

        print("[SERVICE] Starting streaming to the client with the final prompt.")

        # Step 2: Stream with the final prompt
        async for chunk in llm.astream(final_prompt):
            yield chunk.content
