from fastapi import APIRouter, Depends

from backend.core.dependencies import DatabaseSession, get_current_user
from backend.usuarios.schemas.usuario import CambiarPasswordRequest, UsuarioUpdate
from backend.usuarios.services.perfil_service import PerfilService

router = APIRouter(prefix="/perfil", tags=["Perfil"])
service = PerfilService()


@router.get("")
async def get_perfil(
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    return await service.get_perfil(session, current_user["user_id"])


@router.put("")
async def update_perfil(
    body: UsuarioUpdate,
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    return await service.update_perfil(
        session, current_user["user_id"], body.model_dump(exclude_unset=True)
    )


@router.put("/password", status_code=204)
async def change_password(
    body: CambiarPasswordRequest,
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    await service.change_password(
        session, current_user["user_id"], body.password_actual, body.password_nueva
    )
