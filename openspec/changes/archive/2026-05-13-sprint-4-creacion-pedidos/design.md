## Context

Actualmente el sistema tiene:
- Modelos `Pedido`, `DetallePedido`, `HistorialEstadoPedido`, `EstadoPedido` ya creados en SQLAlchemy
- Repositorios `PedidoRepository`, `DetallePedidoRepository`, `HistorialEstadoPedidoRepository` con operaciones básicas
- `CheckoutService` que valida stock y calcula totales
- `UnitOfWork` implementado en `core/uow.py` que expone todos los repositorios
- Direcciones de entrega funcionales con CRUD y ownership por usuario
- Carrito client-side con Zustand + localStorage

Lo que **no existe** aún:
- Endpoint para crear pedidos (`POST /api/v1/pedidos`)
- Lógica de negocio para creación atómica con UoW
- Snapshots de precio y dirección al crear
- Endpoints públicos para consultar pedidos
- Frontend de visualización de pedidos

## Goals / Non-Goals

**Goals:**
- Crear pedido de forma atómica (todo o nada) usando Unit of Work
- Validar stock suficiente dentro de la transacción con SELECT FOR UPDATE
- Generar snapshot de precio de cada producto en `DetallePedido.precio_snapshot`
- Generar snapshot de dirección en `Pedido.direccion_snapshot`
- Registrar estado inicial `PENDIENTE` en `HistorialEstadoPedido` con `estado_anterior_id=NULL`
- Listar pedidos del usuario autenticado con paginación
- Mostrar detalle completo de un pedido (items, historial, totales)
- Listar todos los pedidos (para ADMIN/PEDIDOS) con filtros
- Frontend: pantalla de confirmación, listado de pedidos, detalle

**Non-Goals:**
- Máquina de estados avanzada (transiciones, cancelación) — será en `sprint-4-fsm-pedidos`
- Integración con pagos — será en Sprint 5
- Notificaciones por email — será en Sprint 7
- Filtros avanzados de admin (fecha, estado combinados) — se ampliarán en `sprint-4-admin-gestion-pedidos`

## Decisions

### 1. Creación atómica con Unit of Work existente
**Decisión**: Usar el `UnitOfWork` ya implementado como context manager. El servicio recibe `uow` como parámetro y opera contra los repositorios expuestos.

**Alternativa considerada**: Usar la sesión directamente con commits manuales. Se descarta porque rompe el patrón existente y no garantiza atomicidad real.

**Rationale**: El UoW ya existe y está probado. Commit automático al salir del `async with`, rollback automático en error. Es el patrón correcto para operaciones multi-entidad.

### 2. Validación de stock con SELECT FOR UPDATE dentro del UoW
**Decisión**: Dentro de la transacción del UoW, hacer `SELECT ... FOR UPDATE` sobre cada producto para bloquear la fila hasta el commit. Si algún producto no tiene stock suficiente, se lanza excepción y el UoW hace rollback.

**Rationale**: Evita race conditions donde dos pedidos simultáneos vendan el último stock del mismo producto.

### 3. Snapshot de dirección como JSON string
**Decisión**: Al crear el pedido, se copian los campos relevantes de la dirección a `Pedido.direccion_snapshot` como texto JSON serializado.

**Rationale**: La dirección puede cambiar después de creado el pedido. El snapshot garantiza inmutabilidad del registro histórico (RN-PE03, RN-DA06).

### 4. Snapshot de precio por item
**Decisión**: Cada `DetallePedido` guarda `precio_snapshot` con el precio actual del producto al momento de crear el pedido.

**Rationale**: El precio del producto puede cambiar. El snapshot garantiza que el pedido refleje el precio acordado (RN-PE02, RN-DA06).

### 5. Estado inicial PENDIENTE con FK a EstadoPedido
**Decisión**: El pedido nace con `estado_id` apuntando al registro de `EstadoPedido` con código `PENDIENTE`. Se inserta el primer registro en `HistorialEstadoPedido` con `estado_anterior_id=NULL` y `estado_nuevo_id=ID_PENDIENTE`.

**Rationale**: El seed de la base de datos ya crea los 6 estados con IDs estables. Se referencian por ID. El historial append-only desde el primer registro.

### 6. Rutas separadas para cliente y admin
**Decisión**: 
- `GET /api/v1/pedidos` → lista del usuario autenticado (CLIENT)
- `GET /api/v1/pedidos/{id}` → detalle (solo propietario o ADMIN)
- `GET /api/v1/admin/pedidos` → lista global (ADMIN/PEDIDOS)

**Rationale**: Separación clara de responsabilidades. El endpoint de admin se registra en el router de admin (ya existe `backend/admin/`), o se crea en el router de pedidos con dependencia de roles.

## Data Model

No se modifican los modelos existentes. Los modelos ya están creados:

### Pedido
| Campo | Tipo | Nota |
|-------|------|------|
| id | Integer | PK |
| usuario_id | Integer FK | FK → usuarios.id |
| estado_id | Integer FK | FK → estados_pedido.id (PENDIENTE = 1) |
| direccion_id | Integer FK | FK → direcciones.id |
| forma_pago_id | Integer FK | FK → formas_pago.id |
| total | Numeric(10,2) | Suma de subtotales + costo_envio |
| costo_envio | Numeric(10,2) | Default 500.00 |
| direccion_snapshot | Text | JSON con datos de dirección al crear |
| creado_en | DateTime | Auto |
| actualizado_en | DateTime | Auto |
| eliminado_en | DateTime | Nullable |

