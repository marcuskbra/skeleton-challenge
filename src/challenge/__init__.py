"""
Skeleton Challenge - A modern Python project with simplified 3-layer architecture.

This is the main package for the Skeleton Challenge project, implementing a
simplified 3-layer architecture with:

- API Layer: HTTP endpoints and request/response handling
- Service Layer: Business logic and orchestration (add when needed)
- Data Layer: Models and repository abstractions (add when needed)
- Core: Shared utilities, config, and exceptions

The project follows YAGNI principles - start simple and add complexity only
when needed. Use standard Python exceptions with FastAPI's HTTPException for
error handling.

Key Features:
- Simplified architecture following YAGNI principles
- Type safety with Pydantic models throughout
- Async-first design for high concurrency
- Comprehensive testing with simple fixtures
- Modern Python tooling (uv, ruff, ty)
"""

__version__ = "0.1.0"
__author__ = "Your Name"
