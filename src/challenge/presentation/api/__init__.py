"""
API package - RESTful API implementation.

This package contains all REST API endpoints organized by version.
Each version is isolated to allow for backwards compatibility and
independent evolution of the API.

Supported versions:
- v1: Initial API version with basic CRUD operations and health checks

API design principles:
- RESTful resource-based URLs
- Standard HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Consistent error responses
- Proper status codes
- API versioning via URL prefix
- OpenAPI/Swagger documentation
- Request/response validation
"""
