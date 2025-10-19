# Environment Configuration Guide

## Overview
This project uses environment variables for configuration management across different environments (development, staging, production). Configuration is defined in `.env.example` and loaded via `python-dotenv`.

## Configuration File Structure

### Primary Configuration File
- **`.env.example`** - Template with all available settings and documentation
- **`.env`** - Local configuration (gitignored, create from .env.example)
- **`.env.test`** - Test-specific settings (used by pytest)
- **`.env.production`** - Production settings (keep secure, never commit)

## Configuration Categories

### 1. Application Configuration

**Required Settings**:
```bash
ENVIRONMENT=development  # development, staging, production
APP_NAME=skeleton-challenge
APP_VERSION=0.1.0
DEBUG=false  # NEVER true in production
```

**Server Configuration**:
```bash
HOST=127.0.0.1  # Use 0.0.0.0 for Docker
PORT=8000
```

**When to change**:
- `ENVIRONMENT`: Set per deployment environment
- `DEBUG`: Only true in development (enables detailed errors, auto-reload)
- `HOST`: Use 0.0.0.0 for containers, 127.0.0.1 for local
- `PORT`: Change if port conflict exists

### 2. Logging Configuration

```bash
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=json  # json (production) or text (development)
LOG_FILE=logs/app.log
LOG_MAX_BYTES=10485760  # 10MB
LOG_BACKUP_COUNT=5
```

**Log Level Guidance**:
- **DEBUG**: Development - verbose, all details
- **INFO**: Staging - important events, normal operations
- **WARNING**: Production - warnings and errors only
- **ERROR**: Production critical - errors only
- **CRITICAL**: Production alerts - critical failures only

**Best Practices**:
- Use `json` format in production for log aggregation
- Use `text` format in development for readability
- Rotate logs to prevent disk space issues

### 3. Database Configuration

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DATABASE_POOL_SIZE=10
DATABASE_POOL_TIMEOUT=30
DATABASE_ECHO=false  # Set true to log SQL queries
```

**URL Formats**:
- PostgreSQL: `postgresql://user:pass@host:5432/dbname`
- SQLite: `sqlite:///path/to/db.sqlite` or `sqlite:///:memory:`
- MySQL: `mysql://user:pass@host:3306/dbname`

**Connection Pool Settings**:
- `POOL_SIZE`: Number of persistent connections (10-20 for production)
- `POOL_TIMEOUT`: Seconds to wait for connection (30s recommended)
- `DATABASE_ECHO`: Only enable in development for debugging

**Security Notes**:
- ⚠️ **NEVER commit database credentials**
- Use environment-specific credentials
- Rotate passwords regularly
- Use connection encryption in production

### 4. Cache Configuration

```bash
CACHE_ENABLED=true
CACHE_BACKEND=memory  # memory, redis, memcached
CACHE_TTL=300  # seconds (5 minutes)
CACHE_MAX_SIZE=1000  # entries

# Redis settings (if using Redis)
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=
REDIS_MAX_CONNECTIONS=10
```

**Cache Backend Selection**:
- **memory**: Development, single-instance deployments
- **redis**: Production, multi-instance deployments, persistence needed
- **memcached**: Production, multi-instance, no persistence needed

**TTL Guidelines**:
- Fast-changing data: 60-300s (1-5 minutes)
- Moderate data: 300-1800s (5-30 minutes)
- Slow-changing data: 1800-3600s (30-60 minutes)
- Static data: 3600+ seconds (1+ hours)

### 5. API Configuration

```bash
API_PREFIX=/api/v1
API_TITLE=Skeleton Challenge API
API_VERSION=0.1.0
API_DOCS_ENABLED=true  # ⚠️ DISABLE IN PRODUCTION
API_TIMEOUT=30  # seconds
API_RATE_LIMIT=100  # requests per minute
```

**Security Settings**:
```bash
API_KEY=  # Optional API key
API_KEY_HEADER=X-API-Key
```

