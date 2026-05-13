from pydantic import BaseModel, Field


class ConfigItem(BaseModel):
    clave: str
    valor: str
    descripcion: str | None = None


class UpdateConfigRequest(BaseModel):
    configuraciones: list[ConfigItem]


class FormaPagoRead(BaseModel):
    id: int
    nombre: str
    activo: bool

    model_config = {"from_attributes": True}


class ToggleFormaPagoRequest(BaseModel):
    activo: bool
