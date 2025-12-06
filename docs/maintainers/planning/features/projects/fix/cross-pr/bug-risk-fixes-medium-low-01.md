# Fix Plan: Cross-PR Batch Bug Risk Fixes

**Batch:** bug-risk-fixes-medium-low-01  
**Priority:** 🟡 MEDIUM / 🟢 LOW  
**Effort:** 🟢 LOW / 🟡 MEDIUM  
**Status:** 🔴 Not Started  
**Created:** 2025-12-06  
**Source:** fix-review-report-2025-12-06.md  
**Issues:** 3 issues from 2 PRs

---

## Issues in This Batch

| Issue | PR | Priority | Impact | Effort | Description |
|-------|----|----------|--------|--------|-------------|
| PR24-#1 | #24 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Guard against invalid `display.max_rows` values - Bug risk: Invalid config values crash CLI |
| PR24-#3 | #24 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Fix health URL construction - Bug risk: Health URL construction brittle |
| PR22-#1 | #22 | 🟡 MEDIUM | 🟢 LOW | 🟢 LOW | Bug risk - Use `.get()` for path to avoid KeyError |

---

## Overview

This batch contains 3 bug risk fixes from PRs #22 and #24. These issues could cause crashes or errors in production and should be prioritized.

**Estimated Time:** 1-2 hours  
**Files Affected:**
- `scripts/project_cli/config.py` (PR24-#1)
- `scripts/project_cli/error_handler.py` (PR24-#3)
- `scripts/project_cli/commands/list_cmd.py` (PR22-#1)

**Source PRs:**
- PR #22: Code refactoring - extract helpers (1 issue)
- PR #24: CLI Enhancement & Daily Use Tools (2 issues)

---

## Issue Details

### Issue PR24-#1: Guard Against Invalid `display.max_rows` Values

**Source PR:** #24 - CLI Enhancement & Daily Use Tools  
**Location:** `scripts/project_cli/config.py:82-84`  
**Sourcery Comment:** Comment #1  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
`get_max_rows` currently does `int(self.get(...))` directly, so a non-numeric `display.max_rows` in `~/.projrc` will raise `ValueError` and break list-like commands. Consider catching `ValueError` and falling back to the default (optionally logging a warning) so invalid config values don't crash the CLI.

**Current Code:**
```python
def get_max_rows(self):
    """Get maximum rows to display."""
    return int(self.get('display', 'max_rows', '50'))
```

**Proposed Solution:**
```python
def get_max_rows(self):
    """Get maximum rows to display."""
    default = 50
    value = self.get('display', 'max_rows', str(default))
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
```

**Rationale:** Prevents CLI crashes when users have invalid config values. Gracefully falls back to default.

---

### Issue PR24-#3: Fix Health URL Construction

**Source PR:** #24 - CLI Enhancement & Daily Use Tools  
**Location:** `scripts/project_cli/error_handler.py:99-108` (check_backend_health function)  
**Sourcery Comment:** Comment #3  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟡 MEDIUM

**Description:**
In `check_backend_health`, `base_url.replace('/api', '/api/health')` relies on `/api` appearing in a specific way and may produce incorrect URLs when `/api` occurs elsewhere in the path or when the base URL is customized. Instead, construct the health URL explicitly (e.g. via `urllib.parse` to adjust the path, or by appending `/health` when `base_url` is already the API root).

**Current Code:**
```python
def check_backend_health(base_url: str) -> bool:
    """Check if backend is running and healthy."""
    try:
        health_url = base_url.replace('/api', '/api/health')
        response = requests.get(health_url, timeout=2)
        return response.status_code == 200
    except:
        return False
```

**Proposed Solution:**
```python
from urllib.parse import urljoin

def check_backend_health(base_url: str) -> bool:
    """Check if backend is running and healthy."""
    try:
        # Construct health URL explicitly
        health_url = urljoin(base_url.rstrip('/') + '/', 'health')
        response = requests.get(health_url, timeout=2)
        return response.status_code == 200
    except Exception:
        return False
```

**Alternative (simpler):**
```python
def check_backend_health(base_url: str) -> bool:
    """Check if backend is running and healthy."""
    try:
        # Ensure base_url ends with /, then append health
        base = base_url.rstrip('/')
        health_url = f"{base}/health"
        response = requests.get(health_url, timeout=2)
        return response.status_code == 200
    except Exception:
        return False
```

**Rationale:** More robust URL construction that works with any base URL format, not just those containing `/api`.

---

### Issue PR22-#1: Use `.get()` for Path to Avoid KeyError

**Source PR:** #22 - Code refactoring - extract helpers  
**Location:** `scripts/project_cli/commands/list_cmd.py:65-70`  
**Sourcery Comment:** Comment #1  
**Priority:** 🟡 MEDIUM | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Here `path` is accessed with `project['path'] or 'N/A'` while the other fields use `project.get(..., 'N/A')`. If `path` is ever missing (e.g. API change or partial object), this will raise a `KeyError` and break the CLI instead of failing gracefully. To align with the other fields and avoid this risk, use `project.get('path') or 'N/A'` (or `project.get('path', 'N/A')`).

**Current Code:**
```python
row_data.append(project['path'] or 'N/A')
```

**Proposed Solution:**
```python
row_data.append(project.get('path') or 'N/A')
```

**Rationale:** Prevents KeyError if API response structure changes. Aligns with other field access patterns.

---

## Implementation Steps

1. **Issue PR24-#1: Guard Invalid Config Values**
   - [ ] Open `scripts/project_cli/config.py`
   - [ ] Update `get_max_rows()` method to catch `ValueError` and `TypeError`
   - [ ] Return default value (50) on exception
   - [ ] Add test for invalid config value handling
   - [ ] Verify CLI doesn't crash with invalid `max_rows` value

2. **Issue PR24-#3: Fix Health URL Construction**
   - [ ] Open `scripts/project_cli/error_handler.py`
   - [ ] Import `urllib.parse.urljoin` or use string concatenation
   - [ ] Update `check_backend_health()` to construct health URL explicitly
   - [ ] Test with various base URL formats (with/without trailing slash, custom paths)
   - [ ] Verify health check works correctly

3. **Issue PR22-#1: Use `.get()` for Path**
   - [ ] Open `scripts/project_cli/commands/list_cmd.py`
   - [ ] Change `project['path']` to `project.get('path')`
   - [ ] Verify behavior unchanged for normal cases
   - [ ] Test with missing path key (if possible)

---

## Testing

- [ ] All existing tests pass
- [ ] New test for invalid `max_rows` config value
- [ ] New test for health URL construction with various base URLs
- [ ] Test for missing path key in project dict
- [ ] Manual testing: CLI doesn't crash with invalid config
- [ ] Manual testing: Health check works with custom base URLs
- [ ] No regressions introduced

---

## Files to Modify

- `scripts/project_cli/config.py` - Add error handling to `get_max_rows()` (PR24-#1)
- `scripts/project_cli/error_handler.py` - Fix health URL construction (PR24-#3)
- `scripts/project_cli/commands/list_cmd.py` - Use `.get()` for path access (PR22-#1)

---

## Definition of Done

- [ ] All 3 issues in batch fixed
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Manual testing completed
- [ ] No regressions introduced
- [ ] Ready for PR

---

**Batch Rationale:**
These issues are batched together because they:

- Are bug risks that could cause crashes or errors
- Should be prioritized before other improvements
- Are relatively quick to fix (LOW/MEDIUM effort)
- Prevent potential production issues

