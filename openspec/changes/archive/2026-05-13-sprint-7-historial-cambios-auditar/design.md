## Context

Ya existe:
- Panel admin con navegación
- `BaseRepository` con operaciones CRUD
- Servicios: usuarios, productos, pedidos, pagos
- UoW funcional

## Goals / Non-Goals

**Goals:**
- Modelo AuditLog (id, usuario_id, accion, tabla, registro_id, valor_anterior, valor_nuevo, timestamp, ip_address)
- AuditService con métodos para registrar y consultar
- Endpoint GET /admin/audit con filtros
- Integración de logging en servicios clave
- Frontend: tabla de auditoría con filtros

**Non-Goals:**
- Middleware automático (logging manual desde servicios)
- Export CSV (se puede agregar después)

## Decisions

### 1. Logging manual desde servicios
**Decisión**: Los servicios que modifican datos llaman explícitamente a `AuditService.registrar()`.

**Rationale**: Más control que un middleware automático. Evita ruido de cambios no relevantes.

### 2. Valores como JSON string
**Decisión**: `valor_anterior` y `valor_nuevo` se almacenan como TEXT con JSON serializado.

**Rationale**: Flexible para cualquier entidad. Fácil de comparar en UI.

## Data Model

### AuditLog
| Campo | Tipo | Nota |
|-------|------|------|
| id | Integer | PK |
| usuario_id | Integer FK | Quién hizo el cambio |
| accion | String | CREATE, UPDATE, DELETE |
| tabla | String | usuarios, productos, pedidos, pagos |
| registro_id | Integer | ID del registro modificado |
| valor_anterior | Text | JSON nullable |
| valor_nuevo | Text | JSON nullable |
| ip_address | String | Nullable |
| created_at | DateTime | Auto |

## API Changes

### `GET /api/v1/admin/audit` (ADMIN)
- **Query params**: page, size, tabla, usuario_id, accion, fecha_desde, fecha_hasta
- **Response**: PaginatedResponse[AuditEntry]

## Frontend

```
AdminAuditPage
├── Filtros (tabla dropdown, acción, fechas)
└── AuditTable (ID, usuario, acción, tabla, registro, fecha)
    └── AuditDetailModal (valor_anterior vs valor_nuevo)
```
