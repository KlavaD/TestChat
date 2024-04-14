from fastapi import APIRouter

from app.api.endpoints import message_router, user_router

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(message_router)
