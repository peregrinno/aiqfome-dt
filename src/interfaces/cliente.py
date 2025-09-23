from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseCliente(BaseModel):
    nome: Optional[str] = None
    email: EmailStr


class CreateCliente(BaseCliente):
    nome: Optional[str] = None
    email: EmailStr
    senha: str
    
    model_config = {"from_attributes": True}


class UpdateCliente(BaseCliente):
    nome: Optional[str] = None
    email: Optional[str] = None
    
    model_config = {"from_attributes": True}


class ClienteResponse(BaseModel):
    id: int
    nome: Optional[str] = None
    email: str
    
    model_config = {"from_attributes": True}


class ClientesResponse(BaseModel):
    clientes: list[BaseCliente]


class LoginData(BaseModel):
    email: EmailStr
    senha: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: Optional[str] = None
