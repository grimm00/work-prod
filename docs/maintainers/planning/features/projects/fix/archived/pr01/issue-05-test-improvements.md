# Fix: Test Code Improvements

**Sourcery Issue:** PR #1, Comment #5  
**Location:** `backend/tests/integration/api/test_health.py:9-18`  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

## Problem

1. Using `json.loads(response.data)` instead of Flask's `response.get_json()`
2. Exact string match for content-type may break if charset added

## Solution

Use Flask's built-in methods for more robust testing.

## Implementation

**Files to update:**
- `backend/tests/integration/api/test_health.py`
- `backend/tests/integration/api/test_projects.py`

**Changes:**

1. Replace `json.loads(response.data)` with `response.get_json()`
2. Replace exact content-type match with `startswith()` or `mimetype` check

```python
# Before
data = json.loads(response.data)
assert response.content_type == 'application/json'

# After
data = response.get_json()
assert response.content_type.startswith('application/json')
# Or: assert response.mimetype == 'application/json'
```

3. Remove `import json` if no longer needed

## Testing

Run full test suite to verify no regressions:

```bash
cd backend
pytest -v
```

## ADRs

No ADR needed - test code improvement.

