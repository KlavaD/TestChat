import re

from fastapi import HTTPException
from fastapi_users.exceptions import UserNotExists

from app.models.user import User


async def check_self_message(
        author: User,
        user: User
) -> None:
    """
    Проверка отправки сообщения самому себе
    :param author:
    :param user:
    :return:
    """
    if user.id == author.id:
        raise HTTPException(
            status_code=400,
            detail='Нельзя отправлять сообщение самому себе!'
        )


async def phone_validator(phone_number: str) -> str:
    """
    Приведение номера телефона к +7.
    """
    if re.match(r"^8", phone_number):
        phone_number = re.sub(r"^8", "+7", phone_number)

    return phone_number


async def validation_phone(
        self,
        phone_number: str,
) -> None:
    """
    Проверка дублирования номера телефона
    :param self:
    :param phone_number:
    :return:
    """
    try:
        self.get_by_phone(phone_number)
    except UserNotExists:
        raise HTTPException(
            status_code=400,
            detail='Этот номер телефона уже занят.'
        )
