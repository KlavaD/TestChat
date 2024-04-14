from typing import Optional

from beanie import PydanticObjectId
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from app.core.db import message_collection
from app.models.message import Message
from app.models.user import User


class CRUDMessage:

    async def get_message(self, message_id: ObjectId) -> dict:
        message = await message_collection.find_one(
            {"_id": message_id})
        if message:
            return message

    async def get_all_messages_to_user(self, user: User) -> list:
        messages = []
        async for message in message_collection.find(
                {"message_to": jsonable_encoder(user)}
        ):
            messages.append(message)
        return messages

    async def get_all_message_from_user(self, user: User) -> list:
        messages = []
        async for message in message_collection.find(
                {"message_from": jsonable_encoder(user)}
        ):
            messages.append(message)
        return messages

    async def get_all_message_from_user_to_user(
            self,
            user1: User,
            user2: User
    ) -> list:
        messages = []
        async for message in message_collection.find(
                {
                    "message_from": jsonable_encoder(user1),
                    "message_to": jsonable_encoder(user2)
                }
        ):
            messages.append(message)
        async for message in message_collection.find(
                {
                    "message_from": jsonable_encoder(user2),
                    "message_to": jsonable_encoder(user1)
                }
        ):
            messages.append(message)
        return messages

    async def create_message(
            self,
            message_data,
            author: Optional[User] = None
    ) -> dict:
        message = message_data.dict()
        if author is not None:
            message['message_from'] = jsonable_encoder(author)
        message = await message_collection.insert_one(message)
        new_message = await message_collection.find_one(
            {"_id": message.inserted_id})
        return new_message

    async def update_message(
            self,
            message_data,
            message_id: str
    ) -> bool:
        update_message = await message_collection.update_one(
            {"_id": PydanticObjectId(message_id)}, {"$set": message_data}
        )
        if update_message:
            return True
        return False


message_crud = CRUDMessage()
