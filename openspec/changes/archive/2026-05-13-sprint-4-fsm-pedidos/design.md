## Context

Ya existe:
- Modelos `Pedido`, `DetallePedido`, `HistorialEstadoPedido`, `EstadoPedido` con seed data (6 estados con IDs estables)
- `PedidoService` con creación atómica, listado y detalle
- Endpoints básicos de pedidos
- Unit of Work funcional en `core/uow.py`

Lo que **no existe** aún:
- Lógica de validación de transiciones FSM
- Endpoint para cambiar estado
- Manejo de stock en transiciones (decremento/restauración)
- Endpoint de cancelación con permisos por rol y estado

## Goals / Non-Goals

**Goals:**
- Implementar FSM con mapa de transiciones válidas
- Endpoint `PATCH /pedidos/{id}/estado` para avanzar estado (ADMIN/PEDIDOS)
- Endpoint `PATCH /pedidos/{id}/cancelar` para cancelar (según RN-FS08)
- Decrementar stock atómicamente al pasar PENDIENTE → CONFIRMADO
- Restaurar stock atómicamente al cancelar desde CONFIRMADO
- Registrar todas las transiciones en HistorialEstadoPedido (append-only)
- Endpoint `GET /pedidos/{id}/historial` para historial
- Frontend: timeline visual, botón cancelar con modal de confirmación, selector de estado para admin
- Actualizar OrderDetailModal para incluir acciones de cambio de estado

**Non-Goals:**
- Transición PENDIENTE → CONFIRMADO automática por webhook (será en Sprint 5 con MercadoPago)
- Filtros avanzados de admin (ya viene en sprint-4-admin-gestion-pedidos)
- Notificaciones de cambio de estado (será en Sprint 7)

## Decisions

### 1. Mapa de transiciones como constante centralizada
**Decisión**: Definir un diccionario `TRANSICIONES_VALIDAS` en el servicio FSM que mapea cada estado a sus estados destino permitidos.

```
TRANSICIONES_VALIDAS = {
    "PENDIENTE": ["CONFIRMADO", "CANCELADO"],
    "CONFIRMADO": ["EN_PREPARACION", "CANCELADO"],
    "EN_PREPARACION": ["EN_CAMINO", "CANCELADO"],  # CANCELADO solo ADMIN
    "EN_CAMINO": ["ENTREGADO"],
    "ENTREGADO": [],       # Terminal
    "CANCELADO": [],       # Terminal
}
```

**Rationale**: Simple, explícito, fácil de mantener y testear. El mapa es la fuente de verdad para todas las validaciones.

### 2. Permisos de cancelación por estado y rol
**Decisión**: Validar doble condición: (a) la transición →CANCELADO está permitida desde el estado actual, (b) el usuario tiene el rol adecuado:
- PENDIENTE → CANCELADO: CLIENT (propietario), ADMIN, PEDIDOS
- CONFIRMADO → CANCELADO: ADMIN, PEDIDOS (no CLIENT)
- EN_PREPARACIÓN → CANCELADO: solo ADMIN

**Rationale**: RN-FS08 y RN-RB08 especifican exactamente estos permisos.

### 3. Manejo de stock en transiciones
**Decisión**: 
- Al pasar PENDIENTE → CONFIRMADO: decrementar stock atómicamente con `UPDATE ... SET stock = stock - cantidad WHERE id = :id AND stock >= :cantidad`
- Al cancelar desde CONFIRMADO: restaurar stock con `UPDATE ... SET stock = stock + cantidad WHERE id = :id`
- Ambas operaciones dentro del mismo UoW que el cambio de estado + registro de historial

**Rationale**: Atomicidad garantizada por UoW. La condición `stock >= cantidad` en el UPDATE evita stock negativo por race conditions.

### 4. Historial append-only
**Decisión**: Cada transición registra un nuevo `HistorialEstadoPedido` con estado_anterior_id, estado_nuevo_id, usuario_id, observacion (obligatorio si es CANCELADO), timestamp.

**Rationale**: RN-FS07, RN-DA05. No se actualiza ni elimina nunca.

### 5. Endpoint de cancelación separado
**Decisión**: Usar `PATCH /pedidos/{id}/cancelar` en lugar de unificar todo en el mismo endpoint de estado. La cancelación tiene más reglas (motivo obligatorio, verificación de stock, permisos especiales).

**Rationale**: Separa concerns. El endpoint de estado es para avanzar secuencialmente. El de cancelación es una operación especial con su propia lógica.

## Data Model

No se modifican los modelos existentes. Se reutilizan:

### HistorialEstadoPedido (ya existe)
| Campo | Tipo | Nota |
|-------|------|------|
| estado_anterior_id | Integer FK | Estado previo (NULL en creación) |
| estado_nuevo_id | Integer FK | Estado al que se transiciona |
| usuario_id | Integer FK | Quién realizó la acción (NULL = Sistema) |
| observacion | Text | Motivo (obligatorio en CANCELADO) |
| timestamp | DateTime | Auto |

