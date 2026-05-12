"""
Generic BaseRepository[T] providing common CRUD operations for all entities.

Follows the Repository Pattern to abstract data access from business logic.
All entity-specific repositories should inherit from this class.
"""

from typing import Any, Generic, Optional, Sequence, TypeVar

from sqlalchemy import select, func, update as sa_update, delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository with standard CRUD operations.

    Usage:
        class UsuarioRepository(BaseRepository[Usuario]):
            def __init__(self, session: AsyncSession):
                super().__init__(session, Usuario)
    """

    def __init__(self, session: AsyncSession, model_class: type[ModelType]):
        """
        Initialize the repository.

        Args:
            session: SQLAlchemy async session
            model_class: The ORM model class this repository manages
        """
        self._session = session
        self._model_class = model_class

    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        """
        Get a record by its primary key.

        Args:
            id: Primary key value

        Returns:
            The entity instance or None if not found
        """
        stmt = select(self._model_class).where(self._model_class.id == id)  # type: ignore[attr-defined]
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[dict[str, Any]] = None,
        order_by: Optional[str] = None,
        descending: bool = False,
    ) -> Sequence[ModelType]:
        """
        List records with pagination and optional filters.

        Args:
            skip: Number of records to skip (offset)
            limit: Maximum number of records to return
            filters: Dictionary of column_name: value to filter by
            order_by: Column name to order by
            descending: Whether to sort descending

        Returns:
            List of entity instances
        """
        stmt = select(self._model_class)

        if filters:
            for attr, value in filters.items():
                column = getattr(self._model_class, attr, None)
                if column is not None:
                    stmt = stmt.where(column == value)

        if order_by:
            column = getattr(self._model_class, order_by, None)
            if column is not None:
                if descending:
                    stmt = stmt.order_by(column.desc())
                else:
                    stmt = stmt.order_by(column)

        stmt = stmt.offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def count(self, filters: Optional[dict[str, Any]] = None) -> int:
        """
        Count records matching optional filters.

        Args:
            filters: Dictionary of column_name: value to filter by

        Returns:
            Total count of matching records
        """
        stmt = select(func.count()).select_from(self._model_class)

        if filters:
            for attr, value in filters.items():
                column = getattr(self._model_class, attr, None)
                if column is not None:
                    stmt = stmt.where(column == value)

        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def create(self, obj: ModelType) -> ModelType:
        """
        Create a new record.

        Args:
            obj: Entity instance to create

        Returns:
            The created entity with generated ID
        """
        self._session.add(obj)
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def update(self, id: Any, data: dict[str, Any]) -> Optional[ModelType]:
        """
        Update a record by its primary key.

        Args:
            id: Primary key value
            data: Dictionary of column_name: new_value

        Returns:
            The updated entity or None if not found
        """
        stmt = (
            sa_update(self._model_class)
            .where(self._model_class.id == id)  # type: ignore[attr-defined]
            .values(**data)
            .returning(self._model_class)
        )
        result = await self._session.execute(stmt)
        await self._session.flush()
        return result.scalar_one_or_none()

    async def soft_delete(self, id: Any) -> Optional[ModelType]:
        """
        Soft delete a record by setting its eliminado_en timestamp.

        Args:
            id: Primary key value

        Returns:
            The updated entity or None if not found
        """
        from datetime import datetime, timezone

        stmt = (
            sa_update(self._model_class)
            .where(self._model_class.id == id)  # type: ignore[attr-defined]
            .values(eliminado_en=datetime.now(timezone.utc))
            .returning(self._model_class)
        )
        result = await self._session.execute(stmt)
        await self._session.flush()
        return result.scalar_one_or_none()

    async def hard_delete(self, id: Any) -> bool:
        """
        Permanently delete a record.

        Args:
            id: Primary key value

        Returns:
            True if a record was deleted, False otherwise
        """
        stmt = (
            sa_delete(self._model_class)
            .where(self._model_class.id == id)  # type: ignore[attr-defined]
        )
        result = await self._session.execute(stmt)
        await self._session.flush()
        return result.rowcount > 0

    async def exists(self, id: Any) -> bool:
        """
        Check if a record exists by its primary key.

        Args:
            id: Primary key value

        Returns:
            True if the record exists
        """
        stmt = select(self._model_class).where(self._model_class.id == id)  # type: ignore[attr-defined]
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None
