from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.interfaces import UpdateCliente
from src.models import Clientes


class UserController:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> Clientes:
        cliente = self.session.query(Clientes).filter(Clientes.id == user_id).first()
        
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )
            
        return cliente
    
    def get_by_email(self, email: str) -> Clientes:
        cliente = self.session.query(Clientes).filter(Clientes.email == email).first()
        
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )
            
        return cliente

    def update_cliente(self, cliente: Clientes, cliente_data: UpdateCliente) -> Clientes:

        if cliente_data.email != cliente.email:
            cliente_existe = self.get_by_email(cliente_data.email)
            if cliente_existe and cliente_existe.id != cliente.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email ja cadastrado"
                )
                
        cliente.nome = cliente_data.nome
        cliente.email = cliente_data.email
        
        self.session.add(cliente)
        self.session.commit()
        self.session.refresh(cliente)
        return cliente

    def delete_cliente(self, cliente: Clientes) -> None:
        self.session.delete(cliente)
        self.session.commit()

        return True