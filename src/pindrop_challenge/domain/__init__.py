"""
Domain Layer - Core business logic and rules.

This package contains the heart of the application's business logic, completely
independent of external frameworks, databases, or UI. It follows Domain-Driven
Design (DDD) principles and includes:

- Entities: Core business objects with identity
- Value Objects: Immutable objects defined by their attributes
- Services: Domain services containing business logic
- Interfaces: Port definitions for external integrations
- Errors: Type-safe error handling with discriminated unions

The domain layer has NO dependencies on the infrastructure or presentation
layers, ensuring the business logic remains pure and testable.

Key Principles:
- Business rules are encoded in the domain
- All operations return discriminated unions (Success/Error)
- Entities and value objects are strongly typed with Pydantic
- Domain services orchestrate complex business operations
"""
