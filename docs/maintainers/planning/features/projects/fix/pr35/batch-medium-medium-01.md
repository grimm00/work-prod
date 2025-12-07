# Fix Plan: PR #35 Batch MEDIUM MEDIUM - Batch 01

**PR:** #35  
**Batch:** medium-medium-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟡 MEDIUM  
**Status:** 🔴 Not Started  
**Created:** 2025-12-07  
**Issues:** 3 issues

---

## Issues in This Batch

| Issue   | Priority   | Impact   | Effort   | Description   |
| ------- | ---------- | -------- | -------- | ------------- |
| PR35-#9 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Loop in performance test - refactor to avoid loops |
| PR35-#10 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Loop in performance test - refactor to avoid loops |
| PR35-#11 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Loop in performance test - refactor to avoid loops |

---

## Overview

This batch contains 3 MEDIUM priority issues with MEDIUM effort related to refactoring loops in performance tests. These issues improve code quality by avoiding loops in test functions.

**Estimated Time:** 2-3 hours  
**Files Affected:** 
- `backend/tests/performance/test_query_performance.py`

---

## Issues Details

### Issue PR35-#9: Loop in Performance Test (Lines 19-27)

**Location:** `backend/tests/performance/test_query_performance.py:19-27`  
**Sourcery Comment:** Comment #9  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟡 MEDIUM

**Description:**
Avoid loops in tests. Refactor to use `pytest.mark.parametrize` or separate test functions.

**Current Code:**

```python
def test_list_projects_performance(client, sample_projects):
    """Test that list projects endpoint performs well."""
    start = time.time()
    for _ in range(10):
        response = client.get('/api/projects')
        assert response.status_code == 200
    elapsed = time.time() - start
    assert elapsed < 1.0, f"10 requests took {elapsed:.3f}s, expected < 1.0s"
```

**Proposed Solution:**

```python
@pytest.mark.parametrize('iteration', range(10))
def test_list_projects_performance(client, sample_projects, iteration):
    """Test that list projects endpoint performs well."""
    response = client.get('/api/projects')
    assert response.status_code == 200

def test_list_projects_performance_aggregate(client, sample_projects):
    """Test that list projects endpoint performs well over multiple requests."""
    start = time.perf_counter()
    responses = [client.get('/api/projects') for _ in range(10)]
    elapsed = time.perf_counter() - start
    assert all(r.status_code == 200 for r in responses)
    assert elapsed < 1.0, f"10 requests took {elapsed:.3f}s, expected < 1.0s"
```

---

### Issue PR35-#10: Loop in Performance Test (Lines 48-54)

**Location:** `backend/tests/performance/test_query_performance.py:48-54`  
**Sourcery Comment:** Comment #10  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟡 MEDIUM

**Description:**
Avoid loops in tests. Refactor to use `pytest.mark.parametrize` or separate test functions.

**Current Code:**

```python
def test_get_project_performance(client, sample_projects):
    """Test that get project endpoint performs well."""
    project_id = sample_projects[0].id
    start = time.time()
    for _ in range(10):
        response = client.get(f'/api/projects/{project_id}')
        assert response.status_code == 200
    elapsed = time.time() - start
    assert elapsed < 1.0, f"10 requests took {elapsed:.3f}s, expected < 1.0s"
```

**Proposed Solution:**

```python
@pytest.mark.parametrize('iteration', range(10))
def test_get_project_performance(client, sample_projects, iteration):
    """Test that get project endpoint performs well."""
    project_id = sample_projects[0].id
    response = client.get(f'/api/projects/{project_id}')
    assert response.status_code == 200

def test_get_project_performance_aggregate(client, sample_projects):
    """Test that get project endpoint performs well over multiple requests."""
    project_id = sample_projects[0].id
    start = time.perf_counter()
    responses = [client.get(f'/api/projects/{project_id}') for _ in range(10)]
    elapsed = time.perf_counter() - start
    assert all(r.status_code == 200 for r in responses)
    assert elapsed < 1.0, f"10 requests took {elapsed:.3f}s, expected < 1.0s"
```

---

### Issue PR35-#11: Loop in Performance Test (Lines 75-81)

**Location:** `backend/tests/performance/test_query_performance.py:75-81`  
**Sourcery Comment:** Comment #11  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟡 MEDIUM

**Description:**
Avoid loops in tests. Refactor to use `pytest.mark.parametrize` or separate test functions.

**Current Code:**

```python
def test_search_projects_performance(client, sample_projects):
    """Test that search projects endpoint performs well."""
    start = time.time()
    for _ in range(10):
        response = client.get('/api/projects?search=test')
        assert response.status_code == 200
    elapsed = time.time() - start
    assert elapsed < 1.0, f"10 requests took {elapsed:.3f}s, expected < 1.0s"
```

**Proposed Solution:**

```python
@pytest.mark.parametrize('iteration', range(10))
def test_search_projects_performance(client, sample_projects, iteration):
    """Test that search projects endpoint performs well."""
    response = client.get('/api/projects?search=test')
    assert response.status_code == 200

def test_search_projects_performance_aggregate(client, sample_projects):
    """Test that search projects endpoint performs well over multiple requests."""
    start = time.perf_counter()
    responses = [client.get('/api/projects?search=test') for _ in range(10)]
    elapsed = time.perf_counter() - start
    assert all(r.status_code == 200 for r in responses)
    assert elapsed < 1.0, f"10 requests took {elapsed:.3f}s, expected < 1.0s"
```

---

## Implementation Steps

1. **Issue PR35-#9: Refactor Loop in List Projects Performance Test**
   - [ ] Open `backend/tests/performance/test_query_performance.py`
   - [ ] Find test at lines 19-27
   - [ ] Refactor to use `pytest.mark.parametrize` or separate functions
   - [ ] Update timing to use `time.perf_counter()`
   - [ ] Run test to verify it passes

2. **Issue PR35-#10: Refactor Loop in Get Project Performance Test**
   - [ ] Find test at lines 48-54
   - [ ] Refactor to use `pytest.mark.parametrize` or separate functions
   - [ ] Update timing to use `time.perf_counter()`
   - [ ] Run test to verify it passes

3. **Issue PR35-#11: Refactor Loop in Search Projects Performance Test**
   - [ ] Find test at lines 75-81
   - [ ] Refactor to use `pytest.mark.parametrize` or separate functions
   - [ ] Update timing to use `time.perf_counter()`
   - [ ] Run test to verify it passes

---

## Testing

- [ ] All existing tests pass
- [ ] Performance tests still measure performance correctly
- [ ] No loops remain in test functions
- [ ] Tests are easier to read and maintain
- [ ] No regressions introduced

---

## Files to Modify

- `backend/tests/performance/test_query_performance.py` - Refactor 3 performance tests to avoid loops

---

## Definition of Done

- [ ] All 3 issues in batch fixed
- [ ] Loops removed from test functions
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
These issues are batched together because they:

- Share MEDIUM priority and MEDIUM effort levels
- All relate to the same file (`test_query_performance.py`)
- All involve the same refactoring pattern (removing loops)
- Can be implemented together efficiently

