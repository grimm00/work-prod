# Fix Plan: PR #16 Batch MEDIUM MEDIUM - Batch 01

**PR:** 16  
**Batch:** medium-medium-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟡 MEDIUM  
**Status:** 🔴 Not Started  
**Created:** 2025-12-05  
**Issues:** 1 issue

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR16-#10 | 🟡 MEDIUM | 🟢 LOW | 🟡 MEDIUM | Extract duplicate code into method |

---

## Overview

This batch contains 1 MEDIUM priority issue with MEDIUM effort. This issue improves test code quality by extracting duplicate code.

**Estimated Time:** 1-2 hours  
**Files Affected:**
- `backend/tests/unit/test_map_inventory.py`

---

## Issue Details

### Issue PR16-#10: Extract Duplicate Code into Method

**Location:** `backend/tests/unit/test_map_inventory.py:231`  
**Sourcery Comment:** Comment #10  
**Priority:** 🟡 MEDIUM | **Impact:** 🟢 LOW | **Effort:** 🟡 MEDIUM

**Description:**
The test function `test_map_multiple_projects` has duplicate code patterns for checking project attributes. Extract this into a helper method to reduce duplication and improve maintainability.

**Current Code:**
```python
def test_map_multiple_projects(self):
    """Test mapping multiple projects."""
    inventory_data = {
        'merged:project1': 'Personal',
        'github:project1': 'Personal',
        'local:/Users/cdwilson/Projects/project1': 'Personal',
        'github:project2': 'Work (DRW)',
        'local:/Users/cdwilson/Projects/project3': 'Learning'
    }

    projects = map_classification_to_project(inventory_data)

    assert len(projects) == 3

    # Check project1 (merged)
    project1 = next(p for p in projects if p['name'] == 'project1')
    assert project1['classification'] == 'primary'
    assert 'remote_url' in project1
    assert 'path' in project1

    # Check project2 (github only)
    project2 = next(p for p in projects if p['name'] == 'project2')
    assert project2['classification'] == 'primary'
    assert project2['organization'] == 'DRW'
    assert 'remote_url' in project2

    # Check project3 (local only)
    project3 = next(p for p in projects if p['name'] == 'project3')
    assert project3['classification'] == 'secondary'
    assert 'path' in project3
    assert 'remote_url' not in project3
```

**Proposed Solution:**
```python
def _assert_project_attributes(self, projects, name, **expected_attrs):
    """Helper method to assert project has expected attributes."""
    project = next(p for p in projects if p['name'] == name)
    for attr, value in expected_attrs.items():
        assert project[attr] == value, f"Project {name} {attr} mismatch"
    return project

def test_map_multiple_projects(self):
    """Test mapping multiple projects."""
    inventory_data = {
        'merged:project1': 'Personal',
        'github:project1': 'Personal',
        'local:/Users/cdwilson/Projects/project1': 'Personal',
        'github:project2': 'Work (DRW)',
        'local:/Users/cdwilson/Projects/project3': 'Learning'
    }

    projects = map_classification_to_project(inventory_data)

    assert len(projects) == 3

    # Check project1 (merged)
    project1 = self._assert_project_attributes(
        projects, 'project1',
        classification='primary'
    )
    assert 'remote_url' in project1
    assert 'path' in project1

    # Check project2 (github only)
    project2 = self._assert_project_attributes(
        projects, 'project2',
        classification='primary',
        organization='DRW'
    )
    assert 'remote_url' in project2

    # Check project3 (local only)
    project3 = self._assert_project_attributes(
        projects, 'project3',
        classification='secondary'
    )
    assert 'path' in project3
    assert 'remote_url' not in project3
```

---

## Implementation Steps

1. **Extract Helper Method**
   - [ ] Create `_assert_project_attributes` helper method
   - [ ] Method should find project by name and assert attributes
   - [ ] Handle both equality checks and presence checks (use `in` operator)
   - [ ] Add clear error messages

2. **Refactor Test Function**
   - [ ] Replace duplicate project finding code with helper method calls
   - [ ] Use helper for attribute assertions
   - [ ] Keep presence checks (`in` operator) as separate assertions
   - [ ] Verify test still passes after refactoring

3. **Verify Test Quality**
   - [ ] Test still covers all original cases
   - [ ] Error messages are clear if test fails
   - [ ] No functionality lost in refactoring

---

## Testing

- [ ] All existing tests pass
- [ ] Refactored test passes with same assertions
- [ ] Helper method tested indirectly through test
- [ ] No regressions introduced

---

## Files to Modify

- `backend/tests/unit/test_map_inventory.py` - Extract helper method and refactor test

---

## Definition of Done

- [ ] Helper method extracted
- [ ] Test refactored to use helper
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
This is a single issue batch because:
- MEDIUM priority and MEDIUM effort
- Requires careful refactoring to maintain test quality
- Benefits from focused attention

