# Fix Plan: PR #12 Batch LOW LOW - Batch 01

**PR:** 12  
**Batch:** low-low-01  
**Priority:** 🟢 LOW  
**Effort:** 🟢 LOW  
**Status:** 🔴 Not Started  
**Created:** 2025-12-04  
**Issues:** 2 issues

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR12-#4 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Use named expression |
| PR12-#5 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Raise from previous error |

---

## Overview

This batch contains 2 LOW priority issues with LOW effort. These are minor code quality improvements that can be done quickly.

**Estimated Time:** 30 minutes - 1 hour  
**Files Affected:**
- `backend/app/api/projects.py`
- `scripts/project_cli/commands/list_cmd.py`

---

## Issue Details

### Issue PR12-#4: Use Named Expression

**Location:** `backend/app/api/projects.py:58` (around lines 141-163)  
**Sourcery Comment:** Comment #4  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Use named expression (walrus operator `:=`) to simplify assignment and conditional checks.

**Current Code:**
```python
# Filter by status
if 'status' in request.args:
    status = request.args['status']
    if status in VALID_STATUSES:
        query = query.filter_by(status=status)

# Filter by classification
if 'classification' in request.args:
    classification = request.args['classification']
    if classification in VALID_CLASSIFICATIONS:
        query = query.filter_by(classification=classification)
```

**Proposed Solution:**
```python
# Filter by status
if 'status' in request.args and (status := request.args['status']) in VALID_STATUSES:
    query = query.filter_by(status=status)

# Filter by classification
if 'classification' in request.args and (classification := request.args['classification']) in VALID_CLASSIFICATIONS:
    query = query.filter_by(classification=classification)
```

---

### Issue PR12-#5: Raise from Previous Error

**Location:** `scripts/project_cli/commands/list_cmd.py:22` (around line 239-241)  
**Sourcery Comment:** Comment #5  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Explicitly raise from a previous error to preserve exception context.

**Current Code:**
```python
except Exception as e:
    console.print(f"[red]Error: {e}[/red]")
    raise click.Abort()
```

**Proposed Solution:**
```python
except Exception as e:
    console.print(f"[red]Error: {e}[/red]")
    raise click.Abort() from e
```

---

## Implementation Steps

1. **Issue PR12-#4: Named Expression**
   - [ ] Update status filter to use named expression
   - [ ] Update classification filter to use named expression
   - [ ] Verify functionality unchanged
   - [ ] Run tests to ensure no regressions

2. **Issue PR12-#5: Raise from Previous Error**
   - [ ] Update exception handler in `list_cmd.py` to use `from e`
   - [ ] Verify error messages still display correctly
   - [ ] Test error handling still works

---

## Testing

- [ ] All existing tests pass
- [ ] Filtering still works correctly (status, classification)
- [ ] Error handling still works correctly
- [ ] No regressions introduced

---

## Files to Modify

- `backend/app/api/projects.py` - Use named expressions for filters
- `scripts/project_cli/commands/list_cmd.py` - Raise from previous error

---

## Definition of Done

- [ ] Named expressions used in filter logic (PR12-#4)
- [ ] Exception chaining added (PR12-#5)
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
These issues are batched together because they:
- Share similar priority (LOW) and effort (LOW) levels
- Are quick code quality improvements
- Can be implemented together efficiently
- Don't require extensive testing

