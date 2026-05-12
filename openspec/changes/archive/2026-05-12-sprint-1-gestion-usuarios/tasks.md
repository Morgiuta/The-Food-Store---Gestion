# Tasks: Sprint 1 — Gestión de Usuarios

## Phase 1: Backend — Admin Usuarios

### 1.1 Admin Usuario Service
- [x] 1.1.1 Create `backend/usuarios/services/__init__.py`
- [x] 1.1.2 Create `backend/usuarios/services/admin_usuario_service.py` with list, get, update, toggle_estado

### 1.2 Admin Usuario Routes
- [x] 1.2.1 Create `backend/usuarios/routes/admin_usuarios.py` with 4 endpoints (list, detail, update, toggle estado)
- [x] 1.2.2 Register admin usuarios router in `backend/main.py`

### 1.3 Perfil Service (Cliente)
- [x] 1.3.1 Create `backend/usuarios/services/perfil_service.py` with get_perfil, update_perfil, change_password

### 1.4 Perfil Routes
- [x] 1.4.1 Create `backend/usuarios/routes/perfil.py` with 3 endpoints (get, update, change password)
- [x] 1.4.2 Register perfil router in `backend/main.py`

### 1.5 Update Auth Schemas + Login
- [x] 1.5.1 Update `backend/usuarios/schemas/usuario.py`: Add roles field, CambiarPasswordRequest, UsuarioListResponse
- [x] 1.5.2 Update login: verificar que usuario no esté desactivado → 403

## Phase 2: Backend — Tests

- [x] 2.1 Create `backend/tests/test_admin_usuarios.py` — 20 tests (list, detail, update, toggle estado, last admin)
- [x] 2.2 Create `backend/tests/test_perfil.py` — 11 tests (perfil CRUD, change password, token invalidation)

## Phase 3: Frontend — Admin Users Section

### 3.1 Admin Users Page
- [x] 3.1.1 Create `frontend/src/pages/admin/users-page.tsx` with table, search, rol filter, pagination, actions

### 3.2 Admin Users Components
- [x] 3.2.1 Create `frontend/src/features/usuarios/components/edit-user-modal.tsx` with form + role checkboxes

### 3.3 Admin Users Hook
- [x] 3.3.1 Create `frontend/src/features/usuarios/hooks/use-admin-users.ts` with useAdminUsuarios, useUpdateUsuario, useToggleEstado

## Phase 4: Frontend — Perfil (Cliente)

### 4.1 Profile Page
- [x] 4.1.1 Create `frontend/src/pages/auth/profile-page.tsx` with editable user data + change password button

### 4.2 Change Password Modal
- [x] 4.2.1 Create `frontend/src/features/auth/components/change-password-modal.tsx` with validation + force logout

### 4.3 Router Update
- [x] 4.3.1 Add `/perfil` route to router.tsx (protegida)
- [x] 4.3.2 Add `/admin/usuarios` route to admin layout

## Phase 5: Integration & Final Checks

- [x] 5.1 All backend tests: 117 passed, 0 failed
- [x] 5.2 Frontend tests: 7 passed
- [x] 5.3 TypeScript: tsc --noEmit exit 0
- [x] 5.4 All tasks completed