### IDs de estados (seed)
| Código | ID | es_terminal |
|--------|----|-------------|
| PENDIENTE | 1 | false |
| CONFIRMADO | 2 | false |
| EN_PREPARACION | 3 | false |
| EN_CAMINO | 4 | false |
| ENTREGADO | 5 | true |
| CANCELADO | 6 | true |

## API Changes

### `PATCH /api/v1/pedidos/{id}/estado` (ADMIN/PEDIDOS)
- **Request**: `AvanzarEstadoRequest` (nuevo_estado: str, observacion: str | None)
- **Response**: `200 PedidoDetail`
- **Lógica**:
  1. Obtener pedido con sus detalles (para stock si es CONFIRMADO)
  2. Validar que la transición esté en el mapa FSM
  3. Si es PENDIENTE→CONFIRMADO: decrementar stock de cada producto
  4. Registrar en HistorialEstadoPedido
  5. Actualizar pedido.estado_id
  6. Retornar PedidoDetail actualizado

### `PATCH /api/v1/pedidos/{id}/cancelar` (según estado + rol)
- **Request**: `CancelarPedidoRequest` (motivo: str = obligatorio)
- **Response**: `200 PedidoDetail`
- **Lógica**:
  1. Validar que la cancelación esté permitida desde el estado actual (según RN-FS08)
  2. Validar permisos del usuario según estado actual
  3. Si venía de CONFIRMADO: restaurar stock atómicamente
  4. Registrar en HistorialEstadoPedido con motivo
  5. Actualizar pedido.estado_id = CANCELADO
  6. Retornar PedidoDetail actualizado

### `GET /api/v1/pedidos/{id}/historial` (propietario/ADMIN)
- **Response**: `200 list[HistorialEstadoRead]`
- (Ya implementado parcialmente en change 1, se asegura endpoint dedicado)

## Implementation Notes

### Flujo de avance de estado

```
PATCH /pedidos/{id}/estado { nuevo_estado: "EN_PREPARACION" }
  │
  ├── 1. Obtener pedido (con estado actual)
  ├── 2. Validar nuevo_estado en TRANSICIONES_VALIDAS[estado_actual]
  │     └── Si no válida → HTTP 400 "Transición no permitida"
  ├── 3. Verificar permisos (solo ADMIN/PEDIDOS, no CLIENT)
  │
  └── async with UnitOfWork() as uow:
        │
        ├── 4. Si PENDIENTE→CONFIRMADO:
        │     └── Decrementar stock de cada DetallePedido
        │     └── SELECT FOR UPDATE + UPDATE atómico
        │
        ├── 5. Actualizar pedido.estado_id
        │     └── (No es necesario UPDATE con FK, se asigna directamente)
        │
        ├── 6. Crear HistorialEstadoPedido
        │     └── estado_anterior_id = estado_actual
        │     └── estado_nuevo_id = nuevo_estado
        │     └── usuario_id = current_user.user_id
        │     └── observacion = del request
        │
        └── UoW commit (o rollback si error)
```

### Flujo de cancelación

```
PATCH /pedidos/{id}/cancelar { motivo: "Cliente no lo quiere" }
  │
  ├── 1. Obtener pedido (con detalles si está CONFIRMADO)
  ├── 2. Validar que CANCELADO esté en TRANSICIONES_VALIDAS[estado_actual]
  ├── 3. Validar permisos según estado:
  │     ├── PENDIENTE → CLIENT (owner) / ADMIN / PEDIDOS
  │     ├── CONFIRMADO → ADMIN / PEDIDOS
  │     └── EN_PREPARACIÓN → solo ADMIN
  │
  └── async with UnitOfWork() as uow:
        │
        ├── 4. Si venía de CONFIRMADO:
        │     └── Restaurar stock: UPDATE stock = stock + cantidad
        │
        ├── 5. Actualizar pedido.estado_id = CANCELADO
        │
        ├── 6. Crear HistorialEstadoPedido con motivo
        │
        └── UoW commit (o rollback si error)
```

### Nuevos archivos backend
- `backend/pedidos/services/pedido_fsm_service.py` — Lógica FSM, transiciones, cancelación

### Archivos a modificar
- `backend/pedidos/routes/pedidos.py` — Agregar endpoints de estado y cancelación
- `backend/pedidos/schemas/pedido.py` — Agregar `CancelarPedidoRequest`

### Frontend: nuevos archivos
```
frontend/src/features/pedidos/components/
├── order-history-timeline.tsx    ← Timeline visual de historial
├── cancel-order-modal.tsx        ← Modal de cancelación con motivo
└── change-status-modal.tsx       ← Modal para admin: seleccionar nuevo estado
```

## Risks / Mitigations

| Risk | Mitigation |
|------|------------|
| Race condition en decremento de stock | UPDATE con condición `stock >= cantidad` dentro del UoW |
| Cancelación desde EN_PREPARACIÓN por usuario no autorizado | Validación de roles estricta (solo ADMIN) |
| Cancelación sin motivo registrado | Validación: motivo obligatorio si nuevo_estado = CANCELADO |
| Transición inválida por error de frontend | Validación en backend contra mapa FSM, doble validación |
