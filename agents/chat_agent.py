from langchain_core.messages import SystemMessage

from config.llm_config import llm
from models.ai_models import AgentState


def chatbot_node(state: AgentState):
    """
    Chat agent node, now with a prompt that instructs it to use memory.
    """
    print("[WORKER] Chat Agent (with memory) activated.")

    # We add a system instruction at the beginning of the conversation
    # to guide the LLM's behavior in all turns.
    messages_with_system_prompt = [
        SystemMessage(
            content="""You are a helpful conversational assistant.
        Answer the user's last question based on the conversation history.
        If you don't know the answer, say you don't know. Do not make up information.
        Use the history to remember details about the user, such as name or other information they provide."""
        )
    ]
    messages_with_system_prompt.extend(state["messages"])

    response_message = llm.invoke(messages_with_system_prompt)

    # Returns the response content to the results list
    return {"results": [response_message.content]}
