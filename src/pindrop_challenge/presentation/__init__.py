"""
Presentation Layer - User interfaces and external communication.

This package contains all user-facing interfaces and adapters that allow
external systems and users to interact with the application. It translates
between the external world's format and the domain's format.

Interface types:
- REST APIs (FastAPI, Flask, Django REST)
- GraphQL endpoints
- CLI commands (Click, Typer)
- Web interfaces (templates, SPAs)
- WebSocket handlers
- gRPC services
- Message queue consumers
- Scheduled jobs/cron handlers

Key responsibilities:
- Handle HTTP requests/responses
- Validate input data
- Transform data between external and domain formats
- Handle authentication and authorization
- Manage sessions and state
- Format responses (JSON, XML, HTML)
- Handle errors and return appropriate status codes
- Document API endpoints (OpenAPI/Swagger)

Presentation principles:
- Thin layer - minimal business logic
- Delegates all business operations to domain services
- Handles only presentation concerns
- Transforms between external DTOs and domain models
- Manages request/response lifecycle
- Provides API documentation
- Implements rate limiting and security

The presentation layer depends on both domain and infrastructure layers,
orchestrating them to fulfill user requests.
"""