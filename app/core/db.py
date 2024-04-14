from contextlib import asynccontextmanager

import motor.motor_asyncio
from beanie import init_beanie
from fastapi import FastAPI

from app.core.config import settings
from app.models.user import User

client = motor.motor_asyncio.AsyncIOMotorClient(settings.database_url)

database = client.test_chat


message_collection = database.get_collection("messages_collection")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(
        database=database,
        document_models=[
            User,
        ],
    )
    yield
