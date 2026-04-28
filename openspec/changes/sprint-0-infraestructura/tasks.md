## 1. Repository Structure & Initial Setup

- [ ] 1.1 Create monorepo directory structure with /backend and /frontend directories
- [ ] 1.2 Initialize .git and create .gitignore (node_modules, dist, venv, .env, __pycache__, .DS_Store, *.log)
- [ ] 1.3 Create README.md with project overview, tech stack, and local development instructions
- [ ] 1.4 Create backend feature-first directory structure (/auth, /usuarios, /productos, /categorias, /ingredientes, /pedidos, /pagos, /admin)
- [ ] 1.5 Create frontend FSD directory structure (/app, /pages, /features, /entities, /shared)
- [ ] 1.6 Create .env.example files for both backend and frontend with required variables
- [ ] 1.7 Create docker-compose.yml for PostgreSQL + pgAdmin (port 5432, 5050)

## 2. Backend FastAPI Core Setup

- [ ] 2.1 Initialize Python project with requirements.txt (FastAPI, SQLAlchemy, Alembic, Pydantic v2, python-jose, passlib, slowapi, psycopg2)
- [ ] 2.2 Create FastAPI app with CORS middleware (allow localhost:3000)
- [ ] 2.3 Implement centralized error handling with RFC 7807 responses (HTTPException handlers)
- [ ] 2.4 Add request/response logging middleware
- [ ] 2.5 Configure OpenAPI documentation (Swagger at /docs, ReDoc at /redoc)
- [ ] 2.6 Implement health check endpoint GET /api/v1/health
- [ ] 2.7 Implement rate limiting infrastructure with slowapi (import and configure, but don't apply yet)
- [ ] 2.8 Create main.py with app initialization and startup/shutdown logic

## 3. Database Setup with Alembic

- [ ] 3.1 Initialize Alembic in backend directory with sqlalchemy context
- [ ] 3.2 Create SQLAlchemy Base and database connection configuration
- [ ] 3.3 Implement ERD v5 ORM models (16 tables): Usuario, Rol, UsuarioRol, Categoria, Ingrediente, Producto, ProductoCategoria, ProductoIngrediente, Direccion, Pedido, DetallePedido, HistorialEstadoPedido, RefreshToken, Pago, IngredienterAlergenico, Sesion
- [ ] 3.4 Add soft delete pattern (eliminado_en field) to: Usuario, Producto, Categoria, Ingrediente, Direccion, Pedido
- [ ] 3.5 Add audit timestamps (creado_en, actualizado_en) to all models
- [ ] 3.6 Create Alembic migration: `alembic revision --autogenerate -m "Initial ERD v5 schema"`
- [ ] 3.7 Create seed script (seed.py) to populate roles (ADMIN, STOCK, PEDIDOS, CLIENT), admin user, and initial data
- [ ] 3.8 Test: Run `alembic upgrade head` and verify all tables exist
- [ ] 3.9 Test: Run seed script and verify roles and admin user are created

## 4. Repository Pattern & Unit of Work

- [ ] 4.1 Create BaseRepository[T] generic class with CRUD methods (create, get_by_id, list, update, delete/soft_delete)
- [ ] 4.2 Implement filtering support in BaseRepository.list() (skip, limit, filters dict)
- [ ] 4.3 Create specific repository classes: UsuarioRepository, ProductoRepository, CategoriaRepository, etc. (one per entity)
- [ ] 4.4 Implement Unit of Work class with context manager (async with UoW() as uow:)
- [ ] 4.5 Add repository properties to UoW (uow.usuarios, uow.productos, uow.categorias, etc.)
- [ ] 4.6 Implement UoW.commit() and UoW.rollback() with proper transaction handling
- [ ] 4.7 Test UoW atomicity: create nested entities, force failure on second entity, verify rollback
- [ ] 4.8 Document UoW usage pattern in code comments

## 5. JWT Authentication & Authorization

- [ ] 5.1 Create JWT utility functions: create_access_token(), create_refresh_token(), verify_token()
- [ ] 5.2 Implement JWT payload structure with userId, email, roles, expiresIn
- [ ] 5.3 Create RefreshToken repository for storing/revoking refresh tokens
- [ ] 5.4 Implement Pydantic schemas: TokenResponse, TokenPayload
- [ ] 5.5 Implement FastAPI dependency: get_current_user (extracts JWT from Authorization header)
- [ ] 5.6 Implement FastAPI dependency factory: require_role(*roles) for RBAC
- [ ] 5.7 Create authentication utilities (hash password, verify password with bcrypt, cost ≥ 12)
- [ ] 5.8 Implement token blacklist/revocation on logout (mark refresh_token as revoked)
- [ ] 5.9 Test: Generate token, verify it decodes correctly, test expired token rejection

## 6. Role-Based Access Control (RBAC)

- [ ] 6.1 Create Role enum/constants (ADMIN, STOCK, PEDIDOS, CLIENT)
- [ ] 6.2 Implement M2M relationship between Usuario and Rol with uniqueness constraint
- [ ] 6.3 Create migration for usuario_rol junction table with UNIQUE(usuario_id, rol_id)
- [ ] 6.4 Implement UsuarioRolRepository for managing role assignments
- [ ] 6.5 Add validation: prevent removing last ADMIN from system
- [ ] 6.6 Populate seed data: assign ADMIN role to admin user, CLIENT role structure ready
- [ ] 6.7 Test: Verify get_current_user returns roles in JWT claims
- [ ] 6.8 Test: Verify require_role dependency rejects users without required role

## 7. Error Handling & Validation

- [ ] 7.1 Create Pydantic schemas with validation rules (email format, price > 0, stock >= 0, etc.)
- [ ] 7.2 Implement XSS sanitization function for text inputs
- [ ] 7.3 Create custom exception classes (ValidationError, NotFoundError, ForbiddenError, ConflictError, ServerError)
- [ ] 7.4 Add exception handlers to FastAPI app that return RFC 7807 responses
- [ ] 7.5 Implement centralized error logging with request context (timestamp, error, path, user_id)
- [ ] 7.6 Test: Invalid input returns 422 with RFC 7807 format
- [ ] 7.7 Test: Missing authorization returns 401
- [ ] 7.8 Test: Insufficient role permissions return 403

## 8. React Frontend Core Setup

- [ ] 8.1 Create React project with `npm create vite@latest -- --template react-ts`
- [ ] 8.2 Install dependencies: react-router-dom, axios, zustand, @tanstack/react-query, tailwindcss, postcss, autoprefixer
- [ ] 8.3 Configure Vite: ensure HMR works, build optimizations
- [ ] 8.4 Set up Tailwind CSS with postcss and tailwind.config.js
- [ ] 8.5 Create axios instance with configuration (API_BASE_URL, default headers)
- [ ] 8.6 Implement axios request interceptor to add Authorization header with JWT
- [ ] 8.7 Implement axios response interceptor to handle 401 (refresh token, retry)
- [ ] 8.8 Set up TanStack Query (React Query) with QueryClientProvider
- [ ] 8.9 Create React Router basic structure with BrowserRouter
- [ ] 8.10 Set up .env.local with API_BASE_URL=http://localhost:8000
- [ ] 8.11 Test: npm run dev starts dev server at localhost:5173

## 9. Zustand State Management

- [ ] 9.1 Create authStore with state: { accessToken, refreshToken, user, isAuthenticated }
- [ ] 9.2 Implement authStore actions: setAuth(token, refreshToken, user), logout(), updateUser()
- [ ] 9.3 Create cartStore with state: { items, personalization, totalPrice }
- [ ] 9.4 Implement cartStore actions: addItem(), removeItem(), updateQuantity(), clearCart()
- [ ] 9.5 Configure persist middleware for cartStore (localStorage key: 'cart-store')
- [ ] 9.6 Create paymentStore with state: { status, paymentId, error } (NO persistence)
- [ ] 9.7 Implement paymentStore actions: setStatus(), setPaymentId(), setError(), reset()
- [ ] 9.8 Create uiStore with state: { modals, notifications, loading }
- [ ] 9.9 Implement uiStore actions: openModal(), closeModal(), addNotification(), removeNotification()
- [ ] 9.10 Add TypeScript types for all stores
- [ ] 9.11 Test: authStore persists/restores to localStorage
- [ ] 9.12 Test: paymentStore does NOT persist after page refresh

## 10. Frontend Hooks & Utilities

- [ ] 10.1 Create useAuth hook that selects from authStore (token, user, isAuthenticated)
- [ ] 10.2 Create useCart hook that selects cartStore items and provides actions
- [ ] 10.3 Create custom hook for API calls that handles loading/error/data states
- [ ] 10.4 Create utility function to check if user has role (hasRole(user, role))
- [ ] 10.5 Create constant definitions (API endpoints, roles, states, etc.)
- [ ] 10.6 Create shared/ui components: Button, Input, Card, Modal stubs (basic, styled with Tailwind)

## 11. Frontend Routing & Guards

- [ ] 11.1 Create ProtectedRoute component that checks authentication
- [ ] 11.2 Create RoleProtectedRoute component that checks role permissions
- [ ] 11.3 Redirect unauthenticated users to /login
- [ ] 11.4 Redirect insufficiently-privileged users to /403
- [ ] 11.5 Create basic pages: LoginPage (stub), DashboardPage (stub), NotFoundPage (404)
- [ ] 11.6 Set up route structure with /api/v1 prefix in frontend API calls

## 12. Integration & Testing

- [ ] 12.1 Create backend test fixtures (FastAPI TestClient, database session, sample data)
- [ ] 12.2 Test UoW pattern atomicity (create with failure on 2nd entity, verify rollback)
- [ ] 12.3 Test BaseRepository CRUD operations
- [ ] 12.4 Test get_current_user dependency with valid/expired/missing token
- [ ] 12.5 Test require_role dependency with sufficient/insufficient permissions
- [ ] 12.6 Test health endpoint GET /api/v1/health returns 200
- [ ] 12.7 Create sample endpoint (e.g., GET /api/v1/self that returns current user)
- [ ] 12.8 Test frontend axios interceptor with mock API
- [ ] 12.9 Test Zustand stores with sample dispatches
- [ ] 12.10 Create integration test: frontend calls /api/v1/self, receives current user

## 13. Documentation & Final Checks

- [ ] 13.1 Update README.md with: tech stack, local setup (docker-compose up, npm install, npm run dev), project structure, architectural patterns
- [ ] 13.2 Create ARCHITECTURE.md documenting: Repository pattern, UoW, JWT auth, RBAC, error handling
- [ ] 13.3 Create API.md documenting all endpoints (currently just /health and /api/v1/self)
- [ ] 13.4 Create DATABASE.md documenting: ERD, seed data, soft delete pattern, audit timestamps
- [ ] 13.5 Add code comments to UoW, Repository, and auth utilities explaining patterns
- [ ] 13.6 Review all code for type hints and mypy compliance (backend)
- [ ] 13.7 Review all code for eslint compliance (frontend)
- [ ] 13.8 Verify .env.example files are complete
- [ ] 13.9 Final checklist: docker-compose up works, migrations run, seed script works, backend starts, frontend starts, health endpoint returns 200
- [ ] 13.10 Create CHANGELOG entry for Sprint 0
