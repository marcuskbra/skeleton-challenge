# Test Builders Pattern Guide

## Overview
The test builders pattern provides a flexible, maintainable way to create test data using the Builder pattern. All builders are in `tests/builders.py`.

## Why Use Builders?

**Problems with Raw Test Data**:
```python
# ❌ Hard to maintain, duplicated, brittle
def test_create_order():
    order = {
        "id": "123",
        "customer_id": "456",
        "items": [{"id": "1", "qty": 2}],
        "total": 99.99,
        "created_at": "2024-01-01T00:00:00Z"
    }
```

**Benefits of Builder Pattern**:
```python
# ✅ Reusable, readable, maintainable
def test_create_order():
    order = entity().with_id("123").build()
```

## Available Builders

### 1. EntityBuilder
**Purpose**: Create test domain entities with sensible defaults.

**Factory function**: `entity()`

**Default values**:
- `id`: Random UUID
- `name`: "Test Entity"
- `description`: "Test entity description"
- `created_at`: Current UTC timestamp
- `updated_at`: Current UTC timestamp
- `is_active`: True
- `metadata`: Empty dict

**Methods**:
- `with_id(entity_id: str)` - Set entity ID
- `with_name(name: str)` - Set entity name
- `with_description(description: str)` - Set description
- `with_metadata(metadata: Dict[str, Any])` - Set metadata
- `inactive()` - Mark as inactive
- `created_at(timestamp: datetime)` - Set creation time
- `build()` - Build single entity
- `build_many(count: int, modifier=None)` - Build multiple entities

**Examples**:
```python
from tests.builders import entity

# Simple entity
test_entity = entity().build()

# Customized entity
custom_entity = (
    entity()
    .with_name("Important Entity")
    .with_metadata({"priority": "high"})
    .inactive()
    .build()
)

# Multiple entities
entities = entity().build_many(10)

# Multiple with modifications
entities = entity().build_many(
    5,
    modifier=lambda data, i: {**data, "name": f"Entity {i}"}
)
```

### 2. ValueObjectBuilder
**Purpose**: Create test value objects.

**Factory function**: `value_object()`

**Default values**:
- `value`: None
- `unit`: None
- `precision`: 2

**Methods**:
- `with_value(value: Any)` - Set the value
- `with_unit(unit: str)` - Set the unit
- `with_precision(precision: int)` - Set precision

**Examples**:
```python
from tests.builders import value_object

temperature = (
    value_object()
    .with_value(25.5)
    .with_unit("celsius")
    .with_precision(1)
    .build()
)
```

### 3. RequestBuilder
**Purpose**: Create test API requests.

**Factory function**: `request()`

**Default values**:
- `method`: "POST"
- `endpoint`: "/api/v1/test"
- `headers`: {"Content-Type": "application/json"}
- `body`: Empty dict
- `query_params`: Empty dict

**Methods**:
- `get(endpoint: str)` - Set as GET request
- `post(endpoint: str)` - Set as POST request
- `with_header(key: str, value: str)` - Add header
- `with_body(body: Dict[str, Any])` - Set request body
- `with_query(params: Dict[str, str])` - Set query params
- `with_auth(token: str)` - Add Bearer token

**Examples**:
```python
from tests.builders import request

# GET request
get_req = request().get("/api/v1/orders/123").build()

# POST request with auth
post_req = (
    request()
    .post("/api/v1/orders")
    .with_body({"customer_id": "456", "items": []})
    .with_auth("my-token-123")
    .build()
)

# Custom headers
custom_req = (
    request()
    .post("/api/v1/upload")
    .with_header("Content-Type", "multipart/form-data")
    .with_body({"file": "data"})
    .build()
)
```

### 4. ResponseBuilder
**Purpose**: Create test API responses.

**Factory function**: `response()`

**Default values**:
- `status_code`: 200
- `headers`: {"Content-Type": "application/json"}
- `body`: Empty dict
- `elapsed`: 0.1

**Methods**:
- `with_status(status_code: int)` - Set status code
- `success(data: Any = None)` - Set as successful response
- `error(message: str, status_code: int = 400)` - Set as error response
- `not_found()` - Set as 404
- `unauthorized()` - Set as 401

**Examples**:
```python
from tests.builders import response

# Success response
success_resp = response().success(data={"id": "123"}).build()

# Error response
error_resp = response().error("Invalid input", 400).build()

# 404 response
not_found_resp = response().not_found().build()

# Custom response
custom_resp = (
    response()
    .with_status(201)
    .success(data={"created": True})
    .build()
)
```

### 5. ConfigBuilder
**Purpose**: Create test configurations.

**Factory function**: `config()`

**Default values**:
- `environment`: "test"
- `debug`: True
- `log_level`: "DEBUG"
- `database_url`: "sqlite:///:memory:"
- `cache_enabled`: False
- `features`: Empty dict

