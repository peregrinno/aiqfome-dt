import asyncio
import logging
import time
from datetime import datetime

from settings import redis_settings
from src.services.produto_service import ProdutoService
from src.services.cache_service import CacheService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
UPDATE_INTERVAL = redis_settings.TTL

async def update_cache_task():
    while True:
        try:
            logger.info(f"[{datetime.now().isoformat()}] Iniciando atualização do cache...")
            
            cache = CacheService()
            if not cache.is_connected:
                logger.error("Redis não está disponível. Pulando atualização do cache.")
                await asyncio.sleep(60)  # Tentar novamente em 1 minuto
                continue
            
            success = await ProdutoService.atualizar_cache()
            
            if success:
                logger.info(f"[{datetime.now().isoformat()}] Cache atualizado com sucesso!")
            else:
                logger.error(f"[{datetime.now().isoformat()}] Falha ao atualizar o cache.")
            
            logger.info(f"Próxima atualização em {UPDATE_INTERVAL} segundos.")
            await asyncio.sleep(UPDATE_INTERVAL)
            
        except Exception as e:
            logger.error(f"Erro na tarefa de atualização do cache: {e}")
            await asyncio.sleep(60)  # Tentar novamente em 1 minuto

async def run_cache_updater():
    logger.info("Iniciando o atualizador de cache...")
    await update_cache_task()

if __name__ == "__main__":
    asyncio.run(run_cache_updater())
