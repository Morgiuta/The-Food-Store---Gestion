from typing import Optional, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.core.base_repository import BaseRepository
from backend.productos.models.producto import Producto
from backend.productos.models.producto_categoria import ProductoCategoria
from backend.productos.models.producto_ingrediente import ProductoIngrediente


class ProductoRepository(BaseRepository[Producto]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Producto)

    async def list_public(
        self,
        skip: int = 0,
        limit: int = 100,
        categoria_id: Optional[int] = None,
    ) -> Sequence[Producto]:
        stmt = select(Producto).where(
            Producto.disponible.is_(True),
            Producto.eliminado_en.is_(None),
        )
        if categoria_id is not None:
            stmt = (
                stmt.join(ProductoCategoria)
                .where(ProductoCategoria.categoria_id == categoria_id)
            )
        stmt = (
            stmt
            .offset(skip)
            .limit(limit)
            .order_by(Producto.nombre)
            .options(
                selectinload(Producto.categorias).selectinload(ProductoCategoria.categoria),
                selectinload(Producto.ingredientes).selectinload(ProductoIngrediente.ingrediente),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def list_by_category(
        self, categoria_id: int
    ) -> Sequence[Producto]:
        stmt = (
            select(Producto)
            .join(ProductoCategoria)
            .where(ProductoCategoria.categoria_id == categoria_id)
            .order_by(Producto.nombre)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def search_by_text(
        self, query: str, skip: int = 0, limit: int = 100
    ) -> Sequence[Producto]:
        pattern = f"%{query}%"
        stmt = (
            select(Producto)
            .where(Producto.nombre.ilike(pattern))
            .offset(skip)
            .limit(limit)
            .order_by(Producto.nombre)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def update_stock(
        self, producto_id: int, cantidad: int
    ) -> Optional[Producto]:
        stmt = (
            update(Producto)
            .where(Producto.id == producto_id)
            .values(stock_cantidad=Producto.stock_cantidad + cantidad)
            .returning(Producto)
        )
        result = await self._session.execute(stmt)
        await self._session.flush()
        return result.scalar_one_or_none()

    async def get_low_stock(
        self, threshold: int = 5
    ) -> Sequence[Producto]:
        stmt = (
            select(Producto)
            .where(
                Producto.stock_cantidad < threshold,
                Producto.eliminado_en.is_(None),
            )
            .order_by(Producto.stock_cantidad)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
