## Why

Food Store needs a solid technical foundation before building any domain features. Sprint 0 establishes the infrastructure, architectural patterns, and tooling that all subsequent changes will depend on. Without this foundation, we'll accumulate technical debt and face consistency issues across the codebase. This is the critical first sprint that enables all future work.

## What Changes

- **Backend scaffolding**: Initialize FastAPI project with core middleware, CORS, error handling, and documentation endpoints (Swagger/ReDoc)
- **Database setup**: Configure PostgreSQL with Alembic migrations, ERD v5 (16 tables), and seed data for roles and initial admin
- **Data access patterns**: Implement BaseRepository[T] generic pattern and Unit of Work transactional context manager for atomic operations
- **Frontend scaffolding**: Initialize React + TypeScript + Vite with Tailwind CSS, axios client with JWT interceptor template, and TanStack Query
- **State management**: Configure Zustand stores (authStore, cartStore, paymentStore, uiStore) with localStorage persistence
- **Repository structure**: Establish feature-first backend layout and Feature-Sliced Design frontend layout
- **Error handling**: Implement centralized validation and error formatting following RFC 7807

## Capabilities

### New Capabilities

- `fastapi-backend-core`: FastAPI application with middleware stack (CORS, error handlers, logging), OpenAPI documentation, rate limiting infrastructure, and /api/v1 versioning
- `postgresql-database`: PostgreSQL connection, Alembic migrations, ERD v5 schema with 16 tables, soft delete pattern, and audit timestamps
- `repository-pattern`: Generic BaseRepository[T] with CRUD operations, filtering, soft delete support, and composition over inheritance
- `unit-of-work-pattern`: Unit of Work context manager for atomic transactions, commit/rollback semantics, and change tracking
- `react-frontend-core`: React 18 + TypeScript with Vite bundler, Tailwind CSS styling, axios client with interceptor hooks, and TanStack Query provider
- `zustand-state-management`: Zustand stores (auth, cart, payment, ui) with typed actions/selectors, localStorage persistence middleware, and slice subscriptions
- `error-handling-validation`: Centralized Pydantic v2 schemas, input sanitization, RFC 7807 error responses, and validation error formatting
- `jwt-authentication-core`: JWT infrastructure (token generation, validation, refresh token storage) and FastAPI dependency injections (get_current_user, require_role)
- `rbac-foundation`: Role-based access control (ADMIN, STOCK, PEDIDOS, CLIENT) with M2M relationship and protection against last-admin removal
- `project-structure`: Monorepo with feature-first backend directories (/auth, /usuarios, /productos, etc.) and Feature-Sliced Design frontend layers (/app, /pages, /features, /entities, /shared)

### Modified Capabilities

- None (this is the initial sprint, no existing specs to modify)

## Impact

- **Backend**: All backend services depend on FastAPI setup, database connection, and BaseRepository/UoW patterns
- **Frontend**: All frontend pages and features depend on React setup, axios configuration, and Zustand stores
- **Project structure**: Establishes naming conventions, module layouts, and code organization that all future changes must follow
- **Dependencies**: FastAPI, SQLAlchemy, Alembic, Pydantic v2, python-jose, passlib, slowapi (backend); React, Vite, Zustand, TanStack Query, Tailwind CSS, axios (frontend)
- **Testing**: Establishes test infrastructure expectations and patterns for unit tests, integration tests, and fixtures

## User Stories Covered

From Epic 00 (Infraestructura/Technical Foundation):
- US-000: Inicialización del repositorio y estructura del proyecto
- US-000a: Configuración del entorno backend
- US-000b: Configuración de PostgreSQL, migraciones y seed data
- US-000c: Configuración del entorno frontend
- US-000d: Implementación de patrones base (BaseRepository, Unit of Work, dependencias FastAPI)
- US-000e: Configuración de los stores de Zustand
