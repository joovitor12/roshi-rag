import json

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from models.ai_models import UserRequest
from services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()


@router.post("")
async def chat(request: UserRequest):
    """
    Chat endpoint that now supports response streaming.
    """

    async def stream_generator():
        """Internal generator that consumes from the service and formats for SSE."""
        async for chunk in llm_service.stream_message(request.message):
            if chunk:
                # Server-Sent Event (SSE) format
                # The client will receive each chunk as a "message" event
                response_chunk = {"response": chunk}
                yield f"data: {json.dumps(response_chunk)}\n\n"

    # Returns a StreamingResponse that consumes from our generator
    return StreamingResponse(stream_generator(), media_type="text/event-stream")
