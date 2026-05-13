## Why

Actualmente no hay forma de configurar parámetros del sistema como las formas de pago disponibles, el costo de envío u otras opciones globales. Todo está hardcodeado. El admin necesita una interfaz para gestionar esta configuración sin tocar código.

## What Changes

- Modelo `Configuracion` para almacenar parámetros clave-valor del sistema
- Endpoint `GET /api/v1/admin/config` para obtener configuración
- Endpoint `PUT /api/v1/admin/config` para actualizar configuración
- Endpoint `GET /api/v1/admin/formas-pago` para listar formas de pago
- Endpoint `PATCH /api/v1/admin/formas-pago/{id}` para habilitar/deshabilitar
- Frontend: AdminConfigPage con secciones de configuración general y formas de pago

## Capabilities

### New Capabilities
- `admin-configuracion-global`: Panel de configuración del sistema con parámetros clave-valor (costo de envío, claves de API, etc.) y gestión de formas de pago (habilitar/deshabilitar).

### Modified Capabilities
- *(ninguna)*

## Impact

- **Backend**: Nuevo modelo `Configuracion`, repositorio, servicio y rutas admin.
- **Frontend**: Nueva página `AdminConfigPage` con formularios.
- **Base de datos**: Nueva tabla `configuraciones` (no requiere migración con create_all).
