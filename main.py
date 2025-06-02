from fastapi import FastAPI
import endpoints.chat as chat
from agents.graph.agents_graph import graph_builder

app = FastAPI(
    title="LangGraph Chatbot",
    description="A simple chatbot using LangGraph and FastAPI.",
    version="1.0.0",
)

graph = graph_builder.compile()

app.include_router(chat.router, prefix="/chat", tags=["chat"])
