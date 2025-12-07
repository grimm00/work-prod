# Fix Plan: PR #29 Batch MEDIUM LOW - Batch 03

**PR:** 29  
**Batch:** medium-low-03  
**Priority:** MEDIUM  
**Effort:** LOW  
**Status:** 🔴 Not Started  
**Created:** 2025-12-06  
**Issues:** 2 issues

---

## Issues in This Batch

| Issue   | Priority   | Impact   | Effort   | Description   |
| ------- | ---------- | -------- | -------- | ------------- |
| PR29-#14 | 🟡 MEDIUM | 🟢 LOW | 🟢 LOW | Import test modules - code quality |
| Overall #1 | 🟡 MEDIUM | 🟢 LOW | 🟢 LOW | Centralize sys.path manipulation in CLI tests |

---

## Overview

This batch contains 2 MEDIUM priority issues with LOW effort. These issues improve code quality by centralizing test infrastructure setup.

**Estimated Time:** 1 hour  
**Files Affected:**
- `scripts/project_cli/tests/conftest.py` - Fix import test modules
- Multiple CLI test files - Centralize sys.path manipulation

---

## Issue Details

### Issue PR29-#14: Import Test Modules

**Location:** `scripts/project_cli/tests/conftest.py:18`  
**Sourcery Comment:** Comment #14  
**Priority:** MEDIUM | **Impact:** LOW | **Effort:** LOW

**Description:**

Don't import test modules. The conftest.py imports from `tests.conftest`, which is importing test modules.

**Current Code:**

```python
from tests.conftest import app, client, db, cli_runner
```

**Proposed Solution:**

Import fixtures directly without importing test modules. Use proper fixture imports or refactor to avoid importing test modules.

---

### Issue Overall #1: Centralize sys.path Manipulation

**Location:** Multiple CLI test files  
**Sourcery Comment:** Overall Comment #1  
**Priority:** MEDIUM | **Impact:** LOW | **Effort:** LOW

**Description:**

The CLI tests currently manipulate sys.path in multiple files (e.g., adding backend_dir in several test modules); consider centralizing this path setup in a single helper or conftest to reduce duplication and make future restructuring less brittle.

**Proposed Solution:**

Centralize sys.path manipulation in conftest.py or a shared helper function. Remove duplicate sys.path manipulation from individual test files.

---

## Implementation Steps

1. **Issue PR29-#14: Fix Import Test Modules**
   - [ ] Review import statement in conftest.py
   - [ ] Refactor to avoid importing test modules
   - [ ] Use proper fixture imports
   - [ ] Verify fixtures still work correctly

2. **Issue Overall #1: Centralize sys.path Manipulation**
   - [ ] Identify all files manipulating sys.path
   - [ ] Move sys.path manipulation to conftest.py
   - [ ] Remove duplicate sys.path code from test files
   - [ ] Verify all tests still work

---

## Testing

- [ ] All existing tests pass
- [ ] No regressions introduced
- [ ] Code quality improved

---

## Files to Modify

- `scripts/project_cli/tests/conftest.py` - Fix imports, centralize sys.path
- Multiple CLI test files - Remove duplicate sys.path manipulation

---

## Definition of Done

- [ ] Import test modules issue fixed
- [ ] sys.path manipulation centralized
- [ ] Duplicate code removed
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**

These issues are batched together because they:

- Both relate to test infrastructure setup
- Share similar priority and effort levels
- Can be implemented together efficiently
- Improve code maintainability

