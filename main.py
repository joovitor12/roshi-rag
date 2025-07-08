import sys
import asyncio
from fastapi import FastAPI
import endpoints.chat as chat
from agents.graph.agents_graph import graph_builder

# Fix for Windows asyncio event loop compatibility with Psycopg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(
    title="LangGraph Chatbot",
    description="A simple chatbot using LangGraph and FastAPI.",
    version="1.0.0",
)

graph = graph_builder.compile()

app.include_router(chat.router, prefix="/chat", tags=["chat"])
