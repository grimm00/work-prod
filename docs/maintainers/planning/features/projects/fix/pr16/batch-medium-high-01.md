# Fix Plan: PR #16 Batch MEDIUM HIGH - Batch 01

**PR:** 16  
**Batch:** medium-high-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟠 HIGH  
**Status:** 🔴 Not Started  
**Created:** 2025-12-05  
**Issues:** 1 issue

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR16-#11 | 🟡 MEDIUM | 🟡 MEDIUM | 🟠 HIGH | Low code quality function - complex refactoring needed |

---

## Overview

This batch contains 1 MEDIUM priority issue with HIGH effort. This issue requires refactoring a complex mapping function with low quality score (17%).

**Estimated Time:** 4-6 hours  
**Files Affected:**
- `scripts/map_inventory_to_projects.py`

---

## Issue Details

### Issue PR16-#11: Low Code Quality Function

**Location:** `scripts/map_inventory_to_projects.py:84`  
**Sourcery Comment:** Comment #11  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟠 HIGH

**Description:**
The quality score for `map_classification_to_project` function is below the quality threshold of 25% (currently 17%). The function is complex with multiple passes over data, complex grouping logic, and canonical name resolution.

**Current Code:**
The function is ~420 lines long with:
- Multiple passes over inventory data
- Complex grouping logic using defaultdict
- Canonical name resolution
- Multiple data structures (lists, sets, dicts)
- Nested loops and conditionals

**Proposed Solution:**
Refactor into smaller, focused functions:

```python
def parse_inventory_entries(inventory_data):
    """Parse inventory data into structured entries."""
    entries = []
    for key, classification in inventory_data.items():
        if classification == 'Skip':
            continue
        parsed = parse_project_key(key)
        entries.append({
            'key': key,
            'type': parsed['type'],
            'path': parsed.get('path'),
            'name': parsed['name'],
            'classification': classification
        })
    return entries

def group_entries_by_canonical_name(entries):
    """Group entries by canonical project name."""
    project_groups = defaultdict(list)
    canonical_names = {}
    
    # First pass: identify canonical names from merged/github entries
    for entry in entries:
        if entry['type'] in ('merged', 'github'):
            canonical_names[entry['name']] = entry['name']
    
    # Second pass: group entries
    for entry in entries:
        if entry['type'] in ('merged', 'github'):
            canonical_name = entry['name']
            project_groups[canonical_name].append(entry)
        else:
            # Local entry - try to match to existing group
            matched = False
            for canonical_name, group_entries in project_groups.items():
                for group_entry in group_entries:
                    if (group_entry['classification'] == entry['classification'] and
                        (group_entry['name'] in entry['name'] or 
                         entry['name'] in group_entry['name'])):
                        project_groups[canonical_name].append(entry)
                        matched = True
                        break
                if matched:
                    break
            
            if not matched:
                project_groups[entry['name']].append(entry)
    
    return project_groups

def build_project_data(project_name, entries, seen_projects):
    """Build project data dictionary from grouped entries."""
    if project_name in seen_projects:
        return None
    
    # Prefer merged entry, then local, then github
    merged_entry = next((e for e in entries if e['type'] == 'merged'), None)
    local_entry = next((e for e in entries if e['type'] == 'local'), None)
    github_entry = next((e for e in entries if e['type'] == 'github'), None)
    
    entry = merged_entry or local_entry or github_entry
    if not entry:
        return None
    
    # Determine canonical name
    canonical_name = project_name
    if merged_entry:
        canonical_name = merged_entry['key'].replace('merged:', '')
    elif github_entry:
        canonical_name = github_entry['key'].replace('github:', '')
    
    if canonical_name in seen_projects:
        return None
    
    classification_value = entry['classification']
    project_classification = CLASSIFICATION_MAP.get(classification_value)
    if project_classification is None:
        return None
    
    project_status = STATUS_MAP.get(classification_value, 'active')
    organization = extract_organization(classification_value)
    
    project_data = {
        'name': canonical_name,
        'status': project_status,
        'classification': project_classification,
    }
    
    if local_entry and local_entry.get('path'):
        project_data['path'] = local_entry['path']
    
    if merged_entry or github_entry:
        project_data['remote_url'] = build_github_url(canonical_name)
    
    if organization:
        project_data['organization'] = organization
    
    return project_data, canonical_name

def map_classification_to_project(inventory_data):
    """
    Map inventory classifications to Project model format.
    
    Args:
        inventory_data: Dictionary from classifications-merged.json
        
    Returns:
        List of project dictionaries in format expected by import endpoint
    """
    entries = parse_inventory_entries(inventory_data)
    project_groups = group_entries_by_canonical_name(entries)
    
    projects = []
    seen_projects = set()
    
    for project_name, group_entries in project_groups.items():
        result = build_project_data(project_name, group_entries, seen_projects)
        if result:
            project_data, canonical_name = result
            projects.append(project_data)
            seen_projects.add(canonical_name)
            seen_projects.add(project_name)
    
    return projects
```

---

## Implementation Steps

1. **Analyze Function Structure**
   - [ ] Identify logical sections in current function
   - [ ] Document data flow and dependencies
   - [ ] Identify helper functions to extract

2. **Extract Helper Functions**
   - [ ] Extract `parse_inventory_entries` function
   - [ ] Extract `group_entries_by_canonical_name` function
   - [ ] Extract `build_project_data` function
   - [ ] Write unit tests for each helper function

3. **Refactor Main Function**
   - [ ] Refactor `map_classification_to_project` to use helpers
   - [ ] Simplify main function logic
   - [ ] Ensure same output format

4. **Test Refactoring**
   - [ ] Run all existing tests
   - [ ] Verify output matches original function
   - [ ] Test edge cases
   - [ ] Check code quality score improvement

---

## Testing

- [ ] All existing tests pass
- [ ] Unit tests added for helper functions
- [ ] Integration tests verify refactored function works correctly
- [ ] Edge cases tested (empty data, missing fields, etc.)
- [ ] No regressions introduced
- [ ] Code quality score improved (target: >25%)

---

## Files to Modify

- `scripts/map_inventory_to_projects.py` - Refactor mapping function
- `backend/tests/unit/test_map_inventory.py` - Add tests for helper functions

---

## Definition of Done

- [ ] Function refactored into smaller pieces
- [ ] Helper functions tested
- [ ] All tests passing
- [ ] Code quality score improved
- [ ] Code reviewed
- [ ] Documentation updated (if needed)
- [ ] Ready for PR

---

**Batch Rationale:**
This is a single issue batch because:
- HIGH effort requires focused attention
- Complex refactoring needs careful planning
- Function works correctly, so this is quality improvement only
- Can be deferred to dedicated refactoring session

