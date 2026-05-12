# Design: Sprint 1 — Seguridad Avanzada

## Architecture Overview

Tres ejes de mejora: rate limiting granular, navegación por rol, y páginas de error dedicadas.

```
Backend:
  slowapi → Limiter por endpoint (login, register, create order)
         → Headers X-RateLimit-*
  require_role → Mapeo explícito de rutas → roles

Frontend:
  useAuth → hasRole() → Navigation dinámico
         → ProtectedRoute / RoleProtectedRoute → ErrorPages
         → uiStore → Toast notifications
```

## Components

### Backend — Rate Limiting Avanzado
- **Responsibility**: Rate limiting granular por endpoint sensible
- **Ubicación**: `backend/core/rate_limit.py` (ya existe), ajustes en `backend/main.py`
- **Límites**:
  - `POST /auth/login`: 5/15min por IP ✅ ya implementado
  - `POST /auth/register`: 3/hour por IP (fortalecer desde 10/min)
  - `POST /pedidos`: 10/hour por usuario (nuevo)

### Backend — Segregación de Roles
- **Responsibility**: Mapeo explícito rol → endpoints
- **Ya implementado**: `require_role` dependency en auth/routes/roles.py
- **Mejora**: Agregar verificación de ownership (CLIENT solo ve sus datos)
- **Tabla de permisos**:

| Endpoint | Roles Permitidos |
|----------|-----------------|
| /admin/* | ADMIN |
| /perfil/* | CLIENT, ADMIN |
| /pedidos (GET) | CLIENT (propios), PEDIDOS, ADMIN |
| /pedidos (POST) | CLIENT |
| /productos (GET público) | Sin auth |
| /productos (POST/PUT/DELETE) | STOCK, ADMIN |
| /categorias (POST/PUT/DELETE) | STOCK, ADMIN |
| /ingredientes (POST/PUT/DELETE) | STOCK, ADMIN |

### Frontend — Navegación por Rol
- **Responsibility**: Menú que se adapta al rol del usuario
- **Ubicación**: `frontend/src/app/layouts/main-layout.tsx` y `frontend/src/app/layouts/admin-layout.tsx`
- **Estructura del menú**:

```
No autenticado: Catálogo | Login | Registrarse
CLIENT:         Catálogo | Mi Carrito | Mis Pedidos | Mi Perfil
STOCK:          Dashboard | Productos | Categorías | Ingredientes
PEDIDOS:        Dashboard | Pedidos
ADMIN:          Dashboard | Usuarios | Productos | Categorías | Ingredientes | Pedidos | Configuración
```

### Frontend — Páginas de Error
- **401 Unauthorized**: Mensaje "No has iniciado sesión" + botón "Ir al login"
- **403 Forbidden**: Mensaje "No tienes permisos para acceder a esta página" + botón "Volver al inicio"
- **404 Not Found**: Mensaje "Página no encontrada" + botón "Volver al inicio"
- Ya existen páginas 403 y 404 stub. Completar con diseño coherente.

### Frontend — Notificaciones de Error
- **Responsibility**: Toast/alertas globales para errores de permisos
- **Ubicación**: `frontend/src/app/store/ui-store.ts` (ya existe)
- **Mejora**: Agregar notificación automática cuando el interceptor recibe 401/403

## Implementation Notes

- **Rate limiting register**: Cambiar de `10/minute` a `3/hour` (más restrictivo para prevenir abuso)
- **Rate limiting pedidos**: Usar key_func por usuario (`lambda request: str(current_user.user_id)`)
- **Menú dinámico**: Usar el hook `useAuth().hasRole()` para renderizar condicionalmente los items del menú
- **Páginas de error**: Ya existen stubs, solo completar el diseño con Tailwind
- **Notificaciones**: Usar el uiStore existente para agregar notificaciones cuando el interceptor detecte 401/403

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Rate limit muy agresivo en register (3/hora) puede frustrar usuarios legítimos | Suficiente para uso normal; se puede ajustar si hay quejas |
| Menú dinámico puede tener flickering al cargar | Usar estado de carga del authStore para mostrar skeleton |
| Páginas de error pueden quedar inconsistentes con el diseño general | Usar los mismos componentes UI (Button, Card) ya existentes |
