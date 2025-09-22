from fastapi import APIRouter

from .routes import cliente_route


api_router = APIRouter()

api_router.include_router(cliente_route, prefix="/auth", tags=["Autenticação"])
