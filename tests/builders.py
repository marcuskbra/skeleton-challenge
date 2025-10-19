"""
Test data builders following the Builder pattern for creating test objects.

This module provides reusable builders for creating test data in a maintainable way.
All builders support method chaining and sensible defaults.

Available builders:
- EntityBuilder - Domain entities with identity
- ValueObjectBuilder - Value objects
- RequestBuilder - API requests
- ResponseBuilder - API responses
- ConfigBuilder - Configuration objects
- ErrorBuilder - Error objects

Factory functions (use these):
- entity() -> EntityBuilder
- value_object() -> ValueObjectBuilder
- request() -> RequestBuilder
- response() -> ResponseBuilder
- config() -> ConfigBuilder
- error() -> ErrorBuilder

Quick examples:
    >>> # Create simple entity
    >>> test_entity = entity().build()

    >>> # Customize entity
    >>> custom = entity().with_name("Test").with_metadata({"key": "value"}).build()

    >>> # Create multiple entities
    >>> entities = entity().build_many(10)

    >>> # API request
    >>> req = request().post("/api/v1/items").with_auth("token").build()

    >>> # Success response
    >>> resp = response().success(data={"id": "123"}).build()
"""

from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4

# ============================================================================
# Base Builder Class
# ============================================================================


class Builder:
    """
    Base builder class for creating test objects.

    Provides common functionality for all builders including method chaining
    and batch creation with modifiers.

    Methods:
        with_field(name, value): Set any field value
        build(): Build single object
        build_many(count, modifier): Build multiple objects with optional modifications

    Example:
        >>> builder = Builder()
        >>> obj = builder.with_field("name", "test").build()
        >>> objs = builder.build_many(5, lambda data, i: {**data, "index": i})
    """

    def __init__(self):
        self._data = {}

    def with_field(self, name: str, value: Any) -> "Builder":
        """Set a field value."""
        self._data[name] = value
        return self

    def build(self) -> Dict[str, Any]:
        """Build the final object."""
        return self._data.copy()

    def build_many(self, count: int, modifier=None) -> List[Dict[str, Any]]:
        """Build multiple objects with optional modifications."""
        results = []
        for i in range(count):
            data = self.build()
            if modifier:
                data = modifier(data, i)
            results.append(data)
        return results


# ============================================================================
# Domain Entity Builders
# ============================================================================


class EntityBuilder(Builder):
    """
    Builder for creating test domain entities with sensible defaults.

    Default values:
        - id: Random UUID
        - name: "Test Entity"
        - description: "Test entity description"
        - created_at: Current UTC timestamp
        - updated_at: Current UTC timestamp
        - is_active: True
        - metadata: {}

    Methods:
        with_id(entity_id): Set entity ID
        with_name(name): Set entity name
        with_description(description): Set description
        with_metadata(metadata): Set metadata dict
        inactive(): Mark entity as inactive
        created_at(timestamp): Set creation timestamp

    Example:
        >>> from tests.builders import entity
        >>> test_entity = (
        ...     entity()
        ...     .with_name("Important Item")
        ...     .with_metadata({"priority": "high"})
        ...     .build()
        ... )
    """

    def __init__(self):
        super().__init__()
        # Set default values
        self._data = {
            "id": str(uuid4()),
            "name": "Test Entity",
            "description": "Test entity description",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "is_active": True,
            "metadata": {},
        }

    def with_id(self, entity_id: str) -> "EntityBuilder":
        """Set entity ID."""
        self._data["id"] = entity_id
        return self

    def with_name(self, name: str) -> "EntityBuilder":
        """Set entity name."""
        self._data["name"] = name
        return self

    def with_description(self, description: str) -> "EntityBuilder":
        """Set entity description."""
        self._data["description"] = description
        return self

    def with_metadata(self, metadata: Dict[str, Any]) -> "EntityBuilder":
        """Set entity metadata."""
        self._data["metadata"] = metadata
        return self

    def inactive(self) -> "EntityBuilder":
        """Mark entity as inactive."""
        self._data["is_active"] = False
        return self

    def created_at(self, timestamp: datetime) -> "EntityBuilder":
        """Set creation timestamp."""
        self._data["created_at"] = timestamp.isoformat()
        return self


# ============================================================================
# Value Object Builders
# ============================================================================


