from fastapi import APIRouter, Depends

from backend.admin.schemas.config import (
    ConfigItem,
    FormaPagoRead,
    ToggleFormaPagoRequest,
    UpdateConfigRequest,
)
from backend.admin.services.admin_config_service import AdminConfigService
from backend.core.dependencies import DatabaseSession, RoleRequired
from backend.core.uow import UnitOfWork

router = APIRouter(prefix="/admin", tags=["Admin Config"])
service = AdminConfigService()


@router.get("/config", response_model=list[ConfigItem])
async def get_config(
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN"])),
):
    """Get all system configurations."""
    async with UnitOfWork(session) as uow:
        configs = await service.get_config(uow)
    return configs


@router.put("/config", response_model=list[ConfigItem])
async def update_config(
    body: UpdateConfigRequest,
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN"])),
):
    """Update system configurations."""
    configs_data = [c.model_dump() for c in body.configuraciones]
    async with UnitOfWork(session) as uow:
        configs = await service.update_config(uow, configs_data)
    return configs


@router.get("/formas-pago", response_model=list[FormaPagoRead])
async def get_formas_pago(
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN"])),
):
    """List all payment methods."""
    async with UnitOfWork(session) as uow:
        formas = await service.get_formas_pago(uow)
    return formas


@router.patch("/formas-pago/{forma_id}", response_model=FormaPagoRead)
async def toggle_forma_pago(
    forma_id: int,
    body: ToggleFormaPagoRequest,
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN"])),
):
    """Enable or disable a payment method."""
    async with UnitOfWork(session) as uow:
        forma = await service.toggle_forma_pago(uow, forma_id, body.activo)
    return forma
