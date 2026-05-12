import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture(autouse=True)
async def disable_rate_limiting():
    from backend.auth.routes.auth import limiter as auth_limiter
    auth_limiter.enabled = False
    yield
    auth_limiter.enabled = True


async def seed_roles(session: AsyncSession):
    from backend.auth.models.rol import Rol
    roles = [
        Rol(nombre="ADMIN", descripcion="Acceso total al sistema"),
        Rol(nombre="STOCK", descripcion="Gestión de inventario y productos"),
        Rol(nombre="PEDIDOS", descripcion="Gestión de pedidos"),
        Rol(nombre="CLIENT", descripcion="Usuario cliente"),
    ]
    session.add_all(roles)
    await session.flush()


async def create_user(
    session: AsyncSession,
    email: str,
    password: str = "password123",
    roles: list[str] | None = None,
):
    from backend.auth.models.rol import Rol
    from backend.auth.models.usuario import Usuario
    from backend.auth.models.usuario_rol import UsuarioRol
    from backend.core.security import get_password_hash

    user = Usuario(
        nombre="Test User",
        email=email,
        password_hash=get_password_hash(password),
        telefono="1234567890",
    )
    session.add(user)
    await session.flush()
    await session.refresh(user)

    if roles:
        for rol_name in roles:
            stmt = select(Rol).where(Rol.nombre == rol_name)
            result = await session.execute(stmt)
            rol = result.scalar_one()
            ur = UsuarioRol(usuario_id=user.id, rol_id=rol.id)
            session.add(ur)
        await session.flush()

    return user


async def get_stock_token(client: AsyncClient, session: AsyncSession) -> str:
    await seed_roles(session)
    await create_user(session, "stock@test.com", roles=["STOCK"])
    response = await client.post("/api/v1/auth/login", json={
        "email": "stock@test.com",
        "password": "password123",
    })
    return response.json()["access_token"]


async def auth_header(client: AsyncClient, session: AsyncSession) -> dict:
    token = await get_stock_token(client, session)
    return {"Authorization": f"Bearer {token}"}


class TestIngredientes:

    async def test_create_ingrediente(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        response = await client.post(
            "/api/v1/ingredientes",
            json={"nombre": "Harina", "descripcion": "Harina de trigo", "es_alergeno": True},
            headers=headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Harina"
        assert data["descripcion"] == "Harina de trigo"
        assert data["es_alergeno"] is True
        assert "id" in data
        assert "creado_en" in data

    async def test_list_ingredientes(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        await client.post(
            "/api/v1/ingredientes", json={"nombre": "Sal"}, headers=headers,
        )
        await client.post(
            "/api/v1/ingredientes", json={"nombre": "Pimienta"}, headers=headers,
        )
        response = await client.get("/api/v1/ingredientes")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2

    async def test_list_filter_by_allergen(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        await client.post(
            "/api/v1/ingredientes",
            json={"nombre": "Leche", "es_alergeno": True},
            headers=headers,
        )
        await client.post(
            "/api/v1/ingredientes",
            json={"nombre": "Agua", "es_alergeno": False},
            headers=headers,
        )
        response = await client.get("/api/v1/ingredientes?es_alergeno=true")
        assert response.status_code == 200
        data = response.json()
        assert all(item["es_alergeno"] is True for item in data)

    async def test_get_by_id(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        create_resp = await client.post(
            "/api/v1/ingredientes", json={"nombre": "Azúcar"}, headers=headers,
        )
        ing_id = create_resp.json()["id"]
        response = await client.get(f"/api/v1/ingredientes/{ing_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == ing_id
        assert data["nombre"] == "Azúcar"

    async def test_get_by_id_not_found(self, client: AsyncClient, session: AsyncSession):
        response = await client.get("/api/v1/ingredientes/9999")
        assert response.status_code == 404

    async def test_update_ingrediente(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        create_resp = await client.post(
            "/api/v1/ingredientes", json={"nombre": "Pan"}, headers=headers,
        )
        ing_id = create_resp.json()["id"]
        response = await client.put(
            f"/api/v1/ingredientes/{ing_id}",
            json={"nombre": "Pan integral", "descripcion": "Harina integral"},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Pan integral"
        assert data["descripcion"] == "Harina integral"

    async def test_delete_ingrediente(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        create_resp = await client.post(
            "/api/v1/ingredientes", json={"nombre": "Manteca"}, headers=headers,
        )
        ing_id = create_resp.json()["id"]
        response = await client.delete(f"/api/v1/ingredientes/{ing_id}", headers=headers)
        assert response.status_code == 204
        get_resp = await client.get(f"/api/v1/ingredientes/{ing_id}")
        assert get_resp.status_code == 404

    async def test_create_duplicate_name(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        await client.post(
            "/api/v1/ingredientes", json={"nombre": "Queso"}, headers=headers,
        )
        response = await client.post(
            "/api/v1/ingredientes", json={"nombre": "Queso"}, headers=headers,
        )
        assert response.status_code == 409

    async def test_update_duplicate_name(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        await client.post(
            "/api/v1/ingredientes", json={"nombre": "Tomate"}, headers=headers,
        )
        create_resp = await client.post(
            "/api/v1/ingredientes", json={"nombre": "Cebolla"}, headers=headers,
        )
        ing_id = create_resp.json()["id"]
        response = await client.put(
            f"/api/v1/ingredientes/{ing_id}",
            json={"nombre": "Tomate"},
            headers=headers,
        )
        assert response.status_code == 409

    async def test_unauthorized_create(self, client: AsyncClient, session: AsyncSession):
        response = await client.post(
            "/api/v1/ingredientes",
            json={"nombre": "Huevo"},
        )
        assert response.status_code == 401
