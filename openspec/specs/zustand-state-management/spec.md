# zustand-state-management Specification

## Purpose
TBD - created by archiving change sprint-0-infraestructura. Update Purpose after archive.
## Requirements
### Requirement: authStore for authentication state
The system SHALL provide a Zustand store managing authentication state: accessToken, refreshToken, user data, and authentication status.

#### Scenario: authStore holds token and user
- **WHEN** a user logs in
- **THEN** authStore.setAuth() stores accessToken, refreshToken, and user object
- **WHEN** authStore.getToken() is called
- **THEN** the current accessToken is returned

### Requirement: cartStore for shopping cart
The system SHALL provide a Zustand store managing shopping cart state: items array, quantities, personalization (excluded ingredients), and totals. Cart state SHALL persist to localStorage.

#### Scenario: Cart persists to localStorage
- **WHEN** items are added to cart
- **THEN** the cart state is saved to localStorage with key 'cart-store'
- **WHEN** the browser is refreshed
- **THEN** the cart state is restored from localStorage

### Requirement: paymentStore for payment operations
The system SHALL provide a Zustand store managing payment state: payment status, payment ID, error messages. This store SHALL NOT persist to localStorage (session-only).

#### Scenario: Payment state is session-only
- **WHEN** a payment is processed
- **THEN** paymentStore.setPaymentStatus('processing') updates the state
- **WHEN** the browser is refreshed
- **THEN** the payment state is cleared (no persistence)

### Requirement: uiStore for UI state
The system SHALL provide a Zustand store managing transient UI state: modals, sidebars, notifications, loading states.

#### Scenario: UI state manages modal visibility
- **WHEN** uiStore.openModal('product-detail') is called
- **THEN** uiStore.isModalOpen('product-detail') returns true

### Requirement: Typed selectors
The system SHALL provide typed selector functions for accessing store state to enable React component optimization with shallow equality.

#### Scenario: Selectors enable granular subscriptions
- **WHEN** a component uses `const token = authStore((s) => s.accessToken)`
- **THEN** the component only re-renders when the accessToken changes, not when other parts of authStore change

### Requirement: Middleware support
The system SHALL support Zustand middleware (persist, devtools) with proper configuration for each store.

#### Scenario: Persist middleware saves to localStorage
- **WHEN** cartStore is initialized with persist middleware
- **THEN** state is automatically saved to localStorage on every change

### Requirement: Actions and state separation
The system SHALL organize store exports to separate state (getters) from actions (setters) for clear intent.

#### Scenario: Store provides clear action names
- **WHEN** authStore is used
- **THEN** actions like setAuth(), logout(), updateUser() are clearly named and typed

