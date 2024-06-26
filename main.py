import uvicorn
from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.db import lifespan

app = FastAPI(
    lifespan=lifespan,
    title=settings.app_title,
    description=settings.app_description,
)

app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", log_level="info")
