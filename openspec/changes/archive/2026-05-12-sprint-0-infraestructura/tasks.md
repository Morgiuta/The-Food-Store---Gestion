## 1. Repository Structure & Initial Setup

- [x] 1.1 Create monorepo directory structure with /backend and /frontend directories
- [x] 1.2 Create .gitignore (node_modules, dist, venv, .env, __pycache__, .DS_Store, *.log)
- [x] 1.3 Create README.md with project overview, tech stack, and local development instructions
- [x] 1.4 Create backend feature-first directory structure (/auth, /usuarios, /productos, /categorias, /ingredientes, /pedidos, /pagos, /admin)
- [x] 1.5 Create frontend FSD directory structure (/app, /pages, /features, /entities, /shared)
- [x] 1.6 Create .env.example files for both backend and frontend with required variables
- [x] 1.7 Create docker-compose.yml for PostgreSQL + pgAdmin (port 5432, 5050)

## 2. Backend FastAPI Core Setup

- [x] 2.1 Create requirements.txt (FastAPI, SQLAlchemy, Alembic, Pydantic v2, python-jose, passlib, slowapi, psycopg2)
- [x] 2.2 Create FastAPI app with CORS middleware (allow localhost:3000, localhost:5173) — `backend/main.py`
- [x] 2.3 Implement centralized error handling with RFC 7807 responses — `backend/middleware/error_handler.py`
- [x] 2.4 Add request/response logging middleware — `backend/middleware/logging.py`
- [x] 2.5 Configure OpenAPI documentation (Swagger at /docs, ReDoc at /redoc) — `backend/main.py`
- [x] 2.6 Implement health check endpoint GET /api/v1/health — `backend/api/v1/routes/health.py`
- [x] 2.7 Implement rate limiting infrastructure with slowapi — `backend/main.py`
- [x] 2.8 Create main.py with app initialization and startup/shutdown logic — `backend/main.py`

## 3. Database Setup with Alembic

- [x] 3.1 Initialize Alembic in backend directory — `backend/alembic/` + `backend/alembic.ini`
- [x] 3.2 Create SQLAlchemy Base and database connection configuration — `backend/core/database.py`
- [x] 3.3 Implement ERD v5 ORM models (16 tables): Usuario, Rol, UsuarioRol, Categoria, Ingrediente, Producto, ProductoCategoria, ProductoIngrediente, DireccionEntrega, Pedido, DetallePedido, HistorialEstadoPedido, RefreshToken, Pago, FormaPago, EstadoPedido
- [x] 3.4 Add soft delete pattern (eliminado_en field) to: Usuario, Producto, Categoria, Ingrediente, DireccionEntrega, Pedido
- [x] 3.5 Add audit timestamps (creado_en, actualizado_en) to all models
- [x] 3.6 Create Alembic migration: `backend/alembic/versions/001_initial_erd_v5_schema.py`
- [x] 3.7 Create seed script (seed.py) to populate roles (ADMIN, STOCK, PEDIDOS, CLIENT), admin user, and initial data
- [x] 3.8 Test: Create all tables in PostgreSQL (16 tables + 4 indexes via Docker) — verified with `\dt`
- [x] 3.9 Test: Run seed script and verify roles and admin user are created — 4 roles, 1 admin, 6 estados, 2 formas_pago

## 4. Repository Pattern & Unit of Work

- [x] 4.1 Create BaseRepository[T] generic class with CRUD methods — `backend/core/base_repository.py`
- [x] 4.2 Implement filtering support in BaseRepository.list() (skip, limit, filters dict)
- [x] 4.3 Create specific repository classes (one per entity) — 11 repositories in auth/, categorias/, ingredientes/, productos/, pedidos/, pagos/
- [x] 4.4 Implement Unit of Work class with context manager — `backend/core/uow.py`
- [x] 4.5 Add repository properties to UoW (uow.usuarios, uow.productos, uow.categorias, etc.)
- [x] 4.6 Implement UoW.commit() and UoW.rollback() with proper transaction handling
- [x] 4.7 Test: UoW atomicity test exists in `backend/tests/test_base_repository.py`
- [x] 4.8 Document UoW usage pattern in code comments

