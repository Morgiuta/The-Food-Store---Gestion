## Why

El Sprint 0 estableció la infraestructura base con JWT utilities y el modelo de Usuario/Rol, pero no implementó los endpoints de autenticación reales. Sin registro, login, refresh token y logout funcionales, ningún cliente puede usar la plataforma. Este change implementa el ciclo completo de autenticación que todos los sprints siguientes (catálogo, carrito, pedidos, pagos) necesitan como dependencia.

## What Changes

- **Backend**: Endpoints REST para registro, login, refresh token y logout con todas las reglas de negocio asociadas
- **Rate limiting**: Configurar slowapi en el endpoint de login (5 intentos/15 min por IP)
- **Frontend**: LoginPage y RegisterPage funcionales con validación en tiempo real, integración con authStore
- **Auth hooks**: useAuth hook completo con login, register, logout, hasRole
- **Interceptor**: Finalizar el interceptor de Axios para refresh automático de tokens en 401
- **RBAC endpoints**: Asignación y revocación de roles (admin only) con protección de último admin

## Capabilities

### New Capabilities
- `user-registration`: Registro de nuevos usuarios con validación, hash bcrypt y asignación automática de rol CLIENT
- `user-login`: Autenticación con email/contraseña, generación de JWT + refresh token, rate limiting
- `token-refresh`: Rotación de refresh tokens con detección de replay attacks
- `user-logout`: Invalidación de refresh tokens y limpieza de sesión
- `frontend-auth-flow`: UI de login/registro con validación, hooks, interceptor y guards de ruta
- `role-assignment`: Endpoints de admin para asignar/revocar roles con protección de último admin

### Modified Capabilities
- `jwt-authentication-core`: Se modifican los requisitos para conectar las utilidades JWT existentes con endpoints reales y agregar rate limiting
- `rbac-foundation`: Se agregan los endpoints REST de asignación de roles

## Impact

- **Backend**: Se crean `backend/auth/routes/auth.py`, `backend/auth/services/auth_service.py`, se modifica `backend/auth/schemas/auth.py`
- **Frontend**: Se completa `frontend/src/pages/auth/login-page.tsx`, `register-page.tsx`, `frontend/src/shared/hooks/use-auth.ts`
- **Dependencias nuevas**: slowapi ya incluido en requirements.txt (del Sprint 0)
- **Seguridad**: Rate limiting en login, detección de replay attacks en refresh, mensajes de error genéricos en login
