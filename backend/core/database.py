"""
Database configuration and session management using SQLAlchemy async.
"""

from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from backend.core.config import get_settings

settings = get_settings()

# Convention for naming constraints consistently
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    metadata = metadata


def get_database_url() -> str:
    """
    Get the database URL, converting to async driver if needed.
    Tests can override via TEST_DATABASE_URL env var.
    """
    import os
    test_url = os.environ.get("TEST_DATABASE_URL")
    if test_url:
        return test_url

    url = settings.DATABASE_URL
    # Convert postgresql:// to postgresql+asyncpg:// for async driver
    if url.startswith("postgresql://") and "+" not in url:
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


# Async engine for PostgreSQL (lazy creation)
_engine = None


def get_engine():
    """Get or create the async database engine."""
    global _engine
    if _engine is None:
        url = get_database_url()
        is_postgres = "postgresql" in url
        kwargs = {"echo": settings.DEBUG}
        if is_postgres:
            kwargs["pool_pre_ping"] = True
            kwargs["pool_size"] = 5
            kwargs["max_overflow"] = 10
        _engine = create_async_engine(url, **kwargs)
    return _engine


engine = get_engine()

# Session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides a database session.
    Yields an async session and ensures it is closed after use.
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
