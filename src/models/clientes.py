from sqlalchemy import Column, String

from .base_model import BaseModel


class Clientes(BaseModel):
    __tablename__ = "clientes"
    
    nome = Column(String, nullable=True)
    email = Column(String)
    senha = Column(String)

    def __str__(self):
        return self.email