**Methods**:
- `production()` - Set production config
- `development()` - Set development config
- `with_database(url: str)` - Set database URL
- `with_cache(enabled: bool = True)` - Enable/disable cache
- `with_feature(name: str, enabled: bool = True)` - Set feature flag

**Examples**:
```python
from tests.builders import config

# Test config (default)
test_cfg = config().build()

# Production config
prod_cfg = config().production().build()

# Development with features
dev_cfg = (
    config()
    .development()
    .with_feature("beta_ui", True)
    .with_feature("new_algorithm", False)
    .build()
)

# Custom database
db_cfg = config().with_database("postgresql://localhost/test").build()
```

### 6. ErrorBuilder
**Purpose**: Create test error objects.

**Factory function**: `error()`

**Default values**:
- `type`: "GenericError"
- `message`: "An error occurred"
- `code`: "ERR_GENERIC"
- `details`: Empty dict
- `timestamp`: Current UTC timestamp

**Methods**:
- `validation_error(field: str, message: str)` - Create validation error
- `not_found(resource: str)` - Create not found error
- `permission_denied(action: str)` - Create permission error

**Examples**:
```python
from tests.builders import error

# Generic error
generic_err = error().build()

# Validation error
validation_err = (
    error()
    .validation_error("email", "Invalid format")
    .build()
)

# Not found error
not_found_err = error().not_found("Order").build()

# Permission error
permission_err = error().permission_denied("delete_order").build()
```

## Base Builder Class

All builders inherit from `Builder` base class with common methods:

**Methods**:
- `with_field(name: str, value: Any)` - Set any field
- `build()` - Build single object
- `build_many(count: int, modifier=None)` - Build multiple objects

**Example**:
```python
# Using with_field for custom fields
custom = entity().with_field("custom_prop", "value").build()

# Using build_many with modifier
entities = entity().build_many(
    3,
    modifier=lambda data, i: {**data, "name": f"Entity-{i}"}
)
```

## Testing Patterns

### Pattern 1: Arrange-Act-Assert with Builders
```python
def test_create_order():
    # Arrange
    customer = entity().with_name("John Doe").build()
    order_data = {
        "customer_id": customer["id"],
        "items": [{"id": "1", "qty": 2}]
    }
    
    # Act
    result = create_order(order_data)
    
    # Assert
    assert result["customer_id"] == customer["id"]
```

### Pattern 2: Fixture with Builders
```python
import pytest
from tests.builders import entity

@pytest.fixture
def test_customer():
    return entity().with_name("Test Customer").build()

@pytest.fixture
def inactive_customer(test_customer):
    test_customer["is_active"] = False
    return test_customer

def test_activate_customer(inactive_customer):
    result = activate(inactive_customer["id"])
    assert result["is_active"] is True
```

### Pattern 3: Parameterized Tests with Builders
```python
import pytest
from tests.builders import entity

@pytest.mark.parametrize("status", ["active", "inactive", "pending"])
def test_filter_by_status(status):
    # Create 5 entities with different statuses
    entities = entity().build_many(
        5,
        modifier=lambda data, i: {**data, "status": status}
    )
    
    result = filter_entities(status=status)
    assert len(result) == 5
```

### Pattern 4: Complex Test Scenarios
```python
from tests.builders import entity, request, response

def test_order_workflow():
    # Setup test data
    customer = entity().with_name("John").build()
    order = entity().with_id("ORD-123").build()
    
    # Simulate API request
    req = (
        request()
        .post("/api/v1/orders")
        .with_body({"customer_id": customer["id"]})
        .with_auth("token-123")
        .build()
    )
    
    # Execute
    result = process_order(req)
    
    # Verify
    expected_resp = response().success(data=order).build()
    assert result["status_code"] == expected_resp["status_code"]
```

## Best Practices

1. **Always use builders for test data** - Don't create raw dicts/objects
2. **Use factory functions** - `entity()` not `EntityBuilder()`
3. **Chain method calls** - Makes tests more readable
4. **Use build_many with modifiers** - For creating variations
5. **Create custom builders** - For domain-specific test data
6. **Keep builders simple** - Don't add business logic
7. **Use fixtures with builders** - Combine both patterns

## Creating Custom Builders

```python
from tests.builders import Builder

class OrderBuilder(Builder):
    """Custom builder for Order entities."""
    
    def __init__(self):
        super().__init__()
        self._data = {
            "id": str(uuid4()),
            "customer_id": "",
            "items": [],
            "total": 0.0,
            "status": "draft"
        }
    
    def with_customer(self, customer_id: str):
        self._data["customer_id"] = customer_id
        return self
    
    def with_items(self, items: list):
        self._data["items"] = items
        self._data["total"] = sum(item["price"] for item in items)
        return self
    
    def submitted(self):
        self._data["status"] = "submitted"
        return self

# Factory function
def order() -> OrderBuilder:
    return OrderBuilder()

# Usage
test_order = (
    order()
    .with_customer("CUST-123")
    .with_items([{"id": "1", "price": 10.0}])
    .submitted()
    .build()
)
```
