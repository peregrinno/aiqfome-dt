from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.controllers import FavoritoController
from src.dependencies import get_current_user, get_favorito_controller
from src.interfaces import Produto, ProdutoFavorito, ProdutoSimples
from src.models import Clientes
from src.services.produto_service import ProdutoService

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
