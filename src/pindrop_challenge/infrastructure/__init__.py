"""
Infrastructure Layer - External dependencies and integrations.

This package contains all the technical details and external integrations that
support the domain layer. It provides concrete implementations of the interfaces
defined in the domain layer, handling all interactions with the outside world.

Components:
- Database repositories (PostgreSQL, MongoDB, etc.)
- External API clients (REST, GraphQL, gRPC)
- Message queues (RabbitMQ, Kafka, etc.)
- Cache implementations (Redis, Memcached)
- File system operations
- Email/SMS providers
- Cloud service integrations (AWS, Azure, GCP)
- Configuration management

Key responsibilities:
- Implement domain interfaces with concrete technologies
- Handle data persistence and retrieval
- Manage external service communications
- Provide technical capabilities to the domain
- Convert between domain models and external formats

Infrastructure principles:
- Depends on domain layer (implements interfaces)
- Never called directly by domain layer
- Can use any external library or framework
- Handles all I/O operations
- Manages transactions and connections
- Provides resilience (retries, circuit breakers)
"""