**⚠️ Critical Security**:
- **ALWAYS disable API docs in production** (`API_DOCS_ENABLED=false`)
- Set strict rate limits to prevent abuse
- Use API keys for sensitive endpoints
- Keep timeout reasonable (30s) to prevent hanging

**External API Configuration**:
```bash
EXTERNAL_API_URL=https://api.example.com
EXTERNAL_API_KEY=your-api-key
EXTERNAL_API_TIMEOUT=10
```

### 6. Security Configuration

```bash
# ⚠️ CRITICAL SECURITY SETTINGS
SECRET_KEY=change-this-to-a-random-secret-key
JWT_SECRET=change-this-jwt-secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

**🔴 CRITICAL SECURITY REQUIREMENTS**:
1. **Generate random secrets**: Use `python -c "import secrets; print(secrets.token_urlsafe(64))"`
2. **Different secrets per environment**: Development ≠ Staging ≠ Production
3. **Rotate secrets regularly**: At least quarterly
4. **Never commit secrets to git**: Use secret management tools
5. **Use strong secrets**: Minimum 32 characters, cryptographically random

**CORS Settings**:
```bash
CORS_ENABLED=true
CORS_ORIGINS=*  # ⚠️ Use specific domains in production
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=*
CORS_ALLOW_HEADERS=*
```

**Production CORS**:
```bash
CORS_ORIGINS=https://app.example.com,https://admin.example.com
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=GET,POST,PUT,DELETE
CORS_ALLOW_HEADERS=Content-Type,Authorization
```

**Rate Limiting**:
```bash
RATE_LIMIT_ENABLED=false
RATE_LIMIT_REQUESTS=100  # requests per window
RATE_LIMIT_WINDOW=60  # seconds
```

### 7. Monitoring & Observability

```bash
# Metrics
METRICS_ENABLED=false
METRICS_PORT=9090
PROMETHEUS_ENABLED=false

# Tracing
TRACING_ENABLED=false
JAEGER_AGENT_HOST=localhost
JAEGER_AGENT_PORT=6831

# Health Checks
HEALTH_CHECK_ENABLED=true
HEALTH_CHECK_PATH=/health
READY_CHECK_PATH=/ready
```

**Production Recommendations**:
- Enable metrics in production (`METRICS_ENABLED=true`)
- Enable tracing for distributed systems
- Always enable health checks for Kubernetes/Docker
- Use separate port for metrics (9090) to isolate concerns

### 8. Feature Flags

```bash
FEATURE_NEW_ALGORITHM=false
FEATURE_BETA_UI=false
FEATURE_EXPERIMENTAL_API=false
```

**Best Practices**:
- Use feature flags for gradual rollouts
- Prefix with `FEATURE_` for easy identification
- Default to `false` for safety
- Remove flags after feature is stable
- Document flag purpose and timeline

### 9. Development & Testing

```bash
# Test Configuration
TEST_DATABASE_URL=sqlite:///:memory:
TEST_CACHE_ENABLED=false
TEST_EXTERNAL_APIS_ENABLED=false

# Mock Settings
MOCK_EXTERNAL_SERVICES=false
DRY_RUN=false

