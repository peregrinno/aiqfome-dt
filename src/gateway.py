from fastapi import APIRouter

from .routes import cliente_route, produto_route, health_check_route


api_router = APIRouter()

api_router.include_router(cliente_route, prefix="/auth", tags=["Autenticação"])
api_router.include_router(produto_route, prefix="/produtos", tags=["Produtos"])
api_router.include_router(health_check_route, prefix="/health-check", tags=["Health Check"])
