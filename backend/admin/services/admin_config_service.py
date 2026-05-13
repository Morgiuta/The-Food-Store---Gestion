from typing import Any

from backend.core.exceptions import NotFoundException
from backend.core.uow import UnitOfWork


class AdminConfigService:
    """Service for system configuration."""

    async def get_config(self, uow: UnitOfWork) -> list[dict[str, Any]]:
        configs = await uow.configuraciones.list_all()
        return [
            {
                "clave": c.clave,
                "valor": c.valor,
                "descripcion": c.descripcion,
            }
            for c in configs
        ]

    async def update_config(
        self, uow: UnitOfWork, configs: list[dict[str, str]]
    ) -> list[dict[str, Any]]:
        result = []
        for item in configs:
            conf = await uow.configuraciones.upsert(item["clave"], item["valor"])
            result.append({
                "clave": conf.clave,
                "valor": conf.valor,
                "descripcion": conf.descripcion,
            })
        return result

    async def get_formas_pago(self, uow: UnitOfWork) -> list[dict[str, Any]]:
        formas = await uow.formas_pago.list_all(order_by="nombre")
        return [
            {"id": f.id, "nombre": f.nombre, "activo": f.activo}
            for f in formas
        ]

    async def toggle_forma_pago(
        self, uow: UnitOfWork, id: int, activo: bool
    ) -> dict[str, Any]:
        forma = await uow.formas_pago.toggle_activo(id, activo)
        if not forma:
            raise NotFoundException("Forma de pago no encontrada")
        return {"id": forma.id, "nombre": forma.nombre, "activo": forma.activo}
