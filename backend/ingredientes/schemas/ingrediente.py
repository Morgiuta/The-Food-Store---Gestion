from datetime import datetime

from pydantic import BaseModel, Field


class IngredienteCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: str | None = None
    es_alergeno: bool = False


class IngredienteUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=100)
    descripcion: str | None = None
    es_alergeno: bool | None = None


class IngredienteRead(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    es_alergeno: bool
    creado_en: datetime

    model_config = {"from_attributes": True}
