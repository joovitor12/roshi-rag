from langchain_core.messages import HumanMessage

from agents.graph.agents_graph import graph_builder
from models.ai_models import ChatResponse


class LLMService:
    """
    Service for processing user messages using a state graph.
    """

    def __init__(self):
        self.graph = graph_builder.compile()

    async def process_message(self, user_message: str) -> ChatResponse:
        final_state = self.graph.invoke(
            {"messages": [HumanMessage(content=user_message)]}
        )

        assistant_message = final_state["messages"][-1].content
        return ChatResponse(response=assistant_message)
