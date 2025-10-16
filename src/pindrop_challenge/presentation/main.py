"""
FastAPI application factory and configuration.

This module provides the FastAPI application factory pattern, enabling:
- Testable application instances
- Environment-specific configurations
- Middleware registration
- Error handler setup
- API versioning and routing
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from pindrop_challenge import __version__
from pindrop_challenge.presentation.api.v1 import health

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager for startup and shutdown events.

    Handles:
    - Database connection initialization
    - Cache warmup
    - Background task startup
    - Resource cleanup on shutdown
    """
    # Startup
    logger.info("Starting pindrop-challenge API v%s", __version__)

    yield

    # Shutdown
    logger.info("Shutting down pindrop-challenge API")


def create_app(environment: str = "development") -> FastAPI:
    """
    FastAPI application factory.

    Creates and configures a FastAPI application instance with:
    - CORS middleware
    - Error handlers
    - API routing
    - OpenAPI documentation

    Args:
        environment: Application environment (development, staging, production)

    Returns:
        Configured FastAPI application instance

    """
    app = FastAPI(
        title="Pindrop Challenge API",
        description="A modern Python API with Clean Architecture",
        version=__version__,
        lifespan=lifespan,
        docs_url="/api/docs" if environment != "production" else None,
        redoc_url="/api/redoc" if environment != "production" else None,
        openapi_url="/api/openapi.json" if environment != "production" else None,
    )

    # Configure CORS
    _configure_cors(app, environment)

    # Add middleware
    _configure_middleware(app)

    # Register error handlers
    _register_error_handlers(app)

    # Register routes
    _register_routes(app)

    return app


def _configure_cors(app: FastAPI, environment: str) -> None:
    """
    Configure CORS middleware based on environment.

    Args:
        app: FastAPI application instance
        environment: Application environment

    """
    if environment == "production":
        # Restrict origins in production
        origins = [
            "https://yourdomain.com",
            "https://www.yourdomain.com",
        ]
    else:
        # Allow all origins in development/staging
        origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _configure_middleware(app: FastAPI) -> None:
    """
    Configure additional middleware.

    Args:
        app: FastAPI application instance

    """
    # GZip compression for responses
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log all incoming requests and responses."""
        logger.info(
            "Incoming request: %s %s",
            request.method,
            request.url.path,
        )

        response = await call_next(request)

        logger.info(
            "Response: %s %s - Status: %d",
            request.method,
            request.url.path,
            response.status_code,
        )

        return response


def _register_error_handlers(app: FastAPI) -> None:
    """
    Register custom error handlers for API exceptions.

    Handles FastAPI and Pydantic validation errors with consistent responses.
    Domain errors (discriminated unions) are handled at the endpoint level
    by checking result types and returning appropriate responses.

    Args:
        app: FastAPI application instance

    """

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """Handle FastAPI request validation errors."""
        logger.warning("Validation error: %s", exc.errors())

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "validation_error",
                "message": "Request validation failed",
                "details": exc.errors(),
            },
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_handler(request: Request, exc: ValidationError) -> JSONResponse:
        """Handle Pydantic validation errors."""
        logger.warning("Pydantic validation error: %s", exc.errors())

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "validation_error",
                "message": "Data validation failed",
                "details": exc.errors(),
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle unexpected exceptions."""
        logger.exception("Unhandled exception: %s", str(exc))

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "internal_error",
                "message": "An unexpected error occurred",
            },
        )


def _register_routes(app: FastAPI) -> None:
    """
    Register API routes and routers.

    Args:
        app: FastAPI application instance

    """
    # Include API v1 routers
    app.include_router(health.router, prefix="/api/v1", tags=["health"])


# Create default application instance for uvicorn
app = create_app()
