# Fix Plan: PR #35 Batch MEDIUM MEDIUM - Batch 02

**PR:** #35  
**Batch:** medium-medium-02  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟡 MEDIUM  
**Status:** 🔴 Not Started  
**Created:** 2025-12-07  
**Issues:** 4 issues

---

## Issues in This Batch

| Issue   | Priority   | Impact   | Effort   | Description   |
| ------- | ---------- | -------- | -------- | ------------- |
| PR35-#12 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Loop in performance test - refactor to avoid loops |
| PR35-#13 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Loop in performance test - refactor to avoid loops |
| PR35-#14 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Loop in performance test - refactor to avoid loops |
| PR35-#15 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Loop in performance test - refactor to avoid loops |

---

## Overview

This batch contains 4 MEDIUM priority issues with MEDIUM effort related to refactoring loops in performance tests. These issues improve code quality by avoiding loops in test functions.

**Estimated Time:** 2-3 hours  
**Files Affected:** 
- `backend/tests/performance/test_query_performance.py`

---

## Issues Details

### Issue PR35-#12: Loop in Performance Test (Lines 101-107)

**Location:** `backend/tests/performance/test_query_performance.py:101-107`  
**Sourcery Comment:** Comment #12  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟡 MEDIUM

**Description:**
Avoid loops in tests. Refactor to use `pytest.mark.parametrize` or separate test functions.

**Current Code:**

```python
def test_filter_projects_performance(client, sample_projects):
    """Test that filter projects endpoint performs well."""
    start = time.time()
    for _ in range(10):
        response = client.get('/api/projects?status=active')
        assert response.status_code == 200
    elapsed = time.time() - start
    assert elapsed < 1.0, f"10 requests took {elapsed:.3f}s, expected < 1.0s"
```

**Proposed Solution:**

```python
@pytest.mark.parametrize('iteration', range(10))
def test_filter_projects_performance(client, sample_projects, iteration):
    """Test that filter projects endpoint performs well."""
    response = client.get('/api/projects?status=active')
    assert response.status_code == 200

def test_filter_projects_performance_aggregate(client, sample_projects):
    """Test that filter projects endpoint performs well over multiple requests."""
    start = time.perf_counter()
    responses = [client.get('/api/projects?status=active') for _ in range(10)]
    elapsed = time.perf_counter() - start
    assert all(r.status_code == 200 for r in responses)
    assert elapsed < 1.0, f"10 requests took {elapsed:.3f}s, expected < 1.0s"
```

---

### Issue PR35-#13: Loop in Performance Test (Lines 127-133)

**Location:** `backend/tests/performance/test_query_performance.py:127-133`  
**Sourcery Comment:** Comment #13  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟡 MEDIUM

**Description:**
Avoid loops in tests. Refactor to use `pytest.mark.parametrize` or separate test functions.

**Current Code:**

```python
def test_list_projects_with_pagination_performance(client, sample_projects):
    """Test that paginated list projects endpoint performs well."""
    start = time.time()
    for _ in range(10):
        response = client.get('/api/projects?page=1&per_page=10')
        assert response.status_code == 200
    elapsed = time.time() - start
    assert elapsed < 1.0, f"10 requests took {elapsed:.3f}s, expected < 1.0s"
```

**Proposed Solution:**

```python
@pytest.mark.parametrize('iteration', range(10))
def test_list_projects_with_pagination_performance(client, sample_projects, iteration):
    """Test that paginated list projects endpoint performs well."""
    response = client.get('/api/projects?page=1&per_page=10')
    assert response.status_code == 200

def test_list_projects_with_pagination_performance_aggregate(client, sample_projects):
    """Test that paginated list projects endpoint performs well over multiple requests."""
    start = time.perf_counter()
    responses = [client.get('/api/projects?page=1&per_page=10') for _ in range(10)]
    elapsed = time.perf_counter() - start
    assert all(r.status_code == 200 for r in responses)
    assert elapsed < 1.0, f"10 requests took {elapsed:.3f}s, expected < 1.0s"
```

---

### Issue PR35-#14: Loop in Performance Test (Lines 160-165)

