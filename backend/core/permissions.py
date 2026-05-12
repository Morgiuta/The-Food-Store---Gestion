"""Permission mappings: endpoint → allowed roles."""
from dataclasses import dataclass, field


@dataclass
class EndpointPermission:
    path: str
    methods: list[str]
    allowed_roles: list[str]
    public: bool = False
    owner_check: bool = False  # CLIENT only sees own data


# Permission matrix
PERMISSIONS = [
    # Public endpoints
    EndpointPermission("/auth/login", ["POST"], [], public=True),
    EndpointPermission("/auth/register", ["POST"], [], public=True),
    EndpointPermission("/auth/refresh", ["POST"], [], public=True),
    EndpointPermission("/health", ["GET"], [], public=True),
    EndpointPermission("/productos", ["GET"], [], public=True),
    # Auth required
    EndpointPermission("/auth/logout", ["POST"], ["CLIENT", "ADMIN", "STOCK", "PEDIDOS"]),
    EndpointPermission("/perfil", ["GET", "PUT"], ["CLIENT", "ADMIN", "STOCK", "PEDIDOS"]),
    EndpointPermission("/perfil/password", ["PUT"], ["CLIENT", "ADMIN", "STOCK", "PEDIDOS"]),
    # Admin only
    EndpointPermission("/admin", ["GET", "POST", "PUT", "PATCH", "DELETE"], ["ADMIN"]),
    # Stock + Admin
    EndpointPermission("/productos", ["POST", "PUT", "DELETE"], ["STOCK", "ADMIN"]),
    EndpointPermission("/categorias", ["POST", "PUT", "DELETE"], ["STOCK", "ADMIN"]),
    EndpointPermission("/ingredientes", ["POST", "PUT", "DELETE"], ["STOCK", "ADMIN"]),
    # Pedidos + Admin
    EndpointPermission("/pedidos", ["GET"], ["CLIENT", "PEDIDOS", "ADMIN"], owner_check=True),
    EndpointPermission("/pedidos", ["POST"], ["CLIENT"]),
]
