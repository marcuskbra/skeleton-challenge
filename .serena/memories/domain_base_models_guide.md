# Domain Base Models Guide

## Overview
The domain layer provides base classes for all domain entities, value objects, aggregates, and domain events. These base classes enforce consistent configuration and provide common functionality.

## Base Classes

### DomainEntity
**Purpose**: Base for all mutable domain entities with identity.

**Use when**:
- Entity can change after creation
- Entity has a unique identity (ID)
- Entity is part of business logic but not an aggregate root

**Configuration**:
- `validate_assignment=True` - Validates on attribute changes
- `use_enum_values=False` - Keeps enums as enum types, not strings
- `strict=True` - Strict type checking
- `extra="forbid"` - Prevents unexpected fields

**Example**:
```python
from challenge.domain.base_models import DomainEntity

class Customer(DomainEntity):
    customer_id: str
    name: str
    email: str
    status: CustomerStatus
    
    def activate(self) -> None:
        self.status = CustomerStatus.ACTIVE
```

### ImmutableEntity
**Purpose**: Base for immutable domain entities that cannot change after creation.

**Use when**:
- Entity should never change after creation
- Entity represents historical data or events
- Entity is used in event sourcing

**Configuration**: Same as DomainEntity + `frozen=True`

**Example**:
```python
from challenge.domain.base_models import ImmutableEntity

class OrderSnapshot(ImmutableEntity):
    order_id: str
    total_amount: Money
    items: list[OrderItem]
    created_at: datetime
```

### ValueObject
**Purpose**: Base for all value objects (always immutable).

**Use when**:
- Object is defined by its attributes, not identity
- Object should be compared by value, not reference
- Object represents a concept like Money, Email, Address

**Configuration**: Same as ImmutableEntity (frozen=True)

**Example**:
```python
from challenge.domain.base_models import ValueObject

class Address(ValueObject):
    street: str
    city: str
    postal_code: str
    country: str
    
    def format_display(self) -> str:
        return f"{self.street}, {self.city} {self.postal_code}, {self.country}"
```

### AggregateRoot
**Purpose**: Entry point to aggregates with consistency boundaries.

**Use when**:
- Entity is the root of an aggregate
- Entity needs version control (optimistic locking)
- Entity coordinates multiple related entities

**Built-in fields**:
- `id: str` - Unique identifier
- `version: int` - Version for optimistic locking
- `created_at: datetime` - Creation timestamp
- `updated_at: datetime` - Last update timestamp

**Methods**:
- `increment_version()` - Updates version and timestamp

**Example**:
```python
from challenge.domain.base_models import AggregateRoot

class Order(AggregateRoot):
    customer_id: str
    items: list[OrderItem]
    total: Money
    status: OrderStatus
    
    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)
        self.total = self.total.add(item.price)
        self.increment_version()
    
    def submit(self) -> None:
        if not self.items:
            raise ValueError("Cannot submit empty order")
        self.status = OrderStatus.SUBMITTED
        self.increment_version()
```

### DomainEvent
**Purpose**: Represent things that happened in the domain (immutable).

**Use when**:
- Recording domain events for event sourcing
- Publishing events to other services
- Audit trail and history

**Built-in fields**:
- `event_id: str` - Unique event identifier
- `aggregate_id: str` - ID of aggregate that raised event
- `event_type: str` - Type of event
- `occurred_at: datetime` - When event occurred
- `data: Dict[str, Any]` - Event payload

**Example**:
```python
from challenge.domain.base_models import DomainEvent

class OrderSubmittedEvent(DomainEvent):
    def __init__(self, order_id: str, customer_id: str, total: float):
        super().__init__(
            event_id=str(uuid4()),
            aggregate_id=order_id,
            event_type="OrderSubmitted",
            data={
                "customer_id": customer_id,
                "total": total,
            }
        )
```

## Result Types for Error Handling

### Success
**Purpose**: Base class for successful operation results.

**Use when**: Creating success variants in discriminated unions

**Example**:
```python
from challenge.domain.base_models import Success

class CreateOrderSuccess(Success):
    order_id: str
    order: dict
```

### Error
**Purpose**: Base class for operation errors.

**Fields**:
- `success: bool = False` (frozen)
- `error_code: str` - Error code for categorization
- `message: str` - Human-readable error message
- `details: Optional[Dict[str, Any]]` - Additional error details

**Use when**: Creating error variants in discriminated unions

**Example**:
```python
from challenge.domain.base_models import Error

class InsufficientStockError(Error):
    def __init__(self, product_id: str, requested: int, available: int):
        super().__init__(
            error_code="INSUFFICIENT_STOCK",
            message=f"Only {available} units available",
            details={
                "product_id": product_id,
                "requested": requested,
                "available": available,
            }
        )
```

## Common Value Objects

### Email
**Purpose**: Type-safe email address.

**Validation**: Regex pattern for valid email format

**Methods**:
- `domain` property - Get domain part
- `username` property - Get username part

**Example**:
```python
from challenge.domain.base_models import Email

email = Email(value="user@example.com")
print(email.domain)  # "example.com"
print(email.username)  # "user"
```

### Money
**Purpose**: Monetary amounts with currency.

**Fields**:
- `amount: float` - Amount (≥0)
- `currency: str` - ISO 4217 code (3 letters)

**Methods**:
- `add(other: Money) -> Money` - Add same currency
- `subtract(other: Money) -> Money` - Subtract same currency

**Example**:
```python
from challenge.domain.base_models import Money

price = Money(amount=99.99, currency="USD")
tax = Money(amount=10.00, currency="USD")
total = price.add(tax)  # Money(amount=109.99, currency="USD")
```

### DateRange
**Purpose**: Date range with overlap checking.

**Fields**:
- `start_date: datetime`
- `end_date: datetime`

**Methods**:
- `duration_days` property - Duration in days
- `contains(date: datetime) -> bool` - Check if date in range
- `overlaps(other: DateRange) -> bool` - Check overlap

**Example**:
```python
from challenge.domain.base_models import DateRange
from datetime import datetime

range1 = DateRange(
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 1, 31)
)
print(range1.duration_days)  # 30
print(range1.contains(datetime(2024, 1, 15)))  # True
```

## Decision Guide: Which Base to Use?

```
Need identity (ID)? 
├─ Yes → Can it change after creation?
│         ├─ Yes → Is it aggregate root?
│         │         ├─ Yes → AggregateRoot
│         │         └─ No → DomainEntity
│         └─ No → ImmutableEntity
└─ No → ValueObject

Recording something that happened?
└─ Yes → DomainEvent

Operation result?
├─ Success → Success
└─ Error → Error
```

## Best Practices

1. **Always inherit from base classes** - Never create Pydantic models from scratch
2. **Use ValueObjects for concepts** - Money, Email, Address, etc.
3. **Keep aggregates small** - Only include entities that need consistency
4. **Use DomainEvents for history** - Record all significant domain changes
5. **Never modify frozen objects** - Create new instances instead
6. **Validate in constructors** - Use Pydantic validators for business rules
