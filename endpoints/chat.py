import json
import uuid

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from models.ai_models import UserRequest
from services.llm_service import LLMService

router = APIRouter()
# Use PostgreSQL for persistent memory in production
llm_service = LLMService(use_postgres=True)


@router.post("")
async def chat(request: UserRequest):
    """
    Chat endpoint that now supports response streaming.
    """

    async def stream_generator():
        conversation_id = request.conversation_id or str(uuid.uuid4())

        id_payload = {"conversation_id": conversation_id}
        yield f"event: metadata\ndata: {json.dumps(id_payload)}\n\n"

        async for chunk in llm_service.stream_message(request.message, conversation_id):
            if chunk:
                response_chunk = {"response": chunk}
                yield f"data: {json.dumps(response_chunk)}\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")
