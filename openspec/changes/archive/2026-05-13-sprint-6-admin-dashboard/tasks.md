# Tasks: sprint-6-admin-dashboard

## 1. Backend — Admin Stats Service

- [x] 1.1 Crear `backend/admin/services/admin_stats_service.py` con clase `AdminStatsService`
- [x] 1.2 Implementar `get_stats(uow)` con:
  - total_ventas: SUM de pedidos.total donde estado > PENDIENTE
  - pedidos_hoy: COUNT donde creado_en es hoy
  - usuarios_activos: COUNT usuarios no eliminados con rol CLIENT+
  - stock_bajo: COUNT productos con stock_cantidad < 5 y disponible=true
- [x] 1.3 Implementar `get_revenue(uow, periodo)` con agregación por día/semana/mes
- [x] 1.4 Implementar `get_orders_by_status(uow)` con COUNT y GROUP BY estado
- [x] 1.5 Implementar `get_products_stats(uow)` con productos stock bajo y más vendidos

## 2. Backend — Schemas

- [x] 2.1 Crear schemas en `backend/admin/schemas/stats.py`:
  - `AdminStatsResponse`, `RevenueEntry`, `OrderStatusCount`, `ProductsStatsResponse`

## 3. Backend — Routes

- [x] 3.1 Crear `backend/admin/routes/stats.py` con endpoints
- [x] 3.2 Registrar router en `backend/main.py`

## 4. Frontend — useAdminStats Hook

- [x] 4.1 Crear `frontend/src/features/admin/hooks/useAdminStats.ts`

## 5. Frontend — Dashboard Components

- [x] 5.1 Crear `StatsCards` con 4 KPIs (ventas totales, pedidos hoy, usuarios activos, stock bajo)
- [x] 5.2 Crear `RevenueChart` con selector de período y gráfico de barras (recharts)
- [x] 5.3 Crear `OrdersPieChart` con distribución de pedidos por estado
- [x] 5.4 Crear `LowStockAlerts` con tabla de productos con stock < 5
- [x] 5.5 Crear `TopProductsList` con tabla de productos más vendidos

## 6. Frontend — AdminDashboardPage

- [x] 6.1 Crear `frontend/src/pages/admin/dashboard-page.tsx` integrando todos los componentes
- [x] 6.2 Reemplazar placeholder en router admin

## 7. Backend — Tests

- [x] 7.1 Verificar tests existentes pasan
