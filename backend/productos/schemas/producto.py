from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from backend.categorias.schemas.categoria import CategoriaRead
from backend.ingredientes.schemas.ingrediente import IngredienteRead


class ProductoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    descripcion: str | None = None
    imagen_url: str | None = None
    precio: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    stock_cantidad: int = Field(default=0, ge=0)
    disponible: bool = True
    categoria_ids: list[int] | None = None
    ingrediente_ids: list[int] | None = None


class ProductoUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=200)
    descripcion: str | None = None
    imagen_url: str | None = None
    precio: Decimal | None = Field(None, gt=0, max_digits=10, decimal_places=2)
    stock_cantidad: int | None = Field(None, ge=0)
    disponible: bool | None = None
    categoria_ids: list[int] | None = None
    ingrediente_ids: list[int] | None = None


class ProductoRead(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    imagen_url: str | None
    precio: Decimal
    stock_cantidad: int
    disponible: bool
    categorias: list[CategoriaRead] = []
    ingredientes: list[IngredienteRead] = []
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}
