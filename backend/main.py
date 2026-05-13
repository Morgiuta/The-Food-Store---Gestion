"""
FastAPI application entry point for The Food Store.
Configures middleware, routers, and startup/shutdown events.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from backend.api.v1.routes import health
from backend.auth.routes import auth as auth_routes
from backend.auth.routes import roles as roles_routes
from backend.categorias.routes import categorias as categorias_routes
from backend.ingredientes.routes import ingredientes as ingredientes_routes
from backend.productos.routes import productos as productos_routes
from backend.usuarios.routes import admin_usuarios
from backend.usuarios.routes import perfil
from backend.direcciones.routes import direcciones as direcciones_routes
from backend.pedidos.routes import checkout as checkout_routes
from backend.pedidos.routes import pedidos as pedidos_routes
from backend.admin.routes import pagos as admin_pagos_routes
from backend.admin.routes import stats as admin_stats_routes
from backend.pagos.routes import pagos as pagos_routes
from backend.core.config import get_settings
from backend.core.database import engine, Base
from backend.core.rate_limit import limiter
from backend.middleware.error_handler import register_error_handlers
from backend.middleware.logging import LoggingMiddleware

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan: startup and shutdown events.
    """
    # Startup: create all tables from ORM models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Shutdown: dispose the database engine
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ─── Middleware Stack ─────────────────────────────────────────────────────────

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response logging
app.add_middleware(LoggingMiddleware)

# ─── Error Handlers ──────────────────────────────────────────────────────────

register_error_handlers(app)

# Rate limit error handler
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

# Rate limiter instance (shared across all routes)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# ─── Routers ─────────────────────────────────────────────────────────────────

app.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(auth_routes.router, prefix=settings.API_V1_STR)
app.include_router(roles_routes.router, prefix=settings.API_V1_STR)
app.include_router(categorias_routes.router, prefix=settings.API_V1_STR)
app.include_router(ingredientes_routes.router, prefix=settings.API_V1_STR)
app.include_router(productos_routes, prefix=settings.API_V1_STR)
app.include_router(admin_usuarios.router, prefix=settings.API_V1_STR)
app.include_router(perfil.router, prefix=settings.API_V1_STR)
app.include_router(direcciones_routes.router, prefix=settings.API_V1_STR)
app.include_router(checkout_routes.router, prefix=settings.API_V1_STR)
app.include_router(pedidos_routes.router, prefix=settings.API_V1_STR)
app.include_router(admin_pagos_routes.router, prefix=settings.API_V1_STR)
app.include_router(admin_stats_routes.router, prefix=settings.API_V1_STR)
app.include_router(pagos_routes.router, prefix=settings.API_V1_STR)
