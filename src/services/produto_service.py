import logging
from typing import List, Optional, TypeVar

import httpx

from src.interfaces import Produto

T = TypeVar('T')

logger = logging.getLogger(__name__)

class ProdutoService:
    BASE_URL = "https://fakestoreapi.com"
    
    @classmethod
    async def get_all_produtos(cls) -> List[Produto]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{cls.BASE_URL}/products")
                response.raise_for_status()
                produtos_data = response.json()
                return [Produto(**produto) for produto in produtos_data]
        except Exception as e:
            logger.error(f"Erro ao obter produtos: {e}")
            return []
    
    @classmethod
    async def get_produto_by_id(cls, produto_id: int) -> Optional[Produto]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{cls.BASE_URL}/products/{produto_id}")
                response.raise_for_status()
                produto_data = response.json()
                return Produto(**produto_data)
        except Exception as e:
            logger.error(f"Erro ao obter produto {produto_id}: {e}")
            return None
    
    @classmethod
    async def get_produtos_by_ids(cls, produto_ids: List[str]) -> List[Produto]:
        produtos = []
        for produto_id in produto_ids:
            produto = await cls.get_produto_by_id(int(produto_id))
            if produto:
                produtos.append(produto)
        return produtos
