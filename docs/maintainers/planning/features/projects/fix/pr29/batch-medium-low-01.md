# Fix Plan: PR #29 Batch MEDIUM LOW - Batch 01

**PR:** 29  
**Batch:** medium-low-01  
**Priority:** MEDIUM  
**Effort:** LOW  
**Status:** 🔴 Not Started  
**Created:** 2025-12-06  
**Issues:** 5 issues

---

## Issues in This Batch

| Issue   | Priority   | Impact   | Effort   | Description   |
| ------- | ---------- | -------- | -------- | ------------- |
| PR29-#2 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Test allows multiple outcomes - weakens regression testing |
| PR29-#3 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | CLI tests allow multiple exit codes - reduces test value |
| PR29-#7 | 🟡 MEDIUM | 🟢 LOW | 🟢 LOW | Conditionals in tests - test quality |
| PR29-#8 | 🟡 MEDIUM | 🟢 LOW | 🟢 LOW | Loops in tests - test quality |
| PR29-#9 | 🟡 MEDIUM | 🟢 LOW | 🟢 LOW | Loops in tests - test quality |

---

## Overview

This batch contains 5 MEDIUM priority issues with LOW effort. These issues improve test quality by tightening test expectations and removing conditionals/loops from tests.

**Estimated Time:** 1-2 hours  
**Files Affected:**
- `backend/tests/integration/api/test_projects_edge_cases.py` - Fix test expectations and remove conditionals/loops
- `scripts/project_cli/tests/integration/test_edge_cases.py` - Fix CLI test exit code expectations

---

## Issue Details

### Issue PR29-#2: Test Allows Multiple Outcomes

**Location:** `backend/tests/integration/api/test_projects_edge_cases.py:71-85`  
**Sourcery Comment:** Comment #2  
**Priority:** MEDIUM | **Impact:** MEDIUM | **Effort:** LOW

**Description:**

`test_create_project_with_whitespace_only_name` asserts `response.status_code in [201, 400]` and only checks the body for the 201 case, so the test will pass even if the API flips between accepting and rejecting whitespace-only names. This weakens its usefulness as a regression test.

**Current Code:**

```python
assert response.status_code in [201, 400]
if response.status_code == 201:
    data = json.loads(response.data)
    assert data['name'] == '   	\n  '  # Stored as-is
```

**Proposed Solution:**

Split into two tests: one that documents current behavior (accepts whitespace-only names) and one that documents desired future behavior (reject whitespace-only names) using `@pytest.mark.xfail`.

---

### Issue PR29-#3: CLI Tests Allow Multiple Exit Codes

**Location:** `scripts/project_cli/tests/integration/test_edge_cases.py:25-34`  
**Sourcery Comment:** Comment #3  
**Priority:** MEDIUM | **Impact:** MEDIUM | **Effort:** LOW

**Description:**

Several CLI edge-case tests (e.g., `test_create_with_very_long_name`, `test_create_with_very_long_description`) use `assert result.exit_code in [0, 1]`, which lets them pass whether the command succeeds or fails and hides behavior changes.

**Proposed Solution:**

Assert specific exit codes based on expected behavior. If behavior is intentionally flexible, document why and use separate tests for each expected outcome.

---

### Issue PR29-#7: Conditionals in Tests

**Location:** `backend/tests/integration/api/test_projects_edge_cases.py:83-85`  
**Sourcery Comment:** Comment #7  
**Priority:** MEDIUM | **Impact:** LOW | **Effort:** LOW

**Description:**

Avoid complex code, like conditionals, in test functions. Conditionals reduce test clarity and can hide bugs.

**Proposed Solution:**

Refactor tests to remove conditionals. Use separate test functions or parametrized tests instead.

---

### Issue PR29-#8: Loops in Tests

**Location:** `backend/tests/integration/api/test_projects_edge_cases.py:168-175`  
**Sourcery Comment:** Comment #8  
**Priority:** MEDIUM | **Impact:** LOW | **Effort:** LOW

**Description:**

Avoid complex code, like loops, in test functions. Loops reduce test clarity and can hide bugs.

**Proposed Solution:**

Refactor tests to remove loops. Use parametrized tests or separate test functions instead.

---

### Issue PR29-#9: Loops in Tests

**Location:** `backend/tests/integration/api/test_projects_edge_cases.py:200-207`  
**Sourcery Comment:** Comment #9  
**Priority:** MEDIUM | **Impact:** LOW | **Effort:** LOW

**Description:**

Same as PR29-#8 - avoid loops in tests.

**Proposed Solution:**

Same as PR29-#8 - refactor to use parametrized tests or separate test functions.

---

## Implementation Steps

1. **Issue PR29-#2: Fix Test Expectations**
   - [ ] Split `test_create_project_with_whitespace_only_name` into two tests
   - [ ] One test documents current behavior (accepts)
   - [ ] One test documents desired behavior (rejects) with `@pytest.mark.xfail`
   - [ ] Remove conditional assertion

2. **Issue PR29-#3: Fix CLI Test Exit Codes**
   - [ ] Find all tests using `assert result.exit_code in [0, 1]`
   - [ ] Determine expected behavior for each test
   - [ ] Update assertions to specific exit codes
   - [ ] Document any intentionally flexible behavior

3. **Issues PR29-#7, #8, #9: Remove Conditionals/Loops**
   - [ ] Identify all conditionals/loops in test functions
   - [ ] Refactor to use parametrized tests or separate test functions
   - [ ] Ensure test clarity and maintainability

---

## Testing

- [ ] All existing tests pass
- [ ] New tests added (if needed)
- [ ] Test expectations tightened
- [ ] No regressions introduced

---

## Files to Modify

- `backend/tests/integration/api/test_projects_edge_cases.py` - Fix test expectations, remove conditionals/loops
- `scripts/project_cli/tests/integration/test_edge_cases.py` - Fix CLI test exit code expectations

---

## Definition of Done

- [ ] Test expectations tightened (no multiple outcomes)
- [ ] CLI test exit codes specific
- [ ] Conditionals removed from tests
- [ ] Loops removed from tests
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**

These issues are batched together because they:

- All relate to test quality improvements
- Share similar priority and effort levels
- Can be implemented together efficiently
- Improve test reliability and maintainability

