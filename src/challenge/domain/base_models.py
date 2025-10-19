"""
Base Pydantic models for domain layer.

Following DRY principle to eliminate repeated configuration.
All domain entities and value objects inherit from these bases.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class DomainEntity(BaseModel):
    """
    Base for all mutable domain entities with identity.

    Use this base class when:
    - Entity can change after creation
    - Entity has a unique identity (ID)
    - Entity is part of business logic but not an aggregate root

    Configuration:
    - validate_assignment=True - Validates on attribute changes
    - use_enum_values=False - Keeps enums as enum types, not strings
    - strict=True - Strict type checking
    - extra="forbid" - Prevents unexpected fields

    Example:
        >>> from enum import Enum
        >>> class CustomerStatus(str, Enum):
        ...     ACTIVE = "active"
        ...     INACTIVE = "inactive"
        >>>
        >>> class Customer(DomainEntity):
        ...     customer_id: str
        ...     name: str
        ...     status: CustomerStatus
        ...
        ...     def activate(self) -> None:
        ...         self.status = CustomerStatus.ACTIVE

    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=False,
        strict=True,
        str_strip_whitespace=True,
        extra="forbid",  # Prevent unexpected fields
    )


class ImmutableEntity(BaseModel):
    """
    Base for immutable domain entities that cannot change after creation.

    Use this base class when:
    - Entity should never change after creation
    - Entity represents historical data or events
    - Entity is used in event sourcing or audit logs

    Configuration: Same as DomainEntity + frozen=True

    Example:
        >>> from datetime import datetime
        >>> class OrderSnapshot(ImmutableEntity):
        ...     order_id: str
        ...     total_amount: float
        ...     items: list[dict]
        ...     created_at: datetime
        >>>
        >>> snapshot = OrderSnapshot(
        ...     order_id="ORD-123",
        ...     total_amount=99.99,
        ...     items=[{"id": "1", "qty": 2}],
        ...     created_at=datetime.utcnow()
        ... )
        >>> # snapshot.total_amount = 50.0  # Would raise ValidationError

    """

    model_config = ConfigDict(
        frozen=True,  # Immutable
        validate_assignment=True,
        use_enum_values=False,
        strict=True,
        str_strip_whitespace=True,
        extra="forbid",
    )


class ValueObject(BaseModel):
    """
    Base for all value objects (always immutable).

    Value objects are defined by their attributes rather than identity.
    They are compared by value, not reference, and are always immutable.

    Use this base class when:
    - Object is defined by its attributes, not identity
    - Object should be compared by value equality
    - Object represents a domain concept (Money, Email, Address)

    Configuration: Same as ImmutableEntity (frozen=True)

    Example:
        >>> class Address(ValueObject):
        ...     street: str
        ...     city: str
        ...     postal_code: str
        ...     country: str
        ...
        ...     def format_display(self) -> str:
        ...         return f"{self.street}, {self.city} {self.postal_code}"
        >>>
        >>> addr1 = Address(street="123 Main", city="NYC", postal_code="10001", country="US")
        >>> addr2 = Address(street="123 Main", city="NYC", postal_code="10001", country="US")
        >>> addr1 == addr2  # True - compared by value

    """

    model_config = ConfigDict(
        frozen=True,  # Value objects are always immutable
        validate_assignment=True,
        use_enum_values=False,
        strict=True,
        str_strip_whitespace=True,
        extra="forbid",
    )


class AggregateRoot(DomainEntity):
    """
    Base class for aggregate roots in domain-driven design.

    Aggregate roots are entry points to aggregates and maintain consistency
    boundaries. They coordinate multiple related entities as a single unit.

    Use this base class when:
    - Entity is the root of an aggregate
    - Entity needs version control (optimistic locking)
    - Entity coordinates multiple related entities

    Built-in fields:
    - id: str - Unique identifier
    - version: int - Version for optimistic locking (default: 1)
    - created_at: datetime - Creation timestamp
    - updated_at: datetime - Last update timestamp

    Methods:
    - increment_version() - Updates version and timestamp

    Example:
        >>> from pydantic import Field
        >>> class Order(AggregateRoot):
        ...     customer_id: str
        ...     items: list[dict] = Field(default_factory=list)
        ...     total: float = 0.0
        ...     status: str = "draft"
        ...
        ...     def add_item(self, item: dict) -> None:
        ...         self.items.append(item)
        ...         self.total += item["price"]
        ...         self.increment_version()
        ...
        ...     def submit(self) -> None:
        ...         if not self.items:
        ...             raise ValueError("Cannot submit empty order")
        ...         self.status = "submitted"
        ...         self.increment_version()

    """

    id: str = Field(..., description="Unique identifier for the aggregate")
    version: int = Field(default=1, description="Version for optimistic locking")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def increment_version(self) -> None:
        """Increment version for optimistic locking."""
        self.version += 1
        self.updated_at = datetime.now(timezone.utc)


