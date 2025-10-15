"""
Domain Unit Tests - Pure business logic testing.

This package contains unit tests for the domain layer, which is the heart
of the application containing all business logic and rules. These tests
verify the correctness of domain entities, value objects, domain services,
and business rule enforcement.

Test coverage areas:
- Domain entities: State transitions, invariants, business rules
- Value objects: Immutability, equality, validation
- Domain services: Business operations, calculations, algorithms
- Domain events: Event creation, handling, propagation
- Aggregates: Consistency boundaries, transactional integrity
- Specifications: Business rule evaluation

Testing principles for domain:
- No external dependencies (pure Python)
- Test business logic, not implementation
- Focus on behavior and outcomes
- Test invariant protection
- Verify state transitions
- Test edge cases and boundary conditions
- Use domain language in test names

Example test patterns:
- Given-When-Then for behavior tests
- Property-based testing for invariants
- Parameterized tests for similar scenarios
- Builder pattern for complex test data

The domain layer tests should have the highest
coverage as they protect the core business logic.
"""
