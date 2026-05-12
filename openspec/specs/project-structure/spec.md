# project-structure Specification

## Purpose
TBD - created by archiving change sprint-0-infraestructura. Update Purpose after archive.
## Requirements
### Requirement: Feature-first backend directory structure
The system SHALL organize backend code using feature-first vertical slicing where each feature has its own directory containing: models, repositories, services, routes, and schemas.

#### Scenario: Feature directory is self-contained
- **WHEN** the backend is structured
- **THEN** a feature like /auth contains auth/models.py, auth/schemas.py, auth/repositories.py, auth/routes.py, auth/services.py

### Requirement: Feature-Sliced Design (FSD) frontend structure
The system SHALL organize frontend code following Feature-Sliced Design with layers: /app, /pages, /features, /entities, /shared, following the hierarchy from general to specific.

#### Scenario: FSD layers are organized
- **WHEN** frontend is structured
- **THEN** components are placed in layers: /app (root app), /pages (page-level), /features (feature components), /entities (domain entities), /shared (global utilities)

### Requirement: Shared utilities and constants
The system SHALL provide a /shared directory with constants, utilities, types, and hooks that are reused across features.

#### Scenario: Shared utilities are centralized
- **WHEN** utility functions are needed across multiple features
- **THEN** they are placed in /shared/lib or /shared/utils and imported from there

### Requirement: Conventional commits
The system SHALL follow conventional commits format: type(scope): subject where type is: feat, fix, docs, style, refactor, test, chore.

#### Scenario: Commits follow convention
- **WHEN** a change is committed
- **THEN** the message follows: "feat(auth): add JWT token refresh" or "fix(cart): prevent duplicate items"

### Requirement: .gitignore configuration
The system SHALL include a .gitignore file excluding: node_modules, dist, build, .env, .env.local, .DS_Store, *.log, __pycache__, venv, .venv.

#### Scenario: Sensitive files are not committed
- **WHEN** environment files or build artifacts are created
- **THEN** they are ignored by git

### Requirement: Environment variables configuration
The system SHALL support environment-specific configuration through .env files with sensible defaults in .env.example.

#### Scenario: Environment config is documented
- **WHEN** developers clone the repo
- **THEN** a .env.example file shows required variables with placeholder values

### Requirement: Dependency management
The system SHALL clearly document dependencies in package.json (frontend) and requirements.txt (backend).

#### Scenario: Dependencies are tracked
- **WHEN** packages are installed
- **THEN** package.json or requirements.txt is updated

