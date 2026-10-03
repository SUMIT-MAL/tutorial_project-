from fastapi import APIRouter
from fastapi.responses import HTMLResponse, StreamingResponse

router = APIRouter(prefix="/Home/v1")


@router.post("/home_page")
def home_page():
    return HTMLResponse(
        content="this is a home route",
        status_code={200, "ok"}
    )
