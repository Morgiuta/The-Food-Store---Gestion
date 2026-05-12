from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CategoriaCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: str | None = None
    imagen_url: str | None = None
    padre_id: int | None = None


class CategoriaUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=100)
    descripcion: str | None = None
    imagen_url: str | None = None
    padre_id: int | None = None


class CategoriaRead(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    imagen_url: str | None
    padre_id: int | None
    subcategorias: list[CategoriaRead] = []
    creado_en: datetime

    model_config = {"from_attributes": True}
