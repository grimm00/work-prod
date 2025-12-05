# Fix Plan: Cross-PR Batch Test Quality Improvements

**Batch:** test-quality-medium-low-01  
**Priority:** 🟡 MEDIUM / 🟢 LOW  
**Effort:** 🟢 LOW / 🟡 MEDIUM  
**Status:** 🔴 Not Started  
**Created:** 2025-12-05  
**Source:** fix-review-report-2025-12-05.md  
**Issues:** 9 issues from 3 PRs

---

## Issues in This Batch

| Issue | PR | Priority | Impact | Effort | Description |
|-------|----|----------|--------|--------|-------------|
| PR02-#4 | #2 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Test null path serialization |
| PR02-#6 | #2 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Use IntegrityError in name test |
| PR02-#7 | #2 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Use IntegrityError in path test |
| PR02-#8 | #2 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Test updated_at changes |
| PR13-#1 | #13 | 🟡 MEDIUM | 🟢 LOW | 🟢 LOW | Strengthen test assertions |
| PR16-#4 | #16 | 🟢 LOW | 🟢 LOW | 🟡 MEDIUM | Avoid loops in tests (instance 1) |
| PR16-#5 | #16 | 🟢 LOW | 🟢 LOW | 🟡 MEDIUM | Avoid loops in tests (instance 2) |
| PR16-#6 | #16 | 🟢 LOW | 🟢 LOW | 🟡 MEDIUM | Avoid loops in tests (instance 3) |
| PR16-#7 | #16 | 🟢 LOW | 🟢 LOW | 🟡 MEDIUM | Avoid loops in tests (instance 4) |

---

## Overview

This batch contains 9 test quality improvement issues from 3 PRs. These issues improve test coverage, strengthen assertions, use proper exception types, and reduce test complexity by avoiding loops.

