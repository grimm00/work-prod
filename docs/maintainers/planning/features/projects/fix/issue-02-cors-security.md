# Fix: CORS Security Configuration

**Sourcery Issue:** PR #1, Comment #2  
**Location:** `backend/app/__init__.py:39`  
**Priority:** 🔴 CRITICAL | **Impact:** 🔴 CRITICAL | **Effort:** 🟢 LOW

## Problem

`CORS(app)` with default settings allows all origins, which is:
- Convenient for development
- Security risk in production (allows any website to make API calls)

## Solution

Configure CORS per environment:
- Development: Allow localhost origins only
- Testing: Allow test origins
- Production: Restrict to specific deployed frontend domain

## Implementation

**File 1:** `backend/config.py`

Add CORS settings to each config class:

```python
class Config:
    # ... existing config ...
    
    # CORS settings
    CORS_ORIGINS = []  # Override in subclasses

class DevelopmentConfig(Config):
    # ... existing config ...
    CORS_ORIGINS = [
        'http://localhost:5173',  # Vite dev server
        'http://localhost:3000',  # Alternative frontend port
    ]

class TestingConfig(Config):
    # ... existing config ...
    CORS_ORIGINS = ['http://localhost:5173']

class ProductionConfig(Config):
    # ... existing config ...
    CORS_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
```

**File 2:** `backend/app/__init__.py`

Update CORS initialization:

```python
# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)

# Configure CORS with environment-specific origins
CORS(app, origins=app.config.get('CORS_ORIGINS', []))
```

**File 3:** `backend/.env.example`

Add CORS configuration:

```
# CORS Configuration (Production)
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## Testing

1. Verify development allows localhost:5173
2. Verify production blocks unauthorized origins
3. Test OPTIONS preflight requests
4. Check CORS headers in response

## ADRs

No ADR needed - security configuration update.

