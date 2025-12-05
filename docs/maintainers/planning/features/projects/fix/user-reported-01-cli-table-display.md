# Fix Plan: CLI List Table Display Issue

**Issue:** User-reported  
**Priority:** 🟡 MEDIUM  
**Impact:** 🟡 MEDIUM  
**Effort:** 🟢 LOW  
**Status:** 🔴 Not Started  
**Created:** 2025-12-05  
**Reported By:** User during manual testing (Scenario 24)

---

## Issue Description

**Problem:** The CLI `list` command table doesn't show full table columns - columns are truncated to fit terminal width, making it difficult to see all information.

**Location:** `scripts/project_cli/commands/list_cmd.py:37-52`

**User Context:** During manual testing of Scenario 24 (`./proj list --status active`), user noticed table columns were being truncated and asked if there was a command option to show full columns.

**Current Behavior:**
- Table only shows 4 columns: ID, Name, Path, Created
- Columns truncate to fit terminal width
- No option to expand table or show more columns
- Missing useful columns like Status, Organization, Classification

**Expected Behavior:**
- Table should use full terminal width (`expand=True`)
- Optionally show more columns (Status, Organization, Classification)
- Optionally add `--wide` flag to show all columns
- Columns should wrap or expand rather than truncate

---

## Current Code

```python
# Create table
table = Table(title=f"Projects ({len(projects)})")
table.add_column("ID", style="cyan", justify="right")
table.add_column("Name", style="green")
table.add_column("Path", style="blue")
table.add_column("Created", style="magenta")

# Add rows
for project in projects:
    table.add_row(
        str(project['id']),
        project['name'],
        project['path'] or "[dim]No path[/dim]",
        project['created_at'][:10]  # Just the date
    )

console.print(table)
```

**Issues:**
1. Table doesn't use `expand=True` - defaults to terminal width but truncates columns
2. Only shows 4 columns - missing Status, Organization, Classification that are available in API response
3. No `--wide` flag option to show more columns
4. Columns don't wrap - Rich tables truncate by default

---

## Proposed Solution

### Option 1: Expand Table to Full Width (Quick Fix)

**Change:** Add `expand=True` to Table constructor

```python
table = Table(title=f"Projects ({len(projects)})", expand=True)
```

**Pros:**
- Simple one-line change
- Uses full terminal width
- Reduces truncation

**Cons:**
- Still only shows 4 columns
- Doesn't address missing columns

### Option 2: Expand Table + Add More Columns (Recommended)

**Changes:**
1. Add `expand=True` to Table constructor
2. Add Status, Organization, Classification columns
3. Configure columns to wrap (`no_wrap=False`)

```python
# Create table with expand=True
table = Table(title=f"Projects ({len(projects)})", expand=True)
table.add_column("ID", style="cyan", justify="right", width=5)
table.add_column("Name", style="green", no_wrap=False)  # Allow wrapping
table.add_column("Status", style="yellow", width=10)
table.add_column("Org", style="blue", width=10)
table.add_column("Path", style="blue", no_wrap=False)  # Allow wrapping
table.add_column("Created", style="magenta", width=12)

# Add rows with new columns
for project in projects:
    table.add_row(
        str(project['id']),
        project['name'],
        project.get('status', 'N/A'),
        project.get('organization', 'N/A'),
        project['path'] or "[dim]No path[/dim]",
        project['created_at'][:10]
    )
```

**Pros:**
- Shows more useful information
- Uses full width
- Columns wrap instead of truncate

**Cons:**
- More columns might be overwhelming for some users
- Table might be wider than needed

### Option 3: Add `--wide` Flag (Best UX)

**Changes:**
1. Add `expand=True` to Table constructor (always)
2. Add `--wide` flag to show additional columns
3. Default to 4 columns, `--wide` shows 7 columns

