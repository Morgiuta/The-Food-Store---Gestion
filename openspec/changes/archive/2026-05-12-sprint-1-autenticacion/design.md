# Design: Sprint 1 — Autenticación

## Architecture Overview

Se implementan 4 flujos de autenticación (registro, login, refresh, logout) más endpoints de asignación de roles. Todo el código nuevo sigue los patrones establecidos en Sprint 0: Router → Service → UoW → Repository → Model.

```
Cliente → [Rate Limit] → AuthRouter → AuthService → UoW → UsuarioRepository
                                                       → RefreshTokenRepository
                                                       → UsuarioRolRepository
                                                       → RolRepository
```

## Components

### Auth Routes
- **Responsibility**: Endpoints REST de autenticación
- **Location**: `backend/auth/routes/auth.py`
- **Endpoints**:
  - `POST /api/v1/auth/register` — registro (público, rate limited)
  - `POST /api/v1/auth/login` — login (público, rate limited 5/15min)
  - `POST /api/v1/auth/refresh` — refresh token (público)
  - `POST /api/v1/auth/logout` — logout (requiere auth)

### Auth Service
- **Responsibility**: Lógica de negocio de autenticación
- **Location**: `backend/auth/services/auth_service.py`
- **Key methods**:
  - `register(db, nombre, email, password)` → crea usuario + asigna CLIENT + genera tokens
  - `login(db, email, password)` → verifica credenciales + genera tokens
  - `refresh_token(db, token)` → rotación con detección de replay
  - `logout(db, token)` → invalida refresh token

### Admin Routes (Roles)
- **Responsibility**: Asignación y revocación de roles
- **Location**: Backend routes existente o `backend/auth/routes/roles.py`
- **Endpoints**:
  - `POST /api/v1/admin/usuarios/{id}/roles` — asignar rol (ADMIN only)
  - `DELETE /api/v1/admin/usuarios/{id}/roles/{rol_id}` — revocar rol (ADMIN only)

### Frontend — Auth Pages
- **LoginPage**: Formulario email + password, validación en tiempo real, redirect post-login
- **RegisterPage**: Formulario nombre + email + password + confirmación, redirect post-registro
- **useAuth hook**: login(), register(), logout(), hasRole() conectados a authStore + API
- **Interceptor**: Refresh automático en 401 con cola de requests (ya implementado en Sprint 0)

## Data Model

No se crean nuevas tablas. Se usan las existentes de Sprint 0:
- `usuarios` — para registro y login
- `refresh_tokens` — para refresh y logout
- `usuario_roles` — para asignación de roles
- `roles` — catálogo de roles

### Auth Schemas (actualizar existing)

```
LoginRequest:     email (EmailStr), password (str, min_length=8)
RegisterRequest:  nombre (str, min_length=2), email (EmailStr), password (str, min_length=8)
TokenResponse:    access_token (str), refresh_token (str), token_type (str="bearer"), user (UserResponse)
RefreshRequest:   refresh_token (str)
LogoutResponse:   (204 No Content)
```

## API Changes

| Method | Endpoint | Auth | Rate Limit | Description |
|--------|----------|------|------------|-------------|
| POST | /api/v1/auth/register | No | 10/min | Registrar nuevo cliente |
| POST | /api/v1/auth/login | No | 5/15min IP | Iniciar sesión |
| POST | /api/v1/auth/refresh | No | — | Rotar refresh token |
| POST | /api/v1/auth/logout | Sí | — | Invalidar refresh token |
| POST | /api/v1/admin/usuarios/{id}/roles | ADMIN | — | Asignar rol |
| DELETE | /api/v1/admin/usuarios/{id}/roles/{rol_id} | ADMIN | — | Revocar rol |

### Flujo de Refresh Token Rotation

```
1. Cliente envía refresh_token → POST /auth/refresh
2. Servicio busca token en BD
3. Si NO existe o está revocado → 401
4. Si EXISTE y está marcado como usado (replay) → revocar TODOS los tokens del usuario → 401
5. Si EXISTE y es válido:
   a. Marcar token actual como revocado
   b. Generar NUEVO par access + refresh
   c. Guardar nuevo refresh token en BD
   d. Retornar nuevos tokens
```

## Implementation Notes

- **Rate limiting en login**: Usar slowapi con `@limiter.limit("5/15minutes")` en el endpoint. Configurar key_func por IP.
- **Detección de replay**: Cada refresh token al usarse se marca como `revocado_en`. Si llega un token que ya estaba revocado → se invalida todo el usuario (ataque de replay).
- **Mensajes de error de login**: El mensaje de error es genérico: "Email o contraseña incorrectos". No revelar si el email existe.
- **Rotación de refresh**: Siempre generar nuevo refresh token + nuevo access token. El access token anterior sigue siendo válido por hasta 30 min (stateless).
- **Frontend**: Login exitoso → guardar en authStore + redirigir a /productos. Register exitoso → auto-login + redirigir.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Rate limiting en login puede bloquear IPs compartidas (NAT) | Configurar ventana de 15 min, 5 intentos es generoso para un humano |
| Replay attack detection puede generar falsos positivos si el cliente reintenta | El refresh tiene retry queue en frontend que evita duplicados |
| Token rotation puede dejar sesiones huérfanas si el refresh se pierde | El cliente siempre recibe un nuevo refresh; si se pierde, usuario debe re-loguearse |
