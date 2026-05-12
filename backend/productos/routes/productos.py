from fastapi import APIRouter, Depends

from backend.core.dependencies import DatabaseSession, get_current_user, require_role
from backend.productos.schemas.producto import ProductoCreate, ProductoUpdate
from backend.productos.services.producto_service import ProductoService

router = APIRouter(prefix="/productos", tags=["Productos"])
service = ProductoService()


async def require_stock_or_admin(current_user: dict = Depends(get_current_user)) -> dict:
    return await require_role(["STOCK", "ADMIN"], current_user)


@router.get("")
async def list_public(
    session: DatabaseSession,
    skip: int = 0,
    limit: int = 100,
    categoria_id: int | None = None,
):
    return await service.list_public(session, skip=skip, limit=limit, categoria_id=categoria_id)


@router.get("/admin")
async def list_admin(
    session: DatabaseSession,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(require_stock_or_admin),
):
    return await service.list_admin(session, skip=skip, limit=limit)


@router.get("/{producto_id}")
async def get_by_id(producto_id: int, session: DatabaseSession):
    return await service.get_by_id(session, producto_id)


@router.post("", status_code=201)
async def create(
    body: ProductoCreate,
    session: DatabaseSession,
    current_user: dict = Depends(require_stock_or_admin),
):
    return await service.create(session, body.model_dump())


@router.put("/{producto_id}")
async def update(
    producto_id: int,
    body: ProductoUpdate,
    session: DatabaseSession,
    current_user: dict = Depends(require_stock_or_admin),
):
    return await service.update(session, producto_id, body.model_dump(exclude_unset=True))


@router.delete("/{producto_id}", status_code=204)
async def delete(
    producto_id: int,
    session: DatabaseSession,
    current_user: dict = Depends(require_stock_or_admin),
):
    await service.delete(session, producto_id)