class DomainEvent(ImmutableEntity):
    """
    Base class for domain events.

    Domain events represent things that happened in the domain. They are
    always immutable and used for event sourcing, audit trails, and history.

    Use this base class when:
    - Recording domain events for event sourcing
    - Publishing events to other services
    - Creating audit trail and history

    Built-in fields:
    - event_id: str - Unique event identifier
    - aggregate_id: str - ID of aggregate that raised event
    - event_type: str - Type of event (e.g., "OrderSubmitted")
    - occurred_at: datetime - When event occurred
    - data: Dict[str, Any] - Event payload

    Example:
        >>> from uuid import uuid4
        >>> class OrderSubmittedEvent(DomainEvent):
        ...     def __init__(self, order_id: str, customer_id: str, total: float):
        ...         super().__init__(
        ...             event_id=str(uuid4()),
        ...             aggregate_id=order_id,
        ...             event_type="OrderSubmitted",
        ...             data={"customer_id": customer_id, "total": total}
        ...         )

    """

    event_id: str = Field(..., description="Unique event identifier")
    aggregate_id: str = Field(..., description="ID of the aggregate that raised the event")
    event_type: str = Field(..., description="Type of the event")
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    data: Dict[str, Any] = Field(default_factory=dict, description="Event payload")


# ============================================================================
# Result Types for Type-Safe Error Handling
# ============================================================================


class Success(BaseModel):
    """
    Base class for successful operation results in discriminated unions.

    Use when creating success variants for type-safe error handling.

    Example:
        >>> class CreateOrderSuccess(Success):
        ...     order_id: str
        ...     order: dict
        >>>
        >>> CreateOrderResult = Union[CreateOrderSuccess, ValidationError, ConflictError]

    """

    success: bool = Field(default=True, frozen=True)

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )


class Error(BaseModel):
    """
    Base class for operation errors in discriminated unions.

    Fields:
    - success: bool = False (frozen)
    - error_code: str - Error code for categorization
    - message: str - Human-readable error message
    - details: Optional[Dict[str, Any]] - Additional error context

    Use when creating error variants for type-safe error handling.

    Example:
        >>> class InsufficientStockError(Error):
        ...     def __init__(self, product_id: str, requested: int, available: int):
        ...         super().__init__(
        ...             error_code="INSUFFICIENT_STOCK",
        ...             message=f"Only {available} units available",
        ...             details={
        ...                 "product_id": product_id,
        ...                 "requested": requested,
        ...                 "available": available,
        ...             }
        ...         )

    """

    success: bool = Field(default=False, frozen=True)
    error_code: str = Field(..., description="Error code for categorization")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )


# ============================================================================
# Common Value Objects
# ============================================================================


class Email(ValueObject):
    """
    Value object representing a type-safe email address.

    Validation: Regex pattern ensures valid email format.

    Properties:
    - domain: Get domain part of email
    - username: Get username part of email

    Example:
        >>> email = Email(value="user@example.com")
        >>> print(email.domain)  # "example.com"
        >>> print(email.username)  # "user"
        >>> str(email)  # "user@example.com"

    """

    value: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")

    def __str__(self) -> str:
        return self.value

    @property
    def domain(self) -> str:
        """Get the domain part of the email."""
        return self.value.split("@")[1]

    @property
    def username(self) -> str:
        """Get the username part of the email."""
        return self.value.split("@")[0]


class Money(ValueObject):
    """
    Value object representing a monetary amount with currency.

    Fields:
    - amount: float (≥0) - Amount in smallest unit
    - currency: str - ISO 4217 currency code (3 letters, e.g., "USD")

    Methods:
    - add(other: Money) -> Money - Add same currency amounts
    - subtract(other: Money) -> Money - Subtract same currency amounts

    Example:
        >>> price = Money(amount=99.99, currency="USD")
        >>> tax = Money(amount=10.00, currency="USD")
        >>> total = price.add(tax)
        >>> print(total)  # "USD 109.99"

    """

    amount: float = Field(..., ge=0, description="Amount in the smallest unit (cents)")
    currency: str = Field(..., pattern=r"^[A-Z]{3}$", description="ISO 4217 currency code")

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"

    def add(self, other: "Money") -> "Money":
        """Add two money values (must be same currency)."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def subtract(self, other: "Money") -> "Money":
        """Subtract two money values (must be same currency)."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot subtract {other.currency} from {self.currency}")
        if self.amount < other.amount:
            raise ValueError("Result would be negative")
        return Money(amount=self.amount - other.amount, currency=self.currency)


class DateRange(ValueObject):
    """
    Value object representing a date range with overlap checking.

    Fields:
    - start_date: datetime - Range start
    - end_date: datetime - Range end

    Properties:
    - duration_days: int - Duration in days

    Methods:
    - contains(date: datetime) -> bool - Check if date in range
    - overlaps(other: DateRange) -> bool - Check if ranges overlap

    Example:
        >>> from datetime import datetime
        >>> range1 = DateRange(
        ...     start_date=datetime(2024, 1, 1),
        ...     end_date=datetime(2024, 1, 31)
        ... )
        >>> print(range1.duration_days)  # 30
        >>> range1.contains(datetime(2024, 1, 15))  # True

    """

    start_date: datetime = Field(...)
    end_date: datetime = Field(...)

    @property
    def duration_days(self) -> int:
        """Get duration in days."""
        return (self.end_date - self.start_date).days

    def contains(self, date: datetime) -> bool:
        """Check if a date is within this range."""
        return self.start_date <= date <= self.end_date

    def overlaps(self, other: "DateRange") -> bool:
        """Check if this range overlaps with another."""
        return not (self.end_date < other.start_date or self.start_date > other.end_date)
