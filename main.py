from app.service import run_agent
from fastapi import FastAPI
from app.api import home, ai_respones
import os
from dotenv import load_dotenv

# Load variables into os.environ before importing LangChain/LangGraph
load_dotenv()

# MUST be executed before any LangChain/LangGraph modules are evaluated

app = FastAPI(title="pc_bulider main endpoint", version="0.0.1")


app.include_router(
    home.router
)


app.include_router(
    router=ai_respones.router,
)

"""
async def test_run_agent():
    user_input = "I want to build a gaming PC with a budget of $1500. Can you suggest the best components for it?"
    async for chunk in run_agent(user_inputs=user_input):
        return chunk

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_run_agent())
"""
