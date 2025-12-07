# Fix Plan: PR #35 Batch MEDIUM LOW - Batch 01

**PR:** #35  
**Batch:** medium-low-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟢 LOW  
**Status:** 🔴 Not Started  
**Created:** 2025-12-07  
**Issues:** 4 issues

---

## Issues in This Batch

| Issue   | Priority   | Impact   | Effort   | Description   |
| ------- | ---------- | -------- | -------- | ------------- |
| PR35-#3 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW   | Test assertion weakness - whitespace-only names |
| PR35-#4 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW   | Test assertion weakness - Rich table output |
| PR35-#5 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW   | Performance test flakiness - tight thresholds |
| PR35-#6 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW   | Test assertion weakness - CORS_ORIGINS default |

---

## Overview

This batch contains 4 MEDIUM priority issues with LOW effort related to test quality improvements. These issues strengthen test assertions and improve test reliability.

**Estimated Time:** 1-2 hours  
**Files Affected:** 
- `scripts/project_cli/tests/integration/test_edge_cases.py`
- `scripts/project_cli/tests/integration/test_list_cmd.py`
- `backend/tests/performance/test_query_performance.py`
- `backend/tests/integration/test_production_config.py`

---

## Issues Details

### Issue PR35-#3: Test Assertion Weakness - Whitespace-Only Names

**Location:** `scripts/project_cli/tests/integration/test_edge_cases.py:84-86`  
**Sourcery Comment:** Comment #3  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
The test assertion allows both success and failure and doesn't check the output, so it no longer constrains behavior for whitespace-only names and will pass through regressions. Should assert the current outcome explicitly or at least assert something about the reported result.

**Current Code:**

```python
# Should reject whitespace-only names
assert result.exit_code != 0 or 'error' in result.output.lower()
```

**Proposed Solution:**

```python
# API currently accepts whitespace-only names (may be trimmed server-side)
# Test verifies command doesn't crash and documents current behavior
assert result.exit_code in [0, 1]  # May succeed or fail validation
# TODO: Strengthen assertion to verify actual behavior (accept or reject)
# For now, explicitly document current behavior
if result.exit_code == 0:
    assert 'created' in result.output.lower() or 'project' in result.output.lower()
else:
    assert 'error' in result.output.lower()
```

**Alternative (if we want to enforce rejection):**

```python
# Should reject whitespace-only names
assert result.exit_code != 0, "Whitespace-only names should be rejected"
assert 'error' in result.output.lower() or 'invalid' in result.output.lower()
```

---

### Issue PR35-#4: Test Assertion Weakness - Rich Table Output

**Location:** `scripts/project_cli/tests/integration/test_list_cmd.py:130-131`  
**Sourcery Comment:** Comment #4  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
Checking `'Full'` and `'Project'` separately avoids Rich wrapping issues but makes the test more prone to false positives if those words appear elsewhere. Should assert on something more specific (e.g., project path/ID or less ambiguous substring).

**Current Code:**

```python
assert result.exit_code == 0
# Rich table may wrap text, so check for parts of the name
assert 'Full' in result.output and 'Project' in result.output
```

**Proposed Solution:**

```python
assert result.exit_code == 0
# Check for project path/ID or use regex that tolerates line breaks
import re
# Match "Full Project" allowing for line breaks
assert re.search(r'Full\s+Project', result.output, re.MULTILINE) or \
       '/test/full' in result.output or \
       'Full Project' in result.output.replace('\n', ' ')
```

