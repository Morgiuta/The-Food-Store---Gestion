from fastapi import APIRouter, Depends, Query

from backend.core.dependencies import DatabaseSession, get_current_user
from backend.direcciones.schemas.direccion import DireccionCreate, DireccionUpdate
from backend.direcciones.services.direccion_service import DireccionService

router = APIRouter(prefix="/direcciones", tags=["Direcciones"])
service = DireccionService()


@router.get("")
async def list_direcciones(
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
):
    """Listar todas las direcciones del usuario actual."""
    return await service.list_by_user(session, current_user["user_id"], skip=skip, limit=limit)


@router.get("/{direccion_id}")
async def get_direccion(
    direccion_id: int,
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    """Obtener una dirección específica del usuario actual."""
    return await service.get_by_id(session, direccion_id, current_user["user_id"])


@router.post("", status_code=201)
async def create_direccion(
    body: DireccionCreate,
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    """Crear una nueva dirección. La primera dirección se marca como predeterminada."""
    return await service.create(session, current_user["user_id"], body.model_dump())


@router.put("/{direccion_id}")
async def update_direccion(
    direccion_id: int,
    body: DireccionUpdate,
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    """Actualizar una dirección existente."""
    return await service.update(
        session, direccion_id, current_user["user_id"], body.model_dump(exclude_unset=True)
    )


@router.delete("/{direccion_id}", status_code=204)
async def delete_direccion(
    direccion_id: int,
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    """Eliminar una dirección (soft delete)."""
    await service.delete(session, direccion_id, current_user["user_id"])


@router.post("/{direccion_id}/predeterminada")
async def set_predeterminada(
    direccion_id: int,
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    """Marcar una dirección como predeterminada."""
    return await service.set_predeterminada(session, direccion_id, current_user["user_id"])