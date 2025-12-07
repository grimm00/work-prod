# Fix Plan: PR08-#2 - Null Status Validation Bug

**Issue ID:** PR08-#2  
**Sourcery Comment:** Comment #2  
**Priority:** 🟠 HIGH  
**Impact:** 🟠 HIGH  
**Effort:** 🟡 MEDIUM  
**Status:** 🔴 Not Fixed  
**Created:** 2025-12-04

---

## Problem

**Location:** `backend/app/api/projects.py:76-85` (update_project function)

**Description:**
When a client sends `"status": null` in the request payload, validation is skipped (because `data['status'] is not None` fails), but the code still tries to update `project.status = data['status']`, which attempts to write NULL to a non-null column. This raises an `IntegrityError` that's surfaced as a generic 409 Conflict, which is confusing for clients.

**Current Code:**
```python
# Validate status if provided
if 'status' in data and data['status'] is not None:
    if data['status'] not in VALID_STATUSES:
        return jsonify({
            'error': f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"
        }), 400

# Later...
if 'status' in data:
    project.status = data['status']  # This assigns None if data['status'] is None!
```

**The Bug:**
1. Payload: `{"status": null}`
2. Validation check passes (because None is not validated)
3. Update code runs: `project.status = None`
4. Database rejects NULL value (column is NOT NULL)
5. IntegrityError caught and returned as generic 409
6. Client gets confusing "Database integrity error" instead of clear validation error

**User Impact:**
- Confusing error messages (409 instead of 400)
- Poor API UX (validation error should be 400 Bad Request)
- Harder to debug for API consumers

---

## Solution

### Option 1: Reject Explicit Null (Recommended)

Treat `"status": null` as a validation error:

```python
# Validate status if provided
if 'status' in data:
    if data['status'] is None:
        return jsonify({'error': 'Status cannot be null'}), 400
    if data['status'] not in VALID_STATUSES:
        return jsonify({
            'error': f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"
        }), 400
```

**Benefits:**
- Clear, explicit validation error
- Proper 400 status code
- Consistent with other validation

### Option 2: Skip Update on Null

Don't update status if value is None:

```python
# Validate status if provided and not None
if 'status' in data and data['status'] is not None:
    if data['status'] not in VALID_STATUSES:
        return jsonify({
            'error': f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"
        }), 400

# Later, in update section:
if 'status' in data and data['status'] is not None:
    project.status = data['status']
```

**Benefits:**
- Allows clients to send `"status": null` without error (it's ignored)
- No database constraint violation

**Drawback:**
- Less explicit - null is silently ignored rather than rejected

### Recommendation: Option 1

**Reason:** More explicit and provides better API feedback. If a client sends `"status": null`, they should know it's not allowed.

---

## Implementation Steps

1. **Update validation in `update_project`**
   - Add explicit null check before enum validation
   - Return 400 with clear message: "Status cannot be null"

2. **Consider same issue for `classification`**
   - Check if classification has same problem
   - Classification is nullable, so null might be valid (to clear the field)
   - If clearing is valid, add skip logic; if not, reject null

3. **Add tests for null values**
   ```python
   def test_update_project_null_status_rejected(client):
       """Test that null status value is rejected with 400."""
       # Create a project first
       response = client.post('/api/projects', 
                            json={'name': 'Test'}, 
                            content_type='application/json')
       project_id = json.loads(response.data)['id']
       
       # Try to update with null status
       response = client.patch(f'/api/projects/{project_id}',
                             json={'status': None},
                             content_type='application/json')
       
       assert response.status_code == 400
       data = json.loads(response.data)
       assert 'cannot be null' in data['error'].lower()
   ```

4. **Check `create_project` function**
   - Same validation logic should be added there
   - `status` defaults to 'active' in create, so less likely to be an issue
   - But explicit null should still be rejected

5. **Update manual testing guide**
   - Add scenario for null value handling
   - Document expected behavior

---

## Design Decision: Nullable vs Non-Nullable Fields

**Fields that are NOT NULL (required):**
- `status` - Must always have a value (defaults to 'active')

**Fields that ARE nullable (optional):**
- `classification` - Can be null (not all projects classified)
- `organization` - Can be null
- `description` - Can be null
- `remote_url` - Can be null
- `path` - Can be null

**Validation Strategy:**
- **Non-nullable fields:** Reject explicit `null` with 400 error
- **Nullable fields:** Allow `null` to clear the value, or skip update if `null`

**For this fix, focus on `status` field which is non-nullable.**

---

## Files to Modify

- `backend/app/api/projects.py`
  - Update `update_project` validation
  - Update `create_project` validation (if needed)
- `backend/tests/integration/api/test_projects.py`
  - Add test for null status rejection (update)
  - Add test for null status rejection (create, if applicable)
- `docs/maintainers/planning/features/projects/manual-testing.md`
  - Add null value scenario

---

## Related Issues

- **PR08 Overall-1**: Validation duplication (should refactor validation together)
- **Classification null handling**: Need to decide if null should clear the field

---

## Testing

### Integration Tests

```python
@pytest.mark.integration
def test_update_project_null_status_returns_400(client):
    """Test that updating status to null returns 400."""
    # Create project
    response = client.post('/api/projects', 
                         json={'name': 'Test Project'},
                         content_type='application/json')
    project_id = json.loads(response.data)['id']
    
    # Try to set status to null
    response = client.patch(f'/api/projects/{project_id}',
                          json={'status': None},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'null' in data['error'].lower() or 'required' in data['error'].lower()

@pytest.mark.integration
def test_update_project_null_classification_allowed(client):
    """Test that classification can be cleared with null (if that's the design)."""
    # Create project with classification
    response = client.post('/api/projects', 
                         json={'name': 'Test', 'classification': 'primary'},
                         content_type='application/json')
    project_id = json.loads(response.data)['id']
    
    # Clear classification
    response = client.patch(f'/api/projects/{project_id}',
                          json={'classification': None},
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['classification'] is None
```

---

## Definition of Done

- [ ] Null status value rejected with 400 Bad Request (not 409)
- [ ] Clear error message returned
- [ ] Applied to both `update_project` and `create_project` (if needed)
- [ ] Decision made on nullable field handling (classification, etc.)
- [ ] Tests added for null value scenarios
- [ ] Manual testing guide updated
- [ ] No more IntegrityError for null status

---

**Priority Justification:**
🟠 HIGH because this creates a **confusing user experience**:
- Wrong HTTP status code (409 instead of 400)
- Generic error message hides the real problem
- Makes API harder to use and debug
- Could lead to client-side workarounds

This **should be fixed before merging PR #8** for good API design.

