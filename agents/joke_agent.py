# agents/joke_agent.py
from config.llm_config import llm
from models.ai_models import AgentState


async def joke_node(state: AgentState):
    """
    Agent node that generates a joke.
    """
    print("[AGENT] Joke Agent activated")

    user_message = state["messages"][-1].content

    prompt = f"Please tell a short and funny joke. If the user mentioned a topic '{user_message}', try to make a joke about it."

    response_message = await llm.ainvoke(prompt)

    return {"results": [response_message.content]}
