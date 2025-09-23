from .cliente import (
    BaseCliente,
    CreateCliente,
    UpdateCliente,
    ClienteResponse,
    ClientesResponse,
    LoginData,
    Token,
    TokenData,
)

from .produto import (
    Produto,
    ProdutoSimples,
    ProdutoFavorito,
    ProdutosList,
    ProdutosFavoritosList,
    Rating,
)

__all__ = [
    "BaseCliente",
    "CreateCliente",
    "UpdateCliente",
    "ClienteResponse",
    "ClientesResponse",
    "LoginData",
    "Token",
    "TokenData",
    "Produto",
    "ProdutoSimples",
    "ProdutoFavorito",
    "ProdutosList",
    "ProdutosFavoritosList",
    "Rating",
]
