from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import Field, BaseModel

from app.core.user import current_user
from app.models.user import User


class Message(BaseModel):
    text: str
    message_to: User
    message_from: User = Field(current_user)
    created: Optional[datetime] = Field(datetime.now())
    read: Optional[bool] = Field(False)
