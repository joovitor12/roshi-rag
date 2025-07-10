from typing import AsyncGenerator

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from agents.graph.agents_graph import graph_builder
from config.llm_config import llm


class LLMService:
    """
    Service for processing user messages using a state graph.
    """

    def __init__(self, use_postgres=False):
        """
        Initialize LLM Service with memory support

        Args:
            use_postgres: If True, uses PostgreSQL for persistent memory.
                         If False, uses in-memory storage (default for testing).
        """
        self.use_postgres = use_postgres
        self.memory = None
        self.graph = None
        self._conn_string = "postgresql://postgres:1234@localhost:5432/roshi_rag_memory"
        self._memory_context = None

        if not use_postgres:
            # Use in-memory storage for testing
            from langgraph.checkpoint.memory import MemorySaver

            self.memory = MemorySaver()
            self.graph = graph_builder.compile(checkpointer=self.memory)

    async def _initialize_memory(self):
        """Initialize PostgreSQL memory if needed"""
        if self.use_postgres and self.memory is None:
            try:
                # Use the context manager correctly for PostgreSQL
                self._memory_context = AsyncPostgresSaver.from_conn_string(
                    self._conn_string
                )
                self.memory = await self._memory_context.__aenter__()

                # Create the necessary tables automatically
                await self.memory.setup()

                self.graph = graph_builder.compile(checkpointer=self.memory)
                print("✅ PostgreSQL memory initialized successfully")
            except Exception as e:
                print(f"❌ Failed to initialize PostgreSQL memory: {e}")
                print("🔄 Falling back to in-memory storage")
                from langgraph.checkpoint.memory import MemorySaver

                self.memory = MemorySaver()
                self.graph = graph_builder.compile(checkpointer=self.memory)
                self.use_postgres = False

    async def close(self):
        """Close the memory context manager if using PostgreSQL"""
        if self._memory_context is not None:
            await self._memory_context.__aexit__(None, None, None)
            self.memory = None
            self.graph = None
            self._memory_context = None

    async def stream_message(
        self, user_message: str, conversation_id: str
    ) -> AsyncGenerator[str, None]:
        # Initialize memory if not already done
        await self._initialize_memory()

        config = {"configurable": {"thread_id": conversation_id}}

        # --- EXPLICIT AND CORRECTED STATE LOGIC ---

        # 1. Actively fetches the most recent conversation state from the database.
        if self.use_postgres:
            thread_state = await self.graph.aget_state(config)
        else:
            thread_state = self.graph.get_state(config)

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

        # --- PROCESSING COMPLETE ---

        final_prompt = final_state.get("results", [])[-1]

        if not final_prompt or not isinstance(final_prompt, str):
            print(
                f"⚠️ [SERVICE] The graph for conversation {conversation_id} did not produce a final prompt."
            )
            return

        print(f"🚀 [SERVICE] Starting streaming for conversation {conversation_id}.")

        async for chunk in llm.astream(final_prompt):
            yield chunk.content
