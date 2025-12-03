# Projects Feature - Phase 3: Projects API - Delete & Archive

**Phase:** 3 - Projects API - Delete & Archive (Backend + CLI)  
**Duration:** 1 day  
**Status:** 🔴 Not Started  
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
- [ ] Test DELETE /api/projects/<id> returns 204 No Content
- [ ] Test DELETE removes project from database
- [ ] Test DELETE on non-existent project returns 404
- [ ] Test project cannot be retrieved after deletion

#### 2. Implement DELETE Endpoint (TDD - GREEN)
- [ ] Add DELETE route to `backend/app/api/projects.py`
- [ ] Implement hard delete: `db.session.delete(project)`
- [ ] Return 204 No Content on success
- [ ] Tests pass ✅

#### 3. Write Archive Tests (TDD - RED)
- [ ] Test archiving sets classification to 'archive' and status to 'completed'
- [ ] Test archived projects still appear in list
- [ ] Test archived projects filterable

#### 4. Implement Archive Endpoint (TDD - GREEN)
- [ ] Add PUT /api/projects/<id>/archive route
- [ ] Set `classification='archive'` and `status='completed'`
- [ ] Return updated project

#### 5. Enhance CLI
- [ ] Add `proj delete <id>` command with confirmation
- [ ] Add `proj archive <id>` command
- [ ] Test commands

---

## ✅ Completion Criteria

- [ ] DELETE endpoint works and removes projects
- [ ] Archive endpoint works and updates classification
- [ ] Tests pass with coverage > 80%
- [ ] CLI delete/archive commands work
- [ ] Safety confirmations in place

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

**Last Updated:** 2025-12-02  
**Status:** 🔴 Not Started  
**Next:** Begin after Phase 2 complete
