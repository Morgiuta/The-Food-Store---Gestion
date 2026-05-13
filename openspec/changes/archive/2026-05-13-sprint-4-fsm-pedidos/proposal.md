## Why

Actualmente los pedidos se crean en estado PENDIENTE pero **no pueden avanzar a través de los estados del ciclo de vida** (CONFIRMADO → EN_PREPARACIÓN → EN_CAMINO → ENTREGADO) ni pueden cancelarse. Sin la máquina de estados, el sistema no puede procesar pedidos más allá de su creación. Esto bloquea toda la operación de la tienda.

## What Changes

- Implementar **FSM (Finite State Machine)** con mapa de transiciones válidas entre estados
- Endpoint `PATCH /api/v1/pedidos/{id}/estado` para avanzar estado (ADMIN/PEDIDOS)
- Endpoint `PATCH /api/v1/pedidos/{id}/cancelar` para cancelar pedido (según permisos por estado)
- Validación de reglas de negocio para cada transición (RN-FS01 a RN-FS09)
- Decremento atómico de stock al confirmar pedido (PENDIENTE → CONFIRMADO)
- Restauración atómica de stock al cancelar desde CONFIRMADO
- Endpoint `GET /api/v1/pedidos/{id}/historial` para historial cronológico
- **Frontend**: OrderHistoryTimeline, CancelOrderButton con confirmación
- **Frontend admin**: Selector de estado para avanzar/cancelar pedidos

## Capabilities

### New Capabilities
- `pedido-fsm`: Máquina de estados de pedidos con validación de transiciones, control de permisos por rol, registro append-only en HistorialEstadoPedido, y manejo atómico de stock (decremento al confirmar, restauración al cancelar).

### Modified Capabilities
- *(ninguna — extensión de funcionalidad existente)*

## Impact

- **Backend**: Nuevo `PedidoFsmService` con lógica de FSM. Endpoints para transicionar y cancelar pedidos. Modificaciones menores a `PedidoService` (reutilizar métodos de detalle).
- **Frontend**: Nuevos componentes `OrderHistoryTimeline`, `CancelOrderModal`, `ChangeStatusModal`. Actualización de `OrderDetailModal` para incluir acciones.
- **Base de datos**: No requiere migraciones. Los estados ya existen (PENDIENTE=1, CONFIRMADO=2, EN_PREPARACION=3, EN_CAMINO=4, ENTREGADO=5, CANCELADO=6).
- **Dependencias**: Depende de `sprint-4-creacion-pedidos` (ya archivado).
