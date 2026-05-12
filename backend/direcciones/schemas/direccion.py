from datetime import datetime

from pydantic import BaseModel, Field


class DireccionCreate(BaseModel):
    calle: str = Field(..., min_length=1, max_length=200)
    numero: str = Field(..., min_length=1, max_length=20)
    piso: str | None = Field(None, max_length=20)
    departamento: str | None = Field(None, max_length=20)
    ciudad: str = Field(..., min_length=1, max_length=100)
    codigo_postal: str = Field(..., min_length=1, max_length=20)
    referencia: str | None = Field(None, max_length=500)


class DireccionUpdate(BaseModel):
    calle: str | None = Field(None, min_length=1, max_length=200)
    numero: str | None = Field(None, min_length=1, max_length=20)
    piso: str | None = Field(None, max_length=20)
    departamento: str | None = Field(None, max_length=20)
    ciudad: str | None = Field(None, min_length=1, max_length=100)
    codigo_postal: str | None = Field(None, min_length=1, max_length=20)
    referencia: str | None = Field(None, max_length=500)


class DireccionRead(BaseModel):
    id: int
    usuario_id: int
    calle: str
    numero: str
    piso: str | None
    departamento: str | None
    ciudad: str
    codigo_postal: str
    referencia: str | None
    es_predeterminada: bool
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}