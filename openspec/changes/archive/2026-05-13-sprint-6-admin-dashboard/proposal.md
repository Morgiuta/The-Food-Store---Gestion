## Why

El panel de administración actual tiene un placeholder en el dashboard y links a secciones, pero **no muestra ninguna métrica ni KPI**. El admin no puede ver ingresos, cantidad de pedidos, usuarios activos o productos con stock bajo sin consultar directamente la base de datos.

## What Changes

- Endpoint `GET /api/v1/admin/stats` con KPIs: total ventas, pedidos hoy, usuarios activos, stock bajo
- Endpoint `GET /api/v1/admin/stats/revenue` con ingresos por período (día, semana, mes)
- Endpoint `GET /api/v1/admin/stats/orders` con pedidos por estado
- Endpoint `GET /api/v1/admin/stats/products` con productos de bajo stock y más vendidos
- Frontend: AdminDashboard con StatsCards, RevenueChart, OrdersChart, LowStockAlert, TopProductsList
- useAdminStats hook con TanStack Query

## Capabilities

### New Capabilities
- `admin-dashboard-metrics`: Dashboard administrativo con KPIs en tiempo real, gráficos de ingresos (recharts), distribución de pedidos por estado, alertas de stock bajo y top productos.

### Modified Capabilities
- *(ninguna)*

## Impact

- **Backend**: Nuevo `AdminStatsService` y router `admin/routes/stats.py`.
- **Frontend**: Nuevos componentes de dashboard con recharts. Reemplaza placeholder actual en `/admin/dashboard`.
- **Dependencias**: recharts ya está en package.json. Depende de sprints anteriores (pedidos, productos, usuarios).
