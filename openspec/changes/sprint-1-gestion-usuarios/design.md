# Design: Sprint 1 — Gestión de Usuarios

## Architecture Overview

Se implementan 2 módulos: administración de usuarios (admin) y perfil/cambio de contraseña (cliente). Siguen el mismo patrón Router → Service → UoW → Repository establecido.

```
Admin → AdminUsuarioRouter → AdminUsuarioService → UoW → UsuarioRepository
                                                    → UsuarioRolRepository
                                                    → RefreshTokenRepository

Cliente → PerfilRouter → PerfilService → UoW → UsuarioRepository
                                             → RefreshTokenRepository
```

## Components

### Admin Usuario Routes
- **Responsibility**: Endpoints de gestión administrativa de usuarios
- **Location**: `backend/usuarios/routes/admin_usuarios.py`
- **Endpoints**:
  - `GET /api/v1/admin/usuarios` — listar usuarios (ADMIN only), con paginación, búsqueda por nombre/email, filtro por rol
  - `GET /api/v1/admin/usuarios/{id}` — ver detalle de usuario (ADMIN only)
  - `PUT /api/v1/admin/usuarios/{id}` — editar datos de usuario (ADMIN only)
  - `PATCH /api/v1/admin/usuarios/{id}/estado` — activar/desactivar usuario (ADMIN only, protege último admin)

### Admin Usuario Service
- **Responsibility**: Lógica de negocio para administración de usuarios
- **Location**: `backend/usuarios/services/admin_usuario_service.py`
- **Key methods**:
  - `list_usuarios(session, skip, limit, search, rol)` → lista paginada con filtros
  - `get_usuario(session, usuario_id)` → detalle de usuario con roles
  - `update_usuario(session, admin_user, usuario_id, data)` → editar datos
  - `toggle_estado(session, admin_user, usuario_id)` → activar/desactivar, protege último admin, invalida tokens

### Perfil Routes (Cliente)
- **Responsibility**: Endpoints de perfil del cliente autenticado
- **Location**: `backend/usuarios/routes/perfil.py`
- **Endpoints**:
  - `GET /api/v1/perfil` — ver perfil propio (requiere auth)
  - `PUT /api/v1/perfil` — editar datos propios (requiere auth)
  - `PUT /api/v1/perfil/password` — cambiar contraseña (requiere auth)

### Perfil Service
- **Responsibility**: Lógica de perfil del cliente
- **Location**: `backend/usuarios/services/perfil_service.py`
- **Key methods**:
  - `get_perfil(session, user_id)` → datos del usuario autenticado
  - `update_perfil(session, user_id, data)` → actualizar nombre, email, teléfono
  - `change_password(session, user_id, password_actual, password_nueva)` → verificar actual, hashear nueva, invalidar tokens

### Frontend — Admin Usuarios
- **AdminUsersPage**: Tabla paginada de usuarios con búsqueda y filtro por rol
- **EditUserModal**: Modal para editar datos de usuario
- **ToggleUserStatus**: Botón para activar/desactivar con confirmación
- **useAdminUsers hook**: fetch, search, edit, toggle status

### Frontend — Perfil
- **ProfilePage**: Formulario con datos del usuario, opción de cambiar contraseña
- **ChangePasswordModal**: Modal con campos de contraseña actual y nueva

## Data Model

No se crean nuevas tablas. Se usan las existentes:
- `usuarios` — se agrega lógica de activo/inactivo (usando `eliminado_en` como flag de desactivación)
- `refresh_tokens` — se invalidan al desactivar usuario o cambiar contraseña
- `usuario_roles` — consulta de roles

### Schemas actualizados

```
UsuarioUpdate (admin):
  nombre: str | None
  email: EmailStr | None
  telefono: str | None
  roles: list[str] | None  # solo admin puede cambiar roles

CambiarPasswordRequest:
  password_actual: str
  password_nueva: str (min_length=8)

UsuarioListResponse:
  items: list[UsuarioRead]
  total: int
  page: int
  limit: int
```

## API Changes

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/v1/admin/usuarios | ADMIN | Listar usuarios (paginado, search, rol filter) |
| GET | /api/v1/admin/usuarios/{id} | ADMIN | Detalle de usuario |
| PUT | /api/v1/admin/usuarios/{id} | ADMIN | Editar usuario |
| PATCH | /api/v1/admin/usuarios/{id}/estado | ADMIN | Activar/desactivar |
| GET | /api/v1/perfil | Auth | Ver perfil propio |
| PUT | /api/v1/perfil | Auth | Editar perfil propio |
| PUT | /api/v1/perfil/password | Auth | Cambiar contraseña |

## Implementation Notes

- **Desactivar usuario**: Se usa `eliminado_en` como flag de desactivación (soft delete existente). Al desactivar, se invalida todos los refresh tokens del usuario. Al activar, se limpia `eliminado_en`.
- **Login con usuario desactivado**: En el servicio de login (sprint-1), verificar que el usuario no tenga `eliminado_en` seteado. Si está desactivado → 403 "Cuenta desactivada".
- **Protección último admin**: No permitir desactivar a un usuario si es el último con rol ADMIN.
- **Cambio de contraseña**: Verificar contraseña actual con `verify_password`, hashear nueva con `get_password_hash`, invalidar todos los refresh tokens.
- **Paginación en listado**: Usar los parámetros `skip`/`limit` existentes en BaseRepository. Devolver `items` + `total`.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Admin desactiva su propia cuenta sin querer | No permitir desactivarse a sí mismo (validación en service) |
| Pérdida de acceso al cambiar contraseña | El frontend puede mostrar confirmación y forzar re-login |
| Performance con muchos usuarios | Paginación obligatoria, índices en email y nombre |
