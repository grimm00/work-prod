# Projects Feature - Phase 2: Create Project

**Phase:** 2 - Create Project (Second Vertical Slice)  
**Duration:** 2 days  
**Status:** 🔴 Not Started  
**Prerequisites:** Phase 1 complete

---

## 📋 Overview

Phase 2 delivers the second complete vertical slice: creating new projects. This phase extends the Project model with core fields (organization, classification, status) and implements create functionality with validation on both client and server.

**Success Definition:** Can create a project via UI and see it appear in the project list.

---

## 🎯 Goals

1. **Extended Project Model** - Add organization, classification, status fields
2. **POST /api/projects Endpoint** - Create new project with validation
3. **ProjectForm Component** - Form for creating projects
4. **Validation** - Client-side and server-side validation
5. **Integration** - Created project appears in list immediately

---

## 📝 TDD Tasks

### 1. Write Backend Validation Tests
- [ ] Test required field validation (name required)
- [ ] Test field length limits (name max 200 chars)
- [ ] Test duplicate detection (unique path or remote_url)
- [ ] Test valid classification values
- [ ] Test valid status values

### 2. Extend Project Model
- [ ] Add fields: `organization` (String), `classification` (Enum), `status` (Enum)
- [ ] Add validation rules
- [ ] Create migration: `flask db migrate -m "Add organization, classification, status"`
- [ ] Update `to_dict()` method

### 3. Write API POST Test
- [ ] Test successful creation (201 Created)
- [ ] Test validation errors (400 Bad Request)
- [ ] Test duplicate handling (409 Conflict)
- [ ] Test response includes created project

### 4. Implement POST /api/projects Endpoint
- [ ] Validate request JSON
- [ ] Check for duplicates
- [ ] Create project record
- [ ] Return created project JSON

### 5. Write Frontend Form Test
- [ ] Test form rendering
- [ ] Test form validation
- [ ] Test submit handler
- [ ] Test success/error states

### 6. Implement ProjectForm Component
- [ ] Form fields: name, path, organization, classification, status
- [ ] Client-side validation
- [ ] Zustand action: `createProject()`
- [ ] Success message and redirect to list

### 7. Integration Test
- [ ] Fill form → submit → see in list
- [ ] Test validation errors display

### 8. Manual Testing
- [ ] Create project via UI
- [ ] Verify appears in list
- [ ] Test validation (empty name, etc.)

---

## ✅ Completion Criteria

- [ ] Project model has core fields
- [ ] POST endpoint validates and creates projects
- [ ] ProjectForm renders and submits
- [ ] Client and server validation working
- [ ] Created projects appear in list
- [ ] All tests passing

---

## 📦 Deliverables

- Extended Project model with migration
- POST /api/projects endpoint
- ProjectForm component
- Zustand createProject action
- Backend and frontend tests

---

## 🔗 Dependencies

**Prerequisites:** Phase 1 complete  
**Blocks:** Phase 3

---

**Last Updated:** 2025-12-02  
**Status:** 🔴 Not Started

