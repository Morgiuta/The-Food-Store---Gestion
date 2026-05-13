from decimal import Decimal

from fastapi import APIRouter, Depends, Query

from backend.core.dependencies import DatabaseSession, RoleRequired, get_current_user, require_role
from backend.core.uow import UnitOfWork
from backend.productos.schemas.producto import ProductoCreate, ProductoUpdate
from backend.productos.services.producto_service import ProductoService

router = APIRouter(prefix="/productos", tags=["Productos"])
service = ProductoService()


async def require_stock_or_admin(current_user: dict = Depends(get_current_user)) -> dict:
    return await require_role(["STOCK", "ADMIN"], current_user)


@router.get("/search")
async def search(
    session: DatabaseSession,
    q: str = Query("", min_length=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    precio_min: Decimal | None = Query(None),
    precio_max: Decimal | None = Query(None),
    categoria_id: int | None = Query(None),
):
    return await service.search(session, q, skip, limit, precio_min, precio_max, categoria_id)


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


@router.patch("/{producto_id}/disponibilidad")
async def toggle_disponibilidad(
    producto_id: int,
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN", "STOCK"])),
):
    """Toggle product disponibilidad (ADMIN/STOCK only)."""
    from backend.productos.services.producto_service import ProductoService
    service = ProductoService()
    async with UnitOfWork(session) as uow:
        producto = await service.toggle_disponibilidad(uow, producto_id)
    return {"id": producto.id, "disponible": producto.disponible}


@router.get("/{producto_id}/ingredientes")
async def list_ingredientes_producto(
    producto_id: int,
    session: DatabaseSession,
):
    """List ingredients of a product (public)."""
    from backend.productos.services.producto_service import ProductoService
    service = ProductoService()
    async with UnitOfWork(session) as uow:
        ingredientes = await service.list_ingredientes(uow, producto_id)
    return ingredientes


@router.post("/{producto_id}/ingredientes", status_code=201)
async def add_ingrediente_producto(
    producto_id: int,
    body: dict,
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN", "STOCK"])),
):
    """Add ingredient to product (ADMIN/STOCK only)."""
    from backend.productos.services.producto_service import ProductoService
    service = ProductoService()
    async with UnitOfWork(session) as uow:
        result = await service.add_ingrediente(uow, producto_id, body["ingrediente_id"], body.get("es_removible", True))
    return result


@router.delete("/{producto_id}/ingredientes/{ingrediente_id}", status_code=204)
async def remove_ingrediente_producto(
    producto_id: int,
    ingrediente_id: int,
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN", "STOCK"])),
):
    """Remove ingredient from product (ADMIN/STOCK only)."""
    from backend.productos.services.producto_service import ProductoService
    service = ProductoService()
    async with UnitOfWork(session) as uow:
        await service.remove_ingrediente(uow, producto_id, ingrediente_id)
