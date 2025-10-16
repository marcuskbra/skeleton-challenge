# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**skeleton-challenge** - A modern Python project using Clean Architecture, Python 3.12+, managed with `uv` for fast dependency management.

## Architecture Overview

This project uses a **simplified 3-layer Clean Architecture**:
- **Presentation Layer**: API endpoints, CLI commands, external interfaces
- **Domain Layer**: Entities, value objects, services, discriminated union error models
- **Infrastructure Layer**: External integrations, database access, file system operations

The architecture follows YAGNI principles to reduce boilerplate while maintaining clean boundaries and strong typing through discriminated unions.

### Clean Architecture Benefits
- **Clear separation of concerns**: Each layer has specific responsibilities
- **Dependency inversion**: Domain layer has no dependencies on external layers
- **Testability**: Easy to test business logic in isolation
- **Maintainability**: Changes in one layer don't affect others
- **Type safety**: Strong typing with Pydantic models and discriminated unions

## Build & Test Commands

- Install dependencies: `uv pip install -e .` (or use `make install`)
- Install dev dependencies: `uv pip install -e ".[dev,test-integration]"` (or use `make dev-install`)
- Run application: `python -m challenge` (or use `make run`)
- Run unit tests only (default): `pytest tests/unit/` (or use `make test`)
- Run all tests: `pytest tests/` (or use `make test-all`)
- Run integration tests: `pytest tests/integration/` (or use `make test-integration`)
- Run single test: `pytest tests/path/to/test_file.py::test_function_name -v`
- Run tests with coverage: `pytest --cov=src --cov-report=html` (or use `make coverage`)
- Run linter: `ruff check src/ tests/` (or use `make lint`)
- Format code: `ruff format src/ tests/` (or use `make format`)
- Type check: `ty check src/ tests/` (not pyright)
- Run all validation: `make validate`

## Technical Stack

- **Python version**: Python 3.12+ (for performance and modern features)
- **Async support**: Full async/await support for high concurrency
- **Data validation**: Pydantic for data validation and serialization
- **Testing**: `pytest` for unit and integration tests with fixtures
- **Package management**: `uv` for fast, reliable package management (10-100x faster than pip)
- **Project config**: `pyproject.toml` for configuration and dependency management
- **Environment**: Use virtual environment in `.venv` for dependency isolation
- **Dependencies**: Separate production and dev dependencies in `pyproject.toml`
- **Linting**: `ruff` for style and error checking (Rust-based, very fast)
- **Type checking**: Strong typing throughout. Use `ty` from Astral team
- **Project layout**: Organize code with `src/` layout for better packaging

## Code Style Guidelines

- **Formatting**: Black-compatible formatting via `ruff format` with 120 char line length
- **Imports**: Sort imports with `ruff` (stdlib, third-party, local)
- **f-strings**: Prefer f-strings for string interpolation over `.format()` or `%`
- **Type hints**: Use native Python type hints (e.g., `list[str]` not `List[str]`)
- **Documentation**: Google-style docstrings for all modules, classes, functions
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Function length**: Keep functions short (< 30 lines) and single-purpose
- **PEP 8**: Follow PEP 8 style guide (enforced via `ruff`)

## Python Best Practices

- **File handling**: Prefer `pathlib.Path` over `os.path`
- **Debugging**: Use `logging` module instead of `print`
- **Error handling**: Use discriminated unions (Success/Error types) for type-safe error handling
- **Function arguments**: Avoid mutable default arguments (use `None` and check)
- **Data containers**: Leverage `Pydantic` models for data validation and serialization
- **Configuration**: Use environment variables for configuration (python-dotenv)
- **Security**: Never store/log credentials, validate inputs, set appropriate timeouts
- **Context managers**: Use `with` statements for resource management

## Development Patterns & Best Practices

- **Favor simplicity**: Choose the simplest solution that meets requirements
- **KISS principle**: Keep It Simple, Stupid - avoid unnecessary complexity
- **YAGNI principle**: You Aren't Gonna Need It - avoid over-engineering
- **SOLID principles**:
  - Single Responsibility
  - Open/Closed
  - Liskov Substitution
  - Interface Segregation
  - Dependency Inversion
- **Clean architecture**: Separate code into presentation, domain, infrastructure layers
- **Domain-centric design**: Domain layer contains entities, value objects, services, and business logic
- **DRY principle**: Avoid code duplication; reuse existing functionality
- **Configuration management**: Use environment variables for different environments
- **Focused changes**: Only implement explicitly requested changes
- **Preserve patterns**: Follow existing code patterns when making changes
- **File size**: Keep files under 300 lines; refactor when exceeding this limit
- **Test coverage**: Write comprehensive unit and integration tests (≥80% coverage)
- **Modular design**: Create reusable, modular components
- **Logging**: Implement appropriate logging levels (debug, info, warning, error)
- **Error handling**: Use discriminated unions for compile-time verified error handling
- **Security best practices**: Input validation, output encoding, secure defaults
- **Performance**: Profile before optimizing, optimize critical paths only
- **Dependency management**: Add libraries only when essential

## Testing Guidelines

### Testing Strategy

- **Test Types**:
  - Unit tests for domain logic (fast, isolated)
  - Integration tests for external integrations
  - Contract tests for interface requirements
