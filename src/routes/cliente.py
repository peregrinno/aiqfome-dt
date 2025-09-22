from fastapi import APIRouter, Depends, status

from src.interfaces import CreateCliente, UpdateCliente, ClienteResponse, LoginData, Token
from src.controllers import AuthController, UserController
from src.dependencies import get_auth_controller, get_current_user, check_user_not_exists, get_user_controller
from src.models import Clientes

route = APIRouter()


@route.post("/clientes", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED, description="Cria um novo cliente")
async def create_cliente(
    cliente_data: CreateCliente = Depends(check_user_not_exists),
    auth_controller: AuthController = Depends(get_auth_controller)
):
    return auth_controller.register(cliente_data)


@route.post("/login", response_model=Token, description="Autentica um cliente")
async def login(
    login_data: LoginData,
    auth_controller: AuthController = Depends(get_auth_controller)
):
    return auth_controller.authenticate(login_data)


@route.get("/clientes/me", response_model=ClienteResponse, description="Retorna os dados do cliente autenticado")
async def get_current_cliente_data(current_user: Clientes = Depends(get_current_user)):
    return current_user


@route.put("/clientes/me", response_model=ClienteResponse, description="Atualiza os dados do cliente autenticado")
async def update_current_cliente_data(
    cliente_data: UpdateCliente,
    current_user: Clientes = Depends(get_current_user),
    user_controller: UserController = Depends(get_user_controller)
):
    return user_controller.update_cliente(current_user, cliente_data)

@route.delete("/clientes/me", description="Deleta o cliente autenticado")
async def delete_current_cliente_data(
    current_user: Clientes = Depends(get_current_user),
    user_controller: UserController = Depends(get_user_controller)
):
    return user_controller.delete_cliente(current_user)