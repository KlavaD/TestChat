from typing import Optional

from beanie import Document
from fastapi_users_db_beanie import BeanieUserDatabase, BeanieBaseUser
from pydantic import HttpUrl, Field


class User(BeanieBaseUser, Document):
    username: Optional[str] = Field(None)
    avatar: Optional[HttpUrl] = Field(None)
    phone_number: Optional[str] = Field(None)
    bio: Optional[str] = Field(None)


async def get_user_db():
    yield BeanieUserDatabase(User)