- **Builder Pattern**: Use test builders for maintainable test data (see `tests/builders.py`)
- **Parameterized Tests**: Use `@pytest.mark.parametrize` for test variations
- **Performance Testing**: Validate response times for critical operations
- **Error Scenarios**: Test both Success and Error paths in discriminated unions

### Test Organization

```
tests/
├── unit/               # Fast, isolated unit tests
│   ├── domain/        # Domain layer tests
│   ├── infrastructure/# Infrastructure tests (mocked)
│   └── presentation/  # Presentation tests
├── integration/       # Tests with real external dependencies
├── builders.py        # Test data builders (Builder pattern)
└── conftest.py        # Shared fixtures
```

### Testing Patterns

1. **Builder Pattern for Test Data**:
   ```python
   from tests.builders import entity, request

   test_entity = entity().with_name("Test").with_metadata({"key": "value"}).build()
   entities = entity().build_many(10)
   ```

2. **Parameterized Testing**:
   ```python
   @pytest.mark.parametrize("input_value,expected", [
       ("valid", True),
       ("invalid", False),
   ])
   def test_validation(input_value, expected):
       assert validate(input_value) == expected
   ```

3. **Testing Async Code**:
   ```python
   @pytest.mark.asyncio
   async def test_async_operation():
       result = await async_function()
       assert result.success
   ```

### Test Coverage Requirements

- **Unit Tests**: ≥ 80% coverage for domain logic
- **Integration Tests**: Cover all external integration points
- **Error Paths**: Test all error scenarios using discriminated unions
- **Edge Cases**: Include boundary conditions and edge cases

## Development Workflow

- **Version control**: Commit frequently with clear, conventional commit messages
- **Test-Driven Development**: Write tests before implementation
- **TDD Cycle**:
  1. **Red**: Create failing tests that define requirements
  2. **Green**: Implement minimal code to pass tests
  3. **Refactor**: Optimize while maintaining test compliance
- **Continuous Testing**: Run tests before every commit
- **Code Review**: Self-review changes before committing
- **Impact assessment**: Evaluate how changes affect other parts of the codebase
- **Documentation**: Document complex logic and public APIs
- **Branch strategy**: Use feature branches for development

## Error Handling Pattern

**IMPORTANT**: This project uses discriminated unions for error handling, not exceptions.

### Pattern Overview
Every domain operation returns a discriminated union of Success/Error types:

```python
from challenge.domain.errors import (
    GetEntityResult,
    GetEntitySuccess,
    NotFoundError
)

# Domain service method
async def get_entity(self, entity_id: str) -> GetEntityResult:
    # Validate input
    if not entity_id:
        return ValidationError(
            message="Entity ID is required",
            field_errors={"entity_id": "Cannot be empty"}
        )

    # Try to get entity
    entity = await self.repository.get(entity_id)
    if not entity:
        return NotFoundError(
            message="Entity not found",
            resource_type="Entity",
            resource_id=entity_id
        )

    return GetEntitySuccess(entity=entity.model_dump())

# Consumer handles both cases
result = await service.get_entity(entity_id)

if isinstance(result, NotFoundError):
    logger.error(f"Not found: {result.message}")
    raise HTTPException(status_code=404, detail=result.message)

if isinstance(result, ValidationError):
    logger.error(f"Validation failed: {result.field_errors}")
    raise HTTPException(status_code=400, detail=result.field_errors)

# Type checker knows result is GetEntitySuccess here
return result.entity
```

### Benefits of Discriminated Unions
- **Type Safety**: Compiler/type-checker verifies all cases are handled
- **Explicit Error Handling**: Can't forget to handle errors
- **Better Documentation**: Return types clearly show possible outcomes
- **No Hidden Exceptions**: All failure modes are explicit

### Testing with Discriminated Unions
Always test both success and error paths:

```python
# Test success case
async def test_get_entity_success():
    result = await service.get_entity("valid-id")
    assert isinstance(result, GetEntitySuccess)
    assert result.entity["id"] == "valid-id"

# Test error case
async def test_get_entity_not_found():
    result = await service.get_entity("invalid-id")
    assert isinstance(result, NotFoundError)
    assert result.resource_id == "invalid-id"
```

## Common Patterns

### Adding a New Domain Entity
1. Create entity in `src/challenge/domain/entities/`
2. Inherit from `DomainEntity` or `ImmutableEntity`
3. Use Pydantic Field for validation
4. Write unit tests with builders

### Adding a Domain Service Method
1. Define method in service class
2. Return discriminated union (Success | Error types)
3. Handle all error cases explicitly
4. Write tests for both success and error paths

### Adding an API Endpoint
1. Create endpoint in presentation layer
2. Call domain service
3. Handle discriminated union result
4. Convert to appropriate HTTP response

## Important Reminders

- Do what has been asked; nothing more, nothing less
- NEVER create files unless they're absolutely necessary
- ALWAYS prefer editing an existing file to creating a new one
- NEVER proactively create documentation files unless explicitly requested
- Follow existing patterns in the codebase
- Use type hints for all function signatures
- Write tests for all new functionality
- Keep functions focused and single-purpose
- Use meaningful variable and function names
