from app.utils import AiErrorHandeler
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.service import run_agent
import json
from loguru import logger

router = APIRouter(prefix="/v1")


@router.post("/ai_respones")
async def main(inputs):
    async def event_stream_respones(inputs=inputs):
        try:
            async for chunk in run_agent(user_inputs=inputs):
                if isinstance(chunk, dict) and "model" in chunk:
                    messages = chunk["model"].get("messages", [])
                    if messages:
                        last_msg = messages[-1]
                        if hasattr(last_msg, "content") and last_msg.content:
                            payload = {"text": last_msg.content}
                            yield f"data: {json.dumps(payload)}\n\n"
        except AiErrorHandeler as error:
            logger.warning(str(error))
            raise RuntimeError(error)
    return StreamingResponse(
        content=event_stream_respones(),
        media_type="text/event-stream",
        status_code=200
    )
