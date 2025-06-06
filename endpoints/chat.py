from fastapi import APIRouter
from services.llm_service import LLMService
from models.ai_models import ChatResponse, UserRequest


router = APIRouter()
llm_service = LLMService()


@router.post("", response_model=ChatResponse)
async def chat(request: UserRequest):
    """
    Endpoint for processing user messages.
    """
    response = await llm_service.process_message(request.message)
    return response