### DetallePedido
| Campo | Tipo | Nota |
|-------|------|------|
| id | Integer | PK |
| pedido_id | Integer FK | FK → pedidos.id |
| producto_id | Integer FK | FK → productos.id |
| cantidad | Integer | ≥ 1 |
| precio_snapshot | Numeric(10,2) | Precio al momento de crear |
| subtotal | Numeric(10,2) | precio_snapshot × cantidad |
| personalizacion | ARRAY(Integer) | IDs de ingredientes excluidos |

### HistorialEstadoPedido
| Campo | Tipo | Nota |
|-------|------|------|
| id | Integer | PK |
| pedido_id | Integer FK | FK → pedidos.id |
| estado_anterior_id | Integer FK | NULL para el primer registro |
| estado_nuevo_id | Integer FK | FK → estados_pedido.id |
| usuario_id | Integer FK | FK → usuarios.id (NULL = Sistema) |
| observacion | Text | Opcional |
| timestamp | DateTime | Auto |

## API Changes

### `POST /api/v1/pedidos` (CLIENT)
- **Request body**: `CrearPedidoRequest` (items: list[ItemPedidoRequest], direccion_id: int)
- **Response**: `201 PedidoDetail`
- **Auth**: Bearer token (CLIENT o ADMIN)
- **Lógica**:
  1. Validar items (mínimo 1, productos existentes, disponibles, stock suficiente)
  2. Validar dirección (existente y del usuario)
  3. Bloquear productos con SELECT FOR UPDATE
  4. Calcular total (suma precio_snapshot × cantidad + costo_envio)
  5. Generar snapshot de dirección
  6. Crear Pedido (estado_id = PENDIENTE)
  7. Crear DetallePedido para cada item
  8. Crear HistorialEstadoPedido inicial
  9. Devolver PedidoDetail creado

### `GET /api/v1/pedidos` (CLIENT)
- **Query params**: page, size
- **Response**: `200 PaginatedResponse[PedidoRead]`
- **Auth**: Bearer token
- **Filtro**: Solo pedidos del usuario autenticado

### `GET /api/v1/pedidos/{id}` (CLIENT/ADMIN)
- **Response**: `200 PedidoDetail` (con items e historial)
- **Auth**: Bearer token (propietario o ADMIN)

### `GET /api/v1/pedidos/admin` (ADMIN/PEDIDOS)
- **Query params**: page, size, estado_id
- **Response**: `200 PaginatedResponse[PedidoRead]`

## Implementation Notes

### Flujo de creación de pedido (secuencia)

```
Router (POST /api/v1/pedidos)
  │
  ├── 1. Validar CrearPedidoRequest con Pydantic
  ├── 2. Obtener usuario autenticado
  │
  └── async with UnitOfWork() as uow:
        │
        ├── 3. PedidoService.crear(uow, body, usuario)
        │     │
        │     ├── 3a. Iterar items → uow.productos.get_by_id()
        │     │     └── Validar: existe, disponible, stock >= cantidad
        │     │     └── SELECT FOR UPDATE en cada producto
        │     │
        │     ├── 3b. Validar dirección (si direccion_id != None)
        │     │     └── uow.direcciones verificar ownership
        │     │
        │     ├── 3c. Calcular total
        │     │     └── subtotal = Σ(precio_snapshot × cantidad)
        │     │     └── costo_envio = 500 (tarifa plana)
        │     │     └── total = subtotal + costo_envio
        │     │
        │     ├── 3d. Crear Pedido (estado PENDIENTE)
        │     │     └── uow.pedidos.create(pedido)
        │     │     └── uow.flush (solo si es necesario)
        │     │
        │     ├── 3e. Crear DetallePedido × N
        │     │     └── Cada uno con precio_snapshot y subtotal
        │     │
        │     ├── 3f. Crear HistorialEstadoPedido inicial
        │     │     └── estado_anterior_id = NULL
        │     │     └── estado_nuevo_id = PENDIENTE
        │     │
        │     └── 3g. Retornar pedido creado
        │
        └── UoW commit automático (o rollback si hay error)
```

### Nuevos archivos backend
- `backend/pedidos/services/pedido_service.py` — Lógica de creación, listado, detalle
- `backend/pedidos/routes/pedidos.py` — Endpoints REST

### Archivos a modificar
- `backend/main.py` — Registrar nuevo router
- `backend/pedidos/schemas/pedido.py` — Ya existe, verificar schemas necesarios
- `backend/pedidos/repositories/pedido.py` — Verificar métodos existentes

### Frontend: nueva estructura
```
frontend/src/features/pedidos/
├── hooks/useOrders.ts
├── components/
│   ├── order-card.tsx
│   ├── order-detail-modal.tsx
│   └── order-status-badge.tsx

frontend/src/pages/pedidos/
├── order-list-page.tsx
├── order-confirmation-page.tsx
```

## Risks / Mitigations

| Risk | Mitigation |
|------|------------|
| Race condition en stock entre pedidos simultáneos | SELECT FOR UPDATE dentro del UoW bloquea las filas hasta el commit |
| Error en medio de la creación deja datos parciales | UoW con rollback automático en cualquier excepción |
| Usuario intenta crear pedido con dirección de otro usuario | Validación de ownership antes de crear |
| Precios desactualizados entre validación y creación | La validación de stock y la creación ocurren en la misma transacción |
