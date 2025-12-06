# Fix Plan: PR #29 Batch MEDIUM MEDIUM - Batch 01

**PR:** 29  
**Batch:** medium-medium-01  
**Priority:** MEDIUM  
**Effort:** MEDIUM  
**Status:** 🔴 Not Started  
**Created:** 2025-12-06  
**Issues:** 3 issues

---

## Issues in This Batch

| Issue   | Priority   | Impact   | Effort   | Description   |
| ------- | ---------- | -------- | -------- | ------------- |
| PR29-#4 | 🟡 MEDIUM | 🟢 LOW | 🟡 MEDIUM | Code duplication in CLI test fixtures - maintainability |
| Overall #2 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Scope API mocking more narrowly |
| Overall #3 | 🟡 MEDIUM | 🟢 LOW | 🟠 HIGH | Improve CLI script loading mechanism |

---

## Overview

This batch contains 3 MEDIUM priority issues with MEDIUM/HIGH effort. These issues improve code maintainability and test infrastructure quality.

**Estimated Time:** 2-3 hours  
**Files Affected:**
- `scripts/project_cli/tests/conftest.py` - Refactor mock_api_for_cli fixture
- `scripts/project_cli/tests/integration/test_helpers.py` - Centralize FlaskTestClientAdapter usage
- `scripts/project_cli/tests/integration/cli_loader.py` - Improve CLI script loading
- Multiple CLI test files - Update to use centralized helpers

---

## Issue Details

### Issue PR29-#4: Code Duplication in CLI Test Fixtures

**Location:** `scripts/project_cli/tests/conftest.py:41-50`  
**Sourcery Comment:** Comment #4  
**Priority:** MEDIUM | **Impact:** LOW | **Effort:** MEDIUM

**Description:**

This fixture re-implements the `FlaskTestClientAdapter` wiring and `requests`/`Session` monkeypatching already provided by `FlaskTestClientAdapter`/`mock_api_client` in `scripts/project_cli/tests/integration/test_helpers.py`. To avoid drift and simplify maintenance, consider delegating from `mock_api_for_cli` to that shared helper (e.g., `mock_api_client(test_client, monkeypatch)`), and keep only the CLI-specific health-check and config overrides here.

**Current Code:**

The `mock_api_for_cli` fixture duplicates the FlaskTestClientAdapter setup logic.

**Proposed Solution:**

Extract shared FlaskTestClientAdapter setup to a helper function in `test_helpers.py`, then have `mock_api_for_cli` delegate to it, keeping only CLI-specific overrides (health check, config).

---

### Issue Overall #2: Scope API Mocking More Narrowly

**Location:** `scripts/project_cli/tests/conftest.py` and `test_helpers.py`  
**Sourcery Comment:** Overall Comment #2  
**Priority:** MEDIUM | **Impact:** MEDIUM | **Effort:** MEDIUM

**Description:**

The FlaskTestClientAdapter and mock_api_for_cli fixtures patch requests.Session.__init__ and top-level requests methods globally; scoping this more narrowly (e.g., via context managers or per-test session objects) would reduce the risk of surprising side effects if other tests or utilities use requests.

**Proposed Solution:**

Use context managers or per-test session objects to scope API mocking more narrowly, reducing global side effects.

---

### Issue Overall #3: Improve CLI Script Loading

**Location:** `scripts/project_cli/tests/integration/cli_loader.py`  
**Sourcery Comment:** Overall Comment #3  
**Priority:** MEDIUM | **Impact:** LOW | **Effort:** HIGH

**Description:**

The cli_loader executes the proj script via exec, which can be fragile; if possible, exposing the Click group from a regular Python module and importing that in tests would give you a more robust and debuggable loading mechanism.

**Proposed Solution:**

Refactor CLI to expose Click group from a regular Python module that can be imported directly, rather than executing the script file.

---

## Implementation Steps

1. **Issue PR29-#4: Centralize CLI Test Fixtures**
   - [ ] Extract shared FlaskTestClientAdapter setup to helper function
   - [ ] Update `mock_api_for_cli` to delegate to shared helper
   - [ ] Keep only CLI-specific overrides in `mock_api_for_cli`
   - [ ] Update all test files to use centralized helper

2. **Issue Overall #2: Scope API Mocking**
   - [ ] Refactor mocking to use context managers
   - [ ] Or use per-test session objects
   - [ ] Ensure no global side effects
   - [ ] Test that other utilities using requests aren't affected

3. **Issue Overall #3: Improve CLI Script Loading**
   - [ ] Refactor `proj` script to expose Click group from module
   - [ ] Update `cli_loader.py` to import directly
   - [ ] Remove exec-based loading
   - [ ] Update all test files to use new loading mechanism

---

## Testing

- [ ] All existing tests pass
- [ ] No regressions introduced
- [ ] Mocking scoped correctly (no global side effects)
- [ ] CLI loading more robust

---

## Files to Modify

- `scripts/project_cli/tests/conftest.py` - Refactor mock_api_for_cli fixture
- `scripts/project_cli/tests/integration/test_helpers.py` - Add shared helper function
- `scripts/project_cli/tests/integration/cli_loader.py` - Improve CLI loading
- `scripts/project_cli/proj` - Refactor to expose Click group from module (if needed)
- All CLI test files - Update to use centralized helpers

---

## Definition of Done

- [ ] Code duplication removed
- [ ] API mocking scoped narrowly
- [ ] CLI loading improved
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**

These issues are batched together because they:

- All relate to test infrastructure improvements
- Share similar priority and effort levels
- Can be implemented together to improve overall test quality
- Reduce maintenance burden and improve test reliability

