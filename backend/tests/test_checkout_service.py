import pytest
import pytest_asyncio
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture(autouse=True)
async def disable_rate_limiting():
    from backend.auth.routes.auth import limiter as auth_limiter
    auth_limiter.enabled = False
    yield
    auth_limiter.enabled = True


async def create_test_producto(session: AsyncSession, nombre: str = "Test Product", stock: int = 10, precio: float = 100.0):
    from backend.productos.models.producto import Producto
    from backend.categorias.models.categoria import Categoria

    # Crear categoría si no existe
    categoria = Categoria(nombre="Test Category")
    session.add(categoria)
    await session.flush()

    producto = Producto(
        nombre=nombre,
        descripcion="Test description",
        precio=precio,
        stock_cantidad=stock,
        disponible=True,
        categoria_id=categoria.id,
    )
    session.add(producto)
    await session.flush()
    await session.refresh(producto)
    return producto


class TestCheckoutService:
    """Tests para CheckoutService"""

    async def test_validar_stock_sufficient(self, session: AsyncSession):
        """Verificar que la validación pasa con stock suficiente"""
        from backend.pedidos.services.checkout_service import CheckoutService

        producto = await create_test_producto(session, stock=10)

        service = CheckoutService()
        result = await service.validar_stock(session, [
            {"producto_id": producto.id, "cantidad": 5}
        ])

        assert result["valido"] is True
        assert len(result["errores"]) == 0

    async def test_validar_stock_insufficient(self, session: AsyncSession):
        """Verificar que la validación falla con stock insuficiente"""
        from backend.pedidos.services.checkout_service import CheckoutService

        producto = await create_test_producto(session, stock=3)

        service = CheckoutService()
        result = await service.validar_stock(session, [
            {"producto_id": producto.id, "cantidad": 5}
        ])

        assert result["valido"] is False
        assert len(result["errores"]) > 0
        assert "Stock insuficiente" in result["errores"][0]

    async def test_validar_stock_producto_no_existe(self, session: AsyncSession):
        """Verificar que falla si el producto no existe"""
        from backend.pedidos.services.checkout_service import CheckoutService

        service = CheckoutService()
        result = await service.validar_stock(session, [
            {"producto_id": 99999, "cantidad": 1}
        ])

        assert result["valido"] is False
        assert "no encontrado" in result["errores"][0]

    async def test_validar_stock_producto_no_disponible(self, session: AsyncSession):
        """Verificar que falla si el producto no está disponible"""
        from backend.pedidos.services.checkout_service import CheckoutService

        producto = await create_test_producto(session, disponible=False)

        service = CheckoutService()
        result = await service.validar_stock(session, [
            {"producto_id": producto.id, "cantidad": 1}
        ])

        assert result["valido"] is False
        assert "no disponible" in result["errores"][0]

    async def test_validar_stock_multiple_items(self, session: AsyncSession):
        """Verificar validación con múltiples items"""
        from backend.pedidos.services.checkout_service import CheckoutService

        prod1 = await create_test_producto(session, "Producto 1", stock=5)
        prod2 = await create_test_producto(session, "Producto 2", stock=10)

        service = CheckoutService()
        result = await service.validar_stock(session, [
            {"producto_id": prod1.id, "cantidad": 3},
            {"producto_id": prod2.id, "cantidad": 5},
        ])

        assert result["valido"] is True
        assert len(result["items_validados"]) == 2

    async def test_calcular_total_basic(self, session: AsyncSession):
        """Verificar cálculo de total"""
        from backend.pedidos.services.checkout_service import CheckoutService

        service = CheckoutService()
        items = [
            {"producto_id": 1, "cantidad": 2, "precio": 100.0},
            {"producto_id": 2, "cantidad": 1, "precio": 50.0},
        ]

        result = await service.calcular_total(items, direccion_id=1)

        # subtotal = (100*2) + (50*1) = 250
        # costo_envio = 500 (tarifa plana)
        # total = 250 + 500 = 750
        assert result["subtotal"] == 250.0
        assert result["costo_envio"] == 500.0
        assert result["total"] == 750.0

    async def test_calcular_total_empty_items(self, session: AsyncSession):
        """Verificar cálculo con items vacíos"""
        from backend.pedidos.services.checkout_service import CheckoutService

        service = CheckoutService()
        result = await service.calcular_total([], direccion_id=1)

        assert result["subtotal"] == 0.0
        assert result["costo_envio"] == 500.0
        assert result["total"] == 500.0