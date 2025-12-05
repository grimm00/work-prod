# Fix Plan: PR #12 Batch MEDIUM LOW - Batch 01

**PR:** 12  
**Batch:** medium-low-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟢 LOW  
**Status:** 🔴 Not Started  
**Created:** 2025-12-04  
**Issues:** 2 issues

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR12-#1 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Use `click.Choice` for CLI validation |
| PR12-#2 | 🟡 MEDIUM | 🟢 LOW | 🟢 LOW | Tighten test expectations for invalid status |

---

## Overview

This batch contains 2 MEDIUM priority issues with LOW effort. These issues improve CLI validation and test quality.

**Estimated Time:** 1-2 hours  
**Files Affected:**
- `scripts/project_cli/commands/list_cmd.py`
- `backend/tests/integration/api/test_projects.py`

---

## Issue Details

### Issue PR12-#1: Use click.Choice for CLI Validation

**Location:** `scripts/project_cli/commands/list_cmd.py:13-18`  
**Sourcery Comment:** Comment #1  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
Because `status` and `classification` only accept specific values, consider using `click.Choice([...])` for these options. That way invalid inputs are rejected at the CLI instead of being sent to the API and silently ignored, which currently leads to unfiltered results.

**Current Code:**
```python
@click.option('--status', '-s', help='Filter by status (active, paused, completed, cancelled)')
@click.option('--classification', '-c', help='Filter by classification (primary, secondary, archive, maintenance)')
```

**Proposed Solution:**
```python
@click.option(
    '--status', '-s',
    type=click.Choice(['active', 'paused', 'completed', 'cancelled'], case_sensitive=False),
    help='Filter by status (active, paused, completed, cancelled)'
)
@click.option(
    '--classification', '-c',
    type=click.Choice(['primary', 'secondary', 'archive', 'maintenance'], case_sensitive=False),
    help='Filter by classification (primary, secondary, archive, maintenance)'
)
```

---

### Issue PR12-#2: Tighten Test Expectations for Invalid Status

**Location:** `backend/tests/integration/api/test_projects.py:661-670`  
**Sourcery Comment:** Comment #2  
**Priority:** 🟡 MEDIUM | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
The phase description says invalid filter values are ignored and all projects are returned, but this test currently permits both 200 and 400, which under-specifies the behavior and can hide regressions. Please assert the specific contract you want to guarantee (e.g., `status_code == 200` and all projects returned).

**Current Code:**
```python
@pytest.mark.integration
def test_filter_projects_invalid_status_value(client):
    # Test currently allows both 200 and 400
    response = client.get('/api/projects?status=invalid')
    assert response.status_code in [200, 400]  # Under-specified
```

**Proposed Solution:**
```python
@pytest.mark.integration
def test_filter_projects_invalid_status_value(client):
    """Test that invalid status values are ignored and all projects returned."""
    response = client.get('/api/projects?status=invalid')
    assert response.status_code == 200  # Specific contract
    data = response.get_json()
    assert isinstance(data, list)
    # Should return all projects (invalid filter ignored)
```

---

## Implementation Steps

1. **Issue PR12-#1: CLI Validation**
   - [ ] Update `list_cmd.py` to use `click.Choice` for `--status` option
   - [ ] Update `list_cmd.py` to use `click.Choice` for `--classification` option
   - [ ] Test CLI with invalid values to verify error messages
   - [ ] Verify valid values still work correctly

2. **Issue PR12-#2: Test Expectations**
   - [ ] Update `test_filter_projects_invalid_status_value` to assert status_code == 200
   - [ ] Verify test passes with current implementation
   - [ ] Check if similar tests need updating (invalid classification, etc.)

---

## Testing

- [ ] All existing tests pass
- [ ] CLI validation tested with invalid status values
- [ ] CLI validation tested with invalid classification values
- [ ] CLI validation tested with valid values (still works)
- [ ] Test for invalid status asserts correct behavior (200, all projects)
- [ ] No regressions introduced

---

## Files to Modify

- `scripts/project_cli/commands/list_cmd.py` - Add click.Choice validation
- `backend/tests/integration/api/test_projects.py` - Tighten test expectations

---

## Definition of Done

- [ ] CLI validates status and classification at input (PR12-#1)
- [ ] Invalid values show clear error messages
- [ ] Test expectations match documented behavior (PR12-#2)
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
These issues are batched together because they:
- Share similar priority (MEDIUM) and effort (LOW) levels
- Both improve code quality and user experience
- Can be implemented together efficiently
- Related to validation/contract clarity

