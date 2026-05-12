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
    roles: list[str] | None = None


class UsuarioRead(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: str | None
    roles: list[str]
    eliminado_en: datetime | None
    creado_en: datetime
    actualizado_en: datetime

    model_config = {"from_attributes": True}


class UsuarioListResponse(BaseModel):
    items: list[UsuarioRead]
    total: int


class CambiarPasswordRequest(BaseModel):
    password_actual: str
    password_nueva: str = Field(..., min_length=8, max_length=128)
