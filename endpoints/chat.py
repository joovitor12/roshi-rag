from fastapi import APIRouter

from models.ai_models import ChatResponse, UserRequest
from services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()


@router.post("", response_model=ChatResponse)
async def chat(request: UserRequest):
    """
    Endpoint for processing user messages.
    """
    print(f"Request received: '{request.message}")
    response = await llm_service.process_message(request.message)
    return response
