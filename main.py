from app.service import run_agent
from fastapi import FastAPI
from app.api import home, ai_respones

app = FastAPI(title="pc_bulider main endpoint", version="0.0.1")


app.include_router(
    home.router
)


app.include_router(
    ai_respones.router
)
