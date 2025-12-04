# Projects Feature - Phase 3: Projects API - Delete & Archive

**Phase:** 3 - Projects API - Delete & Archive (Backend + CLI)  
**Duration:** 1 day  
**Status:** ✅ Complete  
**Completed:** 2025-12-04  
**Prerequisites:** Phase 2 complete

---

## 📋 Overview

Phase 3 implements DELETE endpoint and archive functionality. This phase allows removing projects permanently or archiving them for historical reference. By the end, you can delete and archive projects via API and CLI.

**Success Definition:** Can delete and archive projects via curl/CLI with appropriate safeguards.

---

## 🎯 Goals

1. **DELETE /api/projects/<id> Endpoint** - Permanently delete projects
2. **PUT /api/projects/<id>/archive Endpoint** - Archive projects (soft delete)
3. **CLI Delete/Archive Commands** - `proj delete` and `proj archive`
4. **Safety Checks** - Confirm before delete, validate archive state

---

## 📝 Tasks

### TDD Flow

#### 1. Write DELETE Endpoint Tests (TDD - RED)
- [x] Test DELETE /api/projects/<id> returns 204 No Content
- [x] Test DELETE removes project from database
- [x] Test DELETE on non-existent project returns 404
- [x] Test project cannot be retrieved after deletion

#### 2. Implement DELETE Endpoint (TDD - GREEN)
- [x] Add DELETE route to `backend/app/api/projects.py`
- [x] Implement hard delete: `db.session.delete(project)`
- [x] Return 204 No Content on success
- [x] Tests pass ✅

#### 3. Write Archive Tests (TDD - RED)
- [x] Test archiving sets classification to 'archive' and status to 'completed'
- [x] Test archived projects still appear in list
- [x] Test archived projects filterable

#### 4. Implement Archive Endpoint (TDD - GREEN)
- [x] Add PUT /api/projects/<id>/archive route
- [x] Set `classification='archive'` and `status='completed'`
- [x] Return updated project

#### 5. Enhance CLI
- [x] Add `proj delete <id>` command with confirmation
- [x] Add `proj archive <id>` command
- [x] Test commands

---

## ✅ Completion Criteria

- [x] DELETE endpoint works and removes projects
- [x] Archive endpoint works and updates classification
- [x] Tests pass with coverage > 80% (92% achieved)
- [x] CLI delete/archive commands work
- [x] Safety confirmations in place

---

## 📦 Deliverables

1. DELETE /api/projects/<id> endpoint
2. PUT /api/projects/<id>/archive endpoint  
3. Enhanced CLI with delete/archive
4. Tests for deletion and archiving

---

## 💡 curl Examples

```bash
# Archive a project
curl -X PUT http://localhost:5000/api/projects/1/archive | jq

# Delete a project (permanent)
curl -X DELETE http://localhost:5000/api/projects/1

# Verify deletion
curl http://localhost:5000/api/projects/1
# Expected: 404
```

---

**Last Updated:** 2025-12-04  
**Status:** ✅ Complete  
**Next:** Phase 4 - Search & Filter Projects
