# Fix Plan: Cross-PR Batch Code Refactoring

**Batch:** code-refactoring-medium-medium-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟡 MEDIUM  
**Status:** 🔴 Not Started  
**Created:** 2025-12-05  
**Source:** fix-review-report-2025-12-05.md  
**Issues:** 2 issues from 2 PRs

---

## Issues in This Batch

| Issue | PR | Priority | Impact | Effort | Description |
|-------|----|----------|--------|--------|-------------|
| PR16-#10 | #16 | 🟡 MEDIUM | 🟢 LOW | 🟡 MEDIUM | Extract duplicate code into method |
| PR18-Overall-#2 | #18 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Factor column configuration into helper |

---

## Overview

This batch contains 2 MEDIUM/MEDIUM refactoring issues from 2 PRs. These issues improve code organization by extracting duplicate code and factoring complex logic into helper functions.

**Estimated Time:** 2-3 hours  
**Files Affected:**
- `backend/app/api/projects.py` (PR16-#10)
- `scripts/project_cli/commands/list_cmd.py` (PR18-Overall-#2)

**Source PRs:**
- PR #16: Phase 5: Bulk Import (1 issue)
- PR #18: CLI Enhancement & Daily Use Tools (1 issue)

---

## Issue Details

### Issue PR16-#10: Extract Duplicate Code into Method

**Source PR:** #16 - Phase 5: Bulk Import  
**Location:** `backend/app/api/projects.py:231` (around lines 100-150)  
**Sourcery Comment:** Comment #10  
**Priority:** 🟡 MEDIUM | **Impact:** 🟢 LOW | **Effort:** 🟡 MEDIUM

**Description:**
Extract duplicate code into a method to reduce duplication and improve maintainability. The validation logic for `classification` and `status` appears in multiple places (`create_project`, `update_project`, `import_projects`).

**Current Code:**
```python
# In create_project():
if 'classification' in data and data['classification'] is not None:
    if data['classification'] not in VALID_CLASSIFICATIONS:
        return jsonify({
            'error': f"Invalid classification. Must be one of: {', '.join(VALID_CLASSIFICATIONS)}"
        }), 400

# Validate status if provided
if 'status' in data:
    if data['status'] is None:
        return jsonify({'error': 'Status cannot be null'}), 400
    if data['status'] not in VALID_STATUSES:
        return jsonify({
            'error': f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"
        }), 400

# Similar code in update_project() and import_projects()
```

**Proposed Solution:**
```python
def validate_project_data(data):
    """
    Validate project data for classification and status.
    
    Returns:
        tuple: (error_response, error_code) or (None, None) if valid
    """
    # Validate classification if provided
    if 'classification' in data and data['classification'] is not None:
        if data['classification'] not in VALID_CLASSIFICATIONS:
            return jsonify({
                'error': f"Invalid classification. Must be one of: {', '.join(VALID_CLASSIFICATIONS)}"
            }), 400
    
    # Validate status if provided
    if 'status' in data:
        if data['status'] is None:
            return jsonify({'error': 'Status cannot be null'}), 400
        if data['status'] not in VALID_STATUSES:
            return jsonify({
                'error': f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"
            }), 400
    
    return None, None

# Usage in create_project(), update_project(), import_projects():
error_response, error_code = validate_project_data(data)
if error_response:
    return error_response, error_code
```

**Benefits:**
- Reduces code duplication
- Single source of truth for validation logic
- Easier to maintain and update
- Consistent error messages

---

### Issue PR18-Overall-#2: Factor Column Configuration into Helper

**Source PR:** #18 - CLI Enhancement & Daily Use Tools  
**Location:** `scripts/project_cli/commands/list_cmd.py:45-97`  
**Sourcery Comment:** Overall Comment #2  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟡 MEDIUM

**Description:**
The `wide` flag currently drives both additional columns and wrapping behavior; if you anticipate more view modes in the future, you might factor column configuration into a small helper (e.g., `build_table(wide: bool)`) to keep the command function focused on data retrieval and orchestration.

**Current Code:**
```python
# Create table with expand=True to use full terminal width
table = Table(title=f"Projects ({len(projects)})", expand=True)
table.add_column("ID", style="cyan", justify="right")
table.add_column("Name", style="green", no_wrap=False)  # Allow wrapping

# Determine which columns to show:
# - Show Status if --wide flag OR --status filter is used
# - Show Org if --wide flag OR --org filter is used
# - Show Classification if --wide flag OR --classification filter is used
# - Show Description if --wide flag OR --search filter is used (to show where match occurred)
show_status = wide or status is not None
show_org = wide or organization is not None
show_classification = wide or classification is not None
show_description = wide or search is not None

# Add columns based on filters and --wide flag
if show_status:
    table.add_column("Status", style="yellow")
if show_org:
    table.add_column("Org", style="blue")
if show_classification:
    table.add_column("Classification", style="magenta")

table.add_column("Path", style="blue", no_wrap=False)  # Allow wrapping

# Add Description column if searching or using --wide
if show_description:
    table.add_column("Description", style="dim", no_wrap=False)  # Allow wrapping

table.add_column("Created", style="magenta")

# Add rows conditionally based on visible columns
for project in projects:
    row_data = [
        str(project['id']),
        project['name'],
    ]
    if show_status:
        row_data.append(project.get('status', 'N/A'))
    if show_org:
        row_data.append(project.get('organization', 'N/A'))
    if show_classification:
        row_data.append(project.get('classification', 'N/A'))
    
    row_data.append(project['path'] or "[dim]No path[/dim]")
    
    # Add Description column if searching or using --wide
    if show_description:
        description = project.get('description', '')
        row_data.append(description or "[dim]No description[/dim]")
    
    row_data.append(project['created_at'][:10])  # Just the date
    table.add_row(*row_data)
```

**Proposed Solution:**
```python
def build_projects_table(projects, wide=False, status=None, organization=None, 
                        classification=None, search=None):
    """
    Build a Rich Table for displaying projects.
    
    Args:
        projects: List of project dictionaries
        wide: Whether to show all columns
        status: Status filter (if used, shows Status column)
        organization: Organization filter (if used, shows Org column)
        classification: Classification filter (if used, shows Classification column)
        search: Search filter (if used, shows Description column)
    
    Returns:
        Table: Configured Rich Table ready for display
    """
    table = Table(title=f"Projects ({len(projects)})", expand=True)
    
    # Determine which columns to show
    show_status = wide or status is not None
    show_org = wide or organization is not None
    show_classification = wide or classification is not None
    show_description = wide or search is not None
    
    # Add columns
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Name", style="green", no_wrap=False)
    
    if show_status:
        table.add_column("Status", style="yellow")
    if show_org:
        table.add_column("Org", style="blue")
    if show_classification:
        table.add_column("Classification", style="magenta")
    
    table.add_column("Path", style="blue", no_wrap=False)
    
    if show_description:
        table.add_column("Description", style="dim", no_wrap=False)
    
    table.add_column("Created", style="magenta")
    
    # Add rows
    for project in projects:
        row_data = [
            str(project['id']),
            project['name'],
        ]
        if show_status:
            row_data.append(project.get('status', 'N/A'))
        if show_org:
            row_data.append(project.get('organization', 'N/A'))
        if show_classification:
            row_data.append(project.get('classification', 'N/A'))
        
        row_data.append(project['path'] or "[dim]No path[/dim]")
        
        if show_description:
            description = project.get('description', '')
            row_data.append(description or "[dim]No description[/dim]")
        
        row_data.append(project['created_at'][:10])
        table.add_row(*row_data)
    
    return table

# Usage in list_projects():
table = build_projects_table(
    projects,
    wide=wide,
    status=status,
    organization=organization,
    classification=classification,
    search=search
)
console.print(table)
```

**Benefits:**
- Separates table configuration from command logic
- Easier to add new view modes in the future
- More testable (can test table building independently)
- Cleaner command function focused on orchestration

---

## Implementation Steps

### 1. Issue PR16-#10: Extract Duplicate Code into Method
   - [ ] Create `validate_project_data()` helper function in `backend/app/api/projects.py`
   - [ ] Move classification and status validation logic into helper
   - [ ] Update `create_project()` to use helper
   - [ ] Update `update_project()` to use helper
   - [ ] Update `import_projects()` to use helper
   - [ ] Run tests to verify functionality unchanged
   - [ ] Verify error messages are consistent

### 2. Issue PR18-Overall-#2: Factor Column Configuration into Helper
   - [ ] Create `build_projects_table()` helper function in `scripts/project_cli/commands/list_cmd.py`
   - [ ] Move table creation and column configuration logic into helper
   - [ ] Move row building logic into helper
   - [ ] Update `list_projects()` to use helper
   - [ ] Test CLI command with various filter combinations
   - [ ] Verify table display is unchanged
   - [ ] Test with `--wide` flag

---

## Testing

- [ ] All existing tests pass
- [ ] API validation still works correctly (create, update, import)
- [ ] CLI table display unchanged
- [ ] Error messages consistent
- [ ] No regressions introduced

**Run tests:**
```bash
# Backend tests
cd backend
source ../venv/bin/activate
pytest tests/integration/api/test_projects.py -v
pytest tests/integration/api/test_projects_import.py -v

# CLI tests (manual)
cd scripts/project_cli
./proj list
./proj list --wide
./proj list --status active
./proj list --search test
```

---

## Files to Modify

- `backend/app/api/projects.py` - Extract validation helper (PR16-#10)
- `scripts/project_cli/commands/list_cmd.py` - Extract table building helper (PR18-Overall-#2)

---

## Definition of Done

- [ ] All 2 issues in batch fixed
- [ ] Validation helper extracted and used in all endpoints
- [ ] Table building helper extracted and used in CLI command
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
This batch was created from fix-review report recommendations. These issues are batched together because they:

- Share similar priority and effort levels (both MEDIUM/MEDIUM)
- Both involve extracting code into helper functions
- Both improve code organization and maintainability
- Can be implemented together efficiently
- Were identified as "Code Refactoring" in review report
- Reduce duplication and improve testability

**Source PRs:**
- PR #16: 1 issue (extract duplicate validation)
- PR #18: 1 issue (factor column configuration)

---

**Last Updated:** 2025-12-05  
**Next:** Use `/fix-implement` to implement this batch

