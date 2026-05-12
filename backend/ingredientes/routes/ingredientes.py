from fastapi import APIRouter, Depends, Query

from backend.core.dependencies import DatabaseSession, get_current_user, require_role
from backend.ingredientes.schemas.ingrediente import IngredienteCreate, IngredienteUpdate
from backend.ingredientes.services.ingrediente_service import IngredienteService

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])
service = IngredienteService()


async def require_stock_or_admin(current_user: dict = Depends(get_current_user)) -> dict:
    return await require_role(["STOCK", "ADMIN"], current_user)


@router.get("")
async def list_ingredientes(
    session: DatabaseSession,
    es_alergeno: bool | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
):
    return await service.list(session, es_alergeno=es_alergeno, skip=skip, limit=limit)


@router.get("/{ingrediente_id}")
async def get_ingrediente(ingrediente_id: int, session: DatabaseSession):
    return await service.get_by_id(session, ingrediente_id)


@router.post("", status_code=201)
async def create_ingrediente(
    body: IngredienteCreate,
    session: DatabaseSession,
    current_user: dict = Depends(require_stock_or_admin),
):
    return await service.create(session, body.model_dump())


@router.put("/{ingrediente_id}")
async def update_ingrediente(
    ingrediente_id: int,
    body: IngredienteUpdate,
    session: DatabaseSession,
    current_user: dict = Depends(require_stock_or_admin),
):
    return await service.update(session, ingrediente_id, body.model_dump(exclude_unset=True))


@router.delete("/{ingrediente_id}", status_code=204)
async def delete_ingrediente(
    ingrediente_id: int,
    session: DatabaseSession,
    current_user: dict = Depends(require_stock_or_admin),
):
    await service.delete(session, ingrediente_id)
