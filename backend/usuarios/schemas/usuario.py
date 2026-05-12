from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    telefono: str | None = Field(None, max_length=20)


class UsuarioUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
    telefono: str | None = Field(None, max_length=20)


class UsuarioRead(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: str | None
    roles: list[str]
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}
