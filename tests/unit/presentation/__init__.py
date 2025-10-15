"""
Presentation Unit Tests - Interface and controller testing with mocked services.

This package contains unit tests for the presentation layer, which handles
all user-facing interfaces and external communication. Tests verify request
handling, response formatting, and proper delegation to domain services.

Test coverage areas:
- API endpoints: Request validation, response formatting, status codes
- CLI commands: Argument parsing, output formatting, error messages
- Controllers: Request routing, service orchestration, error handling
- Serializers: Data transformation between external and domain formats
- Middleware: Authentication, authorization, request processing
- WebSocket handlers: Connection management, message handling
- GraphQL resolvers: Query and mutation logic

Testing approaches:
- Mock all domain services and repositories
- Test request validation and sanitization
- Verify correct HTTP status codes
- Test error response formatting
- Validate API contract compliance
- Test pagination and filtering logic
- Verify rate limiting and throttling

Key testing patterns:
- Mock services at interface boundaries
- Test input validation thoroughly
- Verify authorization checks
- Test content negotiation
- Validate CORS and security headers
- Test API versioning logic
- Verify OpenAPI/Swagger compliance

Presentation tests ensure external interfaces
behave correctly without invoking business logic.
"""