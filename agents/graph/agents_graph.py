# agents/graph/agents_graph.py
from langgraph.graph import END, START, StateGraph

from agents.chat_agent import chatbot_node
from agents.joke_agent import joke_node
from agents.supervisor_agent import planner_node  # Renomeado para planejador
from agents.synthesizer_agent import synthesizer_node
from models.ai_models import AgentState

graph_builder = StateGraph(AgentState)

graph_builder.add_node("planner", planner_node)
graph_builder.add_node("chat_agent", chatbot_node)
graph_builder.add_node("joke_agent", joke_node)
graph_builder.add_node("synthesizer", synthesizer_node)

graph_builder.add_edge(START, "planner")


# Roteador simples que decide qual worker chamar
def router(state: AgentState):
    # O planner deve colocar a sua decisão em 'tasks'
    if "joke_agent" in state["tasks"]:
        return "joke_agent"
    return "chat_agent"


graph_builder.add_conditional_edges(
    "planner",
    router,
    {
        "chat_agent": "chat_agent",
        "joke_agent": "joke_agent",
    },
)

# Os workers agora apontam para o sintetizador
graph_builder.add_edge("chat_agent", "synthesizer")
graph_builder.add_edge("joke_agent", "synthesizer")

# O sintetizador aponta para o fim
graph_builder.add_edge("synthesizer", END)
