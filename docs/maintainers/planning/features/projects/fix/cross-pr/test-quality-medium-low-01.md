# Fix Plan: Cross-PR Batch Test Quality - MEDIUM LOW

**Batch:** test-quality-medium-low-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟢 LOW  
**Status:** 🔴 Not Started  
**Created:** 2025-12-05  
**Source:** fix-review-report-2025-12-05.md  
**Issues:** 4 issues from 4 PRs

---

## Issues in This Batch

| Issue   | PR  | Priority   | Impact   | Effort   | Description                |
| ------- | --- | ---------- | -------- | -------- | -------------------------- |
| PR02-#4 | 2   | 🟡 MEDIUM  | 🟡 MEDIUM| 🟢 LOW   | Test null path serialization |
| PR02-#8 | 2   | 🟡 MEDIUM  | 🟡 MEDIUM| 🟢 LOW   | Test updated_at changes |
| PR08-#3 | 8   | 🟡 MEDIUM  | 🟡 MEDIUM| 🟢 LOW   | Missing test: empty JSON body |
| PR13-#1 | 13  | 🟡 MEDIUM  | 🟢 LOW   | 🟢 LOW   | Strengthen test assertions |

---

## Overview

This batch contains 4 MEDIUM priority issues with LOW effort from 4 PRs. These issues improve test coverage and quality by adding missing tests, strengthening assertions, and catching edge cases.

**Estimated Time:** 2-3 hours  
**Files Affected:** 
- `backend/tests/integration/api/test_projects.py` (all issues)

**Source PRs:**

- PR #2: Phase 1: List & Get Projects
- PR #8: Phase 2: Create & Update Projects
- PR #13: Fix Batch (pr12-batch-medium-medium-01)

---

## Issue Details

### Issue PR02-#4: Test Null Path Serialization

**Source PR:** #2 - Phase 1: List & Get Projects  
**Location:** `backend/tests/integration/api/test_projects.py`  
**Sourcery Comment:** Comment #4  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
Add test to verify that null path values are properly serialized in API responses.

**Note:** Specific details need to be extracted from PR #2 Sourcery review.

**Related Files:**

- `backend/tests/integration/api/test_projects.py`

---

### Issue PR02-#8: Test updated_at Changes

**Source PR:** #2 - Phase 1: List & Get Projects  
**Location:** `backend/tests/integration/api/test_projects.py`  
**Sourcery Comment:** Comment #8  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
Add test to verify that `updated_at` timestamp changes when a project is updated.

**Note:** Specific details need to be extracted from PR #2 Sourcery review.

**Related Files:**

- `backend/tests/integration/api/test_projects.py`

---

### Issue PR08-#3: Missing Test - Empty JSON Body

**Source PR:** #8 - Phase 2: Create & Update Projects  
**Location:** `backend/tests/integration/api/test_projects.py:120-129`  
**Sourcery Comment:** Comment #3  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
`test_create_project_missing_name` only covers the case where `path` is present but `name` is missing. The code also returns 400 for an empty body (`{}`) or no body (`None` from `get_json()`), but that isn't directly tested. Adding a test like `test_create_project_empty_body_returns_400` (e.g. `client.post('/api/projects', data='', content_type='application/json')` or `json={}`) would capture that behavior and help prevent regressions.

**Current Code:**

```python
@pytest.mark.integration
def test_create_project_missing_name(client):
    """Test that POST without name returns 400."""
    response = client.post('/api/projects',
                          json={'path': '/test'},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
```

**Proposed Solution:**

Add new test:

```python
@pytest.mark.integration
def test_create_project_empty_body_returns_400(client):
    """Test that POST with empty JSON body returns 400."""
    response = client.post('/api/projects',
                          json={},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

@pytest.mark.integration
def test_create_project_no_body_returns_400(client):
    """Test that POST with no body returns 400."""
    response = client.post('/api/projects',
                          data='',
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
```

**Related Files:**

- `backend/tests/integration/api/test_projects.py`

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
data = json.loads(response.data)
assert isinstance(data, list)
assert len(data) == 2

# Ensure that the returned projects are exactly the ones created in this test
returned_names = {project["name"] for project in data}
assert returned_names == {project1.name, project2.name}
```

**Related Files:**

- `backend/tests/integration/api/test_projects.py`

---

## Implementation Steps

1. **Issue PR02-#4: Test Null Path Serialization**
   - [ ] Extract specific test details from PR #2 review
   - [ ] Add test for null path serialization
   - [ ] Run tests to verify

2. **Issue PR02-#8: Test updated_at Changes**
   - [ ] Extract specific test details from PR #2 review
   - [ ] Add test to verify `updated_at` changes on update
   - [ ] Run tests to verify

3. **Issue PR08-#3: Missing Test - Empty JSON Body**
   - [ ] Add `test_create_project_empty_body_returns_400` test
   - [ ] Add `test_create_project_no_body_returns_400` test
   - [ ] Run tests to verify both scenarios

4. **Issue PR13-#1: Strengthen Test Assertions**
   - [ ] Update `test_filter_projects_invalid_status_value_ignored` test
   - [ ] Add assertion to verify returned projects match created projects
   - [ ] Run tests to verify

---

## Testing

- [ ] All existing tests pass
- [ ] New tests added and passing
- [ ] Test coverage improved
- [ ] Edge cases covered
- [ ] No regressions introduced

---

## Files to Modify

- `backend/tests/integration/api/test_projects.py` - All test improvements

---

## Definition of Done

- [ ] All 4 issues in batch fixed
- [ ] Tests passing
- [ ] Test coverage improved
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
This batch was created from fix-review report recommendations. These issues are batched together because they:

- Share similar priority and effort levels (all MEDIUM/LOW)
- Address test quality improvements
- Can be implemented together efficiently
- Were identified as "Test Quality Improvements" in review report
- Improve test coverage and quality
- Catch edge cases
- Provide better test assertions

