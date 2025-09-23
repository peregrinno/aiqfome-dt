import json
import logging
from typing import List, Optional, TypeVar

import httpx

from settings import redis_settings
from src.interfaces import Produto
from src.services.cache_service import CacheService

T = TypeVar('T')

logger = logging.getLogger(__name__)

class ProdutoService:
    BASE_URL = "https://fakestoreapi.com"
    CACHE_KEY_ALL = "produtos:all"
    CACHE_KEY_PRODUTO = "produto:{}"
    
    @classmethod
    async def get_all_produtos(cls) -> List[Produto]:
        cache = CacheService()
        if cache.is_connected:
            cached_produtos = cache.get_models(cls.CACHE_KEY_ALL, Produto)
            if cached_produtos:
                logger.info("Produtos obtidos do cache")
                return cached_produtos
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{cls.BASE_URL}/products")
                response.raise_for_status()
                produtos_data = response.json()
                produtos = [Produto(**produto) for produto in produtos_data]
                
                if cache.is_connected:
                    cache.set_models(cls.CACHE_KEY_ALL, produtos)
                    logger.info("Produtos salvos no cache")
                
                return produtos
        except Exception as e:
            logger.error(f"Erro ao obter produtos: {e}")
            return []
    
    @classmethod
    async def get_produto_by_id(cls, produto_id: int) -> Optional[Produto]:
        cache_key = cls.CACHE_KEY_PRODUTO.format(produto_id)
        cache = CacheService()
        if cache.is_connected:
            cached_produto = cache.get_model(cache_key, Produto)
            if cached_produto:
                logger.info(f"Produto {produto_id} obtido do cache")
                return cached_produto
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{cls.BASE_URL}/products/{produto_id}")
                response.raise_for_status()
                produto_data = response.json()
                produto = Produto(**produto_data)
                
                if cache.is_connected:
                    cache.set_model(cache_key, produto)
                    logger.info(f"Produto {produto_id} salvo no cache")
                
                return produto
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
    
    @classmethod
    async def atualizar_cache(cls) -> bool:
        logger.info("Atualizando cache de produtos...")
        cache = CacheService()
        if not cache.is_connected:
            logger.error("Redis não está disponível para atualização do cache")
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{cls.BASE_URL}/products")
                response.raise_for_status()
                produtos_data = response.json()
                produtos = [Produto(**produto) for produto in produtos_data]
                
                cache.set_models(cls.CACHE_KEY_ALL, produtos)
                
                for produto in produtos:
                    cache_key = cls.CACHE_KEY_PRODUTO.format(produto.id)
                    cache.set_model(cache_key, produto)
                
                logger.info(f"Cache atualizado com sucesso: {len(produtos)} produtos")
                return True
        except Exception as e:
            logger.error(f"Erro ao atualizar cache de produtos: {e}")
            return False
