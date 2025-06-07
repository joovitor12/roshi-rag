# agents/synthesizer_agent.py
from langchain_core.messages import AIMessage, BaseMessage

from models.ai_models import AgentState


def synthesizer_node(state: AgentState):
    """
    Node that synthetize all results of the workers into a final response.
    """
    print(f"Entered synthesizer agent with state: {state}")
    final_response_parts = [
        item.content if isinstance(item, BaseMessage) else str(item)
        for item in state["results"]
    ]

    final_response = "\n".join(final_response_parts)

    return {"messages": [AIMessage(content=final_response)]}
