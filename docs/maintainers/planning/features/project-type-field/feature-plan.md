# Project Type Field - Feature Plan

**Feature:** Add `project_type` field  
**Status:** 🔴 Not Started  
**Created:** 2025-12-23  
**Last Updated:** 2025-12-23  
**Owner:** work-prod

---

## 📋 Overview

Add a new `project_type` enum field to the projects table to classify projects by type.

**Problem Statement:**

The current `classification` field uses values `primary`, `secondary`, `archive`, `maintenance` which represent **priority/importance**, not **project type**. Users need to answer "What kind of project is this?" (Work, Personal, Learning, Inactive) - a fundamentally different question.

Current data loss:
- Personal, Work, and Apprenti all map to `primary`
- 40 "primary" projects include Work, Personal, AND Learning mixed together
- Cannot filter by "show me all Work projects"

**Solution:**

Add `project_type` field with enum values: `Work`, `Personal`, `Learning`, `Inactive`

---

## 🎯 Success Criteria

- [ ] `project_type` field exists in database with proper enum values
- [ ] Existing 48 projects have `project_type` populated via backfill
- [ ] API supports filtering by `project_type` parameter
- [ ] OpenAPI spec updated with new field
- [ ] Mapping script populates `project_type` for new imports
- [ ] All tests pass

---

## 📅 Implementation Phases

### Phase 1: Schema Migration (~2 hours)

**Goal:** Add `project_type` column to database

**Tasks:**
- Create Flask-Migrate migration
- Add `project_type` enum column (nullable initially)
- Add index for filtering performance
- Run migration locally and verify

**Deliverables:**
- Migration file in `migrations/versions/`
- Updated `Project` model

---

### Phase 2: Data Backfill (~2 hours)

**Goal:** Populate `project_type` for existing projects

**Heuristics:**
- `organization = 'DRW'` → `project_type = 'Work'`
- `path LIKE '%/Learning/%'` → `project_type = 'Learning'`
- `classification = 'archive'` → `project_type = 'Inactive'`
- Remaining → `project_type = 'Personal'` (default assumption)

**Tasks:**
- Create backfill script
- Apply heuristics to 48 projects
- Validate results
- Document manual corrections needed

**Deliverables:**
- Backfill script in `scripts/`
- Backfill report showing results

---

### Phase 3: API Updates (~3 hours)

**Goal:** Enable API filtering and documentation

**Tasks:**
- Add `project_type` query parameter to GET `/projects`
- Update OpenAPI spec with new field and parameter
- Update `map_inventory_to_projects.py` to populate both fields
- Add/update tests for new functionality

**Deliverables:**
- API endpoint updated
- OpenAPI spec updated
- Mapping script updated
- Tests added

---

## 📋 Requirements Addressed

| Requirement | Description | Phase |
|-------------|-------------|-------|
| FR-2 | Project Type Classification | All |
| FR-2a | Project Type Field Addition | Phase 1 |
| FR-2b | Required for New Projects | Phase 3 |
| FR-2c | Mapping Script Update | Phase 3 |
| FR-2d | API Filtering | Phase 3 |
| FR-2e | Data Backfill | Phase 2 |
| NFR-2 | Migration Safety | Phase 1 |

---

## ⚠️ Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Heuristics incorrect | Wrong project types | Manual review, allow corrections |
| Migration fails | Database issues | Test locally first, backup before prod |
| API breaks clients | proj-cli issues | Additive change only, test with proj-cli |

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Transition Plan](transition-plan.md)
- [ADR-003: Add project_type Field](../../../../../dev-infra/admin/decisions/project-model-definition/adr-003-add-project-type-field.md)
- [Requirements](../../../../../dev-infra/admin/research/project-model-definition/requirements.md)

---

**Last Updated:** 2025-12-23

