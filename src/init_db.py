from sqlalchemy.exc import SQLAlchemyError
import logging

from .database import engine
from .models.base_model import Base
from .models import Clientes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas definidas nos modelos.
    """
    try:
        logger.info("Criando tabelas no banco de dados...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas criadas com sucesso!")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Erro ao criar tabelas: {e}")
        return False

if __name__ == "__main__":
    init_db()
