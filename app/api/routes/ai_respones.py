from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.service import run_agent
import json
router = APIRouter(prefix="/v1")


@router.post("/ai_respones")
async def main(inputs):
    async def event_stream_respones(inputs=inputs):
        async for chunk in run_agent(user_inputs=inputs):
            if isinstance(chunk, dict) and "model" in chunk:
                messages = chunk["model"].get("messages", [])
                if messages:
                    last_msg = messages[-1]
                    if hasattr(last_msg, "content") and last_msg.content:
                        yield last_msg.content
    return StreamingResponse(
        content=event_stream_respones(),
        media_type="text/event-stream",
        status_code=200
    )
