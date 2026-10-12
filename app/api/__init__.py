from fastapi import APIRouter

from app.api import matching, users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(matching.router, prefix="/match", tags=["matching"])
