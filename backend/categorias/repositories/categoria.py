from typing import Optional, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.categorias.models.categoria import Categoria
from backend.core.base_repository import BaseRepository
from backend.productos.models.producto_categoria import ProductoCategoria


class CategoriaRepository(BaseRepository[Categoria]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Categoria)

    async def get_tree(self) -> Sequence[Categoria]:
        stmt = (
            select(Categoria)
            .options(selectinload(Categoria.subcategorias))
            .order_by(Categoria.padre_id, Categoria.nombre)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_root_categorias(self) -> Sequence[Categoria]:
        stmt = (
            select(Categoria)
            .where(Categoria.padre_id.is_(None))
            .order_by(Categoria.nombre)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_subcategorias(self, padre_id: int) -> Sequence[Categoria]:
        stmt = (
            select(Categoria)
            .where(Categoria.padre_id == padre_id)
            .order_by(Categoria.nombre)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def validate_no_cycles(
        self, categoria_id: int, nuevo_padre_id: int
    ) -> bool:
        if categoria_id == nuevo_padre_id:
            return False
        current = nuevo_padre_id
        while current is not None:
            if current == categoria_id:
                return False
            stmt = select(Categoria.padre_id).where(Categoria.id == current)
            result = await self._session.execute(stmt)
            current = result.scalar_one_or_none()
        return True

    async def count_productos(self, categoria_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(ProductoCategoria)
            .where(ProductoCategoria.categoria_id == categoria_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()
