import logging
import time

from sqlalchemy.exc import SQLAlchemyError

from .database import engine
from .models.base_model import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(max_retries=5, retry_interval=2):
    """
    Inicializa o banco de dados criando todas as tabelas definidas nos modelos.
    Tenta se conectar várias vezes antes de desistir.
    
    Args:
        max_retries: Número máximo de tentativas
        retry_interval: Intervalo entre tentativas em segundos
    
    Returns:
        bool: True se as tabelas foram criadas com sucesso, False caso contrário
    """
    for attempt in range(max_retries):
        try:
            logger.info(f"Tentativa {attempt + 1}/{max_retries} de criar tabelas no banco de dados...")
            Base.metadata.create_all(bind=engine)
            logger.info("Tabelas criadas com sucesso!")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Erro ao criar tabelas (tentativa {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                logger.info(f"Tentando novamente em {retry_interval} segundos...")
                time.sleep(retry_interval)
            else:
                logger.error("Número máximo de tentativas atingido. Desistindo.")
                return False
            
if __name__ == "__main__":
    init_db()
