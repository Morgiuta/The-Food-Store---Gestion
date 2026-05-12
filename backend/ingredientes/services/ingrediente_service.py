from backend.core.exceptions import ConflictException, NotFoundException
from backend.ingredientes.models.ingrediente import Ingrediente
from backend.ingredientes.repositories.ingrediente import IngredienteRepository


class IngredienteService:

    async def list(
        self,
        session,
        es_alergeno: bool | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Ingrediente]:
        repo = IngredienteRepository(session)
        filters: dict = {"eliminado_en": None}
        if es_alergeno is not None:
            filters["es_alergeno"] = es_alergeno
        return await repo.list_all(skip=skip, limit=limit, filters=filters)

    async def get_by_id(self, session, ingrediente_id: int) -> Ingrediente:
        repo = IngredienteRepository(session)
        ingrediente = await repo.get_by_id(ingrediente_id)
        if not ingrediente or ingrediente.eliminado_en is not None:
            raise NotFoundException("Ingrediente no encontrado")
        return ingrediente

    async def create(self, session, data: dict) -> Ingrediente:
        repo = IngredienteRepository(session)
        existing = await repo.list_all(filters={"nombre": data["nombre"]})
        if existing:
            raise ConflictException("Ya existe un ingrediente con ese nombre")
        ingrediente = Ingrediente(**data)
        return await repo.create(ingrediente)

    async def update(self, session, ingrediente_id: int, data: dict) -> Ingrediente:
        repo = IngredienteRepository(session)
        existing = await repo.get_by_id(ingrediente_id)
        if not existing or existing.eliminado_en is not None:
            raise NotFoundException("Ingrediente no encontrado")

        if "nombre" in data and data["nombre"] != existing.nombre:
            nombre_check = await repo.list_all(filters={"nombre": data["nombre"]})
            if nombre_check:
                raise ConflictException("Ya existe un ingrediente con ese nombre")

        updated = await repo.update(ingrediente_id, data)
        return updated

    async def delete(self, session, ingrediente_id: int) -> None:
        repo = IngredienteRepository(session)
        existing = await repo.get_by_id(ingrediente_id)
        if not existing or existing.eliminado_en is not None:
            raise NotFoundException("Ingrediente no encontrado")
        await repo.soft_delete(ingrediente_id)
