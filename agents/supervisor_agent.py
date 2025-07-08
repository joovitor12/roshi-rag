# agents/supervisor_agent.py
from typing import List

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from config.llm_config import llm
from models.ai_models import AgentState


class Plan(BaseModel):
    """Plan of tasks to be executed by the agents."""

    tasks: List[str] = Field(
        description="A list of tasks that need to be executed. It can be 'chat_agent', 'joke_agent', or both."
    )


def create_planner_node():
    """
    Creates the planner node that uses the LLM to define a task plan.
    """
    structured_llm = llm.with_structured_output(Plan)

    system_prompt = """You are a planner responsible for identifying all necessary tasks from a user's query.
    - If the user asks a general question or starts a conversation, add 'chat_agent' to the task list.
    - If the user asks for a joke or something funny, add 'joke_agent' to the task list.
    - Respond with a list of all applicable tasks.
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            (
                "human",
                "Analyze the following user message and generate the task plan: {message}",
            ),
        ]
    )
    planner = prompt | structured_llm

    async def planner_node(state: AgentState):
        print(f"[SUPERVISOR] Planner agent entered with state: {state}")
        last_message = state["messages"][-1].content
        plan = await planner.ainvoke({"message": last_message})
        print(f"[SUPERVISOR] Generated plan: {plan.tasks}")
        return {"tasks": plan.tasks}

    return planner_node


# Renamed to reflect the new function
planner_node = create_planner_node()
