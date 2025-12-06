# Fix Plan: PR #30 Batch MEDIUM MEDIUM - Batch 01

**PR:** 30  
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
| PR30-#1 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Distinguish operational DB errors from data issues |
| PR30-#2 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Use structured error attributes instead of string matching |

---

## Overview

This batch contains 2 MEDIUM priority issues with MEDIUM effort. These issues improve error handling robustness and maintainability in the bulk import functionality.

**Estimated Time:** 2-3 hours  
**Files Affected:**
- `backend/app/api/projects.py` - Import function error handling
- `backend/tests/integration/api/test_projects_uncovered_paths.py` - Tests

---

## Issue Details

### Issue PR30-#1: Distinguish Operational DB Errors

**Location:** `backend/app/api/projects.py:419-428`  
**Sourcery Comment:** Comment #1  
**Priority:** MEDIUM | **Impact:** MEDIUM | **Effort:** MEDIUM

**Description:**

Currently any non-`IntegrityError` is treated as a per-project issue and the loop continues. For systemic DB problems (connectivity, transaction, migrations), this could yield many failures and a confusing partial import. Consider distinguishing operational DB errors from data issues and aborting the import (e.g., return 500 or stop iterating) when an operational error is detected.

**Current Code:**

```python
except IntegrityError as e:
    # Rollback this specific project, but keep the session for others
    db.session.rollback()
    # ... error handling ...
    skipped += 1
    # Continue processing remaining projects

except Exception as e:
    # Generic exception handling - treats all errors as per-project
    # ... error handling ...
    skipped += 1
    # Continue processing remaining projects
```

**Proposed Solution:**

Distinguish between operational DB errors (connectivity, transaction, migrations) and data issues (IntegrityError, validation). For operational errors, abort the import and return 500. For data issues, continue processing.

**Implementation Steps:**

1. Identify operational DB error types (OperationalError, DatabaseError, etc.)
2. Catch operational errors separately from IntegrityError
3. Abort import and return 500 for operational errors
4. Continue processing for data issues (IntegrityError, validation errors)
5. Add tests for operational error handling

---

### Issue PR30-#2: Use Structured Error Attributes

**Location:** `backend/app/api/projects.py:432-433`  
**Sourcery Comment:** Comment #2  
**Priority:** MEDIUM | **Impact:** MEDIUM | **Effort:** MEDIUM

**Description:**

Checking for `'path'` or `'unique'` in `str(e)` is backend- and locale-dependent. Where possible, inspect structured attributes like `e.orig`, `e.params`, or a constraint identifier (e.g., `e.orig.diag.constraint_name` in Postgres) to detect a unique-path violation in a more reliable way.

**Current Code:**

```python
# Determine specific error message
error_msg = 'Failed to import project'
if 'path' in str(e).lower() or 'unique' in str(e).lower():
    error_msg = 'Project with this path already exists'
```

**Proposed Solution:**

Use SQLAlchemy's structured error attributes to detect constraint violations more reliably:
- Check `e.orig` for underlying database error
- Check constraint name if available
- Fallback to string matching only if structured attributes unavailable

**Implementation Steps:**

1. Research SQLAlchemy IntegrityError structure for SQLite
2. Extract constraint information from `e.orig` or `e.params`
3. Check constraint name to identify path uniqueness violation
4. Update error message logic to use structured attributes
5. Add tests for different constraint violation scenarios
6. Document fallback behavior

---

## Testing

- [ ] All existing tests pass
- [ ] New tests added for operational error handling
- [ ] New tests added for structured error attribute detection
- [ ] Test with different database backends (if applicable)
- [ ] Manual testing completed
- [ ] No regressions introduced

---

## Files to Modify

- `backend/app/api/projects.py` - Improve error handling in import_projects function
- `backend/tests/integration/api/test_projects_uncovered_paths.py` - Add tests for error handling improvements

---

## Definition of Done

- [ ] Operational DB errors distinguished from data issues
- [ ] Import aborts for operational errors (returns 500)
- [ ] Structured error attributes used for constraint detection
- [ ] Fallback to string matching if structured attributes unavailable
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Documentation updated (if needed)
- [ ] Ready for PR

---

**Batch Rationale:**

These issues are batched together because they:

- Both improve error handling robustness
- Share similar priority and effort levels
- Affect the same function (`import_projects`)
- Can be implemented together efficiently

