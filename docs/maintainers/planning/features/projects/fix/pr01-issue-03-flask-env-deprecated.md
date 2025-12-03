# Fix: Replace Deprecated FLASK_ENV

**Sourcery Issue:** PR #1, Comment #3  
**Location:** `backend/run.py:14-15`  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW  
**Status:** ✅ Complete (2025-12-03) | **Merged:** PR #4

## Problem

`FLASK_ENV` is deprecated in Flask 2.3+ and will be removed in future versions.
Using it for configuration selection couples code to deprecated behavior.

## Solution

Use custom environment variable `APP_CONFIG` or `FLASK_CONFIG` for explicit configuration selection.

## Implementation

**File 1:** `backend/run.py`

Replace FLASK_ENV usage:

```python
# Load environment variables from .env file
load_dotenv()

# Create Flask app with explicit configuration
# APP_CONFIG can be: 'development', 'testing', 'production'
config_name = os.environ.get('APP_CONFIG', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**File 2:** `backend/.env.example`

Update environment variable documentation:

```
# Application Configuration
# Options: development, testing, production
APP_CONFIG=development

# Database Configuration
DATABASE_URL=sqlite:///instance/work_prod_dev.db
```

**File 3:** Update all documentation referencing FLASK_ENV

- `backend/README.md`
- `README.md`
- Any setup guides

Replace references to FLASK_ENV with APP_CONFIG.

## Testing

1. Test with `APP_CONFIG=development`
2. Test with `APP_CONFIG=production`
3. Test default (no env var set)
4. Verify config selection works correctly

## ADRs

No ADR needed - implementation modernization.

