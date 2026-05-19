import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(ROOT_DIR))

from fastapi import FastAPI

from app.schemas.common_schema import MessageResponse

from app.routers.auth_router import router as auth_router

app = FastAPI(
    title="FastAPI JWT Auth",
    version="1.0.0"
)

app.include_router(auth_router)


@app.get(
    "/",
    response_model=MessageResponse
)
def home():

    return {
        "message": "FastAPI JWT Auth Running Successfully"
    }