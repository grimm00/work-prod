# Fix Plan: PR #30 Batch LOW LOW - Batch 01

**PR:** 30  
**Batch:** low-low-01  
**Priority:** LOW  
**Effort:** LOW  
**Status:** 🔴 Not Started  
**Created:** 2025-12-06  
**Issues:** 1 issue

---

## Issues in This Batch

| Issue   | Priority   | Impact   | Effort   | Description   |
| ------- | ---------- | -------- | -------- | ------------- |
| PR30-#4 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Tighten assertion on error message |

---

## Overview

This batch contains 1 LOW priority issue with LOW effort. This issue improves test quality by tightening assertions to match exact expected behavior.

**Estimated Time:** 15-30 minutes  
**Files Affected:**
- `backend/tests/integration/api/test_projects_uncovered_paths.py` - Test assertion improvement

---

## Issue Details

### Issue PR30-#4: Tighten Error Message Assertion

**Location:** `backend/tests/integration/api/test_projects_uncovered_paths.py:185-190`  
**Sourcery Comment:** Comment #4  
**Priority:** LOW | **Impact:** LOW | **Effort:** LOW

**Description:**

The current check passes if either `'duplicate'` or `'path'` is present, which is quite loose. Since the implementation returns a specific message (`'Project with this path already exists'`), consider asserting that exact string.

**Current Code:**

```python
# Verify error details
assert 'duplicate' in data['errors'][0]['error'].lower() or 'path' in data['errors'][0]['error'].lower()
assert data['errors'][0]['project'] == 'Duplicate Project'
```

**Proposed Solution:**

Assert the exact error message string returned by the API:

```python
# Verify error details
assert data['errors'][0]['error'] == 'Project with this path already exists'
assert data['errors'][0]['project'] == 'Duplicate Project'
```

**Implementation Steps:**

1. Update assertion to check exact error message
2. Verify test still passes
3. Ensure assertion matches API implementation

---

## Testing

- [ ] All existing tests pass
- [ ] Assertion tightened to exact error message
- [ ] Test still passes with tightened assertion
- [ ] No regressions introduced

---

## Files to Modify

- `backend/tests/integration/api/test_projects_uncovered_paths.py` - Tighten error message assertion

---

## Definition of Done

- [ ] Assertion updated to exact error message
- [ ] Test passes with tightened assertion
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**

This is a simple test quality improvement that can be implemented quickly and improves test precision.

