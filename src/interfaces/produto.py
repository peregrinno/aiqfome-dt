from typing import List, Optional

from pydantic import BaseModel, Field


class Rating(BaseModel):
    rate: float
    count: int

class Produto(BaseModel):
    id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    description: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None
    rating: Optional[Rating] = None

class ProdutoSimples(BaseModel):
    id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    image: Optional[str] = None
    rating: Optional[Rating] = None

class ProdutoFavorito(BaseModel):
    produto_id: int = Field(..., gt=0)

class ProdutosList(BaseModel):
    produtos: List[Produto] = Field(..., min_items=1)

class ProdutosFavoritosList(BaseModel):
    favoritos: List[ProdutoSimples] = Field(..., min_items=1)
