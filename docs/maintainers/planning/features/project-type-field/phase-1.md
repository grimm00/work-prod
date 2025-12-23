# Project Type Field - Phase 1: Schema Migration

**Feature:** Add `project_type` field  
**Phase:** 1 of 3  
**Status:** 🔴 Not Started  
**Estimated Effort:** ~2 hours  
**Created:** 2025-12-23  
**Last Updated:** 2025-12-23

---

## 📋 Phase Overview

Add the `project_type` enum column to the projects table using Flask-Migrate.

**Goal:** Database schema ready to accept project type classification data.

---

## 🎯 Phase Goals

- [ ] Create migration for `project_type` enum column
- [ ] Column is nullable (migration safety)
- [ ] Index added for filtering performance
- [ ] Migration runs successfully locally

---

## 📝 Tasks

### Task 1: Update Project Model (~30 min)

**File:** `backend/app/models/project.py`

Add the `project_type` field to the Project model:

```python
from sqlalchemy import Enum

class Project(db.Model):
    # ... existing fields ...
    
    project_type = db.Column(
        Enum('Work', 'Personal', 'Learning', 'Inactive', name='project_type_enum'),
        nullable=True,  # Nullable for migration safety
        index=True      # Index for filtering performance
    )
```

**Acceptance Criteria:**
- [ ] Field added to model
- [ ] Enum values: Work, Personal, Learning, Inactive
- [ ] Column is nullable
- [ ] Index is added
- [ ] `to_dict()` method updated to include `project_type`

---

### Task 2: Create Migration (~30 min)

**Command:**
```bash
cd backend
flask db migrate -m "Add project_type enum column"
```

**Verify Migration File:**
- Check `migrations/versions/` for new migration
- Verify enum creation
- Verify column addition
- Verify index creation

**Acceptance Criteria:**
- [ ] Migration file created
- [ ] Migration contains enum creation
- [ ] Migration contains column addition
- [ ] Migration contains index

---

### Task 3: Run Migration Locally (~30 min)

**Command:**
```bash
cd backend
flask db upgrade
```

**Verify:**
- Column exists in database
- Enum type exists
- Index exists

**Validation Query:**
```sql
-- SQLite: Check column exists
PRAGMA table_info(project);

-- Check column is present
SELECT project_type FROM project LIMIT 1;
```

**Acceptance Criteria:**
- [ ] Migration runs without errors
- [ ] Column exists in database
- [ ] All existing data preserved

---

### Task 4: Update Tests (~30 min)

**Files to Update:**
- `backend/tests/unit/models/test_project.py`
- `backend/tests/integration/api/test_projects.py`

**Test Cases:**
- [ ] Test model accepts valid project_type values
- [ ] Test model accepts NULL project_type
- [ ] Test model rejects invalid project_type values

**Acceptance Criteria:**
- [ ] Unit tests added for new field
- [ ] All existing tests pass
- [ ] New tests pass

---

## ✅ Phase Completion Criteria

- [ ] Project model updated with `project_type` field
- [ ] Migration file created
- [ ] Migration runs successfully locally
- [ ] Tests added and passing
- [ ] Code committed to feature branch

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Transition Plan](transition-plan.md)
- [Phase 2: Data Backfill](phase-2.md)
- [ADR-003](../../../../../dev-infra/admin/decisions/project-model-definition/adr-003-add-project-type-field.md)

---

**Last Updated:** 2025-12-23

