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

from backend.api.v1.routes import health
from backend.core.config import get_settings
from backend.core.database import engine, Base
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

# ─── Routers ─────────────────────────────────────────────────────────────────

app.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])
