"""
Admin routes for dashboard statistics.
"""
from fastapi import APIRouter, Depends, Query

from backend.admin.schemas.stats import (
    AdminStatsResponse,
    ProductsStatsResponse,
)
from backend.admin.services.admin_stats_service import AdminStatsService
from backend.core.dependencies import DatabaseSession, RoleRequired
from backend.core.uow import UnitOfWork

router = APIRouter(prefix="/admin/stats", tags=["Admin Stats"])
service = AdminStatsService()


@router.get("", response_model=AdminStatsResponse)
async def get_stats(
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN"])),
):
    """Get main KPIs for the dashboard."""
    async with UnitOfWork(session) as uow:
        stats = await service.get_stats(uow)
    return stats


@router.get("/revenue")
async def get_revenue(
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN"])),
    periodo: str = Query("day", pattern="^(day|week|month)$"),
):
    """Get revenue aggregated by period."""
    async with UnitOfWork(session) as uow:
        revenue = await service.get_revenue(uow, periodo)
    return revenue


@router.get("/orders")
async def get_orders_by_status(
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN"])),
):
    """Get order counts grouped by status."""
    async with UnitOfWork(session) as uow:
        orders = await service.get_orders_by_status(uow)
    return orders


@router.get("/products", response_model=ProductsStatsResponse)
async def get_products_stats(
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN"])),
):
    """Get low stock products and best sellers."""
    async with UnitOfWork(session) as uow:
        stats = await service.get_products_stats(uow)
    return stats
