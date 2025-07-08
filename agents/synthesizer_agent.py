from langchain_core.messages import AIMessage, HumanMessage

from models.ai_models import AgentState


async def synthesizer_node(state: AgentState):
    """
    Node that creates a high-quality final prompt for the LLM,
    using the conversation history and the worker's suggestion.
    """
    print("🤝 [AGENT] Synthesizer agent activated with context...")

    # Format the conversation history to include in the prompt
    history_str = ""
    for msg in state["messages"]:
        if isinstance(msg, HumanMessage):
            history_str += f"User: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            history_str += f"Assistant: {msg.content}\n"

    # Get the raw response from the worker
    worker_output = "\n".join(state.get("results", []))

    # Create the final, detailed prompt
    final_prompt = f"""You are a conversational AI assistant named Roshi. Your tone is helpful and friendly.
Your task is to formulate the final response for the user.

Analyze the conversation history and the response suggestion from your internal agent to give a final, polished answer that maintains context.

### CONVERSATION HISTORY:
{history_str}
### INTERNAL AGENT RESPONSE SUGGESTION:
{worker_output}

### YOUR FINAL RESPONSE (reply directly to the user):
"""

    print("✨ [AGENT] Final contextualized prompt generated.")

    # Put the final prompt back in the 'results' field for the LLMService to use.
    return {"results": [final_prompt]}
