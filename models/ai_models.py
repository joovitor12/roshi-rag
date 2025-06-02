from pydantic import BaseModel
from typing import Annotated, List
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]


class UserRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
