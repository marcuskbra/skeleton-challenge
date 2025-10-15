# PyCharm Run/Debug Configurations

This directory contains pre-configured run/debug configurations for PyCharm.

## Available Configurations

### 🚀 FastAPI Servers

#### **FastAPI Dev Server** (Recommended for Development)
- **Purpose**: Run FastAPI with auto-reload for development
- **Port**: 8000
- **Features**: Auto-reload on code changes, debug-friendly
- **Environment**: development
- **URL**: http://localhost:8000/api/v1/health

**How to use**:
1. Select "FastAPI Dev Server" from the dropdown
2. Click Debug (bug icon) to start with breakpoints
3. Set breakpoints in your code
4. Make a request to trigger the breakpoint

#### **FastAPI Production**
- **Purpose**: Simulate production environment
- **Port**: 8000
- **Features**: 4 workers, no auto-reload
- **Environment**: production
- **Note**: API docs disabled in production mode

### 🧪 Test Configurations

#### **API Tests**
- **Purpose**: Run only API-related tests
- **Target**: `tests/unit/presentation/api/`
- **Output**: Verbose with short traceback
- **Use for**: Testing health endpoints and API functionality

#### **All Unit Tests**
- **Purpose**: Run all unit tests
- **Target**: `tests/unit/`
- **Output**: Verbose with short traceback
- **Use for**: Full test suite validation

#### **Tests with Coverage**
- **Purpose**: Run tests and generate coverage report
- **Target**: `tests/`
- **Output**: Terminal + HTML report in `htmlcov/`
- **Use for**: Checking test coverage before commits

## 🐛 Debugging Tips

### Setting Breakpoints

**In Health Endpoint** (`src/pindrop_challenge/presentation/api/v1/health.py`):
```python
@router.get("/health")
async def health_check() -> DetailedHealthResponse:
    checks = {  # ← Set breakpoint here
        "application": "healthy",
    }
    return DetailedHealthResponse(...)  # ← Or here
```

**In Middleware** (`src/pindrop_challenge/presentation/main.py`):
```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(...)  # ← Set breakpoint here
    response = await call_next(request)
    return response
```

**In App Factory**:
```python
def create_app(environment: str = "development") -> FastAPI:
    app = FastAPI(...)  # ← Set breakpoint here
    _configure_cors(app, environment)
    return app
```

### Triggering Breakpoints

1. **Start Debug**: Select configuration → Click bug icon
2. **Wait for startup**: "Application startup complete"
3. **Make Request**:
   - Browser: http://localhost:8000/api/v1/health
   - curl: `curl http://localhost:8000/api/v1/health`
   - HTTPie: `http :8000/api/v1/health`
4. **Debug**: PyCharm stops at your breakpoint!

### Debug Console Commands

While stopped at a breakpoint, you can evaluate:
```python
# Check variables
checks
__version__
request.method
request.url.path

# Evaluate expressions
len(checks)
f"Request: {request.method} {request.url.path}"

# Call functions
logger.info("Debug checkpoint")
```

## ⌨️ Keyboard Shortcuts

- **F9**: Resume (continue to next breakpoint)
- **F8**: Step Over
- **F7**: Step Into
- **Shift+F8**: Step Out
- **Alt+F9**: Run to Cursor
- **Ctrl+F8**: Toggle Breakpoint
- **Ctrl+Shift+F8**: View Breakpoints
- **Alt+F10**: Show Execution Point

## 📝 Configuration Details

All configurations use:
- **Python Interpreter**: `.venv/bin/python` (Python 3.12)
- **Working Directory**: Project root
- **Module SDK**: Project virtual environment
- **Source Roots**: Automatically added

### Environment Variables

**Development Server**:
- `PYTHONUNBUFFERED=1` - Immediate output (no buffering)
- `ENVIRONMENT=development` - Development mode

**Production Server**:
- `PYTHONUNBUFFERED=1`
- `ENVIRONMENT=production` - Production mode (docs disabled)

## 🔧 Customization

To modify configurations:
1. Go to `Run` → `Edit Configurations...`
2. Select the configuration
3. Modify as needed
4. Click `Apply` and `OK`

Or edit the XML files directly in this directory.

## 📚 Additional Resources

- [PyCharm Debugging Guide](https://www.jetbrains.com/help/pycharm/debugging-code.html)
- [FastAPI Debugging](https://fastapi.tiangolo.com/tutorial/debugging/)
- [Pytest in PyCharm](https://www.jetbrains.com/help/pycharm/pytest.html)

## 🎯 Quick Start

1. **Start debugging**:
   - Select "FastAPI Dev Server"
   - Click bug icon (Debug)

2. **Set a breakpoint**:
   - Open `src/pindrop_challenge/presentation/api/v1/health.py`
   - Click in gutter next to line 117

3. **Trigger it**:
   - Open http://localhost:8000/api/v1/health
   - Watch PyCharm stop at your breakpoint!

4. **Explore**:
   - Inspect variables
   - Step through code
   - Evaluate expressions in debug console

Happy debugging! 🐛✨
