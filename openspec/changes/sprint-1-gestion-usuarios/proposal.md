## Why

El Sprint 1 de autenticación implementó registro, login y roles, pero los administradores no tienen forma de gestionar los usuarios del sistema (listar, editar, desactivar). Además, los clientes no pueden cambiar su contraseña ni ver su perfil. Este change completa la gestión de usuarios del lado administrativo y del lado del cliente.

## What Changes

- **Backend — Admin**: Endpoints para listar usuarios con paginación/búsqueda, editar datos de usuario, y desactivar usuarios (soft delete con invalidación de tokens)
- **Backend — Cliente**: Endpoint para cambiar contraseña con verificación de contraseña actual, e invalidación de todos los refresh tokens
- **Frontend — Admin**: Sección de usuarios en el panel admin con tabla paginada, búsqueda, filtro por rol, edición y desactivación
- **Frontend — Cliente**: Página de perfil con opción de cambio de contraseña

## Capabilities

### New Capabilities
- `admin-user-management`: CRUD de usuarios para administradores (listar, editar, desactivar) con paginación, búsqueda y filtros
- `client-profile`: Cambio de contraseña para clientes con verificación y rotación de tokens

### Modified Capabilities
- `rbac-foundation`: Se agrega el endpoint de desactivación de usuarios con verificación de último admin
- `react-frontend-core`: Se agregan las páginas de admin usuarios y perfil de cliente

## Impact

- **Backend**: Se crean `backend/usuarios/routes/admin_usuarios.py`, `backend/usuarios/services/admin_usuario_service.py`. Se actualiza `backend/usuarios/schemas/usuario.py`.
- **Frontend**: Se crean páginas admin para usuarios y página de perfil. Se agregan hooks.
- **Seguridad**: Al desactivar un usuario se invalidan todos sus refresh tokens. Al cambiar contraseña también.
- **Dependencias**: Depende de sprint-1-autenticacion (get_current_user, require_role, roles existentes)
