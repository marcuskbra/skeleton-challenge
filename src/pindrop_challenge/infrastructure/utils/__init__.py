"""
Infrastructure Utilities - Technical helper functions and tools.

This module contains utility functions and helper classes that support
infrastructure operations. These utilities are technical in nature and
don't contain business logic.

Common utilities:
- Connection pool managers
- Retry decorators and helpers
- Circuit breaker implementations
- Rate limiters
- Cache decorators
- Database transaction helpers
- Serialization/deserialization helpers
- Logging utilities
- Monitoring and metrics helpers
- Configuration loaders
- Environment variable parsers

Utility characteristics:
- Technical, not business-focused
- Reusable across different infrastructure components
- Stateless or manage technical state only
- Can depend on external libraries
- Should be well-tested and documented

Examples:
- retry_with_backoff() - Decorator for retrying operations
- CircuitBreaker - Class for circuit breaker pattern
- connection_pool() - Database connection pooling
- cache_result() - Decorator for caching function results
- sanitize_sql() - SQL injection prevention
- validate_environment() - Environment configuration validation

"""
