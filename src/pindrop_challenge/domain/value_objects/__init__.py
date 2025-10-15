"""
Domain Value Objects - Immutable objects defined by their attributes.

This module contains value objects, which are immutable objects that are defined
by their attributes rather than a unique identity. Two value objects with the
same attributes are considered equal.

Examples of value objects:
- Email (defined by the email address string)
- Money (defined by amount and currency)
- Address (defined by street, city, postal code, etc.)
- DateRange (defined by start and end dates)
- Coordinates (defined by latitude and longitude)

Value object characteristics:
- Immutable (cannot be changed after creation)
- No identity - equality based on attributes
- Can be freely shared and copied
- Should be small and focused
- Contain validation logic for their attributes
- Inherit from ValueObject base class (frozen Pydantic model)

All value objects should:
- Validate their data on construction
- Provide useful methods for working with the data
- Be comparable based on their attributes
- Be hashable (since they're immutable)
- Have no side effects
"""