import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.categorias.models.categoria import Categoria
from backend.ingredientes.models.ingrediente import Ingrediente

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


async def get_client_token(client: AsyncClient, session: AsyncSession) -> str:
    await seed_roles(session)
    await create_user(session, "client@test.com", roles=["CLIENT"])
    response = await client.post("/api/v1/auth/login", json={
        "email": "client@test.com",
        "password": "password123",
    })
    return response.json()["access_token"]


async def auth_headers(client: AsyncClient, session: AsyncSession) -> dict:
    token = await get_stock_token(client, session)
    return {"Authorization": f"Bearer {token}"}


async def create_categoria(session: AsyncSession, nombre: str = "Bebidas") -> int:
    cat = Categoria(nombre=nombre)
    session.add(cat)
    await session.flush()
    await session.refresh(cat)
    return cat.id


async def create_ingrediente(session: AsyncSession, nombre: str = "Azucar") -> int:
    ing = Ingrediente(nombre=nombre)
    session.add(ing)
    await session.flush()
    await session.refresh(ing)
    return ing.id


class TestProductos:

    async def test_create_producto_with_relations(
        self, client: AsyncClient, session: AsyncSession
    ):
        headers = await auth_headers(client, session)
        cat_id = await create_categoria(session)
        ing_id = await create_ingrediente(session)

        response = await client.post(
            "/api/v1/productos",
            json={
                "nombre": "Coca Cola",
                "precio": 1500.00,
                "stock_cantidad": 10,
                "categoria_ids": [cat_id],
                "ingrediente_ids": [ing_id],
            },
            headers=headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Coca Cola"
        assert data["precio"] == 1500.0
        assert data["stock_cantidad"] == 10
        assert data["disponible"] is True
        assert len(data["categorias"]) == 1
        assert data["categorias"][0]["nombre"] == "Bebidas"
        assert len(data["ingredientes"]) == 1
        assert data["ingredientes"][0]["nombre"] == "Azucar"

    async def test_create_producto_without_relations(
        self, client: AsyncClient, session: AsyncSession
    ):
        headers = await auth_headers(client, session)
        response = await client.post(
            "/api/v1/productos",
            json={
                "nombre": "Pan",
                "precio": 500.00,
                "stock_cantidad": 20,
            },
            headers=headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Pan"
        assert data["precio"] == 500.0
        assert data["categorias"] == []
        assert data["ingredientes"] == []

    async def test_list_public(self, client: AsyncClient, session: AsyncSession):
        headers = await auth_headers(client, session)
        await client.post(
            "/api/v1/productos",
            json={"nombre": "Coca Cola", "precio": 1500.00, "stock_cantidad": 10},
            headers=headers,
        )
        await client.post(
            "/api/v1/productos",
            json={"nombre": "Pan", "precio": 500.00, "stock_cantidad": 20},
            headers=headers,
        )

        response = await client.get("/api/v1/productos")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    async def test_list_public_filtered_by_categoria(
        self, client: AsyncClient, session: AsyncSession
    ):
        headers = await auth_headers(client, session)
        cat_bebidas = await create_categoria(session, "Bebidas")
        cat_comidas = await create_categoria(session, "Comidas")

        await client.post(
            "/api/v1/productos",
            json={
                "nombre": "Coca Cola",
                "precio": 1500.00,
                "stock_cantidad": 10,
                "categoria_ids": [cat_bebidas],
            },
            headers=headers,
        )
        await client.post(
            "/api/v1/productos",
            json={
                "nombre": "Pan",
                "precio": 500.00,
                "stock_cantidad": 20,
                "categoria_ids": [cat_comidas],
            },
            headers=headers,
        )

        response = await client.get(
            f"/api/v1/productos?categoria_id={cat_bebidas}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["nombre"] == "Coca Cola"

    async def test_get_product_detail(
        self, client: AsyncClient, session: AsyncSession
    ):
        headers = await auth_headers(client, session)
        cat_id = await create_categoria(session)
        ing_id = await create_ingrediente(session)

        create_resp = await client.post(
            "/api/v1/productos",
            json={
                "nombre": "Coca Cola",
                "precio": 1500.00,
                "stock_cantidad": 10,
                "categoria_ids": [cat_id],
                "ingrediente_ids": [ing_id],
            },
            headers=headers,
        )
        prod_id = create_resp.json()["id"]

        response = await client.get(f"/api/v1/productos/{prod_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prod_id
        assert data["nombre"] == "Coca Cola"
        assert len(data["categorias"]) == 1
        assert data["categorias"][0]["nombre"] == "Bebidas"
        assert len(data["ingredientes"]) == 1
        assert data["ingredientes"][0]["nombre"] == "Azucar"

    async def test_get_product_not_found(
        self, client: AsyncClient, session: AsyncSession
    ):
        response = await client.get("/api/v1/productos/9999")
        assert response.status_code == 404

    async def test_update_producto(
        self, client: AsyncClient, session: AsyncSession
    ):
        headers = await auth_headers(client, session)
        create_resp = await client.post(
            "/api/v1/productos",
            json={"nombre": "Coca Cola", "precio": 1500.00, "stock_cantidad": 10},
            headers=headers,
        )
        prod_id = create_resp.json()["id"]

        response = await client.put(
            f"/api/v1/productos/{prod_id}",
            json={"nombre": "Coca Cola Zero", "precio": 1600.00},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Coca Cola Zero"
        assert data["precio"] == 1600.0

    async def test_update_producto_m2m(
        self, client: AsyncClient, session: AsyncSession
    ):
        headers = await auth_headers(client, session)
        cat1 = await create_categoria(session, "Bebidas")
        cat2 = await create_categoria(session, "Light")
        ing1 = await create_ingrediente(session, "Azucar")
        ing2 = await create_ingrediente(session, "Edulcorante")

        create_resp = await client.post(
            "/api/v1/productos",
            json={
                "nombre": "Coca Cola",
                "precio": 1500.00,
                "stock_cantidad": 10,
                "categoria_ids": [cat1],
                "ingrediente_ids": [ing1],
            },
            headers=headers,
        )
        prod_id = create_resp.json()["id"]

        response = await client.put(
            f"/api/v1/productos/{prod_id}",
            json={
                "categoria_ids": [cat1, cat2],
                "ingrediente_ids": [ing2],
            },
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["categorias"]) == 2
        cat_names = {c["nombre"] for c in data["categorias"]}
        assert cat_names == {"Bebidas", "Light"}
        assert len(data["ingredientes"]) == 1
        assert data["ingredientes"][0]["nombre"] == "Edulcorante"

    async def test_update_producto_not_found(
        self, client: AsyncClient, session: AsyncSession
    ):
        headers = await auth_headers(client, session)
        response = await client.put(
            "/api/v1/productos/9999",
            json={"nombre": "No Existe"},
            headers=headers,
        )
        assert response.status_code == 404

    async def test_delete_producto_soft_delete(
        self, client: AsyncClient, session: AsyncSession
    ):
        headers = await auth_headers(client, session)
        create_resp = await client.post(
            "/api/v1/productos",
            json={"nombre": "Coca Cola", "precio": 1500.00, "stock_cantidad": 10},
            headers=headers,
        )
        prod_id = create_resp.json()["id"]

        response = await client.delete(
            f"/api/v1/productos/{prod_id}", headers=headers
        )
        assert response.status_code == 204

        get_resp = await client.get(f"/api/v1/productos/{prod_id}")
        assert get_resp.status_code == 404

    async def test_admin_list_includes_non_disponible(
        self, client: AsyncClient, session: AsyncSession
    ):
        headers = await auth_headers(client, session)
        await client.post(
            "/api/v1/productos",
            json={
                "nombre": "Producto No Disponible",
                "precio": 100.00,
                "stock_cantidad": 0,
                "disponible": False,
            },
            headers=headers,
        )

        admin_resp = await client.get("/api/v1/productos/admin", headers=headers)
        assert admin_resp.status_code == 200
        admin_data = admin_resp.json()
        names = [i["nombre"] for i in admin_data["items"]]
        assert "Producto No Disponible" in names

    async def test_public_list_excludes_non_disponible(
        self, client: AsyncClient, session: AsyncSession
    ):
        headers = await auth_headers(client, session)
        await client.post(
            "/api/v1/productos",
            json={
                "nombre": "Visible",
                "precio": 100.00,
                "stock_cantidad": 10,
                "disponible": True,
            },
            headers=headers,
        )
        await client.post(
            "/api/v1/productos",
            json={
                "nombre": "No Visible",
                "precio": 200.00,
                "stock_cantidad": 0,
                "disponible": False,
            },
            headers=headers,
        )

        response = await client.get("/api/v1/productos")
        assert response.status_code == 200
        data = response.json()
        names = [i["nombre"] for i in data["items"]]
        assert "Visible" in names
        assert "No Visible" not in names
        assert data["total"] == 1

    async def test_public_list_excludes_soft_deleted(
        self, client: AsyncClient, session: AsyncSession
    ):
        headers = await auth_headers(client, session)
        create_resp = await client.post(
            "/api/v1/productos",
            json={"nombre": "Delete Me", "precio": 100.00, "stock_cantidad": 10},
            headers=headers,
        )
        prod_id = create_resp.json()["id"]
        await client.delete(f"/api/v1/productos/{prod_id}", headers=headers)

        await client.post(
            "/api/v1/productos",
            json={"nombre": "Keep Me", "precio": 200.00, "stock_cantidad": 10},
            headers=headers,
        )

        response = await client.get("/api/v1/productos")
        assert response.status_code == 200
        data = response.json()
        names = [i["nombre"] for i in data["items"]]
        assert "Delete Me" not in names
        assert "Keep Me" in names
        assert data["total"] == 1

    async def test_unauthorized_create_returns_401(
        self, client: AsyncClient, session: AsyncSession
    ):
        response = await client.post(
            "/api/v1/productos",
            json={"nombre": "Coca Cola", "precio": 1500.00, "stock_cantidad": 10},
        )
        assert response.status_code == 401

    async def test_non_stock_create_returns_403(
        self, client: AsyncClient, session: AsyncSession
    ):
        token = await get_client_token(client, session)
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.post(
            "/api/v1/productos",
            json={"nombre": "Coca Cola", "precio": 1500.00, "stock_cantidad": 10},
            headers=headers,
        )
        assert response.status_code == 403
