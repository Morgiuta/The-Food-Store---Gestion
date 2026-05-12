## ADDED Requirements

### Requirement: Unit of Work context manager
The system SHALL provide a Unit of Work pattern that uses async context managers (async with) to manage database transactions, automatically committing or rolling back based on exception handling.

#### Scenario: Unit of Work commits on success
- **WHEN** an operation completes successfully within `async with UnitOfWork() as uow:`
- **THEN** all changes are automatically committed to the database

#### Scenario: Unit of Work rolls back on exception
- **WHEN** an exception is raised within the Unit of Work context
- **THEN** all changes are rolled back and the database is unchanged

### Requirement: Atomic multi-entity operations
The system SHALL guarantee that operations involving multiple entities (e.g., creating a pedido with detalles) are fully atomic — all succeed or all fail together.

#### Scenario: Multi-entity creation is atomic
- **WHEN** creating a Pedido with 3 DetallePedido entries fails on the 3rd entry
- **THEN** the entire transaction is rolled back; no Pedido is created and no DetallePedido entries are created

### Requirement: Repository instantiation within Unit of Work
The system SHALL allow repositories to be instantiated within a Unit of Work context and automatically participate in the transaction.

#### Scenario: Repository works within UoW context
- **WHEN** repositories are created inside `async with UnitOfWork() as uow: repo = uow.usuarios`
- **THEN** all repository operations use the same database connection/transaction

### Requirement: Change tracking
The system SHALL track which entities have been modified within the Unit of Work and only persist the modified entities.

#### Scenario: Only modified entities are persisted
- **WHEN** an entity is modified and another is left unchanged
- **THEN** only the modified entity is updated in the database

### Requirement: Transactional consistency
The system SHALL prevent partial updates by ensuring all-or-nothing semantics for grouped operations.

#### Scenario: Partial failure is prevented
- **WHEN** updating stock for 5 products but stock validation fails on the 4th
- **THEN** no products are updated and an exception is raised
