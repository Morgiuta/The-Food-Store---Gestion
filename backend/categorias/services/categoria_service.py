from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.categorias.models.categoria import Categoria
from backend.categorias.repositories.categoria import CategoriaRepository
from backend.core.exceptions import ConflictException, NotFoundException


class CategoriaService:

    async def get_tree(self, session) -> list[dict]:
        repo = CategoriaRepository(session)
        categorias = await repo.get_tree()
        roots = [c for c in categorias if c.padre_id is None]
        return [self._build_tree(c) for c in roots]

    async def get_by_id(self, session, categoria_id: int) -> dict:
        stmt = (
            select(Categoria)
            .where(Categoria.id == categoria_id)
            .options(selectinload(Categoria.subcategorias))
        )
        result = await session.execute(stmt)
        categoria = result.scalar_one_or_none()
        if not categoria:
            raise NotFoundException("Categoría no encontrada")
        return self._build_tree(categoria)

    async def create(self, session, data: dict) -> dict:
        repo = CategoriaRepository(session)
        padre_id = data.get("padre_id")
        if padre_id is not None:
            parent = await repo.get_by_id(padre_id)
            if not parent:
                raise NotFoundException("Categoría padre no encontrada")
        categoria = Categoria(**data)
        created = await repo.create(categoria)
        await session.commit()
        return self._categoria_to_dict(created)

    async def update(self, session, categoria_id: int, data: dict) -> dict:
        repo = CategoriaRepository(session)
        existing = await repo.get_by_id(categoria_id)
        if not existing:
            raise NotFoundException("Categoría no encontrada")

        if "padre_id" in data:
            nuevo_padre_id = data["padre_id"]
            if nuevo_padre_id == categoria_id:
                raise ConflictException("Una categoría no puede ser su propio padre")
            if nuevo_padre_id is not None:
                parent = await repo.get_by_id(nuevo_padre_id)
                if not parent:
                    raise NotFoundException("Categoría padre no encontrada")
            if not await repo.validate_no_cycles(categoria_id, nuevo_padre_id):
                raise ConflictException("La asignación crearía un ciclo en la jerarquía")

        updated = await repo.update(categoria_id, data)
        await session.commit()
        return self._categoria_to_dict(updated)

    async def delete(self, session, categoria_id: int) -> None:
        repo = CategoriaRepository(session)
        existing = await repo.get_by_id(categoria_id)
        if not existing:
            raise NotFoundException("Categoría no encontrada")
        count = await repo.count_productos(categoria_id)
        if count > 0:
            raise ConflictException(
                "No se puede eliminar: la categoría tiene productos asociados"
            )
        await repo.soft_delete(categoria_id)
        await session.commit()

    def _build_tree(self, categoria: Categoria) -> dict:
        return {
            "id": categoria.id,
            "nombre": categoria.nombre,
            "descripcion": categoria.descripcion,
            "imagen_url": categoria.imagen_url,
            "padre_id": categoria.padre_id,
            "subcategorias": [self._build_tree(sub) for sub in categoria.subcategorias],
        }

    def _categoria_to_dict(self, categoria: Categoria) -> dict:
        return {
            "id": categoria.id,
            "nombre": categoria.nombre,
            "descripcion": categoria.descripcion,
            "imagen_url": categoria.imagen_url,
            "padre_id": categoria.padre_id,
        }
