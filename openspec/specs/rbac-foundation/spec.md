# rbac-foundation Specification

## Purpose
TBD - created by archiving change sprint-0-infraestructura. Update Purpose after archive.
## Requirements
### Requirement: Role entity and seeding
The system SHALL define roles (ADMIN, STOCK, PEDIDOS, CLIENT) and seed them into the database during initialization.

#### Scenario: Roles are available in database
- **WHEN** seed script runs
- **THEN** all four roles are created in the roles table (or skipped if already exist)

### Requirement: User-Role M2M relationship
The system SHALL support many-to-many relationship between usuarios and roles, allowing a user to have multiple roles.

#### Scenario: User can have multiple roles
- **WHEN** a user is assigned roles ADMIN and STOCK
- **THEN** the usuario_rol junction table has two entries for this user

### Requirement: Unique role per user
The system SHALL enforce that each user-role combination is unique (no duplicate role assignments).

#### Scenario: Duplicate role assignment is rejected
- **WHEN** attempting to assign the same role to a user twice
- **THEN** a constraint violation occurs or application logic rejects it

### Requirement: Role-based access control (RBAC)
The system SHALL implement RBAC where endpoint access is controlled by user roles. Endpoints can specify required roles.

#### Scenario: RBAC protects endpoints
- **WHEN** a STOCK role user attempts to access an ADMIN-only endpoint
- **THEN** 403 Forbidden is returned

### Requirement: Protection against last admin removal
The system SHALL prevent removing the last ADMIN role from the system to avoid lockout.

#### Scenario: Last ADMIN cannot be removed
- **WHEN** attempting to revoke ADMIN role from the only user with ADMIN
- **THEN** the operation is rejected with error message "Cannot remove last ADMIN"

### Requirement: Role assignment endpoints
The system SHALL provide endpoints for ADMIN to assign and revoke roles for other users (PUT /api/v1/admin/usuarios/{id}/roles).

#### Scenario: Admin can assign roles
- **WHEN** ADMIN calls PUT /api/v1/admin/usuarios/{user_id}/roles with roles: ["CLIENT", "STOCK"]
- **THEN** the user's roles are updated to CLIENT and STOCK

### Requirement: Role information in JWT
The system SHALL include user roles in the JWT token for quick authorization checks on every request.

#### Scenario: Roles are in JWT claims
- **WHEN** a user token is decoded
- **THEN** roles array is present in the token payload

