from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from .models import Clientes
from .database import Session
from .interfaces import CreateCliente
from .controllers import AuthController, UserController
from settings import api_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

class Dependencies:
    def __init__(self):
        pass
    
    def check_user_existence(email: str):
        with Session() as session: 
            user = session.query(Clientes).filter_by(email=email).first()
            return user is not None


def check_user_not_exists(body: CreateCliente):
    if Dependencies.check_user_existence(body.email): 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: User already exists"
        )
    return body

async def get_session() -> Session: #type: ignore
    try:
        session = Session()
        yield session
    finally:
        session.close()

async def get_auth_controller(
    session: Session = Depends(get_session), #type: ignore
) -> AuthController:
    return AuthController(
        session
    )
    
async def get_user_controller(
    session: Session = Depends(get_session), #type: ignore
) -> UserController:
    return UserController(
        session
    )
    
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)): #type: ignore
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, api_settings.SECRET_KEY, algorithms=[api_settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.query(Clientes).filter(Clientes.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user