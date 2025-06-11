from typing import AsyncGenerator

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from agents.graph.agents_graph import graph_builder
from config.llm_config import llm


class LLMService:
    """
    Service for processing user messages using a state graph.
    """

    def __init__(self):
        conn_string = (
            "postgresql+asyncpg://postgres:1234@localhost:5432/roshi_rag_memory"
        )
        self.memory = AsyncPostgresSaver.from_conn_string(conn_string)
        self.graph = graph_builder.compile(checkpointer=self.memory)

    async def stream_message(
        self, user_message: str, conversation_id: str
    ) -> AsyncGenerator[str, None]:
        config = {"configurable": {"thread_id": conversation_id}}

        # --- EXPLICIT AND CORRECTED STATE LOGIC ---

        # 1. Actively fetches the most recent conversation state from the database.
        thread_state = await self.graph.get_state(config)

        # 2. Extracts the message history. If it's a new conversation, starts with an empty list.
        messages_history = (
            thread_state.values.get("messages", [])
            if thread_state and thread_state.values
            else []
        )

        # 3. Adds the new user message to the history we just loaded.
        messages_history.append(HumanMessage(content=user_message))

        # 4. Invokes the graph, passing the COMPLETE and updated history.
        # The graph now always receives the entire conversation.
        # The checkpointer will save this new complete state at the end.
        final_state = await self.graph.ainvoke(
            {"messages": messages_history, "results": []}, config=config
        )

        # --- THE REST OF THE FUNCTION REMAINS THE SAME ---

        final_prompt = final_state.get("results", [])[-1]

        if not final_prompt or not isinstance(final_prompt, str):
            print(
                f"⚠️ [SERVICE] The graph for conversation {conversation_id} did not produce a final prompt."
            )
            return

        print(f"🚀 [SERVICE] Starting streaming for conversation {conversation_id}.")

        async for chunk in llm.astream(final_prompt, config=config):
            yield chunk.content
