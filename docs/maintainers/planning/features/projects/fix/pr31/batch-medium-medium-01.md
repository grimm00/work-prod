# Fix Plan: PR #31 Batch MEDIUM MEDIUM - Batch 01

**PR:** 31  
**Batch:** medium-medium-01  
**Priority:** MEDIUM  
**Effort:** MEDIUM  
**Status:** 🔴 Not Started  
**Created:** 2025-12-06  
**Issues:** 2 issues

---

## Issues in This Batch

| Issue   | Priority   | Impact   | Effort   | Description   |
| ------- | ---------- | -------- | -------- | ------------- |
| PR31-#1 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | sys.path mutation at import time - prefer package-based imports |
| PR31-Overall #2 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | mock_session_init bypasses original initializer - wrap original init |

---

## Overview

This batch contains 2 MEDIUM priority issues with MEDIUM effort. These issues improve package structure and test infrastructure robustness.

**Estimated Time:** 2-3 hours  
**Files Affected:**
- `scripts/project_cli/cli.py` - Package import structure
- `scripts/project_cli/tests/conftest.py` - Mock session initialization

---

## Issue Details

### Issue PR31-#1: Avoid sys.path Mutation

**Location:** `scripts/project_cli/cli.py:13-15`  
**Sourcery Comment:** Comment #1 (also Overall #1)  
**Priority:** MEDIUM | **Impact:** MEDIUM | **Effort:** MEDIUM

**Description:**

Changing `sys.path` at import time can lead to hard-to-debug interactions when other tools or tests import this module, especially if they also adjust `sys.path`. Prefer treating this as a proper package (e.g., install in editable mode) and using package/relative imports instead of adding the `scripts` directory to `sys.path` manually.

**Current Code:**

```python
from pathlib import Path

# Add scripts directory to path for package imports
scripts_dir = str(Path(__file__).parent.parent)
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

import click
```

**Proposed Solution:**

Refactor to use proper package structure:
1. Install CLI as a package in editable mode (`pip install -e .`)
2. Use relative imports within the package
3. Remove `sys.path` mutation
4. Update `setup.py` or `pyproject.toml` to define package entry points

**Alternative (if package installation not feasible):**
- Use relative imports within the package
- Only add to `sys.path` when running as script (not at import time)
- Document the requirement for proper package structure

**Implementation Steps:**

1. Research package installation options (setup.py vs pyproject.toml)
2. Create package configuration file
3. Refactor imports to use relative imports
4. Remove `sys.path` mutation from `cli.py`
5. Update `proj` script to use package entry point or proper import
6. Update documentation for installation
7. Test CLI still works after refactoring
8. Update tests if needed

---

### Issue PR31-Overall #2: Wrap Original Session Initializer

**Location:** `scripts/project_cli/tests/conftest.py` (mock_session_init function)  
**Sourcery Comment:** Overall #2  
**Priority:** MEDIUM | **Impact:** MEDIUM | **Effort:** MEDIUM

**Description:**

The `mock_session_init` functions used to patch `requests.Session.__init__` bypass the original initializer entirely; it may be safer to wrap and call the original `__init__` to preserve any internal requests-session setup while still swapping out the HTTP methods.

**Current Code:**

```python
def mock_session_init(self, *args, **kwargs):
    """Initialize session with mocked methods."""
    # Call original init but don't set up real session
    self.headers = {}
    # Replace methods with adapter methods
    self.get = adapter.get
    self.post = adapter.post
    # ...
```

**Proposed Solution:**

Wrap the original `__init__` method to preserve internal setup:

```python
original_init = requests.Session.__init__

def mock_session_init(self, *args, **kwargs):
    """Initialize session with mocked methods, preserving original setup."""
    # Call original init to preserve internal setup
    original_init(self, *args, **kwargs)
    # Replace methods with adapter methods
    self.get = adapter.get
    self.post = adapter.post
    # ...
```

**Implementation Steps:**

1. Store reference to original `requests.Session.__init__`
2. Update `mock_session_init` to call original init first
3. Then replace methods with adapter methods
4. Test that original session setup is preserved
5. Verify tests still pass
6. Check for any side effects from preserving original init

---

## Testing

- [ ] All existing tests pass
- [ ] CLI still works after package refactoring
- [ ] Mock session initialization preserves original setup
- [ ] No regressions introduced
- [ ] Manual testing completed

---

## Files to Modify

- `scripts/project_cli/cli.py` - Remove sys.path mutation, use proper imports
- `scripts/project_cli/tests/conftest.py` - Wrap original session initializer
- `setup.py` or `pyproject.toml` - Add package configuration (if needed)
- `scripts/project_cli/proj` - Update to use package entry point (if needed)
- Documentation - Update installation instructions

---

## Definition of Done

- [ ] sys.path mutation removed from cli.py
- [ ] Package structure improved (or documented requirement)
- [ ] Mock session initializer wraps original init
- [ ] All tests passing
- [ ] CLI functionality verified
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Ready for PR

---

**Batch Rationale:**

These issues are batched together because they:

- Both improve code structure and maintainability
- Share similar priority and effort levels
- Affect test infrastructure and package structure
- Can be implemented together efficiently

