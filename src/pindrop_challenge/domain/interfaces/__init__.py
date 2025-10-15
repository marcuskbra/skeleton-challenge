"""
Domain Interfaces - Port definitions for external integrations.

This module contains abstract interfaces (ports) that define contracts for
external services and infrastructure. These interfaces follow the Dependency
Inversion Principle, allowing the domain layer to define what it needs without
depending on concrete implementations.

Examples of interfaces:
- Repository interfaces (UserRepository, OrderRepository)
- External service interfaces (EmailService, PaymentGateway)
- Event publisher interfaces (EventBus, MessageQueue)
- Cache interfaces (CacheService)

Interface characteristics:
- Abstract base classes (using ABC)
- Define method signatures without implementation
- Use domain objects in method signatures, not primitives
- Return domain objects or discriminated unions
- No infrastructure-specific types or imports

Benefits of interfaces:
- Domain remains independent of infrastructure
- Easy to test with mock implementations
- Can swap implementations without changing domain
- Clear contracts between layers
- Supports multiple implementations (e.g., different databases)

The infrastructure layer provides concrete implementations of these interfaces.
"""
