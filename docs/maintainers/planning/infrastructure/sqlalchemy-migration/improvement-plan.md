# Infrastructure Improvement Plan - SQLAlchemy 2.0 Migration

**Improvement:** Migrate from SQLAlchemy 1.x patterns to 2.0  
**Priority:** 🟢 Low  
**Effort:** Medium  
**Status:** 🔴 Not Started  
**Created:** 2025-12-16  
**Source:** reflection-work-prod-integration-2025-12-16.md

---

## Overview

The current codebase uses SQLAlchemy 1.x patterns that are deprecated in SQLAlchemy 2.0. Specifically, `Query.get()` method shows `LegacyAPIWarning` during tests. This plan addresses migrating to the recommended `Session.get()` pattern.

---

## Problem Statement

### Current Behavior

Tests show deprecation warnings:
```
LegacyAPIWarning: The Query.get() method is considered legacy as of 
the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. 
The method is now available as Session.get()
```

### Impact

- **Current:** Warning only, not blocking functionality
- **Future:** Will break when SQLAlchemy is upgraded to 2.x
- **Testing:** Warnings clutter test output (5 warnings currently)

### Root Cause

Code uses:
```python
# Legacy pattern
Project.query.get(project_id)
```

Instead of:
```python
# SQLAlchemy 2.0 pattern
db.session.get(Project, project_id)
```

---

## Benefits

### Technical Benefits

- Future-proof for SQLAlchemy 2.0 compatibility
- Clean test output (no deprecation warnings)
- Follows current SQLAlchemy best practices
- Prepares codebase for SQLAlchemy 2.x upgrade

### Developer Experience

- Cleaner test output
- Consistent database access patterns
- Modern SQLAlchemy knowledge

---

## Implementation Steps

### Step 1: Identify All Query.get() Usages

**Action:** Search codebase for all `Query.get()` usages

```bash
grep -r "\.query\.get\(" backend/
grep -r "\.query\.get\(" scripts/
```

**Expected Locations:**
- `backend/app/api/projects.py` - API endpoints
- `scripts/project_cli/tests/` - CLI integration tests

### Step 2: Migrate API Endpoints

**File:** `backend/app/api/projects.py`

**Before:**
```python
project = Project.query.get(project_id)
```

**After:**
```python
project = db.session.get(Project, project_id)
```

**Testing:** Run API tests to verify functionality

### Step 3: Migrate Test Code

**Files:** `scripts/project_cli/tests/integration/*.py`

**Before:**
```python
project = Project.query.get(project.id)
```

**After:**
```python
project = db.session.get(Project, project.id)
```

**Note:** May need to import `db` in test files

### Step 4: Verify No Regressions

**Actions:**
1. Run full backend test suite
2. Run CLI test suite
3. Verify no deprecation warnings remain
4. Manual testing of affected endpoints

### Step 5: Update Documentation

**Actions:**
1. Add SQLAlchemy patterns to backend rules
2. Document preferred database access patterns
3. Update any code examples in documentation

---

## Definition of Done

- [ ] All `Query.get()` usages migrated to `Session.get()`
- [ ] All backend tests passing (229+ tests)
- [ ] All CLI tests passing (63+ tests)
- [ ] No SQLAlchemy deprecation warnings in test output
- [ ] Documentation updated with correct patterns
- [ ] Cursor rules updated (if applicable)

---

## Testing Plan

### Unit Tests

- Verify all existing tests pass
- No new test code needed (testing existing functionality)

### Integration Tests

- Test GET /api/projects/:id endpoint
- Test archive endpoint
- Test delete endpoint
- Test any endpoint using get() pattern

### Manual Testing

- Verify project retrieval by ID works
- Verify archive functionality works
- Verify delete functionality works

---

## Risks & Mitigations

### Risk: Breaking Changes

**Mitigation:** 
- `Session.get()` has identical signature to `Query.get()`
- No behavioral changes expected
- Full test suite catches regressions

### Risk: Import Issues

**Mitigation:**
- Ensure `db` is imported where needed
- May need to adjust test fixtures

---

## Timeline

**Estimated Effort:** 2-3 hours

| Phase | Duration | Status |
|-------|----------|--------|
| Identify usages | 15 min | 🔴 Not Started |
| Migrate API endpoints | 30 min | 🔴 Not Started |
| Migrate test code | 30 min | 🔴 Not Started |
| Run test suite | 30 min | 🔴 Not Started |
| Update documentation | 30 min | 🔴 Not Started |
| Review & commit | 15 min | 🔴 Not Started |

---

## Related

- **Reflection:** `docs/maintainers/planning/notes/reflections/reflection-work-prod-integration-2025-12-16.md`
- **Backend Rules:** `.cursor/rules/backend.mdc`
- **SQLAlchemy Docs:** [Session.get()](https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.get)

---

**Last Updated:** 2025-12-16  
**Status:** 🔴 Not Started  
**Next:** Schedule for implementation when prioritized

