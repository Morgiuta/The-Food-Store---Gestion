## Why

Los sprints anteriores implementaron autenticación y gestión de usuarios, pero la seguridad del sistema tiene vacíos importantes: no hay rate limiting consistente en todos los endpoints sensibles, el menú de navegación no se adapta al rol del usuario, y las rutas del frontend necesitan una protección más robusta con páginas de error dedicadas. Este change cierra esas brechas de seguridad y usabilidad.

## What Changes

- **Backend — Rate limiting**: Fortalecer rate limiting en register (3/hora por IP) y agregar en creación de pedido (10/hora por usuario). Headers estándar Retry-After, X-RateLimit-*.
- **Backend — Segregación de roles**: Mapeo explícito de endpoints a roles requeridos, middleware de verificación global, respuesta 403 estandarizada.
- **Frontend — Navegación por rol**: Sidebar/menú que muestra solo las opciones según el rol del usuario autenticado (CLIENT, STOCK, PEDIDOS, ADMIN, o no autenticado).
- **Frontend — Protección de rutas**: Páginas 401, 403 y 404 dedicadas con diseño coherente. Redirects correctos según autenticación y rol.
- **Frontend — Error handling**: Toast/notificaciones globales para errores de permisos.

## Capabilities

### New Capabilities
- `rate-limiting-advanced`: Rate limiting granular por endpoint con slowapi, headeres estándar, y almacenamiento configurable
- `role-based-navigation`: Menú de navegación adaptado al rol del usuario (CLIENT, STOCK, PEDIDOS, ADMIN)
- `frontend-error-pages`: Páginas dedicadas 401, 403, 404 con diseño coherente y navegación

### Modified Capabilities
- `react-frontend-core`: Se mejoran las rutas protegidas con guards más robustos y menú dinámico por rol
- `rbac-foundation`: Se agrega mapeo explícito de endpoints a roles y middleware de verificación

## Impact

- **Backend**: Ajustes en `backend/main.py` para rate limiting granular. Endpoints de pedidos con rate limit por usuario.
- **Frontend**: Modificación del layout principal con menú dinámico. Nuevas páginas de error. Sistema global de notificaciones.
- **Dependencias**: slowapi ya incluido. No hay nuevas dependencias.
