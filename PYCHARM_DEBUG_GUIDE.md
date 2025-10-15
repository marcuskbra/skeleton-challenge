# 🐛 PyCharm Debugging Guide for FastAPI

Quick visual guide to debug your FastAPI application in PyCharm.

## 🎯 Quick Start (3 Steps)

### Step 1: Select Configuration
Look at the top-right of PyCharm:

```
┌─────────────────────────────────────┐
│ FastAPI Dev Server    ▼  ▶  🐛      │
└─────────────────────────────────────┘
         ↑              ↑   ↑   ↑
      Select          Run  |  Debug
                          Edit
```

Click the dropdown and select **"FastAPI Dev Server"**

### Step 2: Set a Breakpoint
Open `src/pindrop_challenge/presentation/api/v1/health.py`:

```python
@router.get("/health")
async def health_check() -> DetailedHealthResponse:
    """Comprehensive health check endpoint."""

    # Click in the left gutter here → 🔴
    checks = {
        "application": "healthy",
    }

    return DetailedHealthResponse(...)
```

Click in the **left gutter** (gray area with line numbers) to add a red dot 🔴

### Step 3: Start Debugging
Click the **bug icon** (🐛) next to the run button

Wait for:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Then visit: http://localhost:8000/api/v1/health

**PyCharm will STOP at your breakpoint!** 🎉

## 📊 Debug Window Layout

When stopped at a breakpoint, you'll see:

```
┌─────────────────────────────────────────────────────────────┐
│                     YOUR CODE HERE                          │
│  Line 117: ▶ checks = {  ← Stopped here                    │
│  Line 118:      "application": "healthy",                   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ Debugger                                                    │
├─────────────────┬───────────────────────────────────────────┤
│ Variables       │ Console                                   │
│                 │                                           │
│ checks = {...}  │ >>> checks                                │
│ __version__ =   │ {'application': 'healthy'}                │
│   '0.1.0'       │                                           │
│                 │ >>> __version__                           │
│                 │ '0.1.0'                                   │
└─────────────────┴───────────────────────────────────────────┘
```

## ⌨️ Keyboard Controls

While debugging:

| Key | Action | Description |
|-----|--------|-------------|
| **F9** | Resume | Continue to next breakpoint |
| **F8** | Step Over | Execute current line, don't enter functions |
| **F7** | Step Into | Enter function calls |
| **Shift+F8** | Step Out | Exit current function |
| **Alt+F9** | Run to Cursor | Continue to where cursor is |
| **Ctrl+F8** | Toggle Breakpoint | Add/remove breakpoint at current line |

## 🎓 Common Debugging Scenarios

### Scenario 1: Debug Request Handling

**Set breakpoint in middleware** (`src/pindrop_challenge/presentation/main.py`):

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # 🔴 Breakpoint here
    logger.info("Incoming request: %s %s", request.method, request.url.path)

    response = await call_next(request)  # 🔴 Or here to see response
    return response
```

**Trigger**: Visit http://localhost:8000/api/v1/health

**Inspect**:
- `request.method` → "GET"
- `request.url.path` → "/api/v1/health"
- `request.headers` → All headers

### Scenario 2: Debug Health Check Logic

**Set breakpoint** (`src/pindrop_challenge/presentation/api/v1/health.py`):

```python
@router.get("/health")
async def health_check() -> DetailedHealthResponse:
    # 🔴 Breakpoint here
    checks = {
        "application": "healthy",
    }

    # 🔴 Or here to inspect before return
    return DetailedHealthResponse(
        status="healthy",
        version=__version__,
        timestamp=datetime.now(timezone.utc),
        ...
    )