## 5. JWT Authentication & Authorization

- [x] 5.1 Create JWT utility functions: create_access_token(), create_refresh_token(), decode_token() — `backend/core/security.py`
- [x] 5.2 Implement JWT payload structure with userId, email, roles, expiresIn
- [x] 5.3 Create RefreshToken repository for storing/revoking refresh tokens — `backend/auth/repositories/refresh_token.py`
- [x] 5.4 Implement Pydantic schemas: TokenResponse, TokenPayload — `backend/auth/schemas/auth.py`
- [x] 5.5 Implement FastAPI dependency: get_current_user — `backend/core/dependencies.py`
- [x] 5.6 Implement FastAPI dependency factory: require_role for RBAC — `backend/core/dependencies.py`
- [x] 5.7 Create authentication utilities (hash password, verify password with bcrypt) — `backend/core/security.py`
- [x] 5.8 Implement token revocation on logout (mark refresh_token as revoked)
- [x] 5.9 Test: Token generation/verification tests in `backend/tests/test_security.py`

## 6. Role-Based Access Control (RBAC)

- [x] 6.1 Create Rol model with constants (ADMIN, STOCK, PEDIDOS, CLIENT) — `backend/auth/models/rol.py`
- [x] 6.2 Implement M2M relationship between Usuario and Rol with uniqueness constraint — `backend/auth/models/usuario_rol.py`
- [x] 6.3 Create migration for usuario_rol junction table with UNIQUE(usuario_id, rol_id)
- [x] 6.4 Implement UsuarioRolRepository for managing role assignments — `backend/auth/repositories/usuario_rol.py`
- [x] 6.5 Add validation: prevent removing last ADMIN (count_admins method)
- [x] 6.6 Populate seed data: assign ADMIN role to admin user, CLIENT role structure ready — `backend/seed.py`
- [x] 6.7 Test: get_current_user tests in `backend/tests/test_dependencies.py`
- [x] 6.8 Test: require_role tests in `backend/tests/test_dependencies.py`

## 7. Error Handling & Validation

- [x] 7.1 Create Pydantic schemas with validation rules (email format, price > 0, stock >= 0, etc.) — all domain schemas
- [x] 7.2 Create custom exception classes (ValidationException, NotFoundException, ForbiddenException, ConflictException, etc.) — `backend/core/exceptions.py`
- [x] 7.3 Add exception handlers to FastAPI app that return RFC 7807 responses — `backend/middleware/error_handler.py`
- [x] 7.4 Implement centralized error logging with request context — `backend/middleware/logging.py` + `backend/middleware/error_handler.py`
- [x] 7.5 Test: Invalid input returns 422 with RFC 7807 format — in test files
- [x] 7.6 Test: Missing authorization returns 401 — in `backend/tests/test_dependencies.py`
- [x] 7.7 Test: Insufficient role permissions return 403 — in `backend/tests/test_dependencies.py`

## 8. React Frontend Core Setup

- [x] 8.1 Create React project with Vite + TypeScript template
- [x] 8.2 Install dependencies: react-router-dom, axios, zustand, @tanstack/react-query, tailwindcss, postcss, autoprefixer
- [x] 8.3 Configure Vite: HMR config, build chunks, path aliases — `frontend/vite.config.ts`
- [x] 8.4 Set up Tailwind CSS with postcss and tailwind.config.js
- [x] 8.5 Create axios instance with configuration — `frontend/src/shared/api/client.ts`
- [x] 8.6 Implement axios request interceptor to add Bearer JWT token
- [x] 8.7 Implement axios response interceptor to handle 401 (refresh token, retry)
- [x] 8.8 Set up TanStack Query (React Query) with QueryClientProvider — `frontend/src/app/providers/query-provider.tsx`
- [x] 8.9 Create React Router basic structure with BrowserRouter — `frontend/src/app/providers/router.tsx`
- [x] 8.10 Set up .env.example with VITE_API_URL, VITE_MP_PUBLIC_KEY
- [x] 8.11 Test: npm install runs successfully (163 packages installed)

