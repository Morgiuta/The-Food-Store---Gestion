## Context

Food Store begins as a greenfield project with no existing codebase. The team is a group of university students working in sprints. We need a foundation that is:
- Simple enough to learn and implement in 3-4 days
- Scalable enough to support 77 user stories across 9 epics
- Consistent enough that all team members follow the same patterns
- Documented enough that future changes reference established conventions

The entire ecosystem depends on Sprint 0 decisions: backend team uses FastAPI patterns, frontend team uses React structure, and payment/admin teams rely on authentication and authorization patterns established here.

## Goals / Non-Goals

**Goals:**
- Establish working development environment with database, backend API, and frontend client
- Implement core architectural patterns (Repository, Unit of Work) used by all subsequent features
- Set up authentication/authorization infrastructure (JWT, RBAC) that all features depend on
- Create consistent error handling and validation across backend
- Enable parallel development on different features once Sprint 0 is complete
- Provide clear directory structure and naming conventions for consistency

**Non-Goals:**
- Business logic (auth login, product catalog) — those come in later sprints
- Performance optimization — defer caching, indexing, monitoring to later sprints
- Frontend UI polish — use basic layouts; styling refinement happens later
- Advanced features like multi-tenancy, webhooks, messaging — handle in future epics
- Production deployment — focus on local development and CI/CD setup later

## Decisions

### Decision 1: FastAPI + SQLAlchemy ORM + Alembic

**Rationale**: FastAPI provides automatic API documentation, type hints with Pydantic validation, and async support out of the box. SQLAlchemy ORM offers type safety and abstraction over raw SQL. Alembic enables version-controlled schema migrations.

**Alternatives Considered:**
- FastAPI + asyncpg (raw async driver) → More performance, but less abstraction; harder to maintain
- Flask + SQLAlchemy → Simpler to learn, but less async support; requires more manual validation
- Django + ORM → Full framework with batteries included, but overkill for API-only backend

**Trade-off**: Some performance cost vs. massive productivity gain. We prioritize development speed.

### Decision 2: Unit of Work + Generic Repository Pattern

**Rationale**: UoW provides ACID guarantees for multi-entity operations (e.g., creating a pedido with detalles atomically). Generic Repository eliminates CRUD boilerplate across 16 entities. Both are proven patterns in enterprise applications.

**Alternatives Considered:**
- Direct SQLAlchemy queries scattered across routes → No abstraction; hard to maintain; inconsistent
- Individual repo classes per entity → No reuse of CRUD logic; massive code duplication
- Active Record pattern (entity.save()) → Tight coupling; harder to test; no transaction isolation

**Trade-off**: Initial investment in abstraction layers pays off quickly when we reach dozens of CRUD endpoints.

### Decision 3: JWT + Refresh Token Rotation

**Rationale**: JWT is stateless (no server-side session storage needed) and works well with distributed teams. Refresh token rotation reduces impact of token compromise. Access tokens expire in 30 min; refresh tokens rotate on every refresh and expire in 7 days.

**Alternatives Considered:**
- Session-based auth (store in Redis/DB) → Simpler initially, but requires server-side state; doesn't scale
- Long-lived JWTs → Security risk; token compromise gives attacker weeks of access
- OAuth2 via external provider → Adds external dependency; not necessary for university project

**Trade-off**: Refresh token rotation adds complexity but provides security. Session storage would be simpler.

### Decision 4: Zustand for Frontend State Management

**Rationale**: Zustand is minimal (~2.2kb), no boilerplate, supports middleware (persist), and TypeScript-friendly. Perfect for a university project; students can understand the code.

**Alternatives Considered:**
- Redux → Industry standard, but massive boilerplate; overkill for this scope
- MobX → Powerful but steep learning curve
- Pinia (Vue) → Not compatible with React
- Context API → No built-in persistence or devtools; harder to scale

**Trade-off**: Zustand is less mature than Redux, but perfect for our team and timeline.

### Decision 5: PostgreSQL + Soft Delete Pattern

**Rationale**: PostgreSQL is free, robust, and widely used. Soft delete (eliminado_en timestamp) provides data lineage and audit trails without losing historical data.

**Alternatives Considered:**
- Hard delete (DELETE) → Loss of historical data; can't audit; harder to handle foreign key constraints
- MongoDB → Schemaless, but complicates auditing and transactions; team is more comfortable with SQL
- SQLite → Good for local dev, but doesn't scale for production; PostgreSQL handles both

