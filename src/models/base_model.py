from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    criado_em = Column(DateTime, default=datetime.now())
    atualizado_em = Column(DateTime, default=datetime.now(), onupdate=datetime.now())