import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture(autouse=True)
async def disable_rate_limiting():
    from backend.auth.routes.auth import limiter as auth_limiter
    auth_limiter.enabled = False
    yield
    auth_limiter.enabled = True


class TestCheckoutAPI:
    """Tests de integración para endpoints de checkout"""

    async def test_validar_stock_requires_auth(self, client: AsyncClient):
        """Verificar que validar stock requiere autenticación"""
        response = await client.post(
            "/api/v1/pedidos/validar",
            json={"items": [{"producto_id": 1, "cantidad": 1}]},
        )
        assert response.status_code == 401

    async def test_validar_stock_returns_validation_result(self, client: AsyncClient, session: AsyncSession):
        """Verificar que validar stock retorna resultado"""
        from backend.auth.models.usuario import Usuario
        from backend.auth.models.rol import Rol
        from backend.auth.models.usuario_rol import UsuarioRol
        from backend.productos.models.producto import Producto
        from backend.categorias.models.categoria import Categoria
        from backend.core.security import get_password_hash, create_access_token

        # Crear usuario
        user = Usuario(
            nombre="Test",
            email="checkouttest@test.com",
            password_hash=get_password_hash("password123"),
            telefono="1234567890",
        )
        session.add(user)
        # Crear rol CLIENT
        rol = Rol(nombre="CLIENT")
        session.add(rol)
        await session.flush()
        session.add(UsuarioRol(usuario_id=user.id, rol_id=rol.id))

        # Crear producto
        producto = Producto(
            nombre="Test Product",
            descripcion="Test",
            precio=100.0,
            stock_cantidad=10,
            disponible=True,
        )
        session.add(producto)
        await session.commit()

        token = create_access_token({"sub": str(user.id), "email": user.email, "roles": ["CLIENT"]})

        response = await client.post(
            "/api/v1/pedidos/validar",
            json={"items": [{"producto_id": producto.id, "cantidad": 5}]},
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "valido" in data
        assert "errores" in data
        assert "items_validados" in data

    async def test_validar_stock_with_insufficient_stock(self, client: AsyncClient, session: AsyncSession):
        """Verificar que retorna error cuando hay stock insuficiente"""
        from backend.auth.models.usuario import Usuario
        from backend.auth.models.rol import Rol
        from backend.auth.models.usuario_rol import UsuarioRol
        from backend.productos.models.producto import Producto
        from backend.categorias.models.categoria import Categoria
        from backend.core.security import get_password_hash, create_access_token

        user = Usuario(
            nombre="Test",
            email="stockerror@test.com",
            password_hash=get_password_hash("password123"),
            telefono="1234567890",
        )
        session.add(user)
        rol = Rol(nombre="CLIENT")
        session.add(rol)
        await session.flush()
        session.add(UsuarioRol(usuario_id=user.id, rol_id=rol.id))

        producto = Producto(
            nombre="Low Stock",
            descripcion="Test",
            precio=100.0,
            stock_cantidad=2,
            disponible=True,
        )
        session.add(producto)
        await session.commit()

        token = create_access_token({"sub": str(user.id), "email": user.email, "roles": ["CLIENT"]})

        response = await client.post(
            "/api/v1/pedidos/validar",
            json={"items": [{"producto_id": producto.id, "cantidad": 10}]},
            headers={"Authorization": f"Bearer {token}"},
        )

        data = response.json()
        assert data["valido"] is False
        assert len(data["errores"]) > 0

    async def test_calcular_total_returns_totals(self, client: AsyncClient, session: AsyncSession):
        """Verificar que calcular total retorna los totales"""
        from backend.auth.models.usuario import Usuario
        from backend.auth.models.rol import Rol
        from backend.auth.models.usuario_rol import UsuarioRol
        from backend.core.security import get_password_hash, create_access_token

        user = Usuario(
            nombre="Test",
            email="calctotal@test.com",
            password_hash=get_password_hash("password123"),
            telefono="1234567890",
        )
        session.add(user)
        rol = Rol(nombre="CLIENT")
        session.add(rol)
        await session.flush()
        session.add(UsuarioRol(usuario_id=user.id, rol_id=rol.id))
        await session.commit()

        token = create_access_token({"sub": str(user.id), "email": user.email, "roles": ["CLIENT"]})

        response = await client.post(
            "/api/v1/pedidos/calcular-total",
            json={
                "items": [
                    {"producto_id": 1, "cantidad": 2},
                    {"producto_id": 2, "cantidad": 1},
                ],
                "direccion_id": 1,
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "subtotal" in data
        assert "costo_envio" in data
        assert "total" in data
        assert "direccion_id" in data