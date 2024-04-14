from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from app.api.validator import check_self_message, phone_validator
from app.core.user import UserManager, current_user, get_user_manager
from app.crud.message import message_crud
from app.models.user import User
from app.schemas.message import MessageCreate, MessageRead

router = APIRouter()


@router.post(
    "/create_message_by_phone",
    response_model=MessageRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user), Depends(get_user_manager)],
    name="Создание сообщения по номеру телефона",
    tags=["messages"],
)
async def create_message_by_phone(
    message: MessageCreate,
    author: User = Depends(current_user),
    user_manager: UserManager = Depends(get_user_manager),
) -> MessageRead:
    """
    Создания сообщения, Поиск пользователя по номеру телефона.
    """
    phone = message.message_to
    phone = await phone_validator(phone)
    message_to = await user_manager.get_by_phone(phone)
    await check_self_message(author, message_to)
    message.message_to = jsonable_encoder(message_to)
    new_message = await message_crud.create_message(message, author)
    return new_message


@router.post(
    "/create_message_by_username",
    response_model=MessageRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user), Depends(get_user_manager)],
    name="Создание сообщения по username",
    tags=["messages"],
)
async def create_message_by_username(
    message: MessageCreate,
    author: User = Depends(current_user),
    user_manager: UserManager = Depends(get_user_manager),
) -> MessageRead:
    """
    Создание сообщения. Поиск пользователя по username.
    """
    username = message.message_to
    message_to = await user_manager.get_by_username(username)
    await check_self_message(author, message_to)
    message.message_to = jsonable_encoder(message_to)
    new_message = await message_crud.create_message(message, author)
    return new_message


@router.get(
    "/get_messages_to_me",
    response_model=list[MessageRead],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
    name="Получает все сообщения, адресованные текущему юзеру.",
    tags=["messages"],
)
async def get_all_message_to_me(user: User = Depends(current_user)) -> list:
    """Получает все сообщения, адресованные текущему юзеру."""

    message = await message_crud.get_all_messages_to_user(user)

    return message


@router.get(
    "/get_messages_from_me",
    response_model=list[MessageRead],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
    name="Получает все сообщения, написанные текущим юзером.",
    tags=["messages"],
)
async def get_all_message_from_me(
    author: User = Depends(current_user),
) -> list:
    """Получает все сообщения, написанные текущим юзером."""

    return await message_crud.get_all_message_from_user(author)


@router.get(
    "/get_messages_between_me_and_user/{user_id}",
    response_model=list[MessageRead],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user), Depends(get_user_manager)],
    name="Получает всю переписку между текущим пользователем и заданным по id.",
    tags=["messages"],
)
async def get_all_message_between_me_and_user(
    me: User = Depends(current_user),
    user_manager: UserManager = Depends(get_user_manager),
    user_id: str = None,
):
    """Получает всю переписку между текущим пользователем и заданным по id."""
    user = await user_manager.get(PydanticObjectId(user_id))
    message = await message_crud.get_all_message_from_user_to_user(me, user)

    return message


@router.get(
    "/{message_id}",
    response_model=MessageRead,
    dependencies=[Depends(current_user)],
    response_model_exclude_none=True,
    name="получает сообщение по id",
    tags=["messages"],
)
async def get_message(
    message_id: str,
    me: User = Depends(current_user),
):
    """
    Получает сообщение по id.
    Если сообщение читает получатель, то оно становится прочитанным.
    """

    message = await message_crud.get_message(ObjectId(message_id))
    if message["message_to"] == jsonable_encoder(me):
        await message_crud.update_message({"read": True}, message_id)
        message = await message_crud.get_message(ObjectId(message_id))
    return message