# Debug Settings
DEBUG_SQL=false
DEBUG_REQUESTS=false
PROFILING_ENABLED=false
```

**Test Environment Guidelines**:
- Use in-memory databases for speed
- Disable external APIs to avoid flaky tests
- Enable mocking for third-party services
- Keep tests isolated and reproducible

## Environment-Specific Configurations

### Development Environment
```bash
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
LOG_FORMAT=text
DATABASE_URL=postgresql://dev:dev@localhost:5432/skeleton_dev
CACHE_BACKEND=memory
API_DOCS_ENABLED=true
CORS_ORIGINS=*
METRICS_ENABLED=false
```

### Staging Environment
```bash
ENVIRONMENT=staging
DEBUG=false
LOG_LEVEL=INFO
LOG_FORMAT=json
DATABASE_URL=postgresql://staging:${DB_PASS}@db.staging:5432/skeleton_staging
CACHE_BACKEND=redis
REDIS_URL=redis://redis.staging:6379/0
API_DOCS_ENABLED=true  # For testing
CORS_ORIGINS=https://staging.example.com
METRICS_ENABLED=true
```

### Production Environment
```bash
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
LOG_FORMAT=json
DATABASE_URL=postgresql://${DB_USER}:${DB_PASS}@db.prod:5432/skeleton_prod
CACHE_BACKEND=redis
REDIS_URL=redis://${REDIS_PASS}@redis.prod:6379/0
API_DOCS_ENABLED=false  # ⚠️ CRITICAL
CORS_ORIGINS=https://app.example.com
METRICS_ENABLED=true
PROMETHEUS_ENABLED=true
TRACING_ENABLED=true
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
```

## Security Best Practices

### 1. Secret Management
- **Use secret management tools**: AWS Secrets Manager, HashiCorp Vault, Azure Key Vault
- **Environment variable injection**: Inject secrets at runtime, not in files
- **Principle of least privilege**: Only give access to needed secrets
- **Audit secret access**: Log who accesses secrets and when

### 2. Configuration Validation
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str
    secret_key: str
    database_url: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def validate(self):
        if self.environment == "production":
            assert len(self.secret_key) >= 32, "Production secret too short"
            assert "localhost" not in self.database_url, "Cannot use localhost in prod"
```

### 3. Required vs Optional Settings

**Required (fail if missing)**:
- `ENVIRONMENT`
- `SECRET_KEY`
- `DATABASE_URL`

**Optional (have defaults)**:
- `DEBUG` (default: false)
- `LOG_LEVEL` (default: INFO)
- `CACHE_ENABLED` (default: false)

## Common Pitfalls

### ❌ Mistake 1: Committing Secrets
```bash
# ❌ NEVER DO THIS
git add .env
git commit -m "Add configuration"
```

**✅ Solution**: Add `.env` to `.gitignore`, use `.env.example` for templates

### ❌ Mistake 2: Using Development Settings in Production
```bash
# ❌ DANGEROUS
DEBUG=true  # In production
API_DOCS_ENABLED=true  # In production
CORS_ORIGINS=*  # In production
```

**✅ Solution**: Use environment-specific configuration files, validate settings

### ❌ Mistake 3: Weak Secrets
```bash
# ❌ INSECURE
SECRET_KEY=password123
JWT_SECRET=secret
```

**✅ Solution**: Generate strong random secrets:
```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

### ❌ Mistake 4: Not Rotating Secrets
**✅ Solution**: Rotate secrets quarterly, have rotation process documented

## Quick Setup Guide

### Initial Setup
```bash
# 1. Copy template
cp .env.example .env

# 2. Generate secrets
python -c "import secrets; print(f'SECRET_KEY={secrets.token_urlsafe(64)}')" >> .env
python -c "import secrets; print(f'JWT_SECRET={secrets.token_urlsafe(64)}')" >> .env

# 3. Configure database
echo "DATABASE_URL=postgresql://user:pass@localhost:5432/dbname" >> .env

# 4. Verify
cat .env | grep -E "(SECRET_KEY|JWT_SECRET|DATABASE_URL)"
```

### Deployment Checklist
- [ ] All secrets are environment-specific
- [ ] `DEBUG=false` in production
- [ ] `API_DOCS_ENABLED=false` in production
- [ ] CORS origins are specific domains
- [ ] Database URL uses production credentials
- [ ] Secrets are at least 32 characters
- [ ] Log level is WARNING or ERROR
- [ ] Rate limiting is enabled
- [ ] Health checks are enabled
- [ ] Metrics/tracing are enabled
