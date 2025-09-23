import json
import logging
from typing import Any, Dict, List, Optional, TypeVar, Generic, Type

import redis
from pydantic import BaseModel

from settings import redis_settings

T = TypeVar('T')

logger = logging.getLogger(__name__)

class CacheService:    
    _instance = None
    _redis_client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CacheService, cls).__new__(cls)
            try:
                cls._redis_client = redis.Redis.from_url(redis_settings.URL)
                logger.info(f"Conexão com Redis estabelecida: {redis_settings.URL}")
            except Exception as e:
                logger.error(f"Erro ao conectar ao Redis: {e}")
                cls._redis_client = None
        return cls._instance
    
    @property
    def is_connected(self) -> bool:
        if self._redis_client is None:
            return False
        try:
            return self._redis_client.ping()
        except:
            return False
    
    def get(self, key: str) -> Optional[str]:
        if not self.is_connected:
            return None
        
        try:
            value = self._redis_client.get(key)
            if value:
                return value.decode('utf-8')
            return None
        except Exception as e:
            logger.error(f"Erro ao obter valor do cache para chave {key}: {e}")
            return None
    
    def set(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        if not self.is_connected:
            return False
        
        try:
            ttl = ttl or redis_settings.TTL
            return self._redis_client.set(key, value, ex=ttl)
        except Exception as e:
            logger.error(f"Erro ao definir valor no cache para chave {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        if not self.is_connected:
            return False
        
        try:
            return bool(self._redis_client.delete(key))
        except Exception as e:
            logger.error(f"Erro ao remover valor do cache para chave {key}: {e}")
            return False
    
    def get_model(self, key: str, model_class: Type[T]) -> Optional[T]:
        if not self.is_connected:
            return None
        
        try:
            value = self.get(key)
            if value:
                data = json.loads(value)
                return model_class.model_validate(data)
            return None
        except Exception as e:
            logger.error(f"Erro ao obter modelo do cache para chave {key}: {e}")
            return None
    
    def set_model(self, key: str, model: BaseModel, ttl: Optional[int] = None) -> bool:
        if not self.is_connected:
            return False
        
        try:
            value = model.model_dump_json()
            return self.set(key, value, ttl)
        except Exception as e:
            logger.error(f"Erro ao definir modelo no cache para chave {key}: {e}")
            return False
    
    def get_models(self, key: str, model_class: Type[T]) -> List[T]:
        if not self.is_connected:
            return []
        
        try:
            value = self.get(key)
            if value:
                data_list = json.loads(value)
                return [model_class.model_validate(item) for item in data_list]
            return []
        except Exception as e:
            logger.error(f"Erro ao obter lista de modelos do cache para chave {key}: {e}")
            return []
    
    def set_models(self, key: str, models: List[BaseModel], ttl: Optional[int] = None) -> bool:
        if not self.is_connected:
            return False
        
        try:
            value = json.dumps([model.model_dump() for model in models])
            return self.set(key, value, ttl)
        except Exception as e:
            logger.error(f"Erro ao definir lista de modelos no cache para chave {key}: {e}")
            return False
    
    def clear_cache(self) -> bool:
        if not self.is_connected:
            return False
        
        try:
            return self._redis_client.flushdb()
        except Exception as e:
            logger.error(f"Erro ao limpar cache: {e}")
            return False
