import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import ARRAY
from sqlalchemy.dialects.sqlite import TEXT
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.ext.compiler import compiles

# Set test database URL before importing app modules
import os
os.environ.setdefault("TEST_DATABASE_URL", "sqlite+aiosqlite://")

from backend.core.database import Base, get_db
from backend.main import app

import backend.auth.models
import backend.productos.models
import backend.categorias.models
import backend.ingredientes.models
import backend.pedidos.models
import backend.pagos.models


@compiles(ARRAY, "sqlite")
def compile_array_sqlite(type_, compiler, **kw):
    return "TEXT"


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "sqlite+aiosqlite://",
)


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine) -> AsyncGenerator[AsyncSession, None]:
    connection = await engine.connect()
    transaction = await connection.begin()

    async_session = AsyncSession(bind=connection, expire_on_commit=False)

    yield async_session

    await async_session.close()
    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def _override_get_db():
        yield session

    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
def sample_user_data() -> dict:
    return {
        "nombre": "Test User",
        "email": "testuser@example.com",
        "password_hash": "$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Qlq5P0q1q1q1q1q1q1q1q1q1q",
        "telefono": "1234567890",
    }
