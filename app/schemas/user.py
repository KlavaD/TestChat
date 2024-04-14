from typing import Optional

from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import Field, HttpUrl


class UserRead(schemas.BaseUser[PydanticObjectId]):
    username: Optional[str] = Field(None)
    avatar: Optional[HttpUrl] = Field(None)
    phone_number: Optional[str] = Field(None)
    bio: Optional[str] = Field(None)


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = Field(None)
    avatar: Optional[HttpUrl] = Field(None)
    phone_number: Optional[str] = Field(None)
    bio: Optional[str] = Field(None)
