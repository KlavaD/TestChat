from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import Field, BaseModel

from app.models.user import User


class MessageRead(BaseModel):
    id: PydanticObjectId = Field(alias="_id", default=None)
    text: str
    message_to: User
    message_from: User
    created: Optional[datetime]
    read: Optional[bool] = Field(False)


class MessageCreate(BaseModel):
    message_to: str = Field(...)
    text: str = Field(..., example='Тестовое сообщение')
    created: Optional[datetime] = Field(default_factory=datetime.utcnow)
