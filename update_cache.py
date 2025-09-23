import asyncio
import logging
import sys
from datetime import datetime

from src.services.produto_service import ProdutoService
from src.services.cache_service import CacheService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def main():
    try:
        logger.info(f"[{datetime.now().isoformat()}] Iniciando atualização manual do cache...")
        
        cache = CacheService()
        if not cache.is_connected:
            logger.error("Redis não está disponível. Não é possível atualizar o cache.")
            return 1
        
        success = await ProdutoService.atualizar_cache()
        
        if success:
            logger.info(f"[{datetime.now().isoformat()}] Cache atualizado com sucesso!")
            return 0
        else:
            logger.error(f"[{datetime.now().isoformat()}] Falha ao atualizar o cache.")
            return 1
            
    except Exception as e:
        logger.error(f"Erro ao atualizar o cache: {e}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
