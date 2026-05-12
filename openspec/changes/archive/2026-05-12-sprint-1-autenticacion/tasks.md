# Tasks: Sprint 1 — Autenticación

## Phase 1: Backend — Auth Endpoints

### 1.1 Auth Service
- [x] 1.1.1 Create `backend/auth/services/__init__.py`
- [x] 1.1.2 Create `backend/auth/services/auth_service.py` with register, login, refresh_token, logout

### 1.2 Auth Routes
- [x] 1.2.1 Create `backend/auth/routes/auth.py` with register (10/min), login (5/15min), refresh, logout
- [x] 1.2.2 Register auth router in `backend/main.py` with SlowAPIMiddleware

### 1.3 Role Management Endpoints
- [x] 1.3.1 Create `backend/auth/services/role_service.py` with assign_role, revoke_role (last admin protection)
- [x] 1.3.2 Create `backend/auth/routes/roles.py` with assign/revoke endpoints (ADMIN only)
- [x] 1.3.3 Register admin router in `backend/main.py`

### 1.4 Update Auth Schemas
- [x] 1.4.1 Update `backend/auth/schemas/auth.py`: LoginRequest, RegisterRequest, RefreshRequest, TokenResponse

### 1.5 Rate Limiting Configuration
- [x] 1.5.1 Configure slowapi Limiter in `backend/main.py` with in-memory storage
- [x] 1.5.2 Apply `@limiter.limit("5/15minutes")` to login endpoint
- [x] 1.5.3 Apply `@limiter.limit("10/minute")` to register endpoint
- [x] 1.5.4 Rate limit error handler via slowapi automatic 429 responses

## Phase 2: Backend — Tests

- [x] 2.1 Create `backend/tests/test_auth.py` — 17 tests (register, login, refresh, logout, full flow)
- [x] 2.2 Create `backend/tests/test_roles.py` — 12 tests (assign, revoke, last admin, permissions)

## Phase 3: Frontend — Auth UI

### 3.1 Auth Store Updates
- [x] 3.1.1 Verify auth-store.ts has all needed actions (setAuth, setTokens, logout, updateUser)
- [x] 3.1.2 Verify auth-store.ts persists correctly to localStorage

### 3.2 Login Page
- [x] 3.2.1 Complete `frontend/src/pages/auth/login-page.tsx` with form, validation, error handling, 429 handling

### 3.3 Register Page
- [x] 3.3.1 Complete `frontend/src/pages/auth/register-page.tsx` with form, validation, password match, 409 handling

### 3.4 useAuth Hook
- [x] 3.4.1 Complete `frontend/src/shared/hooks/use-auth.ts` with login, register, logout, hasRole

### 3.5 Axios Interceptor
- [x] 3.5.1 Verify `frontend/src/shared/api/client.ts` interceptors work end-to-end (Bear token + refresh on 401)

### 3.6 Auth Guards
- [x] 3.6.1 Verify ProtectedRoute redirects unauthenticated users to /login
- [x] 3.6.2 Verify RoleProtectedRoute redirects unauthorized users to /403
- [x] 3.6.3 Add route for /admin/* with RoleProtectedRoute(requiredRole="ADMIN")

## Phase 4: Integration & Final Checks

- [x] 4.1 Test full auth flow: Register → Login → Refresh → Logout (57 tests passing)
- [x] 4.2 Test role assignment flow: Admin asigna rol → usuario accede a endpoint protegido (12 tests)
- [x] 4.3 All tests pass: `pytest backend/tests/ -v` → 57 passed, 0 failed
- [x] 4.4 Frontend compiles: `npx tsc --noEmit` → exit 0
- [x] 4.5 All tasks checked off in tasks.md
