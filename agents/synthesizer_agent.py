# agents/synthesizer_agent.py
from langchain_core.messages import BaseMessage

from models.ai_models import AgentState


def synthesizer_node(state: AgentState):
    """
    Node that synthesizes the results from the workers into a SINGLE final prompt.
    It NO LONGER calls the LLM.
    """
    print("[AGENT] Entering the synthesizer...")
    print(f"[AGENT] Results received from workers: {state['results']}")

    final_response_parts = [
        item.content if isinstance(item, BaseMessage) else str(item)
        for item in state["results"]
    ]

    context_for_synthesis = "\n".join(final_response_parts)

    # Builds the final prompt that will be used for streaming
    synthesis_prompt = f"""

    You are a helpful assistant. Combine the following information into a cohesive and useful response for the user.

    Information to combine:
    ---
    {context_for_synthesis}
    ---
    Your final answer:
    """
    print("✨ [AGENT] Final prompt generated for streaming.")

    # Overwrites 'results' with a single item: the final prompt.
    # We will use this in our service.
    return {"results": [synthesis_prompt]}
