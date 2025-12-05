# Fix Plan: PR #16 Batch LOW MEDIUM - Batch 01

**PR:** 16  
**Batch:** low-medium-01  
**Priority:** 🟢 LOW  
**Effort:** 🟡 MEDIUM  
**Status:** 🔴 Not Started  
**Created:** 2025-12-05  
**Issues:** 4 issues

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR16-#4 | 🟢 LOW | 🟢 LOW | 🟡 MEDIUM | Avoid loop in test (line 273-274) |
| PR16-#5 | 🟢 LOW | 🟢 LOW | 🟡 MEDIUM | Avoid loop in test (line 282-283) |
| PR16-#6 | 🟢 LOW | 🟢 LOW | 🟡 MEDIUM | Avoid loop in test (line 289-290) |
| PR16-#7 | 🟢 LOW | 🟢 LOW | 🟡 MEDIUM | Avoid loop in test (line 296-297) |

---

## Overview

This batch contains 4 LOW priority issues with MEDIUM effort. All issues involve refactoring test code to remove loops, improving test clarity and failure diagnosis.

**Estimated Time:** 2-3 hours  
**Files Affected:**
- `backend/tests/unit/test_map_inventory.py`

---

## Issue Details

### Issue PR16-#4: Avoid Loop in Test (Line 273-274)

**Location:** `backend/tests/unit/test_map_inventory.py:273-274`  
**Sourcery Comment:** Comment #4  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟡 MEDIUM

**Description:**
Avoid complex code, like loops, in test functions. Loops reduce test clarity and make failures harder to diagnose.

**Current Code:**
```python
def test_classification_map_completeness(self):
    """Test that all expected classifications have mappings."""
    expected_classifications = [
        'Personal', 'Work (DRW)', 'Apprenti', 'Learning', 'Inactive/Archived', 'Skip'
    ]
    
    for cls in expected_classifications:
        assert cls in CLASSIFICATION_MAP
```

**Proposed Solution:**
Use parametrized test:
```python
@pytest.mark.parametrize("classification", [
    'Personal',
    'Work (DRW)',
    'Apprenti',
    'Learning',
    'Inactive/Archived',
    'Skip'
])
def test_classification_map_completeness(self, classification):
    """Test that expected classification has mapping."""
    assert classification in CLASSIFICATION_MAP
```

---

### Issue PR16-#5: Avoid Loop in Test (Line 282-283)

**Location:** `backend/tests/unit/test_map_inventory.py:282-283`  
**Sourcery Comment:** Comment #5  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟡 MEDIUM

**Description:**
Same as PR16-#4, but for status map completeness test.

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
Use parametrized test (same pattern as PR16-#4).

---

### Issue PR16-#6: Avoid Loop in Test (Line 289-290)

**Location:** `backend/tests/unit/test_map_inventory.py:289-290`  
**Sourcery Comment:** Comment #6  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟡 MEDIUM

**Description:**
Same pattern, but for classification map values test.

**Current Code:**
```python
def test_classification_map_values(self):
    """Test that classification map values are valid Project enum values."""
    valid_classifications = {'primary', 'secondary', 'archive', 'maintenance', None}
    
    for cls, mapped in CLASSIFICATION_MAP.items():
        assert mapped in valid_classifications, f"Invalid classification mapping: {cls} -> {mapped}"
```

**Proposed Solution:**
Use parametrized test:
```python
@pytest.mark.parametrize("classification,mapped_value", [
    ('Personal', 'primary'),
    ('Work (DRW)', 'primary'),
    # ... etc
])
def test_classification_map_values(self, classification, mapped_value):
    """Test that classification map value is valid."""
    valid_classifications = {'primary', 'secondary', 'archive', 'maintenance', None}
    assert CLASSIFICATION_MAP[classification] == mapped_value
    assert mapped_value in valid_classifications
```

---

### Issue PR16-#7: Avoid Loop in Test (Line 296-297)

**Location:** `backend/tests/unit/test_map_inventory.py:296-297`  
**Sourcery Comment:** Comment #7  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟡 MEDIUM

**Description:**
Same pattern, but for status map values test.

**Current Code:**
```python
def test_status_map_values(self):
    """Test that status map values are valid Project enum values."""
    valid_statuses = {'active', 'paused', 'completed', 'cancelled', None}
    
    for cls, mapped in STATUS_MAP.items():
        assert mapped in valid_statuses, f"Invalid status mapping: {cls} -> {mapped}"
```

**Proposed Solution:**
Use parametrized test (same pattern as PR16-#6).

---

## Implementation Steps

1. **Refactor PR16-#4: Classification Map Completeness**
   - [ ] Convert loop to parametrized test
   - [ ] Use `@pytest.mark.parametrize` decorator
   - [ ] Verify test still passes
   - [ ] Verify test failure is clear

2. **Refactor PR16-#5: Status Map Completeness**
   - [ ] Convert loop to parametrized test
   - [ ] Use same pattern as PR16-#4
   - [ ] Verify test still passes

3. **Refactor PR16-#6: Classification Map Values**
   - [ ] Convert loop to parametrized test
   - [ ] Include both classification and mapped value in parameters
   - [ ] Verify test still passes
   - [ ] Verify error messages are clear

4. **Refactor PR16-#7: Status Map Values**
   - [ ] Convert loop to parametrized test
   - [ ] Use same pattern as PR16-#6
   - [ ] Verify test still passes

---

## Testing

- [ ] All existing tests pass
- [ ] Refactored tests pass with same assertions
- [ ] Test failures are clear and indicate which parameter failed
- [ ] No regressions introduced

---

## Files to Modify

- `backend/tests/unit/test_map_inventory.py` - Refactor 4 test functions to use parametrized tests

---

## Definition of Done

- [ ] All 4 test functions refactored
- [ ] Loops removed from tests
- [ ] Parametrized tests working correctly
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
These issues are batched together because they:
- Share LOW priority and MEDIUM effort
- All involve same pattern (removing loops from tests)
- All in same file (`test_map_inventory.py`)
- Can be refactored together efficiently
- Improve test code quality consistently

