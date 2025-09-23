from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.interfaces import ProdutoSimples
from src.models import Clientes, Favoritos
from src.services.produto_service import ProdutoService


class FavoritoController:
    def __init__(self, session: Session):
        self.session = session
    
    async def get_favoritos(self, cliente: Clientes) -> List[ProdutoSimples]:
        favoritos = self._get_or_create_favoritos(cliente)
        produto_ids = favoritos.get_produto_ids()
        
        if not produto_ids:
            return []
        
        produtos_completos = await ProdutoService.get_produtos_by_ids(produto_ids)
        
        produtos_simples = []
        for produto in produtos_completos:
            produtos_simples.append(ProdutoSimples(
                id=produto.id,
                title=produto.title,
                price=produto.price,
                image=produto.image,
                rating=produto.rating
            ))
        
        return produtos_simples
    
    async def adicionar_favorito(self, cliente: Clientes, produto_id: int) -> bool:
        produto = await ProdutoService.get_produto_by_id(produto_id)
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto com ID {produto_id} não encontrado"
            )
        
        favoritos = self._get_or_create_favoritos(cliente)
        resultado = favoritos.add_produto(produto_id)
        
        if resultado:
            self.session.add(favoritos)
            self.session.commit()
            self.session.refresh(favoritos)
            return True
        
        return False
    
    async def remover_favorito(self, cliente: Clientes, produto_id: int) -> bool:
        favoritos = self._get_or_create_favoritos(cliente)
        resultado = favoritos.remove_produto(produto_id)
        
        if resultado:
            self.session.add(favoritos)
            self.session.commit()
            self.session.refresh(favoritos)
            return True
        
        return False
    
    def _get_or_create_favoritos(self, cliente: Clientes) -> Favoritos:
        favoritos = self.session.query(Favoritos).filter_by(cliente_id=cliente.id).first()
        
        if not favoritos:
            favoritos = Favoritos(cliente_id=cliente.id)
            self.session.add(favoritos)
            self.session.commit()
            self.session.refresh(favoritos)
        
        return favoritos
