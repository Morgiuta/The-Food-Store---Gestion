# repository-pattern Specification

## Purpose
TBD - created by archiving change sprint-0-infraestructura. Update Purpose after archive.
## Requirements
### Requirement: Generic BaseRepository[T] pattern
The system SHALL provide a generic BaseRepository[T] class that implements standard CRUD operations (create, read, update, delete, list) for any entity type T without code duplication.

#### Scenario: Create operation
- **WHEN** repository.create(entity) is called
- **THEN** the entity is persisted and returned with an assigned ID

#### Scenario: Read operation
- **WHEN** repository.get_by_id(id) is called
- **THEN** the entity is retrieved or None is returned if not found

#### Scenario: List with filtering
- **WHEN** repository.list(filters) is called
- **THEN** entities matching the filter criteria are returned (respecting pagination skip/limit)

#### Scenario: Update operation
- **WHEN** repository.update(id, updates) is called
- **THEN** the entity is updated with the provided fields and returned

#### Scenario: Delete with soft delete
- **WHEN** repository.delete(id) is called on an entity with eliminado_en field
- **THEN** the entity is soft deleted (eliminado_en is set to current timestamp)

### Requirement: Repository composition
The system SHALL allow repositories to be composed/inherited for specific entity logic without redefining CRUD operations.

#### Scenario: Specific repository extends BaseRepository
- **WHEN** UsuarioRepository extends BaseRepository[Usuario]
- **THEN** all BaseRepository methods are available and can be extended with custom logic

### Requirement: Filtering and pagination
The system SHALL support flexible filtering (field-based and custom predicates) and pagination (skip, limit) in list operations.

#### Scenario: Paginated results
- **WHEN** repository.list(skip=10, limit=20) is called
- **THEN** entities 10-30 are returned and total count is provided

### Requirement: Transaction-aware repositories
The system SHALL allow repositories to be used within a Unit of Work context for atomic multi-entity operations.

#### Scenario: Repository works within UoW
- **WHEN** repository is instantiated within a Unit of Work context
- **THEN** all repository operations participate in the same transaction

