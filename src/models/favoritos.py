from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .base_model import BaseModel
from .clientes import Clientes

class Favoritos(BaseModel):
    __tablename__ = "favoritos"
    
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    produto_ids = Column(String, nullable=False)
    
    cliente = relationship("Clientes", back_populates="favoritos")
    
    def __init__(self, cliente_id, produto_ids=None):
        self.cliente_id = cliente_id
        self.produto_ids = produto_ids or ""
    
    def add_produto(self, produto_id):
        """Adiciona um produto à lista de favoritos"""
        ids = self.get_produto_ids()
        if str(produto_id) not in ids:
            ids.append(str(produto_id))
            self.produto_ids = ",".join(ids)
            return True
        return False
    
    def remove_produto(self, produto_id):
        """Remove um produto da lista de favoritos"""
        ids = self.get_produto_ids()
        if str(produto_id) in ids:
            ids.remove(str(produto_id))
            self.produto_ids = ",".join(ids)
            return True
        return False
    
    def get_produto_ids(self):
        """Retorna a lista de IDs de produtos favoritos"""
        if not self.produto_ids:
            return []
        return self.produto_ids.split(",")
    
    def __str__(self):
        return f"Favoritos do cliente {self.cliente_id}: {self.produto_ids}"

Clientes.favoritos = relationship("Favoritos", back_populates="cliente", uselist=False)
