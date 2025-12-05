# Fix Plan: PR #2 Batch MEDIUM LOW - Batch 01

**PR:** #2  
**Batch:** medium-low-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟢 LOW  
**Status:** 🔴 Not Started  
**Created:** 2025-12-05  
**Issues:** 4 issues

---

## Issues in This Batch

| Issue   | Priority   | Impact   | Effort   | Description                      |
| ------- | ---------- | -------- | -------- | -------------------------------- |
| PR02-#4 | 🟡 MEDIUM  | 🟡 MEDIUM | 🟢 LOW   | Test null path serialization     |
| PR02-#6 | 🟡 MEDIUM  | 🟡 MEDIUM | 🟢 LOW   | Use IntegrityError in name test  |
| PR02-#7 | 🟡 MEDIUM  | 🟡 MEDIUM | 🟢 LOW   | Use IntegrityError in path test   |
| PR02-#8 | 🟡 MEDIUM  | 🟡 MEDIUM | 🟢 LOW   | Test updated_at changes           |

---

## Overview

This batch contains 4 MEDIUM priority issues with LOW effort. These issues are all related to test improvements and better test coverage/assertions.

**Estimated Time:** 1-2 hours  
**Files Affected:**

- `backend/tests/integration/api/test_projects.py` (PR02-#4)
- `backend/tests/unit/models/test_project.py` (PR02-#6, #7, #8)

---

## Issue Details

### Issue PR02-#4: Test Null Path Serialization

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

Add assertion to verify `project3` has `path=None` in the response:

```python
# Check project with no path is serialized with path=None (null in JSON)
project_without_path = next((p for p in data if p.get("name") == "Project 3"), None)
assert project_without_path is not None
assert "path" in project_without_path
assert project_without_path["path"] is None
```

---

### Issue PR02-#6: Use IntegrityError in Name Test

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
    from datetime import datetime, timedelta
    
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
    import time
    time.sleep(0.1)
    
    # Update project
    project.name = "Updated Project"
    db.session.commit()
    
    # Verify updated_at changed but created_at didn't
    assert project.created_at == original_created_at
    assert project.updated_at > original_updated_at
```

---

## Implementation Steps

1. **Issue PR02-#4: Test Null Path Serialization**
   - [ ] Open `backend/tests/integration/api/test_projects.py`
   - [ ] Find `test_list_projects_with_data` function
   - [ ] Add assertion to check `project3` has `path=None` in response
   - [ ] Run test to verify it passes

2. **Issue PR02-#6: Use IntegrityError in Name Test**
   - [ ] Open `backend/tests/unit/models/test_project.py`
   - [ ] Find `test_project_name_required` function
   - [ ] Import `IntegrityError` from `sqlalchemy.exc`
   - [ ] Replace `Exception` with `IntegrityError` in `pytest.raises`
   - [ ] Add `db.session.rollback()` after the exception
   - [ ] Run test to verify it passes

3. **Issue PR02-#7: Use IntegrityError in Path Test**
   - [ ] Open `backend/tests/unit/models/test_project.py`
   - [ ] Find `test_project_path_unique` function
   - [ ] Import `IntegrityError` from `sqlalchemy.exc` (if not already imported)
   - [ ] Replace `Exception` with `IntegrityError` in `pytest.raises`
   - [ ] Add `db.session.rollback()` after the exception
   - [ ] Run test to verify it passes

4. **Issue PR02-#8: Test Updated At Changes**
   - [ ] Open `backend/tests/unit/models/test_project.py`
   - [ ] Find `test_project_timestamps` function
   - [ ] Add test logic to update project and verify `updated_at` changes
   - [ ] Verify `created_at` remains unchanged
   - [ ] Run test to verify it passes

---

## Testing

- [ ] All existing tests pass
- [ ] New test assertions added and passing
- [ ] No regressions introduced
- [ ] Test coverage maintained or improved

**Run tests:**
```bash
cd backend
source ../venv/bin/activate
pytest tests/integration/api/test_projects.py::test_list_projects_with_data -v
pytest tests/unit/models/test_project.py::test_project_name_required -v
pytest tests/unit/models/test_project.py::test_project_path_unique -v
pytest tests/unit/models/test_project.py::test_project_timestamps -v
```

---

## Files to Modify

- `backend/tests/integration/api/test_projects.py` - Add null path serialization assertion (PR02-#4)
- `backend/tests/unit/models/test_project.py` - Use IntegrityError and add rollback (PR02-#6, #7)
- `backend/tests/unit/models/test_project.py` - Add updated_at change test (PR02-#8)

---

## Definition of Done

- [ ] All 4 issues in batch fixed
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Documentation updated (if needed)
- [ ] Ready for PR

---

**Batch Rationale:**
These issues are batched together because they:

- Share similar priority and effort levels (all MEDIUM/LOW)
- All related to test improvements and better assertions
- Can be implemented together efficiently
- Improve test quality and coverage
- Use similar patterns (exception handling, test assertions)

