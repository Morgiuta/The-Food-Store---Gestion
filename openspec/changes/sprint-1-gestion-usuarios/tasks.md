# Tasks: Sprint 1 — Gestión de Usuarios

## Phase 1: Backend — Admin Usuarios

### 1.1 Admin Usuario Service
- [ ] 1.1.1 Create `backend/usuarios/services/__init__.py`
- [ ] 1.1.2 Create `backend/usuarios/services/admin_usuario_service.py`:
  - `list_usuarios(session, skip, limit, search, rol)` — lista paginada con búsqueda y filtro
  - `get_usuario(session, usuario_id)` — detalle con roles
  - `update_usuario(session, admin_user, usuario_id, data)` — editar datos + roles
  - `toggle_estado(session, admin_user, usuario_id)` — activar/desactivar, protege último admin, invalida tokens

### 1.2 Admin Usuario Routes
- [ ] 1.2.1 Create `backend/usuarios/routes/admin_usuarios.py`:
  - `GET /api/v1/admin/usuarios` — listar (query: skip, limit, search, rol)
  - `GET /api/v1/admin/usuarios/{id}` — detalle
  - `PUT /api/v1/admin/usuarios/{id}` — editar
  - `PATCH /api/v1/admin/usuarios/{id}/estado` — activar/desactivar
- [ ] 1.2.2 Register admin usuarios router in `backend/main.py`

### 1.3 Perfil Service (Cliente)
- [ ] 1.3.1 Create `backend/usuarios/services/perfil_service.py`:
  - `get_perfil(session, user_id)` — datos del usuario autenticado
  - `update_perfil(session, user_id, data)` — editar nombre, email, teléfono
  - `change_password(session, user_id, password_actual, password_nueva)` — verificar actual, hashear nueva, invalidar tokens

### 1.4 Perfil Routes
- [ ] 1.4.1 Create `backend/usuarios/routes/perfil.py`:
  - `GET /api/v1/perfil` — ver perfil propio
  - `PUT /api/v1/perfil` — editar perfil
  - `PUT /api/v1/perfil/password` — cambiar contraseña
- [ ] 1.4.2 Register perfil router in `backend/main.py`

### 1.5 Update Auth Schemas + Login
- [ ] 1.5.1 Update `backend/usuarios/schemas/usuario.py`: Agregar `CambiarPasswordRequest`
- [ ] 1.5.2 Update `backend/auth/services/auth_service.py` login: verificar que usuario no esté desactivado (eliminado_en IS NULL) → 403 si está desactivado

## Phase 2: Backend — Tests

- [ ] 2.1 Create `backend/tests/test_admin_usuarios.py`:
  - Test list usuarios as admin returns 200 with pagination
  - Test list usuarios as non-admin returns 403
  - Test list usuarios with search filter
  - Test get usuario detail as admin
  - Test update usuario as admin
  - Test toggle estado desactiva usuario
  - Test toggle estado protege último admin
  - Test desactivar usuario invalida sus tokens

- [ ] 2.2 Create `backend/tests/test_perfil.py`:
  - Test get perfil returns current user data
  - Test update perfil changes name/email
  - Test change password succeeds with correct current password
  - Test change password fails with incorrect current password
  - Test change password invalidates all refresh tokens

## Phase 3: Frontend — Admin Users Section

### 3.1 Admin Users Page
- [ ] 3.1.1 Create `frontend/src/pages/admin/users-page.tsx`:
  - Tabla paginada con columnas: nombre, email, roles, estado, acciones
  - Search input para filtrar por nombre/email
  - Select de filtro por rol
  - Botón de editar usuario (abre modal)
  - Botón de activar/desactivar con confirmación
  - Indicador visual de estado (activo/desactivado)

### 3.2 Admin Users Components
- [ ] 3.2.1 Create `frontend/src/features/usuarios/components/edit-user-modal.tsx`:
  - Formulario con nombre, email, teléfono
  - Selector de roles (checkboxes para ADMIN, STOCK, PEDIDOS, CLIENT)
  - Validación y envío

### 3.3 Admin Users Hook
- [ ] 3.3.1 Create `frontend/src/features/usuarios/hooks/use-admin-users.ts`:
  - `useUsuarios(skip, limit, search, rol)` — TanStack Query
  - `useUpdateUsuario()` — mutation
  - `useToggleEstado()` — mutation

## Phase 4: Frontend — Perfil (Cliente)

### 4.1 Profile Page
- [ ] 4.1.1 Create `frontend/src/pages/auth/profile-page.tsx`:
  - Mostrar datos del usuario autenticado
  - Formulario para editar nombre, email, teléfono
  - Botón "Cambiar contraseña" abre modal

### 4.2 Change Password Modal
- [ ] 4.2.1 Create `frontend/src/features/auth/components/change-password-modal.tsx`:
  - Campo: contraseña actual
  - Campo: nueva contraseña (min 8 chars)
  - Campo: confirmar nueva contraseña
  - Validación y manejo de errores

### 4.3 Router Update
- [ ] 4.3.1 Add `/perfil` route to router.tsx (ruta protegida)
- [ ] 4.3.2 Add `/admin/usuarios` route to admin layout

## Phase 5: Integration & Final Checks

- [ ] 5.1 Run all tests: `pytest backend/tests/ -v`
- [ ] 5.2 Run frontend tests: `npm test`
- [ ] 5.3 Verify TypeScript: `npx tsc --noEmit`
- [ ] 5.4 Mark all tasks as completed
