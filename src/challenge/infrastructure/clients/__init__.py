"""
External API Clients - Integration with external services.

This module contains client implementations for communicating with external
services and APIs. These clients handle all the technical details of external
communication while implementing domain interfaces.

Types of clients:
- REST API clients (using httpx or requests)
- GraphQL clients
- gRPC clients
- WebSocket clients
- Database clients
- Message queue clients
- Cloud service SDK wrappers

Client responsibilities:
- HTTP request/response handling
- Authentication and authorization
- Rate limiting and throttling
- Retry logic and circuit breakers
- Request/response transformation
- Error handling and mapping
- Connection pooling
- Timeout management

Best practices:
- Use async/await for I/O operations
- Implement proper error handling
- Add comprehensive logging
- Use connection pooling
- Handle retries with exponential backoff
- Map external errors to domain errors
- Validate responses before returning
- Use type-safe data models (Pydantic)
"""
