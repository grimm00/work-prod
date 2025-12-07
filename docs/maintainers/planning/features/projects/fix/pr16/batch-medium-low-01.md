# Fix Plan: PR #16 Batch MEDIUM LOW - Batch 01

**PR:** 16  
**Batch:** medium-low-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟢 LOW  
**Status:** ✅ Complete  
**Created:** 2025-12-05  
**Completed:** 2025-12-05  
**Issues:** 2 issues

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR16-#1 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Validate request body shape more strictly |
| PR16-#3 | 🟡 MEDIUM | 🟢 LOW | 🟢 LOW | Add test for non-JSON requests |

---

## Overview

This batch contains 2 MEDIUM priority issues with LOW effort. These issues improve API validation and test coverage.

**Estimated Time:** 1 hour  
**Files Affected:**
- `backend/app/api/projects.py`
- `backend/tests/integration/api/test_projects_import.py`

---

## Issue Details

### Issue PR16-#1: Validate Request Body Shape More Strictly

**Location:** `backend/app/api/projects.py:322-340`  
**Sourcery Comment:** Comment #1  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
As written, any JSON value will pass: if `data` isn't a dict or `projects` isn't a list, we treat it as empty, return 201, and emit all-zero stats, masking client errors. Please explicitly enforce `isinstance(data, dict)` and `isinstance(projects_data, list)` and return a 400 with a clear message when those expectations are not met.

**Current Code:**
```python
try:
    data = request.get_json()
except Exception:
    return jsonify({'error': 'Invalid JSON'}), 400

imported = 0
skipped = 0
errors = []

projects_data = data.get('projects', [])

for project_data in projects_data:
```

**Proposed Solution:**
```python
try:
    data = request.get_json()
except Exception:
    return jsonify({'error': 'Invalid JSON'}), 400

if not isinstance(data, dict):
    return jsonify({'error': 'Request body must be a JSON object'}), 400

if 'projects' not in data:
    return jsonify({'error': "Missing 'projects' field"}), 400

projects_data = data['projects']
if not isinstance(projects_data, list):
    return jsonify({'error': "'projects' field must be a list"}), 400

imported = 0
skipped = 0
errors = []

for project_data in projects_data:
```

---

### Issue PR16-#3: Add Test for Non-JSON Requests

**Location:** `backend/tests/integration/api/test_projects_import.py:13-22`  
**Sourcery Comment:** Comment #3  
**Priority:** 🟡 MEDIUM | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
We currently only test the invalid JSON body case with `content_type='application/json'`. Please also add a test that sends a non‑JSON request (e.g., form data or plain text without the JSON content-type) and asserts the 400 status and `{'error': 'Content-Type must be application/json'}` response from the `if not request.is_json` branch to cover that path and guard against regressions.

**Current Code:**
```python
@pytest.mark.integration
def test_import_invalid_json(client):
    """Test that invalid JSON returns 400 Bad Request."""
    response = client.post(
        '/api/projects/import',
        json={'invalid': 'json'},
        content_type='application/json'
    )
    assert response.status_code == 400
```

**Proposed Solution:**
```python
@pytest.mark.integration
def test_import_invalid_json(client):
    """Test that invalid JSON returns 400 Bad Request."""
    response = client.post(
        '/api/projects/import',
        json={'invalid': 'json'},
        content_type='application/json'
    )
    assert response.status_code == 400

@pytest.mark.integration
def test_import_non_json_content_type(client):
    """Test that non-JSON Content-Type returns 400 Bad Request."""
    response = client.post(
        '/api/projects/import',
        data='not json',
        content_type='text/plain'
    )
    assert response.status_code == 400
    assert response.json['error'] == 'Content-Type must be application/json'
```

---

## Implementation Steps

1. **Issue PR16-#1: Request Body Validation**
   - [x] Add `isinstance(data, dict)` check after JSON parsing
   - [x] Add check for 'projects' key presence
   - [x] Add `isinstance(projects_data, list)` check
   - [x] Return 400 with clear error messages for each validation failure
   - [x] Update docstring to reflect new error cases
   - [x] Test validation with invalid request bodies

2. **Issue PR16-#3: Non-JSON Test**
   - [x] Add new test `test_import_non_json_content_type`
   - [x] Send request with non-JSON Content-Type (e.g., `text/plain`)
   - [x] Assert 400 status code
   - [x] Assert error message matches expected
   - [x] Verify test passes with current implementation

---

## Testing

- [x] All existing tests pass
- [x] New test added for non-JSON Content-Type
- [x] Tests added for invalid request body shapes (non-dict, missing 'projects', non-list 'projects')
- [x] Manual testing completed (if needed)
- [x] No regressions introduced

---

## Files to Modify

- `backend/app/api/projects.py` - Add request body validation
- `backend/tests/integration/api/test_projects_import.py` - Add non-JSON test

---

## Definition of Done

- [x] Request body validation added (PR16-#1)
- [x] Non-JSON Content-Type test added (PR16-#3)
- [x] All tests passing
- [ ] Code reviewed
- [x] Documentation updated (docstring updated)
- [ ] Ready for PR

---

**Batch Rationale:**
These issues are batched together because they:
- Share MEDIUM priority and LOW effort
- Both improve API robustness and test coverage
- Can be implemented together efficiently
- Related to import endpoint validation