**Location:** `backend/tests/performance/test_query_performance.py:160-165`  
**Sourcery Comment:** Comment #14  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟡 MEDIUM

**Description:**
Avoid loops in tests. Refactor to use `pytest.mark.parametrize` or separate test functions.

**Current Code:**

```python
def test_get_project_not_found_performance(client):
    """Test that 404 responses are fast."""
    start = time.time()
    for _ in range(10):
        response = client.get('/api/projects/99999')
        assert response.status_code == 404
    elapsed = time.time() - start
    assert elapsed < 0.5, f"10 requests took {elapsed:.3f}s, expected < 0.5s"
```

**Proposed Solution:**

```python
@pytest.mark.parametrize('iteration', range(10))
def test_get_project_not_found_performance(client, iteration):
    """Test that 404 responses are fast."""
    response = client.get('/api/projects/99999')
    assert response.status_code == 404

def test_get_project_not_found_performance_aggregate(client):
    """Test that 404 responses are fast over multiple requests."""
    start = time.perf_counter()
    responses = [client.get('/api/projects/99999') for _ in range(10)]
    elapsed = time.perf_counter() - start
    assert all(r.status_code == 404 for r in responses)
    assert elapsed < 0.5, f"10 requests took {elapsed:.3f}s, expected < 0.5s"
```

---

### Issue PR35-#15: Loop in Performance Test (Lines 187-195)

**Location:** `backend/tests/performance/test_query_performance.py:187-195`  
**Sourcery Comment:** Comment #15  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟡 MEDIUM

**Description:**
Avoid loops in tests. Refactor to use `pytest.mark.parametrize` or separate test functions.

**Current Code:**

```python
def test_list_projects_empty_database_performance(client):
    """Test that listing projects on empty database is fast."""
    start = time.time()
    for _ in range(10):
        response = client.get('/api/projects')
        assert response.status_code == 200
    elapsed = time.time() - start
    assert elapsed < 0.5, f"10 requests took {elapsed:.3f}s, expected < 0.5s"
```

**Proposed Solution:**

```python
@pytest.mark.parametrize('iteration', range(10))
def test_list_projects_empty_database_performance(client, iteration):
    """Test that listing projects on empty database is fast."""
    response = client.get('/api/projects')
    assert response.status_code == 200

def test_list_projects_empty_database_performance_aggregate(client):
    """Test that listing projects on empty database is fast over multiple requests."""
    start = time.perf_counter()
    responses = [client.get('/api/projects') for _ in range(10)]
    elapsed = time.perf_counter() - start
    assert all(r.status_code == 200 for r in responses)
    assert elapsed < 0.5, f"10 requests took {elapsed:.3f}s, expected < 0.5s"
```

---

## Implementation Steps

1. **Issue PR35-#12: Refactor Loop in Filter Projects Performance Test**
   - [ ] Open `backend/tests/performance/test_query_performance.py`
   - [ ] Find test at lines 101-107
   - [ ] Refactor to use `pytest.mark.parametrize` or separate functions
   - [ ] Update timing to use `time.perf_counter()`
   - [ ] Run test to verify it passes

2. **Issue PR35-#13: Refactor Loop in Paginated List Performance Test**
   - [ ] Find test at lines 127-133
   - [ ] Refactor to use `pytest.mark.parametrize` or separate functions
   - [ ] Update timing to use `time.perf_counter()`
   - [ ] Run test to verify it passes

3. **Issue PR35-#14: Refactor Loop in 404 Performance Test**
   - [ ] Find test at lines 160-165
   - [ ] Refactor to use `pytest.mark.parametrize` or separate functions
   - [ ] Update timing to use `time.perf_counter()`
   - [ ] Run test to verify it passes

4. **Issue PR35-#15: Refactor Loop in Empty Database Performance Test**
   - [ ] Find test at lines 187-195
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

- `backend/tests/performance/test_query_performance.py` - Refactor 4 performance tests to avoid loops

---

## Definition of Done

- [ ] All 4 issues in batch fixed
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
- Continuation of batch-medium-medium-01 (same refactoring pattern)

