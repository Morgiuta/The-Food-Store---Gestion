# error-handling-validation Specification

## Purpose
TBD - created by archiving change sprint-0-infraestructura. Update Purpose after archive.
## Requirements
### Requirement: Pydantic v2 validation schemas
The system SHALL use Pydantic v2 for request/response validation with separate schemas per entity for different operations (Create, Update, Read).

#### Scenario: Create schema differs from Update schema
- **WHEN** creating a user, email is required; when updating, email can be optional
- **THEN** UserCreate requires email, UserUpdate makes it optional
- **WHEN** validation fails
- **THEN** FastAPI automatically returns 422 with detailed error info

### Requirement: RFC 7807 error responses
The system SHALL return all errors in RFC 7807 JSON format with fields: type, title, status, detail, instance.

#### Scenario: Validation error returns RFC 7807
- **WHEN** an invalid request is sent (e.g., missing required field)
- **THEN** response is HTTP 422 with: { type: "about:blank", title: "Validation Error", status: 422, detail: "...", instance: "/api/v1/users" }

### Requirement: Input sanitization
The system SHALL sanitize all text inputs to prevent XSS attacks by stripping HTML tags and dangerous characters from user-provided strings.

#### Scenario: HTML tags are stripped from user input
- **WHEN** a user provides input "<script>alert('xss')</script>"
- **THEN** the system stores/returns it sanitized, or rejects it based on content policy

### Requirement: Custom validation logic
The system SHALL allow defining custom validators on Pydantic models for complex validation rules (e.g., price > 0, stock >= 0).

#### Scenario: Negative prices are rejected
- **WHEN** creating a product with price = -10
- **THEN** validation fails with clear error message

### Requirement: Centralized error handling
The system SHALL provide exception handlers for common error types (ValidationError, NotFoundError, ForbiddenError, ConflictError, ServerError) that return consistent RFC 7807 responses.

#### Scenario: 404 error returns standard format
- **WHEN** a resource is not found
- **THEN** a 404 NotFoundError is caught and returned as RFC 7807 { status: 404, title: "Not Found", ... }

### Requirement: Error logging
The system SHALL log all errors with severity levels (info, warning, error) including request context for debugging.

#### Scenario: Errors are logged with context
- **WHEN** a server error occurs
- **THEN** a log entry includes: timestamp, error type, message, request path, user ID (if available)

