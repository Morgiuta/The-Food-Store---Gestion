"""
Unit of Work pattern for managing atomic transactions.

The UoW encapsulates a database session and exposes repositories,
ensuring that multi-entity operations are atomic (all-or-nothing).
"""

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.repositories.refresh_token import RefreshTokenRepository
from backend.auth.repositories.rol import RolRepository
from backend.auth.repositories.usuario_rol import UsuarioRolRepository
from backend.categorias.repositories.categoria import CategoriaRepository
from backend.ingredientes.repositories.ingrediente import IngredienteRepository
from backend.admin.repositories.configuracion import ConfiguracionRepository
from backend.pagos.repositories.forma_pago import FormaPagoRepository
from backend.pagos.repositories.pago import PagoRepository
from backend.pedidos.repositories.detalle_pedido import DetallePedidoRepository
from backend.pedidos.repositories.historial_estado import HistorialEstadoPedidoRepository
from backend.pedidos.repositories.pedido import PedidoRepository
from backend.productos.repositories.producto import ProductoRepository
from backend.usuarios.repositories.usuario import UsuarioRepository


class UnitOfWork:
    """
    Unit of Work context manager for atomic database operations.

    Usage:
        async with UnitOfWork(session) as uow:
            user = await uow.usuarios.get_by_id(1)
            await uow.usuarios.update(1, {"nombre": "new name"})
            await uow.commit()
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the Unit of Work.

        Args:
            session: SQLAlchemy async session
        """
        self._session = session
        self._repositories: dict[str, object] = {}

        # Initialize all repositories
        self.usuarios: UsuarioRepository = self._get_or_create_repo(
            "usuarios", UsuarioRepository
        )
        self.roles: RolRepository = self._get_or_create_repo("roles", RolRepository)
        self.usuario_roles: UsuarioRolRepository = self._get_or_create_repo(
            "usuario_roles", UsuarioRolRepository
        )
        self.refresh_tokens: RefreshTokenRepository = self._get_or_create_repo(
            "refresh_tokens", RefreshTokenRepository
        )
        self.categorias: CategoriaRepository = self._get_or_create_repo(
            "categorias", CategoriaRepository
        )
        self.ingredientes: IngredienteRepository = self._get_or_create_repo(
            "ingredientes", IngredienteRepository
        )
        self.productos: ProductoRepository = self._get_or_create_repo(
            "productos", ProductoRepository
        )
        self.pedidos: PedidoRepository = self._get_or_create_repo(
            "pedidos", PedidoRepository
        )
        self.detalles_pedido: DetallePedidoRepository = self._get_or_create_repo(
            "detalles_pedido", DetallePedidoRepository
        )
        self.historial_estados: HistorialEstadoPedidoRepository = self._get_or_create_repo(
            "historial_estados", HistorialEstadoPedidoRepository
        )
        self.configuraciones: ConfiguracionRepository = self._get_or_create_repo(
            "configuraciones", ConfiguracionRepository
        )
        self.formas_pago: FormaPagoRepository = self._get_or_create_repo(
            "formas_pago", FormaPagoRepository
        )
        self.pagos: PagoRepository = self._get_or_create_repo("pagos", PagoRepository)

    def _get_or_create_repo(self, key: str, repo_class: type) -> object:
        """Get or create a repository instance."""
        if key not in self._repositories:
            self._repositories[key] = repo_class(self._session)
        return self._repositories[key]

    async def commit(self) -> None:
        """Commit the current transaction."""
        await self._session.commit()

    async def rollback(self) -> None:
        """Rollback the current transaction."""
        await self._session.rollback()

    async def __aenter__(self) -> "UnitOfWork":
        """Enter the async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object],
    ) -> None:
        """
        Exit the async context manager.
        Commits on success, rolls back on exception.
        """
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
