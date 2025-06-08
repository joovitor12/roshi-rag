# agents/graph/agents_graph.py
from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph

from agents.chat_agent import chatbot_node
from agents.joke_agent import joke_node
from agents.supervisor_agent import planner_node
from agents.synthesizer_agent import synthesizer_node
from models.ai_models import AgentState

graph_builder = StateGraph(AgentState)

graph_builder.add_edge(START, "planner")
graph_builder.add_node("planner", planner_node)
graph_builder.add_node("chat_agent", chatbot_node)
graph_builder.add_node("joke_agent", joke_node)
graph_builder.add_node("synthesizer", synthesizer_node)


def dispatcher(state: AgentState):
    """
    Reads the list of tasks and uses the `Send` API to dispatch each one
    to the corresponding node. This happens in parallel.
    """
    tasks = state["tasks"]
    print(f"Graph -> Dispatching tasks: {tasks}")
    return [Send(task, state) for task in state["tasks"]]


graph_builder.add_conditional_edges("planner", dispatcher)

graph_builder.add_edge("chat_agent", "synthesizer")
graph_builder.add_edge("joke_agent", "synthesizer")

graph_builder.add_edge("synthesizer", END)
