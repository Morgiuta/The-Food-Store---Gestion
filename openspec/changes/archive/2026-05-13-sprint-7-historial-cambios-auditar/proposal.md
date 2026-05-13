## Why

El sistema no registra quién hizo qué cambio ni cuándo. Sin un registro de auditoría, es imposible rastrear modificaciones a usuarios, productos, pedidos o pagos. Esto es crítico para la operación del negocio y la resolución de incidentes.

## What Changes

- Modelo `AuditLog` con usuario, acción, tabla, registro_id, valor_anterior, valor_nuevo, timestamp
- Servicio `AuditService` para registrar cambios de forma centralizada
- Endpoint `GET /api/v1/admin/audit` con filtros (tabla, usuario, fecha)
- Integración con servicios existentes para registrar cambios clave
- Frontend: AdminAuditPage con tabla, filtros y detalle de cambios

## Capabilities

### New Capabilities
- `audit-log`: Sistema de auditoría con registro append-only de cambios sobre entidades críticas, consultable desde el panel admin con filtros.

### Modified Capabilities
- *(ninguna)*

## Impact

- **Backend**: Nuevo modelo `AuditLog`, repositorio, servicio y endpoint admin.
- **Base de datos**: Nueva tabla `audit_logs` (se crea con create_all).
- **Frontend**: Nueva página `AdminAuditPage` con tabla paginada y filtros.
