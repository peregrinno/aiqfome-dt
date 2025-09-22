from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.models import Clientes
from src.auth import verify_password, get_password_hash, create_access_token
from src.interfaces import CreateCliente, LoginData, Token


class AuthController:
    def __init__(self, session: Session):
        self.session = session

    def register(self, cliente_data: CreateCliente) -> Clientes:
        hashed_password = get_password_hash(cliente_data.senha)

        cliente_existente = self.session.query(Clientes).filter(Clientes.email == cliente_data.email).first()
        
        if cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        
        cliente = Clientes(
            nome=cliente_data.nome,
            email=cliente_data.email,
            senha=hashed_password
        )
        
        self.session.add(cliente)
        self.session.commit()
        self.session.refresh(cliente)
        
        return cliente

    def authenticate(self, login_data: LoginData) -> Token:
        cliente = self.session.query(Clientes).filter(Clientes.email == login_data.email).first()
        
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not verify_password(login_data.senha, cliente.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(data={"sub": str(cliente.id)})
        
        return Token(access_token=access_token, token_type="bearer")
