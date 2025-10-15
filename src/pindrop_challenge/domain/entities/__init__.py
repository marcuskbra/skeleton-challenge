"""
Domain Entities - Core business objects with identity.

This module contains domain entities, which are objects that have a distinct
identity that runs through time and different states. Unlike value objects,
entities are mutable and are distinguished by their identity rather than their
attributes.

Examples of entities:
- User (identified by user_id)
- Order (identified by order_id)
- Product (identified by SKU or product_id)

Entity characteristics:
- Have a unique identifier (ID)
- Can change over time while maintaining identity
- Two entities with the same attributes but different IDs are different
- Inherit from DomainEntity or AggregateRoot base classes
- Contain business logic relevant to the entity

All entities should:
- Validate their own state
- Enforce business invariants
- Raise domain events when significant changes occur
- Be serializable via Pydantic for persistence
"""
