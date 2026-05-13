## Why

El usuario ya puede navegar el catálogo, agregar productos al carrito, gestionar direcciones y validar stock desde el checkout preview. Sin embargo, aún **no puede confirmar un pedido**. No existe un endpoint que tome los items validados del checkout, cree el pedido con snapshots de precios y dirección, registre el historial inicial y descuente stock atómicamente. Sin esta funcionalidad, el flujo de compra está incompleto.

## What Changes

- Nuevo endpoint `POST /api/v1/pedidos` para crear pedidos de forma atómica
- Nuevo endpoint `GET /api/v1/pedidos` para listar pedidos del usuario autenticado
- Nuevo endpoint `GET /api/v1/pedidos/{id}` para ver detalle de un pedido
- Nuevo endpoint `GET /api/v1/pedidos/admin` para que ADMIN/PEDIDOS listen todos los pedidos
- Servicio de creación de pedidos con Unit of Work (transacción atómica)
- Generación de snapshots de precio por producto y dirección de entrega al crear el pedido
- Validación de stock suficiente dentro de la transacción (SELECT FOR UPDATE)
- Registro inicial en HistorialEstadoPedido (append-only, estado_desde=NULL)
- Frontend: OrderConfirmationPage, OrderListPage, OrderCard, OrderDetailModal
- Frontend: useOrders hook para conectar con los nuevos endpoints

## Capabilities

### New Capabilities
- `pedido-creation`: Creación atómica de pedidos con validación de stock, snapshots de precio y dirección, y registro de historial inicial. Incluye endpoints para crear, listar (propios y admin) y ver detalle.
- `pedido-list-client`: Listado de pedidos del cliente autenticado con paginación y detalle.
- `pedido-list-admin`: Listado global de pedidos para roles ADMIN y PEDIDOS con filtros.

### Modified Capabilities
- *(ninguna — es funcionalidad completamente nueva)*

## Impact

- **Backend**: Nuevo servicio `PedidoService` con lógica de creación atómica via UoW. Nuevos endpoints en `pedidos/routes/pedidos.py`. Los modelos, repositorios y schemas ya existen parcialmente (creados en sprints anteriores) pero se completarán según necesidad.
- **Frontend**: Nuevos componentes de visualización de pedidos (OrderConfirmationPage, OrderListPage, OrderCard, OrderDetailModal). Nuevo hook `useOrders`.
- **Base de datos**: Las tablas `pedidos`, `detalles_pedido`, `historial_estados_pedido` ya existen por migraciones previas. No se requieren nuevas migraciones.
- **Dependencias**: Depende de `sprint-3-checkout-preview` y `sprint-3-direcciones-entrega` (ya archivados).
