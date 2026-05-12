from fastapi import APIRouter, Depends, Query

from backend.core.dependencies import DatabaseSession, get_current_user, require_role
from backend.usuarios.schemas.usuario import UsuarioUpdate
from backend.usuarios.services.admin_usuario_service import AdminUsuarioService

router = APIRouter(prefix="/admin", tags=["Admin"])
service = AdminUsuarioService()


async def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    return await require_role(["ADMIN"], current_user)


@router.get("/usuarios")
async def list_usuarios(
    session: DatabaseSession,
    current_user: dict = Depends(require_admin),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    search: str | None = Query(None),
    rol: str | None = Query(None),
):
    return await service.list_usuarios(session, skip, limit, search, rol)


@router.get("/usuarios/{usuario_id}")
async def get_usuario(
    usuario_id: int,
    session: DatabaseSession,
    current_user: dict = Depends(require_admin),
):
    return await service.get_usuario(session, usuario_id)


@router.put("/usuarios/{usuario_id}")
async def update_usuario(
    usuario_id: int,
    body: UsuarioUpdate,
    session: DatabaseSession,
    current_user: dict = Depends(require_admin),
):
    return await service.update_usuario(
        session, current_user, usuario_id, body.model_dump(exclude_unset=True)
    )


@router.patch("/usuarios/{usuario_id}/estado")
async def toggle_estado(
    usuario_id: int,
    session: DatabaseSession,
    current_user: dict = Depends(require_admin),
):
    return await service.toggle_estado(session, current_user, usuario_id)
