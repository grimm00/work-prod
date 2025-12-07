# User Feedback: Table Column Visibility

**PR:** #18  
**Date:** 2025-12-05  
**Context:** Manual testing of `--wide` flag  
**Type:** UX Improvement Suggestion

---

## Feedback

**Issue:** When filtering by a column (e.g., `--status active`), that column should be visible in the table output automatically, even without the `--wide` flag.

**Current Behavior:**
- `./proj list --status active` shows 4 columns: ID, Name, Path, Created
- Status column is not visible (filtered but not shown)
- User must use `--wide` flag to see Status column

**Expected Behavior:**
- `./proj list --status active` should automatically show Status column
- Filtered columns should be visible by default
- Makes it easier to verify filters are working correctly

**User Context:**
- Testing Scenario 24 (CLI - Filter by Status)
- Noticed that when filtering by status, the Status column wasn't visible
- Had to use `--wide` flag to see what was being filtered

---

## Analysis

**Priority:** 🟡 MEDIUM  
**Impact:** 🟡 MEDIUM (UX improvement)  
**Effort:** 🟡 MEDIUM

**Rationale:**
- Improves user experience by showing filtered columns automatically
- Makes filter verification easier
- Reduces need to use `--wide` flag for common use cases
- Logical: if you're filtering by it, you probably want to see it

**Implementation Considerations:**

1. **Auto-show filtered columns:**
   - If `--status` is used, show Status column automatically
   - If `--org` is used, show Org column automatically
   - If `--classification` is used, show Classification column automatically
   - `--wide` flag still shows all columns

2. **Column visibility logic:**
   ```python
   # Always show: ID, Name, Path, Created
   # Show if filtered: Status (if --status), Org (if --org), Classification (if --classification)
   # Show if --wide: All columns
   ```

3. **Backward compatibility:**
   - Default view (no filters, no --wide) still shows 4 columns
   - Filtered views automatically show relevant columns
   - `--wide` flag still works as before

---

## Proposed Solution

**Option 1: Auto-show filtered columns (Recommended)**

When a filter is used, automatically show that column:

```python
# Determine which columns to show
show_status = wide or status is not None
show_org = wide or organization is not None
show_classification = wide or classification is not None

# Add columns conditionally
if show_status:
    table.add_column("Status", style="yellow")
if show_org:
    table.add_column("Org", style="blue")
if show_classification:
    table.add_column("Classification", style="magenta")
```

**Pros:**
- Better UX - filtered columns visible automatically
- Makes filter verification easier
- Logical behavior

**Cons:**
- Slightly more complex logic
- Table width varies based on filters

**Option 2: New flag `--show-filtered`**

Add a flag to show filtered columns:

```python
@click.option('--show-filtered', is_flag=True, help='Show columns for active filters')
```

**Pros:**
- Explicit control
- Backward compatible

**Cons:**
- Requires remembering another flag
- Less intuitive than auto-showing

---

## Recommendation

**Use Option 1 (Auto-show filtered columns)** because:
1. Better UX - filtered columns visible automatically
2. Makes filter verification easier
3. Logical behavior - if filtering by it, show it
4. `--wide` flag still works for showing all columns

**Implementation:**
- Update `list_cmd.py` to show columns based on active filters
- Update manual testing guide scenarios
- Test with various filter combinations

---

## Related

- **PR:** #18
- **Scenario:** Scenario 24 (CLI - Filter by Status)
- **Fix Plan:** Could be added to `user-reported-01-cli-table-display.md` or new fix plan

---

**Status:** ✅ Implemented (PR #18)  
**Implemented:** 2025-12-05  
**Next:** Test implementation and verify behavior

