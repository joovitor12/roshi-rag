from config.llm_config import llm
from models.ai_models import AgentState


def chatbot_node(state: AgentState):
    """
    Node function for processing chat messages using the LLM.
    """
    print("Worker -> Agent Chat activated")
    # The LLM is invoked with the message history.
    # state["messages"] will come as a list of BaseMessage (e.g., HumanMessage, AIMessage).
    response_message = llm.invoke(state["messages"])

    # The node returns a dictionary that updates the state.
    # 'add_messages' will ensure that this new message is appended to the existing list.
    return {"results": [response_message.content]}
