## ADDED Requirements

### Requirement: React 18 with TypeScript strict mode
The system SHALL initialize a React 18 application with TypeScript strict mode enabled for type safety and better IDE support.

#### Scenario: React app starts with TypeScript
- **WHEN** `npm run dev` is executed
- **THEN** the React development server starts and React DevTools can connect

### Requirement: Vite bundler integration
The system SHALL use Vite as the build tool with optimized development and production builds, HMR (Hot Module Replacement) for development, and code splitting for production.

#### Scenario: Development server provides HMR
- **WHEN** a component file is modified
- **THEN** the change is reflected in the browser immediately without full page reload

### Requirement: Tailwind CSS integration
The system SHALL integrate Tailwind CSS with PostCSS and provide pre-configured tailwind.config.js with project-specific color palette and breakpoints.

#### Scenario: Tailwind classes are available
- **WHEN** a component uses Tailwind classes like `className="bg-blue-500 p-4"`
- **THEN** the styles are applied correctly and optimized CSS is generated for production

### Requirement: Axios client with JWT interceptor hooks
The system SHALL provide a configured axios instance with hooks for intercepting requests (to add JWT token) and responses (to handle 401 and refresh token).

#### Scenario: Request interceptor adds JWT token
- **WHEN** an authenticated request is made
- **THEN** the Authorization header is automatically added with the JWT token

### Requirement: TanStack Query (React Query) provider
The system SHALL integrate TanStack Query with default configuration for managing server state, caching, and automatic refetching.

#### Scenario: Query provider is available
- **WHEN** the app starts
- **THEN** QueryClientProvider is set up and hooks like useQuery and useMutation are available

### Requirement: React Router setup
The system SHALL configure React Router with basic route structure supporting public and private (protected) routes.

#### Scenario: Router is initialized
- **WHEN** the app starts
- **THEN** routes are set up and navigation works

### Requirement: Environment configuration
The system SHALL support environment-specific configuration (development, staging, production) with API_BASE_URL pointing to backend.

#### Scenario: API URL is configurable
- **WHEN** the app starts
- **THEN** axios client uses the correct API base URL from environment