class ValueObjectBuilder(Builder):
    """Builder for creating test value objects."""

    def __init__(self):
        super().__init__()
        self._data = {
            "value": None,
            "unit": None,
            "precision": 2,
        }

    def with_value(self, value: Any) -> "ValueObjectBuilder":
        """Set the value."""
        self._data["value"] = value
        return self

    def with_unit(self, unit: str) -> "ValueObjectBuilder":
        """Set the unit."""
        self._data["unit"] = unit
        return self

    def with_precision(self, precision: int) -> "ValueObjectBuilder":
        """Set the precision."""
        self._data["precision"] = precision
        return self


# ============================================================================
# Request/Response Builders
# ============================================================================


class RequestBuilder(Builder):
    """
    Builder for creating test API requests.

    Default values:
        - method: "POST"
        - endpoint: "/api/v1/test"
        - headers: {"Content-Type": "application/json"}
        - body: {}
        - query_params: {}

    Methods:
        get(endpoint): Set as GET request
        post(endpoint): Set as POST request
        with_header(key, value): Add request header
        with_body(body): Set request body
        with_query(params): Set query parameters
        with_auth(token): Add Bearer authorization header

    Example:
        >>> from tests.builders import request
        >>> req = (
        ...     request()
        ...     .post("/api/v1/orders")
        ...     .with_body({"customer_id": "123"})
        ...     .with_auth("my-token")
        ...     .build()
        ... )
    """

    def __init__(self):
        super().__init__()
        self._data = {
            "method": "POST",
            "endpoint": "/api/v1/test",
            "headers": {"Content-Type": "application/json"},
            "body": {},
            "query_params": {},
        }

    def get(self, endpoint: str) -> "RequestBuilder":
        """Set as GET request."""
        self._data["method"] = "GET"
        self._data["endpoint"] = endpoint
        return self

    def post(self, endpoint: str) -> "RequestBuilder":
        """Set as POST request."""
        self._data["method"] = "POST"
        self._data["endpoint"] = endpoint
        return self

    def with_header(self, key: str, value: str) -> "RequestBuilder":
        """Add a header."""
        self._data["headers"][key] = value
        return self

    def with_body(self, body: Dict[str, Any]) -> "RequestBuilder":
        """Set request body."""
        self._data["body"] = body
        return self

    def with_query(self, params: Dict[str, str]) -> "RequestBuilder":
        """Set query parameters."""
        self._data["query_params"] = params
        return self

    def with_auth(self, token: str) -> "RequestBuilder":
        """Add authorization header."""
        self._data["headers"]["Authorization"] = f"Bearer {token}"
        return self


class ResponseBuilder(Builder):
    """
    Builder for creating test API responses.

    Default values:
        - status_code: 200
        - headers: {"Content-Type": "application/json"}
        - body: {}
        - elapsed: 0.1

    Methods:
        with_status(status_code): Set HTTP status code
        success(data): Set as successful response (200)
        error(message, status_code): Set as error response
        not_found(): Set as 404 Not Found
        unauthorized(): Set as 401 Unauthorized

    Example:
        >>> from tests.builders import response
        >>> success_resp = response().success(data={"id": "123"}).build()
        >>> error_resp = response().error("Invalid input", 400).build()
        >>> not_found = response().not_found().build()
    """

    def __init__(self):
        super().__init__()
        self._data = {
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "body": {},
            "elapsed": 0.1,
        }

    def with_status(self, status_code: int) -> "ResponseBuilder":
        """Set status code."""
        self._data["status_code"] = status_code
        return self

    def success(self, data: Any = None) -> "ResponseBuilder":
        """Set as successful response."""
        self._data["status_code"] = 200
        self._data["body"] = {"success": True, "data": data}
        return self

    def error(self, message: str, status_code: int = 400) -> "ResponseBuilder":
        """Set as error response."""
        self._data["status_code"] = status_code
        self._data["body"] = {"success": False, "error": message}
        return self

    def not_found(self) -> "ResponseBuilder":
        """Set as 404 not found."""
        return self.error("Resource not found", 404)

    def unauthorized(self) -> "ResponseBuilder":
        """Set as 401 unauthorized."""
        return self.error("Unauthorized", 401)


# ============================================================================
# Configuration Builders
# ============================================================================


