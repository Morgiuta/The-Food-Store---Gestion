from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from backend.auth.services.role_service import RoleService
from backend.core.dependencies import DatabaseSession, get_current_user, require_role

router = APIRouter(prefix="/admin", tags=["Admin"])
role_service = RoleService()


class AssignRoleRequest(BaseModel):
    rol_nombre: str = Field(..., min_length=1)


async def require_admin_role(
    current_user: dict = Depends(get_current_user),
) -> dict:
    return await require_role(["ADMIN"], current_user)


@router.post("/usuarios/{usuario_id}/roles")
async def assign_role(
    usuario_id: int,
    body: AssignRoleRequest,
    session: DatabaseSession,
    current_user: dict = Depends(require_admin_role),
):
    """Assign a role to a user (ADMIN only)."""
    return await role_service.assign_role(
        session, current_user, usuario_id, body.rol_nombre
    )


@router.delete("/usuarios/{usuario_id}/roles/{rol_nombre}")
async def revoke_role(
    usuario_id: int,
    rol_nombre: str,
    session: DatabaseSession,
    current_user: dict = Depends(require_admin_role),
):
    """Revoke a role from a user (ADMIN only)."""
    return await role_service.revoke_role(
        session, current_user, usuario_id, rol_nombre
    )
