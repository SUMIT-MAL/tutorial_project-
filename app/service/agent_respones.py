from app.src import AiAgentManger
from loguru import logger
from app.utils import AiErrorHandeler
from fastapi.exceptions import HTTPException
service = AiAgentManger()


async def run_agent(user_inputs: str):
    try:
        async for chunks in service.run_agent(
            user_input=user_inputs
        ):
            logger.info("agent is running")
            yield chunks
    except AiErrorHandeler as error:
        raise HTTPException(status_code=403, detail=error)