class ConfigBuilder(Builder):
    """
    Builder for creating test configurations.

    Default values:
        - environment: "test"
        - debug: True
        - log_level: "DEBUG"
        - database_url: "sqlite:///:memory:"
        - cache_enabled: False
        - features: {}

    Methods:
        production(): Set production configuration
        development(): Set development configuration
        with_database(url): Set database URL
        with_cache(enabled): Enable/disable cache
        with_feature(name, enabled): Set feature flag

    Example:
        >>> from tests.builders import config
        >>> test_cfg = config().build()
        >>> prod_cfg = config().production().build()
        >>> dev_cfg = config().development().with_feature("beta_ui", True).build()
    """

    def __init__(self):
        super().__init__()
        self._data = {
            "environment": "test",
            "debug": True,
            "log_level": "DEBUG",
            "database_url": "sqlite:///:memory:",
            "cache_enabled": False,
            "features": {},
        }

    def production(self) -> "ConfigBuilder":
        """Set production configuration."""
        self._data["environment"] = "production"
        self._data["debug"] = False
        self._data["log_level"] = "INFO"
        return self

    def development(self) -> "ConfigBuilder":
        """Set development configuration."""
        self._data["environment"] = "development"
        self._data["debug"] = True
        self._data["log_level"] = "DEBUG"
        return self

    def with_database(self, url: str) -> "ConfigBuilder":
        """Set database URL."""
        self._data["database_url"] = url
        return self

    def with_cache(self, enabled: bool = True) -> "ConfigBuilder":
        """Enable/disable cache."""
        self._data["cache_enabled"] = enabled
        return self

    def with_feature(self, name: str, enabled: bool = True) -> "ConfigBuilder":
        """Set a feature flag."""
        self._data["features"][name] = enabled
        return self


# ============================================================================
# Error Builders
# ============================================================================


class ErrorBuilder(Builder):
    """
    Builder for creating test error objects.

    Default values:
        - type: "GenericError"
        - message: "An error occurred"
        - code: "ERR_GENERIC"
        - details: {}
        - timestamp: Current UTC timestamp

    Methods:
        validation_error(field, message): Create validation error
        not_found(resource): Create not found error
        permission_denied(action): Create permission denied error

    Example:
        >>> from tests.builders import error
        >>> validation_err = error().validation_error("email", "Invalid format").build()
        >>> not_found_err = error().not_found("Order").build()
        >>> permission_err = error().permission_denied("delete_order").build()
    """

    def __init__(self):
        super().__init__()
        self._data = {
            "type": "GenericError",
            "message": "An error occurred",
            "code": "ERR_GENERIC",
            "details": {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def validation_error(self, field: str, message: str) -> "ErrorBuilder":
        """Create validation error."""
        self._data["type"] = "ValidationError"
        self._data["code"] = "ERR_VALIDATION"
        self._data["message"] = f"Validation failed for field: {field}"
        self._data["details"] = {"field": field, "error": message}
        return self

    def not_found(self, resource: str) -> "ErrorBuilder":
        """Create not found error."""
        self._data["type"] = "NotFoundError"
        self._data["code"] = "ERR_NOT_FOUND"
        self._data["message"] = f"{resource} not found"
        self._data["details"] = {"resource": resource}
        return self

    def permission_denied(self, action: str) -> "ErrorBuilder":
        """Create permission denied error."""
        self._data["type"] = "PermissionError"
        self._data["code"] = "ERR_PERMISSION"
        self._data["message"] = f"Permission denied for action: {action}"
        self._data["details"] = {"action": action}
        return self


# ============================================================================
# Factory Functions
# ============================================================================


def entity() -> EntityBuilder:
    """
    Create a new entity builder.

    Returns:
        EntityBuilder for creating test domain entities

    Example:
        >>> test_entity = entity().with_name("Test").build()
    """
    return EntityBuilder()


def value_object() -> ValueObjectBuilder:
    """
    Create a new value object builder.

    Returns:
        ValueObjectBuilder for creating test value objects

    Example:
        >>> temp = value_object().with_value(25.5).with_unit("celsius").build()
    """
    return ValueObjectBuilder()


def request() -> RequestBuilder:
    """
    Create a new request builder.

    Returns:
        RequestBuilder for creating test API requests

    Example:
        >>> req = request().post("/api/v1/items").with_auth("token").build()
    """
    return RequestBuilder()


def response() -> ResponseBuilder:
    """
    Create a new response builder.

    Returns:
        ResponseBuilder for creating test API responses

    Example:
        >>> resp = response().success(data={"id": "123"}).build()
    """
    return ResponseBuilder()


def config() -> ConfigBuilder:
    """
    Create a new config builder.

    Returns:
        ConfigBuilder for creating test configurations

    Example:
        >>> cfg = config().production().with_feature("beta", True).build()
    """
    return ConfigBuilder()


def error() -> ErrorBuilder:
    """
    Create a new error builder.

    Returns:
        ErrorBuilder for creating test error objects

    Example:
        >>> err = error().validation_error("email", "Invalid format").build()
    """
    return ErrorBuilder()
