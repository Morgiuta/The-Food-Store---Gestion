## Context

Ya existe:
- Panel admin con layout y sidebar navegando a secciones
- Placeholder en `/admin/dashboard`
- `PedidoRepository.count_by_status()` para contar pedidos por estado
- `BaseRepository.count()` genérico
- Modelos: Pedido, Producto, Usuario, Pago
- `recharts` en package.json

## Goals / Non-Goals

**Goals:**
- 4 endpoints de estadísticas para el dashboard
- Frontend: KPIs, gráfico de ingresos, distribución de pedidos, stock bajo, top productos
- Reemplazar placeholder del dashboard

**Non-Goals:**
- Caché de estadísticas (se puede agregar después)
- Exportación de datos
- Configuración global (será sprint-6-admin-configuracion)

## Decisions

### 1. Endpoints separados por métrica
**Decisión**: Endpoints separados para cada tipo de métrica: /stats, /stats/revenue, /stats/orders, /stats/products.

**Rationale**: Cada métrica tiene diferente frecuencia de consulta. Separar permite caching granular y evita queries pesadas innecesarias.

### 2. Queries directas con SQLAlchemy
**Decisión**: Usar SQLAlchemy `select(func.count())`, `func.sum()` y `func.date_trunc()` para agregaciones.

**Rationale**: Los repositorios existentes ya tienen lo básico. Para agregaciones específicas se usan queries directas en el servicio.

### 3. Recharts para gráficos
**Decisión**: Usar `recharts` (ya instalado) con componentes `BarChart`, `LineChart`, `PieChart`.

**Rationale**: Librería ya en el proyecto, componentes declarativos, buena integración con React.

## API Changes

### `GET /api/v1/admin/stats` (ADMIN)
- **Response**: `AdminStatsResponse` con:
  - `total_ventas: Decimal` (suma de totales de pedidos CONFIRMADO+)
  - `pedidos_hoy: int`
  - `usuarios_activos: int`
  - `stock_bajo: int` (productos con stock < 5)

### `GET /api/v1/admin/stats/revenue` (ADMIN)
- **Query params**: periodo (day|week|month)
- **Response**: list[{ fecha, ingresos }]

### `GET /api/v1/admin/stats/orders` (ADMIN)
- **Response**: list[{ estado, cantidad }]

### `GET /api/v1/admin/stats/products` (ADMIN)
- **Response**: `{ stock_bajo: list[{id, nombre, stock}], mas_vendidos: list[{id, nombre, total_vendido}] }`

## Frontend Components

```
AdminDashboardPage (pages/admin/dashboard-page.tsx)
├── StatsCards (4 KPIs en tarjetas)
├── RevenueChart (gráfico de ingresos con selector de período)
├── OrdersPieChart (distribución de pedidos por estado)
├── LowStockAlerts (tabla de productos con stock bajo)
└── TopProductsList (tabla de productos más vendidos)
```
