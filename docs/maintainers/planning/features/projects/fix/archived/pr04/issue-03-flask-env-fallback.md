# Fix Plan: PR #4 Issue #3 - FLASK_ENV Fallback Missing

**PR:** #4  
**Sourcery Comment:** #3  
**Status:** 🔴 CRITICAL - Breaking Change  
**Created:** 2025-12-03  
**Fixed:** 🔴 Not Fixed

---

## Priority Assessment

- **Priority:** 🔴 CRITICAL
- **Impact:** 🔴 CRITICAL
- **Effort:** 🟢 LOW

---

## Problem Description

### What Went Wrong

PR #4 changed configuration loading from `FLASK_ENV` to `APP_CONFIG` without providing a fallback. This is a **breaking change** that will break any existing deployment using `FLASK_ENV=production`.

**Current Code** (in `backend/run.py`):
```python
config_name = os.environ.get('APP_CONFIG', 'development')
app = create_app(config_name)
```

**Problem:**
- Deployments with `FLASK_ENV=production` will get `config_name='development'`
- Production app runs with development configuration
- Wrong database, debug mode enabled, security implications

### Sourcery Feedback

"With this change, environments that only set `FLASK_ENV=production` will now run with the default `'development'` config, which is a regression. Please either fall back to `FLASK_ENV` when `APP_CONFIG` is unset or fail explicitly."

### Current Impact

**⚠️ CRITICAL:** This bug is already in the `develop` branch (merged in PR #4). Any deployment from `develop` will be affected.

---

## Solution Approach

### Option 1: Fallback to FLASK_ENV (RECOMMENDED)

Maintain backwards compatibility by checking both environment variables:

```python
# backend/run.py
config_name = os.environ.get('APP_CONFIG') or os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)
```

**Pros:**
- Backwards compatible
- Existing deployments keep working
- Gradual migration path

**Cons:**
- Still supports deprecated FLASK_ENV

### Option 2: Fail Explicitly

Require APP_CONFIG and fail if not set:

```python
config_name = os.environ.get('APP_CONFIG')
if not config_name:
    raise RuntimeError("APP_CONFIG environment variable required")
app = create_app(config_name)
```

**Pros:**
- Forces explicit configuration
- No ambiguity

**Cons:**
- Breaking change (intentional this time)
- Requires deployment updates

### Recommended: Option 1 (Backwards Compatible Fallback)

---

## Implementation Steps

### 1. Update `backend/run.py`

```python
# Load environment variables from .env file
load_dotenv()

# Create Flask app with explicit configuration
# APP_CONFIG can be: 'development', 'testing', 'production'
# Falls back to FLASK_ENV for backwards compatibility, then 'development'
config_name = os.environ.get('APP_CONFIG') or os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)
```

### 2. Add Comment Explaining Fallback

```python
# Backwards compatibility: Support both APP_CONFIG (new) and FLASK_ENV (deprecated)
# Priority: APP_CONFIG > FLASK_ENV > 'development'
```

### 3. Update Documentation

Update `backend/README.md` to document:
- Primary: Use `APP_CONFIG`
- Fallback: `FLASK_ENV` still supported
- Migration: Recommend switching to `APP_CONFIG`

---

## Testing Requirements

### Test Scenarios

1. **APP_CONFIG set:** Should use APP_CONFIG
   ```bash
   APP_CONFIG=production python backend/run.py
   # Verify ProductionConfig loaded
   ```

2. **FLASK_ENV set (no APP_CONFIG):** Should use FLASK_ENV
   ```bash
   FLASK_ENV=production python backend/run.py
   # Verify ProductionConfig loaded
   ```

3. **Neither set:** Should default to development
   ```bash
   python backend/run.py
   # Verify DevelopmentConfig loaded
   ```

4. **Both set:** APP_CONFIG takes precedence
   ```bash
   APP_CONFIG=testing FLASK_ENV=production python backend/run.py
   # Verify TestingConfig loaded (APP_CONFIG wins)
   ```

### Test Coverage

Add unit test in `backend/tests/test_config.py`:
```python
def test_config_priority():
    """Test that APP_CONFIG takes precedence over FLASK_ENV."""
    # Test scenarios above
```

---

## Related ADRs

- **ADR-0001:** Flask Backend Architecture
- **ADR-0006:** Testing Framework and TDD Approach

---

## Merge Strategy

**Branch:** `fix/critical-config-logging-issues`  
**Target:** `develop`  
**Priority:** URGENT - Must merge before any other PRs

**After Merge:**
- Phase 2 branch must rebase on updated develop
- Document this in Phase 2 PR description

---

**Created:** 2025-12-03  
**Priority:** 🔴 CRITICAL  
**Status:** 🔴 Not Fixed  
**Blocks:** All future PRs until fixed

