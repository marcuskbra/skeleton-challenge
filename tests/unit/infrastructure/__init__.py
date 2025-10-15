"""
Infrastructure Unit Tests - Technical implementation testing with mocked I/O.

This package contains unit tests for the infrastructure layer components.
These tests verify the technical implementations while mocking all external
I/O operations to maintain test isolation and speed.

Test coverage areas:
- Repository implementations: Data access logic with mocked databases
- External API clients: HTTP clients with mocked responses
- Message publishers: Queue interactions with mocked brokers
- Cache implementations: Caching logic with mocked stores
- File system operations: File handling with mocked filesystem
- Configuration loaders: Settings and environment parsing
- Adapters and mappers: Data transformation logic

Testing strategies:
- Mock all I/O operations (database, network, filesystem)
- Test error handling and retry logic
- Verify correct API usage and contracts
- Test connection pool management
- Validate request/response transformations
- Test circuit breaker and fallback logic
- Verify logging and monitoring calls

Mocking approaches:
- Use unittest.mock for Python standard library
- Mock at the boundary (repositories, clients)
- Create fake implementations for testing
- Use fixtures for consistent test data
- Mock time and random for deterministic tests

Infrastructure tests ensure technical components
work correctly without requiring actual external resources.
"""
