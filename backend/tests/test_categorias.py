import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.productos.models.producto import Producto
from backend.productos.models.producto_categoria import ProductoCategoria

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


class TestCategorias:

    async def test_get_tree_empty(self, client: AsyncClient, session: AsyncSession):
        response = await client.get("/api/v1/categorias")
        assert response.status_code == 200
        assert response.json() == []

    async def test_create_root_categoria(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        response = await client.post(
            "/api/v1/categorias",
            json={"nombre": "Bebidas"},
            headers=headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Bebidas"
        assert data["padre_id"] is None
        assert "id" in data

    async def test_create_subcategoria(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        parent_resp = await client.post(
            "/api/v1/categorias",
            json={"nombre": "Bebidas"},
            headers=headers,
        )
        assert parent_resp.status_code == 201
        parent_id = parent_resp.json()["id"]

        child_resp = await client.post(
            "/api/v1/categorias",
            json={"nombre": "Gaseosas", "padre_id": parent_id},
            headers=headers,
        )
        assert child_resp.status_code == 201
        child_data = child_resp.json()
        assert child_data["nombre"] == "Gaseosas"
        assert child_data["padre_id"] == parent_id

    async def test_get_tree_returns_hierarchy(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        p1 = await client.post(
            "/api/v1/categorias", json={"nombre": "Bebidas"}, headers=headers,
        )
        p1_id = p1.json()["id"]
        p2 = await client.post(
            "/api/v1/categorias", json={"nombre": "Comidas"}, headers=headers,
        )
        p2_id = p2.json()["id"]

        await client.post(
            "/api/v1/categorias",
            json={"nombre": "Gaseosas", "padre_id": p1_id},
            headers=headers,
        )
        await client.post(
            "/api/v1/categorias",
            json={"nombre": "Jugos", "padre_id": p1_id},
            headers=headers,
        )

        response = await client.get("/api/v1/categorias")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        bebidas = next(c for c in data if c["nombre"] == "Bebidas")
        assert len(bebidas["subcategorias"]) == 2
        nombres_sub = {s["nombre"] for s in bebidas["subcategorias"]}
        assert nombres_sub == {"Gaseosas", "Jugos"}

        comidas = next(c for c in data if c["nombre"] == "Comidas")
        assert len(comidas["subcategorias"]) == 0

    async def test_get_by_id(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        create_resp = await client.post(
            "/api/v1/categorias", json={"nombre": "Bebidas"}, headers=headers,
        )
        cat_id = create_resp.json()["id"]

        response = await client.get(f"/api/v1/categorias/{cat_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == cat_id
        assert data["nombre"] == "Bebidas"

    async def test_get_by_id_not_found(self, client: AsyncClient, session: AsyncSession):
        response = await client.get("/api/v1/categorias/9999")
        assert response.status_code == 404

    async def test_update_categoria(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        create_resp = await client.post(
            "/api/v1/categorias", json={"nombre": "Bebidas"}, headers=headers,
        )
        cat_id = create_resp.json()["id"]

        response = await client.put(
            f"/api/v1/categorias/{cat_id}",
            json={"nombre": "Bebidas y Licores"},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Bebidas y Licores"
        assert data["id"] == cat_id

    async def test_update_self_parent(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        create_resp = await client.post(
            "/api/v1/categorias", json={"nombre": "Bebidas"}, headers=headers,
        )
        cat_id = create_resp.json()["id"]

        response = await client.put(
            f"/api/v1/categorias/{cat_id}",
            json={"padre_id": cat_id},
            headers=headers,
        )
        assert response.status_code == 409

    async def test_update_cycle(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        p1 = await client.post(
            "/api/v1/categorias", json={"nombre": "Padre"}, headers=headers,
        )
        p1_id = p1.json()["id"]
        c1 = await client.post(
            "/api/v1/categorias",
            json={"nombre": "Hijo", "padre_id": p1_id},
            headers=headers,
        )
        c1_id = c1.json()["id"]

        response = await client.put(
            f"/api/v1/categorias/{p1_id}",
            json={"padre_id": c1_id},
            headers=headers,
        )
        assert response.status_code == 409

    async def test_delete_without_products(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        create_resp = await client.post(
            "/api/v1/categorias", json={"nombre": "Bebidas"}, headers=headers,
        )
        cat_id = create_resp.json()["id"]

        response = await client.delete(f"/api/v1/categorias/{cat_id}", headers=headers)
        assert response.status_code == 204

    async def test_delete_with_products(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_header(client, session)
        cat_resp = await client.post(
            "/api/v1/categorias", json={"nombre": "Bebidas"}, headers=headers,
        )
        cat_id = cat_resp.json()["id"]

        producto = Producto(
            nombre="Coca Cola",
            precio=1500.00,
            stock_cantidad=10,
            disponible=True,
        )
        session.add(producto)
        await session.flush()
        await session.refresh(producto)

        pc = ProductoCategoria(producto_id=producto.id, categoria_id=cat_id)
        session.add(pc)
        await session.flush()

        response = await client.delete(f"/api/v1/categorias/{cat_id}", headers=headers)
        assert response.status_code == 409
        data = response.json()
        assert "productos" in data["detail"].lower()

    async def test_create_unauthorized(self, client: AsyncClient, session: AsyncSession):
        response = await client.post(
            "/api/v1/categorias",
            json={"nombre": "Bebidas"},
        )
        assert response.status_code == 401
