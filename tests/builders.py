"""
Test data builders following the Builder pattern for creating test objects.
This provides a flexible and maintainable way to create test data.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4


# ============================================================================
# Base Builder Class
# ============================================================================


class Builder:
    """Base builder class for creating test objects."""

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
    """Builder for creating test domain entities."""

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
    """Builder for creating test API requests."""

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
    """Builder for creating test API responses."""

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
    """Builder for creating test configurations."""

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
    """Builder for creating test error objects."""

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
    """Create a new entity builder."""
    return EntityBuilder()


def value_object() -> ValueObjectBuilder:
    """Create a new value object builder."""
    return ValueObjectBuilder()


def request() -> RequestBuilder:
    """Create a new request builder."""
    return RequestBuilder()


def response() -> ResponseBuilder:
    """Create a new response builder."""
    return ResponseBuilder()


def config() -> ConfigBuilder:
    """Create a new config builder."""
    return ConfigBuilder()


def error() -> ErrorBuilder:
    """Create a new error builder."""
    return ErrorBuilder()