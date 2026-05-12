## ADDED Requirements

### Requirement: JWT token generation
The system SHALL generate JWT access tokens with payload: userId, email, roles, expiresIn: 30 minutes.

#### Scenario: Access token is created on login
- **WHEN** a user logs in successfully
- **THEN** a JWT access token is generated with 30-minute expiration

### Requirement: JWT token validation
The system SHALL validate JWT tokens by verifying the signature and expiration time.

#### Scenario: Valid token is accepted
- **WHEN** a request includes a valid, non-expired JWT token
- **THEN** the token is validated and decoded successfully

#### Scenario: Expired token is rejected
- **WHEN** a request includes an expired JWT token
- **THEN** validation fails and 401 Unauthorized is returned

### Requirement: Refresh token storage
The system SHALL generate and store refresh tokens in the database with expiration (7 days), allowing token rotation.

#### Scenario: Refresh token is persisted
- **WHEN** a user logs in
- **THEN** a refresh token is generated and stored in refresh_tokens table with expiresAt = now + 7 days

### Requirement: get_current_user dependency
The system SHALL provide a FastAPI dependency `get_current_user` that extracts and validates the JWT token from the Authorization header and returns the current User object.

#### Scenario: Dependency injects current user
- **WHEN** an endpoint uses `current_user: User = Depends(get_current_user)`
- **THEN** FastAPI extracts the JWT from Authorization header, validates it, and injects the User object

#### Scenario: Missing token returns 401
- **WHEN** an endpoint using get_current_user is called without an Authorization header
- **THEN** 401 Unauthorized is returned

### Requirement: require_role dependency factory
The system SHALL provide a dependency factory `require_role(*roles)` that validates the current user has one of the specified roles.

#### Scenario: RBAC validation
- **WHEN** an endpoint uses `Depends(require_role('ADMIN', 'STOCK'))`
- **THEN** if the current user has ADMIN or STOCK role, the endpoint is called; otherwise 403 Forbidden is returned

### Requirement: Token claims extraction
The system SHALL decode JWT tokens and provide utility functions to extract claims (userId, email, roles).

#### Scenario: Claims are extracted from token
- **WHEN** a JWT token is decoded
- **THEN** userId, email, and roles array can be accessed
