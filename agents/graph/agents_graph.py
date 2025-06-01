from langgraph.graph import StateGraph, START
from agents.chat_agent import chatbot_node
from models.ai_models import State

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.set_finish_point("chatbot")