## 9. Zustand State Management

- [x] 9.1 Create authStore with state: { accessToken, refreshToken, user, isAuthenticated } — `frontend/src/app/store/auth-store.ts`
- [x] 9.2 Implement authStore actions: setAuth(), logout(), updateUser(), setTokens()
- [x] 9.3 Create cartStore with state: { items, totalItems, totalPrice } — `frontend/src/app/store/cart-store.ts`
- [x] 9.4 Implement cartStore actions: addItem(), removeItem(), updateQuantity(), clearCart()
- [x] 9.5 Configure persist middleware for cartStore (localStorage key: 'cart-store')
- [x] 9.6 Create paymentStore with state: { status, paymentId, error } (NO persistence) — `frontend/src/app/store/payment-store.ts`
- [x] 9.7 Implement paymentStore actions: setStatus(), setPaymentId(), setError(), reset()
- [x] 9.8 Create uiStore with state: { modals, notifications, loading } — `frontend/src/app/store/ui-store.ts`
- [x] 9.9 Implement uiStore actions: openModal(), closeModal(), addNotification(), removeNotification()
- [x] 9.10 Add TypeScript types for all stores — `frontend/src/shared/types/index.ts`

## 10. Frontend Hooks & Utilities

- [x] 10.1 Create useAuth hook that selects from authStore (token, user, isAuthenticated) + login/register/logout/hasRole — `frontend/src/shared/hooks/use-auth.ts`
- [x] 10.2 Create useCart hook that selects cartStore items and provides actions — `frontend/src/shared/hooks/use-cart.ts`
- [x] 10.3 Create utility function to check if user has role (hasRole) — in use-auth.ts
- [x] 10.4 Create constant definitions (API endpoints, roles, states, etc.) — `frontend/src/shared/constants/index.ts`
- [x] 10.5 Create shared/ui components: Button, Input, Card, Modal, Spinner — all in `frontend/src/shared/ui/`

## 11. Frontend Routing & Guards

- [x] 11.1 Create ProtectedRoute component that checks authentication — `frontend/src/features/auth/components/protected-route.tsx`
- [x] 11.2 Create RoleProtectedRoute component that checks role permissions
- [x] 11.3 Redirect unauthenticated users to /login — in router.tsx
- [x] 11.4 Redirect insufficiently-privileged users to /403 — in router.tsx
- [x] 11.5 Create basic pages: LoginPage, RegisterPage, NotFoundPage (404), ForbiddenPage (403) — all in `frontend/src/pages/`
- [x] 11.6 Set up route structure with /api/v1 prefix in frontend API calls — `frontend/src/shared/api/endpoints.ts`

## 12. Integration & Testing

- [x] 12.1 Create backend test fixtures (FastAPI TestClient, database session) — `backend/tests/conftest.py`
- [x] 12.2 Test UoW pattern atomicity — `backend/tests/test_base_repository.py`
- [x] 12.3 Test BaseRepository CRUD operations — `backend/tests/test_base_repository.py`
- [x] 12.4 Test get_current_user dependency with valid/expired/missing token — `backend/tests/test_dependencies.py`
- [x] 12.5 Test require_role dependency with sufficient/insufficient permissions — `backend/tests/test_dependencies.py`
- [x] 12.6 Test health endpoint GET /api/v1/health returns 200 — `backend/tests/test_health.py`
- [x] 12.7 Test model instantiation and relationships — `backend/tests/test_models.py`
- [x] 12.8 Test JWT token generation, decoding, expiration — `backend/tests/test_security.py`
- [x] 12.9 Test password hashing and verification — `backend/tests/test_security.py`

## 13. Documentation & Final Checks

- [x] 13.1 README.md exists with project overview, tech stack, and local dev instructions
- [x] 13.2 Code comments added to UoW, Repository, and auth utilities
- [x] 13.3 Verify .env.example files are complete for both backend and frontend
- [x] 13.4 Frontend: npm install runs without errors (163 packages)
- [x] 13.5 Backend: requirements.txt with all dependencies installed successfully