**Estimated Time:** 2-3 hours  
**Files Affected:**
- `backend/tests/integration/api/test_projects.py` (PR02-#4, #8, PR13-#1)
- `backend/tests/unit/models/test_project.py` (PR02-#6, #7, #8)
- `backend/tests/unit/test_map_inventory.py` (PR16-#4, #5, #6, #7)

**Source PRs:**
- PR #2: Phase 1: List & Get Projects (4 issues)
- PR #13: Fix Batch (1 issue)
- PR #16: Phase 5: Bulk Import (4 issues)

---

## Issue Details

### Issue PR02-#4: Test Null Path Serialization

**Source PR:** #2 - Phase 1: List & Get Projects  
**Location:** `backend/tests/integration/api/test_projects.py:46-51`  
**Sourcery Comment:** Comment #4  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
`test_list_projects_with_data` creates `project3` without a `path`, but the test only checks the first item and the list length. Please add an assertion that the entry for `"Project 3"` in the response has `path` serialized as `None`/`null`, and is not omitted or replaced with an empty string.

**Current Code:**
```python
def test_list_projects_with_data(client, app):
    """Test GET /api/projects returns list of projects."""
    with app.app_context():
        project1 = Project(name="Project 1", path="/path/1")
        project2 = Project(name="Project 2", path="/path/2")
        project3 = Project(name="Project 3")  # No path
        
        db.session.add_all([project1, project2, project3])
        db.session.commit()
    
    response = client.get('/api/projects')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert isinstance(data, list)
    assert len(data) == 3
    
    # Check first project structure
    assert 'id' in data[0]
    assert 'name' in data[0]
    assert 'path' in data[0]
    assert 'created_at' in data[0]
    assert 'updated_at' in data[0]
```

**Proposed Solution:**
```python
# Check project with no path is serialized with path=None (null in JSON)
project_without_path = next((p for p in data if p.get("name") == "Project 3"), None)
assert project_without_path is not None
assert "path" in project_without_path
assert project_without_path["path"] is None
```

---

### Issue PR02-#6: Use IntegrityError in Name Test

**Source PR:** #2 - Phase 1: List & Get Projects  
**Location:** `backend/tests/unit/models/test_project.py:22-29`  
**Sourcery Comment:** Comment #6  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
The test is expecting a commit-time integrity/validation failure, so catching `Exception` is too broad and may mask other errors. Please import and assert the concrete exception type raised by your stack (e.g. `sqlalchemy.exc.IntegrityError`) with `pytest.raises(IntegrityError)`. After the failure, explicitly roll back the session to leave it in a clean state for later tests.

**Current Code:**
```python
def test_project_name_required(app):
    """Test that name field is required."""
    with pytest.raises(Exception):  # Should raise validation error
        project = Project(path="/test/path")
        # Attempting to commit without name should fail
        from app import db
        db.session.add(project)
        db.session.commit()
```

**Proposed Solution:**
```python
def test_project_name_required(app):
    """Test that name field is required."""
    from app import db
    from sqlalchemy.exc import IntegrityError
    
    with pytest.raises(IntegrityError):
        project = Project(path="/test/path")
        db.session.add(project)
        db.session.commit()
    
    # Roll back to leave session clean
    db.session.rollback()
```

---

### Issue PR02-#7: Use IntegrityError in Path Test

**Source PR:** #2 - Phase 1: List & Get Projects  
**Location:** `backend/tests/unit/models/test_project.py:82-91`  
**Sourcery Comment:** Comment #7  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
This should mirror `test_project_name_required` by asserting the specific database exception (e.g. `IntegrityError`) instead of `Exception`, otherwise any error on `commit()` would make the test pass. Also consider adding a `db.session.rollback()` after the failed commit so the session remains usable for subsequent tests.

**Current Code:**
```python
def test_project_path_unique(app):
    """Test that path must be unique."""
    from app import db
    
    project1 = Project(name="Project 1", path="/same/path")
    db.session.add(project1)
    db.session.commit()
    
    project2 = Project(name="Project 2", path="/same/path")
    db.session.add(project2)
    
    with pytest.raises(Exception):  # Should raise IntegrityError
        db.session.commit()
```

**Proposed Solution:**
```python
def test_project_path_unique(app):
    """Test that path must be unique."""
    from app import db
    from sqlalchemy.exc import IntegrityError
    
    project1 = Project(name="Project 1", path="/same/path")
    db.session.add(project1)
    db.session.commit()
    
    project2 = Project(name="Project 2", path="/same/path")
    db.session.add(project2)
    
    with pytest.raises(IntegrityError):
        db.session.commit()
    
    # Roll back to leave session clean
    db.session.rollback()
```

---

### Issue PR02-#8: Test Updated At Changes

**Source PR:** #2 - Phase 1: List & Get Projects  
**Location:** `backend/tests/unit/models/test_project.py:58-67`  
**Sourcery Comment:** Comment #8  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
This currently only checks that the timestamps are set on insert. To fully cover `onupdate=func.now()`, add a test that updates a persisted `Project`, commits, and asserts that `updated_at` changes while `created_at` remains unchanged.

**Current Code:**
```python
def test_project_timestamps(app):
    """Test that created_at and updated_at are set automatically."""
    from app import db
    
    project = Project(name="Test Project")
    db.session.add(project)
    db.session.commit()
    
    assert project.created_at is not None
    assert project.updated_at is not None
    assert isinstance(project.created_at, datetime)
    assert isinstance(project.updated_at, datetime)
```

**Proposed Solution:**
```python
def test_project_timestamps(app):
    """Test that created_at and updated_at are set automatically."""
    from app import db
    from datetime import datetime
    import time
    
    project = Project(name="Test Project")
    db.session.add(project)
    db.session.commit()
    
    # Verify initial timestamps
    assert project.created_at is not None
    assert project.updated_at is not None
    assert isinstance(project.created_at, datetime)
    assert isinstance(project.updated_at, datetime)
    
    # Store original timestamps
    original_created_at = project.created_at
    original_updated_at = project.updated_at
    
    # Wait a moment to ensure timestamp difference
    time.sleep(0.1)
    
    # Update project
    project.name = "Updated Project"
    db.session.commit()
    
    # Verify updated_at changed but created_at didn't
    assert project.created_at == original_created_at
    assert project.updated_at > original_updated_at
```

---

### Issue PR13-#1: Strengthen Test Assertions

**Source PR:** #13 - Fix Batch (pr12-batch-medium-medium-01)  
**Location:** `backend/tests/integration/api/test_projects.py:775-779`  
**Sourcery Comment:** Comment #1  
**Priority:** 🟡 MEDIUM | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Since the test now verifies that an invalid `status` is ignored and returns a 200 with two projects, also assert that the returned items are specifically `project1` and `project2` (e.g., by ID or name). This guards against cases where the endpoint returns a different set of two projects while still passing the current length check.

**Current Code:**
```python
# Invalid status values are ignored, so all projects should be returned
assert response.status_code == 200
data = json.loads(response.data)
assert isinstance(data, list)
assert len(data) == 2
```

**Proposed Solution:**
```python
# Invalid status values are ignored, so all projects should be returned
assert response.status_code == 200
data = response.get_json()
assert isinstance(data, list)
assert len(data) == 2

# Ensure that the returned projects are exactly the ones created in this test
returned_ids = {project["id"] for project in data}
assert returned_ids == {project1_id, project2_id}
```

---

### Issue PR16-#4: Avoid Loops in Tests (Instance 1)

**Source PR:** #16 - Phase 5: Bulk Import  
**Location:** `backend/tests/unit/test_map_inventory.py:273-274`  
**Sourcery Comment:** Comment #4  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟡 MEDIUM

**Description:**
Avoid complex code, like loops, in test functions. Use `@pytest.mark.parametrize` or extract helper functions to reduce duplication and improve test clarity.

**Current Code:**
```python
def test_classification_map_completeness(self):
    """Test that all expected classifications are mapped."""
    expected_classifications = [
        'Personal', 'Work (DRW)', 'Apprenti', 'Learning', 'Inactive/Archived', 'Skip'
    ]
    
    for cls in expected_classifications:
        assert cls in CLASSIFICATION_MAP
```

**Proposed Solution:**
```python
@pytest.mark.parametrize("classification", [
    'Personal', 'Work (DRW)', 'Apprenti', 'Learning', 'Inactive/Archived', 'Skip'
])
def test_classification_map_completeness(self, classification):
    """Test that all expected classifications are mapped."""
    assert classification in CLASSIFICATION_MAP
```

---

### Issue PR16-#5: Avoid Loops in Tests (Instance 2)

**Source PR:** #16 - Phase 5: Bulk Import  
**Location:** `backend/tests/unit/test_map_inventory.py:282-283`  
**Sourcery Comment:** Comment #5  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟡 MEDIUM

**Description:**
Avoid complex code, like loops, in test functions. Use `@pytest.mark.parametrize` or extract helper functions.

**Current Code:**
```python
def test_status_map_completeness(self):
    """Test that all expected classifications have status mappings."""
    expected_classifications = [
        'Personal', 'Work (DRW)', 'Apprenti', 'Learning', 'Inactive/Archived', 'Skip'
    ]
    
    for cls in expected_classifications:
        assert cls in STATUS_MAP
```

**Proposed Solution:**
```python
@pytest.mark.parametrize("classification", [
    'Personal', 'Work (DRW)', 'Apprenti', 'Learning', 'Inactive/Archived', 'Skip'
])
def test_status_map_completeness(self, classification):
    """Test that all expected classifications have status mappings."""
    assert classification in STATUS_MAP
```

---

### Issue PR16-#6: Avoid Loops in Tests (Instance 3)

**Source PR:** #16 - Phase 5: Bulk Import  
**Location:** `backend/tests/unit/test_map_inventory.py:289-290`  
**Sourcery Comment:** Comment #6  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟡 MEDIUM

**Description:**
Avoid complex code, like loops, in test functions. Use `@pytest.mark.parametrize` or extract helper functions.

**Current Code:**
```python
def test_classification_map_values(self):
    """Test that classification map values are valid Project enum values."""
    valid_classifications = {'primary', 'secondary', 'archive', 'maintenance', None}
    
    for cls, mapped in CLASSIFICATION_MAP.items():
        assert mapped in valid_classifications, f"Invalid classification mapping: {cls} -> {mapped}"
```

**Proposed Solution:**
```python
@pytest.mark.parametrize("classification,mapped_value", [
    ('Personal', 'primary'),
    ('Work (DRW)', 'primary'),
    ('Apprenti', 'primary'),
    ('Learning', 'secondary'),
    ('Inactive/Archived', 'archive'),
    ('Skip', None),
])
def test_classification_map_values(self, classification, mapped_value):
    """Test that classification map values are valid Project enum values."""
    assert CLASSIFICATION_MAP[classification] == mapped_value
    assert mapped_value in {'primary', 'secondary', 'archive', 'maintenance', None}
```

---

### Issue PR16-#7: Avoid Loops in Tests (Instance 4)

**Source PR:** #16 - Phase 5: Bulk Import  
**Location:** `backend/tests/unit/test_map_inventory.py:296-297`  
**Sourcery Comment:** Comment #7  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟡 MEDIUM

**Description:**
Avoid complex code, like loops, in test functions. Use `@pytest.mark.parametrize` or extract helper functions.

**Current Code:**
```python
def test_status_map_values(self):
    """Test that status map values are valid Project enum values."""
    valid_statuses = {'active', 'paused', 'completed', 'cancelled', None}
    
    for cls, mapped in STATUS_MAP.items():
        assert mapped in valid_statuses, f"Invalid status mapping: {cls} -> {mapped}"
```

**Proposed Solution:**
```python
@pytest.mark.parametrize("classification,status_value", [
    ('Personal', 'active'),
    ('Work (DRW)', 'active'),
    ('Apprenti', 'active'),
    ('Learning', 'active'),
    ('Inactive/Archived', 'cancelled'),
    ('Skip', None),
])
def test_status_map_values(self, classification, status_value):
    """Test that status map values are valid Project enum values."""
    assert STATUS_MAP[classification] == status_value
    assert status_value in {'active', 'paused', 'completed', 'cancelled', None}
```

---

## Implementation Steps

### 1. PR02 Issues (Test Improvements)
   - [ ] **PR02-#4:** Add null path serialization assertion to `test_list_projects_with_data`
   - [ ] **PR02-#6:** Update `test_project_name_required` to use `IntegrityError` and add rollback
   - [ ] **PR02-#7:** Update `test_project_path_unique` to use `IntegrityError` and add rollback
   - [ ] **PR02-#8:** Update `test_project_timestamps` to verify `updated_at` changes on update

### 2. PR13 Issue (Strengthen Assertions)
   - [ ] **PR13-#1:** Update `test_filter_projects_invalid_status_value_ignored` to verify returned projects match created projects

### 3. PR16 Issues (Avoid Loops in Tests)
   - [ ] **PR16-#4:** Refactor `test_classification_map_completeness` to use `@pytest.mark.parametrize`
   - [ ] **PR16-#5:** Refactor `test_status_map_completeness` to use `@pytest.mark.parametrize`
   - [ ] **PR16-#6:** Refactor `test_classification_map_values` to use `@pytest.mark.parametrize`
   - [ ] **PR16-#7:** Refactor `test_status_map_values` to use `@pytest.mark.parametrize`

---

## Testing

- [ ] All existing tests pass
- [ ] New test assertions added and passing
- [ ] Parametrized tests cover all cases
- [ ] Test coverage maintained or improved
- [ ] No regressions introduced

**Run tests:**
```bash
cd backend
source ../venv/bin/activate
pytest tests/integration/api/test_projects.py -v
pytest tests/unit/models/test_project.py -v
pytest tests/unit/test_map_inventory.py -v
```

---

## Files to Modify

- `backend/tests/integration/api/test_projects.py` - PR02-#4, PR13-#1
- `backend/tests/unit/models/test_project.py` - PR02-#6, #7, #8
- `backend/tests/unit/test_map_inventory.py` - PR16-#4, #5, #6, #7

---

## Definition of Done

- [ ] All 9 issues in batch fixed
- [ ] Tests passing
- [ ] Test coverage improved
- [ ] Parametrized tests working correctly
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
This batch was created from fix-review report recommendations. These issues are batched together because they:

- Share similar priority and effort levels (MEDIUM/LOW or LOW/MEDIUM)
- All address test quality improvements
- Can be implemented together efficiently
- Were identified as "Test Quality Improvements" in review report
- Improve test coverage, assertions, and clarity
- Reduce test complexity by avoiding loops
- Use proper exception types in tests

**Source PRs:**
- PR #2: 4 issues (test improvements)
- PR #13: 1 issue (strengthen assertions)
- PR #16: 4 issues (avoid loops in tests)

---

**Last Updated:** 2025-12-05  
**Next:** Use `/fix-implement` to implement this batch
