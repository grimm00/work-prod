# Projects Feature - Phase 4: Import Projects

**Phase:** 4 - Import Existing Projects  
**Duration:** 2 days  
**Status:** 🔴 Not Started  
**Prerequisites:** Phase 3 complete

---

## 📋 Overview

Phase 4 imports all 59 existing projects from the inventory POC. This phase extends the Project model to its full schema and implements bulk import with duplicate detection and validation.

**Success Definition:** All 59 projects imported successfully and visible in the UI.

---

## 🎯 Goals

1. **Full Project Model Schema** - Add all remaining fields
2. **POST /api/projects/import** - Bulk import endpoint
3. **Import UI** - JSON paste or file upload interface
4. **Duplicate Detection** - By remote_url or path
5. **Import Summary** - Show success/failure results

---

## 📝 TDD Tasks

### Extend Model to Full Schema

- [ ] Add fields: `remote_url`, `description`, `tech_stack` (JSON), `learning_type`
- [ ] Create `projects_skills` junction table
- [ ] Migration: `flask db migrate -m "Add full project schema"`

### Bulk Import Endpoint

- [ ] Write import endpoint tests
  - Test valid JSON array import
  - Test duplicate detection
  - Test validation errors
  - Test transaction rollback on error
- [ ] Implement POST /api/projects/import
  - Accept JSON array
  - Validate each project
  - Detect duplicates (skip or update)
  - Bulk insert with transaction
  - Return summary: `{imported: N, skipped: M, errors: [...]}`

### Import UI

- [ ] Write import UI tests
- [ ] Create ImportProjects component
  - JSON paste textarea
  - File upload option
  - Progress indicator
  - Results display (imported/skipped/errors)
- [ ] Add import button to projects list

### Data Mapping

- [ ] Map classifications.json to new schema
- [ ] Set learning_type for Learning projects
- [ ] Handle missing fields gracefully

### Manual Testing

- [ ] Import 59 projects from inventory POC
- [ ] Verify all appear in UI
- [ ] Verify duplicate detection works
- [ ] Test error handling

---

## ✅ Completion Criteria

- [ ] Full Project model schema complete
- [ ] Import endpoint validates and imports
- [ ] All 59 projects imported successfully
- [ ] Import UI shows clear results
- [ ] Duplicate detection working
- [ ] All tests passing

---

## 📦 Deliverables

- Full Project model with all fields
- POST /api/projects/import endpoint
- ImportProjects component
- Import results summary UI
- 59 projects in database
- Backend and frontend tests

---

## 🔗 Dependencies

**Prerequisites:** Phase 3 complete  
**Blocks:** Phase 5  
**Data Source:** `scripts/inventory/data/classifications.json`

---

**Last Updated:** 2025-12-02  
**Status:** 🔴 Not Started

