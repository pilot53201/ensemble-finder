from fastapi import APIRouter

from app.api import catalog, invitations, matching, users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(matching.router, prefix="/match", tags=["matching"])

api_router.include_router(catalog.instruments_router, prefix="/instruments", tags=["catalog"])
api_router.include_router(catalog.pieces_router, prefix="/pieces", tags=["catalog"])

api_router.include_router(invitations.router, prefix="/invitations", tags=["invitations"])
