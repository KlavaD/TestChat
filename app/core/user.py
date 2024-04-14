from typing import Optional

from beanie import PydanticObjectId
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.exceptions import UserNotExists
from fastapi_users_db_beanie import BeanieUserDatabase, ObjectIDIDMixin

from app.api.validator import validation_phone
from app.core.config import settings
from app.core.db import database
from app.models.user import User, get_user_db
from app.schemas.user import UserUpdate


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = settings.secret
    verification_token_secret = settings.secret

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ):
        print(f"Пользователь {user.email} зарегистрирован.")

    async def get_by_phone(self, phone: str) -> User:
        user_collection = database["User"]
        user = await user_collection.find_one({"phone_number": phone})
        if user is None:
            raise UserNotExists()

        return User(**user)

    async def get_by_username(self, username: str) -> User:
        user_collection = database["User"]
        user = await user_collection.find_one({"username": username})
        if user is None:
            raise UserNotExists()

        return User(**user)

    async def update(
        self,
        user_update: UserUpdate,
        user: User,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> User:
        await validation_phone(self, user_update.phone_number)
        if safe:
            updated_user_data = user_update.create_update_dict()
        else:
            updated_user_data = user_update.create_update_dict_superuser()
        updated_user = await self._update(user, updated_user_data)
        await self.on_after_update(updated_user, updated_user_data, request)
        return updated_user


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](
    get_user_manager, [auth_backend]
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