```python
@click.command()
@click.option('--status', '-s', help='Filter by status')
@click.option('--org', '-o', 'organization', help='Filter by organization')
@click.option('--classification', '-c', help='Filter by classification')
@click.option('--search', help='Search in names/descriptions')
@click.option('--wide', is_flag=True, help='Show all columns (status, organization, classification)')
def list_projects(status, organization, classification, search, wide):
    # ... existing code ...
    
    # Create table with expand=True
    table = Table(title=f"Projects ({len(projects)})", expand=True)
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Name", style="green", no_wrap=False)
    
    if wide:
        table.add_column("Status", style="yellow")
        table.add_column("Org", style="blue")
        table.add_column("Classification", style="magenta")
    
    table.add_column("Path", style="blue", no_wrap=False)
    table.add_column("Created", style="magenta")
    
    # Add rows conditionally
    for project in projects:
        row_data = [
            str(project['id']),
            project['name'],
        ]
        if wide:
            row_data.extend([
                project.get('status', 'N/A'),
                project.get('organization', 'N/A'),
                project.get('classification', 'N/A'),
            ])
        row_data.extend([
            project['path'] or "[dim]No path[/dim]",
            project['created_at'][:10]
        ])
        table.add_row(*row_data)
```

**Pros:**
- Best user experience - choice of compact or wide view
- Backward compatible - default behavior unchanged
- Progressive disclosure - show more when needed

**Cons:**
- More complex implementation
- Conditional logic for rows

---

## Recommended Approach

**Use Option 3 (--wide flag)** because:
1. Best user experience - users can choose compact or wide view
2. Backward compatible - default behavior unchanged
3. Progressive disclosure - show more information when requested
4. Addresses user's question directly - provides a command option

**Fallback:** If `--wide` flag is too complex, use Option 2 (always show more columns) as it's still better than current state.

---

## Implementation Steps

1. **Add `--wide` flag to command:**
   - [ ] Add `@click.option('--wide', is_flag=True, help='...')` decorator
   - [ ] Add `wide` parameter to function signature

2. **Update table creation:**
   - [ ] Add `expand=True` to Table constructor
   - [ ] Add `no_wrap=False` to Name and Path columns
   - [ ] Conditionally add Status, Org, Classification columns based on `wide` flag

3. **Update row creation:**
   - [ ] Conditionally include Status, Org, Classification in row data
   - [ ] Handle missing values with 'N/A' or empty string

4. **Test:**
   - [ ] Test default view (4 columns)
   - [ ] Test `--wide` view (7 columns)
   - [ ] Test with filters (status, org, classification)
   - [ ] Test with long project names/paths (verify wrapping)
   - [ ] Test with empty/null values

5. **Update manual testing guide:**
   - [ ] Update Scenario 24 to mention `--wide` flag
   - [ ] Add scenario for `--wide` flag usage

---

## Testing

**Test Cases:**

1. **Default view:**
   ```bash
   ./proj list
   # Expected: 4 columns (ID, Name, Path, Created), full width, wrapping enabled
   ```

2. **Wide view:**
   ```bash
   ./proj list --wide
   # Expected: 7 columns (ID, Name, Status, Org, Classification, Path, Created)
   ```

3. **Wide view with filters:**
   ```bash
   ./proj list --wide --status active --org work
   # Expected: Shows filtered results with all 7 columns
   ```

4. **Long content wrapping:**
   ```bash
   ./proj list --wide
   # Expected: Long names/paths wrap instead of truncate
   ```

5. **Empty values:**
   ```bash
   ./proj list --wide
   # Expected: Missing org/status shows 'N/A' or empty gracefully
   ```

**Manual Testing:**
- Run Scenario 24 with `--wide` flag
- Verify table uses full terminal width
- Verify columns don't truncate
- Verify all columns are visible

---

## Files to Modify

- `scripts/project_cli/commands/list_cmd.py` - Add `--wide` flag and update table
- `docs/maintainers/planning/features/projects/manual-testing.md` - Update Scenario 24

---

## Definition of Done

- [ ] `--wide` flag added to `list` command
- [ ] Table uses `expand=True` to use full terminal width
- [ ] Default view shows 4 columns (backward compatible)
- [ ] `--wide` view shows 7 columns (ID, Name, Status, Org, Classification, Path, Created)
- [ ] Columns wrap instead of truncate (`no_wrap=False`)
- [ ] All tests pass
- [ ] Manual testing completed (Scenario 24 updated)
- [ ] Documentation updated

---

## Related Issues

- None (user-reported, not from Sourcery review)

---

**Last Updated:** 2025-12-05  
**Next:** Implement Option 3 (--wide flag) for best user experience