```

**Inspect**:
- `checks` → Dict with component statuses
- `__version__` → Current app version
- `datetime.now(timezone.utc)` → Current UTC time

### Scenario 3: Debug Application Startup

**Set breakpoint** (`src/pindrop_challenge/presentation/main.py`):

```python
def create_app(environment: str = "development") -> FastAPI:
    # 🔴 Breakpoint here
    app = FastAPI(
        title="Pindrop Challenge API",
        description="A modern Python API with Clean Architecture",
        version=__version__,
        lifespan=lifespan,
    )

    # 🔴 Or here to check after CORS config
    _configure_cors(app, environment)

    return app
```

**Inspect**:
- `environment` → "development" or "production"
- `app.routes` → All registered routes
- `app.middleware_stack` → Middleware configuration

## 🔍 Debug Console Tips

While stopped at a breakpoint, use the **Console** tab to evaluate expressions:

```python
# Check variable values
>>> checks
{'application': 'healthy'}

# Evaluate expressions
>>> f"Version: {__version__}"
'Version: 0.1.0'

# Call functions
>>> logger.info("Debug checkpoint reached")

# Check request details
>>> request.headers.get("user-agent")
'Mozilla/5.0...'

# Test conditions
>>> "application" in checks
True
```

## 📝 Available Configurations

You have 5 pre-configured debug setups:

### 🚀 Server Configurations

1. **FastAPI Dev Server** ⭐ (Recommended)
   - Auto-reload enabled
   - Development mode
   - Port 8000
   - **Use for**: Day-to-day development

2. **FastAPI Production**
   - 4 workers
   - No auto-reload
   - Production mode (no docs)
   - **Use for**: Testing production behavior

### 🧪 Test Configurations

3. **API Tests**
   - Tests: `tests/unit/presentation/api/`
   - **Use for**: Testing API endpoints

4. **All Unit Tests**
   - Tests: `tests/unit/`
   - **Use for**: Full test suite

5. **Tests with Coverage**
   - Tests: `tests/`
   - Generates HTML report
   - **Use for**: Coverage analysis

## 💡 Pro Tips

### Conditional Breakpoints

Right-click on a breakpoint (red dot) → **More** → Add condition:

```python
# Only stop when specific condition is true
request.url.path == "/api/v1/health"
```

### Evaluate Expression

While debugging, select any expression in your code → Right-click → **Evaluate Expression**

### Watch Variables

**Debugger** tab → **Variables** → Right-click variable → **Add to Watches**

### Breakpoint on Exception

`Run` → `View Breakpoints...` → Check **"Python Exception Breakpoints"**

### Remote Debugging

You can debug code running in Docker or on another machine:
1. `Run` → `Edit Configurations...`
2. `+` → `Python Remote Debug`
3. Configure host/port
4. Add `pydevd_pycharm` to your code

## 🚨 Troubleshooting

### "Cannot debug: no module named uvicorn"

**Solution**: Make sure project interpreter is set to `.venv`:
1. `File` → `Settings` → `Project: pindrop-challenge` → `Python Interpreter`
2. Select `.venv/bin/python`

### Breakpoints not triggering

**Check**:
1. ✅ Configuration is running (not just "Run", use "Debug")
2. ✅ Red dot is solid (not hollow)
3. ✅ Code matches what's running (save all files)
4. ✅ Request actually reaches that code path

### "Address already in use"

**Solution**: Stop other processes on port 8000:
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>
```

Or change port in configuration:
- Edit `FastAPI Dev Server` → Change `--port 8000` to `--port 8001`

## 📚 Next Steps

1. **Try it now**:
   - Select "FastAPI Dev Server"
   - Set breakpoint in `health_check()`
   - Click Debug 🐛
   - Visit http://localhost:8000/api/v1/health

2. **Explore**:
   - Try different breakpoint locations
   - Use Step Over (F8) and Step Into (F7)
   - Evaluate expressions in console

3. **Advanced**:
   - Add conditional breakpoints
   - Debug async code
   - Profile performance

Happy debugging! 🐛✨

---

**Need help?** Check `.idea/runConfigurations/README.md` for detailed configuration info.
