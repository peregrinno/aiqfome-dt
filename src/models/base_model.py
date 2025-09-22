from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    criado_em = Column(DateTime, default=datetime.now())
    atualizado_em = Column(DateTime, default=datetime.now(), onupdate=datetime.now())