**Alternative (using Rich's console recording):**

```python
from rich.console import Console
from io import StringIO

console = Console(file=StringIO(), record=True)
# ... render table ...
output = console.export_text()
assert 'Full Project' in output
```

---

### Issue PR35-#5: Performance Test Flakiness - Tight Thresholds

**Location:** `backend/tests/performance/test_query_performance.py:13-22`  
**Sourcery Comment:** Comment #5  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
Hard upper bounds on wall-clock time (e.g., `< 0.1` seconds) are likely to be flaky on noisy or constrained CI. Should relax thresholds (e.g., 250-500ms) or use `time.perf_counter()` instead of `time.time()`.

**Current Code:**

```python
start = time.time()
# ... test code ...
elapsed = time.time() - start
assert elapsed < 0.1, f"Query took {elapsed:.3f}s, expected < 0.1s"
```

**Proposed Solution:**

```python
import time

start = time.perf_counter()  # More accurate for timing
# ... test code ...
elapsed = time.perf_counter() - start
# Relaxed threshold: 500ms (was 100ms) to account for CI variability
assert elapsed < 0.5, f"Query took {elapsed:.3f}s, expected < 0.5s"
```

**Alternative (use pytest marker for optional runs):**

```python
@pytest.mark.performance
@pytest.mark.skipif(
    os.getenv('CI') == 'true',
    reason="Performance tests skipped in CI"
)
def test_query_performance():
    # ... test code ...
```

---

### Issue PR35-#6: Test Assertion Weakness - CORS_ORIGINS Default

**Location:** `backend/tests/integration/test_production_config.py:198-203`  
**Sourcery Comment:** Comment #6  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
The test should verify the documented default, not just the type. Should assert the concrete value (empty list) to catch regressions.

**Current Code:**

```python
def test_production_config_cors_origins_default():
    """Test that CORS_ORIGINS defaults to empty list."""
    app = create_app('production')
    # Should default to empty list (no CORS)
    assert isinstance(app.config['CORS_ORIGINS'], list)
```

**Proposed Solution:**

```python
def test_production_config_cors_origins_default():
    """Test that CORS_ORIGINS defaults to empty list."""
    app = create_app('production')
    # Should default to empty list (no CORS)
    assert app.config['CORS_ORIGINS'] == [], \
        f"Expected empty list, got {app.config['CORS_ORIGINS']}"
```

---

## Implementation Steps

1. **Issue PR35-#3: Strengthen Whitespace-Only Name Test**
   - [ ] Open `scripts/project_cli/tests/integration/test_edge_cases.py`
   - [ ] Update assertion to verify actual behavior
   - [ ] Add explicit check for success/failure output
   - [ ] Run test to verify it passes
   - [ ] Document current behavior if keeping permissive assertion

2. **Issue PR35-#4: Strengthen Rich Table Output Test**
   - [ ] Open `scripts/project_cli/tests/integration/test_list_cmd.py`
   - [ ] Update assertion to use regex or project path/ID
   - [ ] Test with Rich table wrapping scenarios
   - [ ] Run test to verify it passes
   - [ ] Consider using Rich console recording if needed

3. **Issue PR35-#5: Relax Performance Test Thresholds**
   - [ ] Open `backend/tests/performance/test_query_performance.py`
   - [ ] Replace `time.time()` with `time.perf_counter()`
   - [ ] Relax thresholds from 100ms to 500ms
   - [ ] Remove or replace `print()` statements with logging
   - [ ] Run performance tests to verify they're less flaky

4. **Issue PR35-#6: Strengthen CORS_ORIGINS Default Test**
   - [ ] Open `backend/tests/integration/test_production_config.py`
   - [ ] Update assertion to check `== []` instead of `isinstance(list)`
   - [ ] Add descriptive error message
   - [ ] Run test to verify it passes

---

## Testing

- [ ] All existing tests pass
- [ ] Test improvements don't break existing functionality
- [ ] Performance tests are less flaky
- [ ] Test assertions catch regressions as intended
- [ ] No regressions introduced

---

## Files to Modify

- `scripts/project_cli/tests/integration/test_edge_cases.py` - Strengthen whitespace-only name test
- `scripts/project_cli/tests/integration/test_list_cmd.py` - Strengthen Rich table output test
- `backend/tests/performance/test_query_performance.py` - Relax thresholds and use perf_counter
- `backend/tests/integration/test_production_config.py` - Strengthen CORS_ORIGINS default test

---

## Definition of Done

- [ ] All 4 issues in batch fixed
- [ ] Tests passing with improved assertions
- [ ] Performance tests less flaky
- [ ] Code reviewed
- [ ] Documentation updated (if needed)
- [ ] Ready for PR

---

**Batch Rationale:**
These issues are batched together because they:

- Share MEDIUM priority and LOW effort levels
- All relate to test quality improvements
- Can be implemented together efficiently
- Improve test reliability and maintainability

