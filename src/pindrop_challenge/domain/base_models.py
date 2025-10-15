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
    Base for all mutable domain entities.

    Provides standard configuration for domain entities that can change
    after creation. Used for aggregates and entities with identity.
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
    Base for immutable domain entities.

    Provides standard configuration for domain entities that cannot change
    after creation. Ensures immutability through frozen=True.
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
    They are always immutable and provide value equality semantics.
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

    Aggregate roots are the entry points to aggregates and handle
    consistency boundaries.
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

    Domain events represent something that happened in the domain.
    They are always immutable.
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
    """Base class for successful operation results."""

    success: bool = Field(default=True, frozen=True)

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )


class Error(BaseModel):
    """Base class for operation errors."""

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
    """Value object representing an email address."""

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
    """Value object representing a monetary amount."""

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
    """Value object representing a date range."""

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
