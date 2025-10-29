"""
Shared pytest fixtures and configuration for all tests.
"""

import asyncio
import os
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Load test environment variables
load_dotenv(".env.test")


# ============================================================================
# Event Loop Configuration
# ============================================================================


@pytest.fixture(scope="session")
def event_loop_policy():
    """Set event loop policy for async tests."""
    if sys.platform == "win32":
        # Windows requires special handling
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    return asyncio.get_event_loop_policy()


# ============================================================================
# Common Test Fixtures
# ============================================================================


@pytest.fixture
def mock_env_vars():
    """Fixture to temporarily set environment variables for testing."""
    original_env = os.environ.copy()

    def _set_env(**kwargs):
        for key, value in kwargs.items():
            os.environ[key] = str(value)

    yield _set_env

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_http_client():
    """Mock HTTP client for testing external API calls."""
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value.__aenter__.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary directory for test data."""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    return data_dir


# ============================================================================
# Async Test Helpers
# ============================================================================


@pytest.fixture
async def async_client():
    """Create an async HTTP client for integration tests."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        yield client


@pytest.fixture
def test_client():
    """Create a FastAPI test client for API endpoint testing."""
    from challenge.api.main import create_app  # noqa: PLC0415

    app = create_app(environment="test")
    with TestClient(app) as client:
        yield client


# ============================================================================
# Test Data Fixtures
# ============================================================================


@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        "log_level": "DEBUG",
        "environment": "test",
        "cache_enabled": False,
        "api_key": "test-api-key",
    }


@pytest.fixture
def sample_entity_data():
    """Sample entity data for domain tests."""
    return {
        "id": "test-123",
        "name": "Test Entity",
        "created_at": "2024-01-01T00:00:00Z",
        "metadata": {
            "version": "1.0.0",
            "author": "test",
        },
    }


# ============================================================================
# Assertion Helpers
# ============================================================================


class AssertionHelpers:
    """Reusable assertion helpers for tests."""

    @staticmethod
    def assert_valid_uuid(value: str) -> None:
        """Assert that a value is a valid UUID."""
        try:
            uuid.UUID(value)
        except ValueError:
            pytest.fail(f"'{value}' is not a valid UUID")

    @staticmethod
    def assert_datetime_format(value: str, fmt: str = "%Y-%m-%dT%H:%M:%S") -> None:
        """Assert that a value matches a datetime format."""
        try:
            datetime.strptime(value.replace("Z", ""), fmt)
        except ValueError:
            pytest.fail(f"'{value}' does not match format '{fmt}'")

    @staticmethod
    def assert_between(value: float, min_val: float, max_val: float) -> None:
        """Assert that a value is between min and max."""
        assert min_val <= value <= max_val, f"{value} is not between {min_val} and {max_val}"


@pytest.fixture
def assert_helpers():
    """Provide assertion helpers to tests."""
    return AssertionHelpers()


# ============================================================================
# Performance Testing
# ============================================================================


@pytest.fixture
def benchmark_timer():
    """Simple benchmark timer for performance tests."""

    class Timer:
        def __init__(self):
            self.start_time = None
            self.elapsed = None

        def __enter__(self):
            self.start_time = time.perf_counter()
            return self

        def __exit__(self, *args):
            self.elapsed = time.perf_counter() - self.start_time

    return Timer


# ============================================================================
# Markers and Hooks
# ============================================================================


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests (no external dependencies)")
    config.addinivalue_line("markers", "integration: Integration tests (may require external services)")
    config.addinivalue_line("markers", "contract: Contract tests (behavioral requirements)")
    config.addinivalue_line("markers", "slow: Slow tests (>1 second)")
    config.addinivalue_line("markers", "smoke: Smoke tests (basic sanity checks)")
