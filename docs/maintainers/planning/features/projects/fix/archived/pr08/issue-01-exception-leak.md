# Fix Plan: PR08-#1 - Exception Details Leak (Security)

**Issue ID:** PR08-#1  
**Sourcery Comment:** Comment #1  
**Priority:** 🔴 CRITICAL  
**Impact:** 🔴 CRITICAL  
**Effort:** 🟡 MEDIUM  
**Status:** 🔴 Not Fixed  
**Created:** 2025-12-04

---

## Problem

**Location:** `backend/app/api/projects.py:111-113` (and similar in update_project)

**Description:** 
Catching `Exception` and returning `str(e)` to clients risks exposing implementation details (SQL messages, stack traces, etc.) and changes the error response shape from specific branches.

**Current Code:**
```python
except Exception as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), 500
```

**Security Risk:**
- SQL error messages could reveal database schema
- Stack traces could expose file paths and internal logic
- Inconsistent error format from specific error handling branches

---

## Solution

### Option 1: Generic 500 with Server-Side Logging (Recommended)

**Change the exception handler to:**

```python
except IntegrityError:
    db.session.rollback()
    return jsonify({'error': 'Database integrity error'}), 409
except Exception as e:
    db.session.rollback()
    app.logger.error(f"Unexpected error in create_project: {e}", exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500
```

**Benefits:**
- No internal details leaked to clients
- Full error details logged server-side for debugging
- Consistent error response format
- `exc_info=True` includes stack trace in logs

### Option 2: Specific Exception Types

Catch and handle specific exceptions that might occur:

```python
except IntegrityError:
    db.session.rollback()
    return jsonify({'error': 'Database integrity error'}), 409
except ValueError as e:
    db.session.rollback()
    return jsonify({'error': 'Invalid data format'}), 400
except Exception as e:
    db.session.rollback()
    app.logger.error(f"Unexpected error in create_project: {e}", exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500
```

---

## Implementation Steps

1. **Update `create_project` function** in `backend/app/api/projects.py`
   - Replace generic exception message with 'Internal server error'
   - Add `app.logger.error()` call with `exc_info=True`
   
2. **Update `update_project` function** in same file
   - Same changes as above
   
3. **Add test for error logging**
   - Mock an unexpected exception
   - Verify 500 returned with generic message
   - Verify error logged server-side (check `app.logger.error` called)

4. **Update API documentation**
   - Document that 500 errors return generic message
   - Note that full details are logged server-side

---

## Testing

### Unit Test
```python
def test_create_project_unexpected_error_handling(client, app):
    """Test that unexpected errors return generic message and log details."""
    with patch.object(Project, '__init__', side_effect=RuntimeError("Database connection lost")):
        with app.app_context():
            response = client.post('/api/projects', 
                                 json={'name': 'Test Project'},
                                 content_type='application/json')
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert data['error'] == 'Internal server error'
            # Verify no implementation details leaked
            assert 'Database connection' not in data['error']
            assert 'RuntimeError' not in data['error']
```

### Manual Test
1. Temporarily add code to raise an exception
2. Call API endpoint
3. Verify response only contains 'Internal server error'
4. Check server logs contain full error details

---

## Files to Modify

- `backend/app/api/projects.py` - Update exception handling in both functions
- `backend/tests/integration/api/test_projects.py` - Add error handling tests
- `backend/README.md` - Update API docs if needed

---

## Related Issues

- **PR08-#2**: Null status validation (also affects error handling)
- **PR08 Overall-2**: Exception handling duplication (should be refactored together)

---

## Definition of Done

- [ ] Generic error message returned for unexpected exceptions
- [ ] Full error details logged server-side with stack trace
- [ ] Applied to both `create_project` and `update_project`
- [ ] Tests added for error logging
- [ ] Manual testing confirms no details leaked
- [ ] API documentation updated

---

**Priority Justification:**
🔴 CRITICAL because this is a **security vulnerability**. Exposing internal error details can:
- Reveal database schema to potential attackers
- Expose file system paths
- Aid in SQL injection attempts
- Violate security best practices

This **must be fixed before merging PR #8**.

