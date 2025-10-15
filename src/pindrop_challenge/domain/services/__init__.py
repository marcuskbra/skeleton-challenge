"""
Domain Services - Business logic that doesn't belong to a single entity.

This module contains domain services, which encapsulate business logic that
doesn't naturally fit within a single entity or value object. Domain services
are stateless and coordinate operations between multiple domain objects.

Examples of domain services:
- PaymentService (coordinates payment processing)
- PricingService (calculates prices based on business rules)
- NotificationService (handles business notification logic)
- ValidationService (complex validation across entities)

Domain service characteristics:
- Stateless (no instance variables storing state)
- Contain business logic spanning multiple entities
- Named after activities or operations (verbs rather than nouns)
- Return discriminated unions (Success/Error types)
- Depend on interfaces, not concrete implementations

All domain services should:
- Accept domain objects as parameters
- Return domain objects or discriminated unions
- Never depend on infrastructure details
- Use dependency injection for external capabilities
- Be easily testable with mock dependencies
- Orchestrate complex business workflows
"""