**Trade-off**: Soft delete requires more careful query logic (always filter eliminado_en IS NULL) but preserves audit trail.

### Decision 6: Feature-First Backend, Feature-Sliced Frontend

**Rationale**: Feature-first (backend) and FSD (frontend) enable independent development and clear ownership. Each feature has its domain objects, repositories, and UI components co-located.

**Alternatives Considered:**
- Layer-first (backends /models, /routes, /services) → Hard to extract features; encourages shared logic
- Monolithic folders → No structure; team can't work in parallel without merge conflicts

**Trade-off**: Requires more upfront discipline, but enables parallelization.

### Decision 7: RFC 7807 Error Responses

**Rationale**: Standardized error format helps frontend clients handle errors consistently. Follows HTTP standards and makes debugging easier.

**Alternatives Considered:**
- Custom error format { code, message, data } → Works, but non-standard; frontend must learn custom format
- Just HTTP status codes → Insufficient detail for debugging

**Trade-off**: Slightly more verbose responses, but consistent and standard.

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| **Unit of Work complexity** → Developers misuse context manager | Document usage patterns; provide unit tests; code review first few uses |
| **TypeScript strict mode** → Slower initial development | Strict mode catches errors early; saves debugging later; worth the upfront cost |
| **Soft delete performance** → Every query must filter eliminado_en | Add database indexes on (eliminado_en); queries are cached by ORM |
| **JWT token compromise** → Attacker can use access token for 30 min | Mitigated by short 30-min expiration; refresh rotation reduces refresh token window |
| **Zustand lack of devtools** → Harder to debug state changes | Zustand has browser extension; document state structure clearly |
| **PostgreSQL local setup** → Developers must install & configure | Use Docker Compose file; one command (docker-compose up) spins up DB |
| **Feature-first structure** → Some code naturally belongs in /shared | Establish clear boundaries; PR reviews catch violations |
| **Async/await in FastAPI** → Developers may forget await | Use linters (ruff, mypy) to catch missing await |

## Migration Plan

### Phase 1: Initial Setup (Day 1)
1. Create monorepo structure
2. Initialize FastAPI app with basic middleware and error handlers
3. Configure PostgreSQL locally with Docker Compose
4. Generate ERD v5 with Alembic
5. Run seed script to populate roles and admin user
6. Initialize React + Vite + Tailwind

### Phase 2: Patterns & Infrastructure (Day 2)
1. Implement BaseRepository[T] and UoW pattern
2. Implement JWT generation/validation, get_current_user dependency
3. Implement RBAC (require_role dependency)
4. Configure Zustand stores (authStore, cartStore, paymentStore, uiStore)
5. Set up axios interceptors for JWT token refresh
6. Implement centralized error handling (backend + frontend)

### Phase 3: Integration & Documentation (Day 3)
1. Create sample endpoint (e.g., GET /api/v1/health, GET /api/v1/self) to test auth pipeline
2. Create frontend page that calls health endpoint, demonstrating JWT flow
3. Write README with setup instructions (docker-compose up, npm install, npm run dev)
4. Document architectural patterns in ARCHITECTURE.md
5. Code review and refactoring based on feedback

### Rollback Strategy
- If FastAPI setup fails: revert to Flask with minimal changes
- If UoW introduces too much complexity: remove async context manager, use manual commit/rollback
- If JWT refresh causes issues: revert to simple long-lived tokens (less secure, but simpler)

## Open Questions

1. **Database URL**: Should we commit a docker-compose.yml with hardcoded postgres:5432, or support multiple DB URLs?
   - Decision: Commit docker-compose.yml; environment variables override for production
   
2. **Password hashing cost**: bcrypt cost=12 or higher? Higher is more secure but slower.
   - Decision: cost=12 (default); increase in production if needed
   
3. **Token expiration in testing**: Should tests use real time or mocked time?
   - Decision: Mock time in tests to keep tests fast; use python-freezegun
   
4. **Frontend build output**: dist/ or build/?
   - Decision: dist/ (Vite convention)
   
5. **API versioning**: /api/v1/ or /api/users?
   - Decision: /api/v1/ enables future /api/v2/ without breaking clients
