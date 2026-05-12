from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from backend.categorias.models.categoria import Categoria
from backend.core.exceptions import NotFoundException
from backend.ingredientes.models.ingrediente import Ingrediente
from backend.productos.models.producto import Producto
from backend.productos.models.producto_categoria import ProductoCategoria
from backend.productos.models.producto_ingrediente import ProductoIngrediente
from backend.productos.repositories.producto import ProductoRepository


class ProductoService:

    async def list_public(
        self, session, skip: int = 0, limit: int = 100, categoria_id: int | None = None
    ) -> dict:
        repo = ProductoRepository(session)
        items = await repo.list_public(skip=skip, limit=limit, categoria_id=categoria_id)

        count_stmt = select(func.count(Producto.id)).where(
            Producto.disponible.is_(True),
            Producto.eliminado_en.is_(None),
        )
        if categoria_id is not None:
            count_stmt = (
                count_stmt.join(ProductoCategoria)
                .where(ProductoCategoria.categoria_id == categoria_id)
            )
        result = await session.execute(count_stmt)
        total = result.scalar_one()

        return {
            "items": [self._producto_to_dict(p) for p in items],
            "total": total,
        }

    async def list_admin(self, session, skip: int = 0, limit: int = 100) -> dict:
        stmt = select(Producto).offset(skip).limit(limit).order_by(Producto.nombre)
        result = await session.execute(stmt)
        items = result.scalars().all()

        count_stmt = select(func.count(Producto.id)).select_from(Producto)
        result = await session.execute(count_stmt)
        total = result.scalar_one()

        return {
            "items": [self._producto_to_dict(p) for p in items],
            "total": total,
        }

    async def get_by_id(self, session, producto_id: int) -> dict:
        stmt = (
            select(Producto)
            .where(Producto.id == producto_id, Producto.eliminado_en.is_(None))
            .options(
                selectinload(Producto.categorias).selectinload(ProductoCategoria.categoria),
                selectinload(Producto.ingredientes).selectinload(ProductoIngrediente.ingrediente),
            )
        )
        result = await session.execute(stmt)
        producto = result.scalar_one_or_none()
        if not producto:
            raise NotFoundException("Producto no encontrado")
        return self._producto_to_dict(producto, include_relations=True)

    async def create(self, session, data: dict) -> dict:
        repo = ProductoRepository(session)
        categoria_ids = data.pop("categoria_ids", None)
        ingrediente_ids = data.pop("ingrediente_ids", None)

        producto = Producto(**data)
        producto = await repo.create(producto)

        if categoria_ids:
            for cat_id in categoria_ids:
                pc = ProductoCategoria(producto_id=producto.id, categoria_id=cat_id)
                session.add(pc)
            await session.flush()

        if ingrediente_ids:
            for ing_id in ingrediente_ids:
                pi = ProductoIngrediente(producto_id=producto.id, ingrediente_id=ing_id)
                session.add(pi)
            await session.flush()

        await session.refresh(producto)
        return await self.get_by_id(session, producto.id)

    async def update(self, session, producto_id: int, data: dict) -> dict:
        repo = ProductoRepository(session)
        existing = await repo.get_by_id(producto_id)
        if not existing:
            raise NotFoundException("Producto no encontrado")

        categoria_ids = data.pop("categoria_ids", None)
        ingrediente_ids = data.pop("ingrediente_ids", None)

        scalar_fields = {k: v for k, v in data.items() if v is not None}
        if scalar_fields:
            updated = await repo.update(producto_id, scalar_fields)
            if not updated:
                raise NotFoundException("Producto no encontrado")

        if categoria_ids is not None:
            delete_pc = select(ProductoCategoria).where(
                ProductoCategoria.producto_id == producto_id
            )
            existing_pc = (await session.execute(delete_pc)).scalars().all()
            for pc in existing_pc:
                await session.delete(pc)
            await session.flush()

            for cat_id in categoria_ids:
                pc = ProductoCategoria(producto_id=producto_id, categoria_id=cat_id)
                session.add(pc)
            await session.flush()

        if ingrediente_ids is not None:
            delete_pi = select(ProductoIngrediente).where(
                ProductoIngrediente.producto_id == producto_id
            )
            existing_pi = (await session.execute(delete_pi)).scalars().all()
            for pi in existing_pi:
                await session.delete(pi)
            await session.flush()

            for ing_id in ingrediente_ids:
                pi = ProductoIngrediente(producto_id=producto_id, ingrediente_id=ing_id)
                session.add(pi)
            await session.flush()

        return await self.get_by_id(session, producto_id)

    async def delete(self, session, producto_id: int) -> None:
        repo = ProductoRepository(session)
        existing = await repo.get_by_id(producto_id)
        if not existing:
            raise NotFoundException("Producto no encontrado")
        await repo.soft_delete(producto_id)

    def _producto_to_dict(self, producto: Producto, include_relations: bool = False) -> dict:
        result = {
            "id": producto.id,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "imagen_url": producto.imagen_url,
            "precio": float(producto.precio) if isinstance(producto.precio, Decimal) else producto.precio,
            "stock_cantidad": producto.stock_cantidad,
            "disponible": producto.disponible,
            "creado_en": producto.creado_en.isoformat() if producto.creado_en else None,
            "actualizado_en": producto.actualizado_en.isoformat() if producto.actualizado_en else None,
            "categorias": [],
            "ingredientes": [],
        }
        if include_relations:
            result["categorias"] = [
                self._categoria_to_dict(pc.categoria)
                for pc in (producto.categorias or [])
            ]
            result["ingredientes"] = [
                self._ingrediente_to_dict(pi.ingrediente)
                for pi in (producto.ingredientes or [])
            ]
        return result

    def _categoria_to_dict(self, categoria: Categoria) -> dict:
        return {
            "id": categoria.id,
            "nombre": categoria.nombre,
            "descripcion": categoria.descripcion,
            "imagen_url": categoria.imagen_url,
            "padre_id": categoria.padre_id,
            "subcategorias": [],
            "creado_en": categoria.creado_en.isoformat() if categoria.creado_en else None,
        }

    def _ingrediente_to_dict(self, ingrediente: Ingrediente) -> dict:
        return {
            "id": ingrediente.id,
            "nombre": ingrediente.nombre,
            "descripcion": ingrediente.descripcion,
            "es_alergeno": ingrediente.es_alergeno,
            "creado_en": ingrediente.creado_en.isoformat() if ingrediente.creado_en else None,
        }
