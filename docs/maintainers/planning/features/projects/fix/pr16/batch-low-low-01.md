# Fix Plan: PR #16 Batch LOW LOW - Batch 01

**PR:** 16  
**Batch:** low-low-01  
**Priority:** 🟢 LOW  
**Effort:** 🟢 LOW  
**Status:** 🔴 Not Started  
**Created:** 2025-12-05  
**Issues:** 3 issues

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR16-#8 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Swap if expression |
| PR16-#9 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Remove duplicate dict key |
| PR16-#12 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Raise from previous error (3 instances) |

---

## Overview

This batch contains 3 LOW priority issues with LOW effort. These are quick code quality improvements.

**Estimated Time:** 30 minutes  
**Files Affected:**
- `scripts/project_cli/commands/import_cmd.py`
- `backend/tests/unit/test_map_inventory.py`

---

## Issue Details

### Issue PR16-#8: Swap If Expression

**Location:** `scripts/project_cli/commands/import_cmd.py:85`  
**Sourcery Comment:** Comment #8  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Swap if/else branches of if expression to remove negation.

**Current Code:**
```python
border_style="green" if not errors else "yellow"
```

**Proposed Solution:**
```python
border_style="yellow" if errors else "green"
```

---

### Issue PR16-#9: Remove Duplicate Dict Key

**Location:** `backend/tests/unit/test_map_inventory.py:203-208`  
**Sourcery Comment:** Comment #9  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Remove duplicate keys when instantiating dicts.

**Current Code:**
```python
inventory_data = {
    'merged:todolist-repo': 'Personal',
    'github:todolist-repo': 'Personal',
    'local:/Users/cdwilson/Projects/todolist-repo': 'Personal',
    'github:todolist-repo': 'Personal'  # Duplicate key
}
```

**Proposed Solution:**
```python
inventory_data = {
    'merged:todolist-repo': 'Personal',
    'github:todolist-repo': 'Personal',
    'local:/Users/cdwilson/Projects/todolist-repo': 'Personal'
}
```

---

### Issue PR16-#12: Raise From Previous Error

**Location:** `scripts/project_cli/commands/import_cmd.py:40` (3 instances)  
**Sourcery Comment:** Comment #12  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Explicitly raise from a previous error to preserve exception context.

**Current Code:**
```python
except json.JSONDecodeError as e:
    console.print(f"[red]Error: Invalid JSON in file: {e}[/red]")
    raise click.Abort()

except Exception as e:
    console.print(f"[red]Error reading file: {e}[/red]")
    raise click.Abort()

except Exception as e:
    console.print(f"[red]Error importing projects: {e}[/red]")
    raise click.Abort()
```

**Proposed Solution:**
```python
except json.JSONDecodeError as e:
    console.print(f"[red]Error: Invalid JSON in file: {e}[/red]")
    raise click.Abort() from e

except Exception as e:
    console.print(f"[red]Error reading file: {e}[/red]")
    raise click.Abort() from e

except Exception as e:
    console.print(f"[red]Error importing projects: {e}[/red]")
    raise click.Abort() from e
```

---

## Implementation Steps

1. **Issue PR16-#8: Swap If Expression**
   - [ ] Change `border_style="green" if not errors else "yellow"` to `border_style="yellow" if errors else "green"`
   - [ ] Verify behavior unchanged
   - [ ] Test with errors and without errors

2. **Issue PR16-#9: Remove Duplicate Dict Key**
   - [ ] Remove duplicate `'github:todolist-repo'` key from test data
   - [ ] Verify test still passes
   - [ ] Verify test intent unchanged

3. **Issue PR16-#12: Raise From Previous Error**
   - [ ] Add `from e` to first `raise click.Abort()` (JSONDecodeError)
   - [ ] Add `from e` to second `raise click.Abort()` (file reading error)
   - [ ] Add `from e` to third `raise click.Abort()` (import error)
   - [ ] Verify error messages still clear
   - [ ] Test error handling still works

---

## Testing

- [ ] All existing tests pass
- [ ] Error handling still works correctly
- [ ] Test with duplicate key removed still passes
- [ ] No regressions introduced

---

## Files to Modify

- `scripts/project_cli/commands/import_cmd.py` - Swap if expression and add `from e` to raises
- `backend/tests/unit/test_map_inventory.py` - Remove duplicate dict key

---

## Definition of Done

- [ ] If expression swapped (PR16-#8)
- [ ] Duplicate dict key removed (PR16-#9)
- [ ] All raises include `from e` (PR16-#12)
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
These issues are batched together because they:
- Share LOW priority and LOW effort
- All are quick, simple improvements
- Can be fixed together efficiently
- Improve code quality with minimal risk

