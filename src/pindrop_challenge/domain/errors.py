"""
Domain errors using discriminated unions for type-safe error handling.

This module demonstrates the pattern of using discriminated unions
instead of exceptions for error handling.
"""

from typing import Any, Callable, Literal, Union, cast

from pydantic import Field

from .base_models import Error, Success

# ============================================================================
# Common Domain Errors
# ============================================================================


class ValidationError(Error):
    """Validation error for domain operations."""

    error_code: Literal["VALIDATION_ERROR"] = "VALIDATION_ERROR"
    field_errors: dict[str, str] = Field(default_factory=dict)


class NotFoundError(Error):
    """Resource not-found error."""

    error_code: Literal["NOT_FOUND"] = "NOT_FOUND"
    resource_type: str = Field(..., description="Type of resource not found")
    resource_id: str = Field(..., description="ID of the resource not found")


class ConflictError(Error):
    """Conflict error when operation would violate constraints."""

    error_code: Literal["CONFLICT"] = "CONFLICT"
    conflicting_field: str = Field(..., description="Field causing the conflict")


class UnauthorizedError(Error):
    """Unauthorized access error."""

    error_code: Literal["UNAUTHORIZED"] = "UNAUTHORIZED"


class ForbiddenError(Error):
    """Forbidden action error."""

    error_code: Literal["FORBIDDEN"] = "FORBIDDEN"
    required_permission: str = Field(..., description="Permission required for this action")


class BusinessRuleViolationError(Error):
    """Business rule violation error."""

    error_code: Literal["BUSINESS_RULE_VIOLATION"] = "BUSINESS_RULE_VIOLATION"
    rule_name: str = Field(..., description="Name of the violated business rule")


class ExternalServiceError(Error):
    """External service communication error."""

    error_code: Literal["EXTERNAL_SERVICE_ERROR"] = "EXTERNAL_SERVICE_ERROR"
    service_name: str = Field(..., description="Name of the external service")
    status_code: int | None = Field(None, description="HTTP status code if applicable")


class RateLimitError(Error):
    """Rate limit exceeded error."""

    error_code: Literal["RATE_LIMIT_EXCEEDED"] = "RATE_LIMIT_EXCEEDED"
    retry_after: int = Field(..., description="Seconds to wait before retrying")


# ============================================================================
# Example Domain Operation Results
# ============================================================================


class CreateEntitySuccess(Success):
    """Successful entity creation result."""

    entity_id: str = Field(..., description="ID of the created entity")
    entity: dict = Field(..., description="The created entity data")


# Define the union type for create operation
CreateEntityResult = Union[
    CreateEntitySuccess,
    ValidationError,
    ConflictError,
    UnauthorizedError,
]


class GetEntitySuccess(Success):
    """Successful entity retrieval result."""

    entity: dict = Field(..., description="The retrieved entity data")


# Define the union type for get operation
GetEntityResult = Union[
    GetEntitySuccess,
    NotFoundError,
    UnauthorizedError,
]


class UpdateEntitySuccess(Success):
    """Successful entity update result."""

    entity: dict = Field(..., description="The updated entity data")
    updated_fields: list[str] = Field(..., description="List of fields that were updated")


# Define the union type for update operation
UpdateEntityResult = Union[
    UpdateEntitySuccess,
    NotFoundError,
    ValidationError,
    ConflictError,
    UnauthorizedError,
    BusinessRuleViolationError,
]


class DeleteEntitySuccess(Success):
    """Successful entity deletion result."""

    entity_id: str = Field(..., description="ID of the deleted entity")


# Define the union type for delete operation
DeleteEntityResult = Union[
    DeleteEntitySuccess,
    NotFoundError,
    UnauthorizedError,
    BusinessRuleViolationError,
]


# ============================================================================
# Error Handling Utilities
# ============================================================================


def handle_result[T: Success, E: Error](
    result: Union[T, E],
    on_success: Callable[[T], Any],
    on_error: Callable[[E], Any] | None = None,
) -> Any:
    """
    Handle result using callbacks for discriminated unions.

    Args:
        result: The result to handle (Success or Error)
        on_success: Function to call on success
        on_error: Function to call on error (optional)

    Returns:
        The return value of the appropriate handler

    """
    if isinstance(result, Success):
        return on_success(cast(T, result))
    elif on_error:
        return on_error(cast(E, result))
    else:
        # Default error handling
        raise RuntimeError(f"Operation failed: {result.message}")


def is_success[T: Success, E: Error](result: Union[T, E]) -> bool:
    """Check if a result is successful."""
    return isinstance(result, Success)


def is_error[T: Success, E: Error](result: Union[T, E]) -> bool:
    """Check if a result is an error."""
    return isinstance(result, Error)


def unwrap[T: Success, E: Error](result: Union[T, E]) -> T:
    """
    Unwrap a successful result or raise an exception.

    Args:
        result: The result to unwrap

    Returns:
        The success value

    Raises:
        RuntimeError: If the result is an error

    """
    if isinstance(result, Success):
        return cast(T, result)
    raise RuntimeError(f"Cannot unwrap error: {result.message}")


def unwrap_or[T: Success, E: Error](result: Union[T, E], default: T) -> T:
    """
    Unwrap a successful result or return a default value.

    Args:
        result: The result to unwrap
        default: Default value to return on error

    Returns:
        The success value or default

    """
    if isinstance(result, Success):
        return cast(T, result)
    return default
