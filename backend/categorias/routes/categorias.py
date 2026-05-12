from fastapi import APIRouter, Depends

from backend.categorias.schemas.categoria import CategoriaCreate, CategoriaUpdate
from backend.categorias.services.categoria_service import CategoriaService
from backend.core.dependencies import DatabaseSession, get_current_user, require_role

router = APIRouter(prefix="/categorias", tags=["Categorias"])
service = CategoriaService()


async def require_stock_or_admin(current_user: dict = Depends(get_current_user)) -> dict:
    return await require_role(["STOCK", "ADMIN"], current_user)


@router.get("")
async def get_tree(session: DatabaseSession):
    return await service.get_tree(session)


@router.get("/{categoria_id}")
async def get_by_id(categoria_id: int, session: DatabaseSession):
    return await service.get_by_id(session, categoria_id)


@router.post("", status_code=201)
async def create(
    body: CategoriaCreate,
    session: DatabaseSession,
    current_user: dict = Depends(require_stock_or_admin),
):
    return await service.create(session, body.model_dump())


@router.put("/{categoria_id}")
async def update(
    categoria_id: int,
    body: CategoriaUpdate,
    session: DatabaseSession,
    current_user: dict = Depends(require_stock_or_admin),
):
    return await service.update(session, categoria_id, body.model_dump(exclude_unset=True))


@router.delete("/{categoria_id}", status_code=204)
async def delete(
    categoria_id: int,
    session: DatabaseSession,
    current_user: dict = Depends(require_stock_or_admin),
):
    await service.delete(session, categoria_id)
