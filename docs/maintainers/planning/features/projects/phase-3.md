# Projects Feature - Phase 3: Update/Delete CRUD

**Phase:** 3 - Complete CRUD Operations  
**Duration:** 2 days  
**Status:** 🔴 Not Started  
**Prerequisites:** Phase 2 complete

---

## 📋 Overview

Phase 3 completes CRUD operations by adding update (edit) and delete functionality. This phase enables users to modify existing projects and remove projects they no longer need.

**Success Definition:** Can edit and delete projects via UI with confirmation dialogs.

---

## 🎯 Goals

1. **PATCH /api/projects/{id}** - Update existing project
2. **DELETE /api/projects/{id}** - Delete project
3. **Edit UI** - Edit mode in ProjectForm
4. **Delete UI** - Delete button with confirmation
5. **Optimistic Updates** - UI updates before API response

---

## 📝 TDD Tasks

### Update Functionality

- [ ] Write backend update tests
  - Test updating individual fields
  - Test validation on update
  - Test updating non-existent project (404)
- [ ] Implement PATCH /api/projects/{id} endpoint
- [ ] Write frontend edit tests
- [ ] Implement edit functionality in ProjectForm
- [ ] Add Zustand `updateProject()` action

### Delete Functionality

- [ ] Write backend delete tests
  - Test successful deletion (204 No Content)
  - Test deleting non-existent project (404)
- [ ] Implement DELETE /api/projects/{id} endpoint
- [ ] Write frontend delete tests
- [ ] Implement delete button with confirmation dialog
- [ ] Add Zustand `deleteProject()` action

### Integration

- [ ] Test edit → save → see changes in list
- [ ] Test delete → confirm → removed from list
- [ ] Manual testing of all CRUD operations

---

## ✅ Completion Criteria

- [ ] PATCH and DELETE endpoints work
- [ ] Edit project UI functional
- [ ] Delete with confirmation works
- [ ] Optimistic UI updates
- [ ] All tests passing
- [ ] Full CRUD cycle working

---

## 📦 Deliverables

- PATCH and DELETE endpoints
- Edit project UI
- Delete confirmation dialog
- Zustand update/delete actions
- Backend and frontend tests

---

## 🔗 Dependencies

**Prerequisites:** Phase 2 complete  
**Blocks:** Phase 4

---

**Last Updated:** 2025-12-02  
**Status:** 🔴 Not Started


