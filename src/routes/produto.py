from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.security import APIKeyHeader

from settings import api_settings
from src.controllers import FavoritoController
from src.dependencies import get_current_user, get_favorito_controller
from src.interfaces import Produto, ProdutoFavorito, ProdutoSimples
from src.models import Clientes
from src.services.produto_service import ProdutoService
from src.services.cache_service import CacheService

route = APIRouter()

@route.get("/", response_model=List[Produto], description="Lista todos os produtos disponíveis")
async def listar_produtos():
    produtos = await ProdutoService.get_all_produtos()
    return produtos

@route.get("/{produto_id}", response_model=Produto, description="Obtém detalhes de um produto específico")
async def obter_produto(produto_id: int = Path(..., description="ID do produto a ser obtido")):
    produto = await ProdutoService.get_produto_by_id(produto_id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado"
        )
    return produto

@route.get("/favoritos/", response_model=List[ProdutoSimples], description="Lista os produtos favoritos do cliente autenticado")
async def listar_favoritos(
    current_user: Clientes = Depends(get_current_user),
    favorito_controller: FavoritoController = Depends(get_favorito_controller)
):
    favoritos = await favorito_controller.get_favoritos(current_user)
    return favoritos

@route.post("/favoritos/", status_code=status.HTTP_201_CREATED, description="Adiciona um produto aos favoritos")
async def adicionar_favorito(
    produto: ProdutoFavorito,
    current_user: Clientes = Depends(get_current_user),
    favorito_controller: FavoritoController = Depends(get_favorito_controller)
):
    resultado = await favorito_controller.adicionar_favorito(current_user, produto.produto_id)
    if resultado:
        return {"message": f"Produto {produto.produto_id} adicionado aos favoritos com sucesso"}
    return {"message": f"Produto {produto.produto_id} já está nos favoritos"}

@route.delete("/favoritos/{produto_id}", description="Remove um produto dos favoritos")
async def remover_favorito(
    produto_id: int = Path(..., description="ID do produto a ser removido dos favoritos"),
    current_user: Clientes = Depends(get_current_user),
    favorito_controller: FavoritoController = Depends(get_favorito_controller)
):
    resultado = await favorito_controller.remover_favorito(current_user, produto_id)
    if resultado:
        return {"message": f"Produto {produto_id} removido dos favoritos com sucesso"}
    return {"message": f"Produto {produto_id} não está nos favoritos"}


api_key_header = APIKeyHeader(name="X-API-Key")


def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != api_settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chave de API inválida"
        )
    return True


@route.post("/cache/update", description="Atualiza o cache de produtos (requer chave de API)")
async def atualizar_cache(_: bool = Depends(verify_api_key)):
    resultado = await ProdutoService.atualizar_cache()
    if resultado:
        return {"message": "Cache atualizado com sucesso"}
    return {"message": "Erro ao atualizar cache", "status": "error"}


@route.delete("/cache", description="Limpa o cache de produtos (requer chave de API)")
async def limpar_cache(_: bool = Depends(verify_api_key)):
    cache = CacheService()
    if not cache.is_connected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de cache não disponível"
        )
    
    resultado = cache.clear_cache()
    if resultado:
        return {"message": "Cache limpo com sucesso"}
    return {"message": "Erro ao limpar cache", "status": "error"}
