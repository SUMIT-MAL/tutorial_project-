from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.service import run_agent

router = APIRouter(prefix="/respones/v1")


@router.post("/ai_respones")
async def main(inputs):
    async for chunk in run_agent(user_inputs=inputs):
        return StreamingResponse(
            content=chunk,
            media_type="text/event-stream"
        )
