from datetime import datetime, timezone

import pytest

from backend.auth.models.direccion import DireccionEntrega
from backend.auth.models.refresh_token import RefreshToken
from backend.auth.models.rol import Rol
from backend.auth.models.usuario import Usuario
from backend.auth.models.usuario_rol import UsuarioRol
from backend.categorias.models.categoria import Categoria
from backend.ingredientes.models.ingrediente import Ingrediente
from backend.pagos.models.forma_pago import FormaPago
from backend.pagos.models.pago import Pago
from backend.pedidos.models.detalle_pedido import DetallePedido
from backend.pedidos.models.estado_pedido import EstadoPedido
from backend.pedidos.models.historial_estado import HistorialEstadoPedido
from backend.pedidos.models.pedido import Pedido
from backend.productos.models.producto import Producto
from backend.productos.models.producto_categoria import ProductoCategoria
from backend.productos.models.producto_ingrediente import ProductoIngrediente


class TestModelInstantiation:
    def test_usuario_required_fields(self):
        user = Usuario(
            nombre="Test User",
            email="user@test.com",
            password_hash="hashed_password",
        )
        assert user.nombre == "Test User"
        assert user.email == "user@test.com"
        assert user.password_hash == "hashed_password"
        assert user.id is None

    def test_rol_required_fields(self):
        rol = Rol(nombre="ADMIN")
        assert rol.nombre == "ADMIN"

    def test_usuario_rol_required_fields(self):
        ur = UsuarioRol(usuario_id=1, rol_id=1)
        assert ur.usuario_id == 1
        assert ur.rol_id == 1

    def test_refresh_token_required_fields(self):
        rt = RefreshToken(
            token="some-token",
            usuario_id=1,
            expires_at=datetime.now(timezone.utc),
        )
        assert rt.token == "some-token"
        assert rt.usuario_id == 1

    def test_direccion_entrega_required_fields(self):
        direccion = DireccionEntrega(
            usuario_id=1,
            calle="Av. Siempre Viva",
            numero="742",
            ciudad="Springfield",
            codigo_postal="1234",
        )
        assert direccion.calle == "Av. Siempre Viva"
        assert direccion.ciudad == "Springfield"

    def test_producto_required_fields(self):
        prod = Producto(nombre="Pan Francés", precio=150.00)
        assert prod.nombre == "Pan Francés"
        assert prod.precio is not None

    def test_producto_categoria_required_fields(self):
        pc = ProductoCategoria(producto_id=1, categoria_id=1)
        assert pc.producto_id == 1
        assert pc.categoria_id == 1

    def test_producto_ingrediente_required_fields(self):
        pi = ProductoIngrediente(producto_id=1, ingrediente_id=1)
        assert pi.producto_id == 1
        assert pi.ingrediente_id == 1

    def test_categoria_required_fields(self):
        cat = Categoria(nombre="Panadería")
        assert cat.nombre == "Panadería"

    def test_ingrediente_required_fields(self):
        ing = Ingrediente(nombre="Harina")
        assert ing.nombre == "Harina"

    def test_estado_pedido_required_fields(self):
        estado = EstadoPedido(nombre="PENDIENTE")
        assert estado.nombre == "PENDIENTE"

    def test_forma_pago_required_fields(self):
        fp = FormaPago(nombre="Efectivo")
        assert fp.nombre == "Efectivo"

    def test_pedido_required_fields(self):
        pedido = Pedido(usuario_id=1, estado_id=1, total=250.00)
        assert pedido.usuario_id == 1
        assert pedido.total is not None

    def test_detalle_pedido_required_fields(self):
        detalle = DetallePedido(
            pedido_id=1,
            cantidad=2,
            precio_snapshot=100.00,
            subtotal=200.00,
        )
        assert detalle.pedido_id == 1
        assert detalle.cantidad == 2

    def test_historial_estado_required_fields(self):
        historial = HistorialEstadoPedido(
            pedido_id=1,
            estado_nuevo_id=1,
        )
        assert historial.pedido_id == 1
        assert historial.estado_nuevo_id == 1

    def test_pago_required_fields(self):
        pago = Pago(pedido_id=1, monto=500.00)
        assert pago.pedido_id == 1
        assert pago.monto is not None


class TestModelRelationships:
    async def test_usuario_to_rol_via_usuario_rol(self, session):
        user = Usuario(
            nombre="Rel User",
            email="reluser@test.com",
            password_hash="hash123",
        )
        session.add(user)
        await session.flush()

        rol = Rol(nombre="TEST_ROLE")
        session.add(rol)
        await session.flush()

        ur = UsuarioRol(usuario_id=user.id, rol_id=rol.id)
        session.add(ur)
        await session.flush()

        await session.refresh(user)
        assert len(user.roles) == 1
        assert user.roles[0].rol_id == rol.id
        assert user.roles[0].usuario_id == user.id

    async def test_rol_to_usuario_via_usuario_rol(self, session):
        user = Usuario(
            nombre="Rol Rel",
            email="rolrel@test.com",
            password_hash="hash123",
        )
        session.add(user)
        await session.flush()

        rol = Rol(nombre="TEST_ROLE_REVERSE")
        session.add(rol)
        await session.flush()

        ur = UsuarioRol(usuario_id=user.id, rol_id=rol.id)
        session.add(ur)
        await session.flush()

        await session.refresh(rol)
        assert len(rol.usuarios) == 1
        assert rol.usuarios[0].usuario_id == user.id

    async def test_usuario_to_direccion(self, session):
        user = Usuario(
            nombre="Dir User",
            email="diruser@test.com",
            password_hash="hash123",
        )
        session.add(user)
        await session.flush()

        direccion = DireccionEntrega(
            usuario_id=user.id,
            calle="Calle Falsa",
            numero="123",
            ciudad="Buenos Aires",
            codigo_postal="1000",
        )
        session.add(direccion)
        await session.flush()

        await session.refresh(user)
        assert len(user.direcciones) == 1
        assert user.direcciones[0].calle == "Calle Falsa"


class TestSoftDeleteModels:
    SOFT_DELETE_MODELS = [
        (Usuario, {"nombre": "SD", "email": "sd@test.com", "password_hash": "h"}),
        (DireccionEntrega, {"usuario_id": 1, "calle": "Calle", "numero": "1", "ciudad": "C", "codigo_postal": "P"}),
        (Producto, {"nombre": "SD Prod", "precio": 100}),
        (Categoria, {"nombre": "SD Cat"}),
        (Ingrediente, {"nombre": "SD Ing"}),
        (Pedido, {"usuario_id": 1, "estado_id": 1, "total": 100}),
    ]

    NON_SOFT_DELETE_MODELS = [
        Rol, UsuarioRol, RefreshToken, EstadoPedido,
        DetallePedido, HistorialEstadoPedido, Pago, FormaPago,
        ProductoCategoria, ProductoIngrediente,
    ]

    def test_soft_delete_models_have_eliminado_en(self):
        for model_cls, kwargs in self.SOFT_DELETE_MODELS:
            instance = model_cls(**kwargs)
            assert hasattr(instance, "eliminado_en"), (
                f"{model_cls.__name__} should have eliminado_en"
            )
            assert instance.eliminado_en is None

    def test_non_soft_delete_models_lack_eliminado_en(self):
        for model_cls in self.NON_SOFT_DELETE_MODELS:
            assert not hasattr(model_cls, "eliminado_en"), (
                f"{model_cls.__name__} should not have eliminado_en"
            )
