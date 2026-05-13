## Context

Ya existe:
- Modelo `FormaPago` en `backend/pagos/models/forma_pago.py` (id, nombre, activo)
- Panel admin con sidebar y navegación
- `FormaPago` seed data cargada
- UoW y repositorios funcionales

## Goals / Non-Goals

**Goals:**
- Modelo Configuracion con clave-valor
- CRUD de configuración global (GET/PUT)
- Listar formas de pago y habilitar/deshabilitar
- Frontend: sección de configuración en admin

**Non-Goals:**
- Caché de configuración (se implementa después)
- Validación compleja de valores (solo tipos básicos)

## Decisions

### 1. Modelo clave-valor para configuración
**Decisión**: Tabla `configuraciones` con columnas `clave` (UNIQUE) y `valor` (TEXT).

**Rationale**: Simple, extensible, no requiere migraciones al agregar nuevas configuraciones.

### 2. Formas de pago desde modelo existente
**Decisión**: Usar el modelo `FormaPago` existente. Solo permitir toggle de activo/inactivo.

**Rationale**: FormaPago ya tiene seed data y está referenciado desde Pedido.

## Data Model

### Configuracion (nuevo)
| Campo | Tipo | Nota |
|-------|------|------|
| id | Integer | PK |
| clave | String(100) | UNIQUE, NN |
| valor | Text | NN |
| descripcion | Text | Opcional |
| creado_en | DateTime | Auto |

## API Changes

### `GET /api/v1/admin/config` (ADMIN)
- **Response**: `list[{ clave, valor, descripcion }]`

### `PUT /api/v1/admin/config` (ADMIN)
- **Body**: `{ configuraciones: [{ clave, valor }] }`
- **Response**: Config actualizada

### `GET /api/v1/admin/formas-pago` (ADMIN)
- **Response**: `list[{ id, nombre, activo }]`

### `PATCH /api/v1/admin/formas-pago/{id}` (ADMIN)
- **Body**: `{ activo: bool }`
- **Response**: FormaPago actualizada

## Frontend

```
AdminConfigPage
├── ConfigForm (sección: config. general)
│   ├── costo_envio (input numérico)
│   └── otros parámetros
└── PaymentMethodsConfig (sección: formas de pago)
    └── Lista con toggle activo/inactivo
```
