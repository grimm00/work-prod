# Project Type Field - Transition Plan

**Feature:** Add `project_type` field  
**Source ADR:** [ADR-003: Add project_type Field](../../../../../dev-infra/admin/decisions/project-model-definition/adr-003-add-project-type-field.md)  
**Status:** 🔴 Not Started  
**Created:** 2025-12-23  
**Last Updated:** 2025-12-23

---

## 📋 Transition Overview

This transition plan implements ADR-003 by adding a `project_type` field to the work-prod database to enable project type classification.

**Transition Type:** Feature (Schema Change)

**Key Changes:**
1. Add `project_type` enum column to `projects` table
2. Backfill existing projects using heuristics
3. Update API to support filtering by project type
4. Update mapping script to populate new field

---

## 🎯 Transition Goals

From ADR-003:
- Answer "What kind of project is this?" with Work, Personal, Learning, Inactive
- Enable filtering: "Show all Work projects", "Show all Personal projects"
- Support Tier 3 Learning taxonomy (depends on `project_type = 'Learning'`)
- Non-breaking change (additive)

---

## 📅 Transition Phases

| Phase | Name | Status | Effort | Dependencies |
|-------|------|--------|--------|--------------|
| 1 | Schema Migration | 🔴 Not Started | ~2 hours | None |
| 2 | Data Backfill | 🔴 Not Started | ~2 hours | Phase 1 |
| 3 | API Updates | 🔴 Not Started | ~3 hours | Phase 2 |

**Total Estimated Effort:** ~7 hours

---

## 📋 Phase Summaries

### Phase 1: Schema Migration

**Goal:** Add `project_type` column to database

**Key Tasks:**
1. Create Flask-Migrate migration for `project_type` enum
2. Add column as nullable initially (migration safety)
3. Add index for filtering performance
4. Verify migration works locally

**Schema Change:**
```python
project_type = db.Column(
    Enum('Work', 'Personal', 'Learning', 'Inactive', name='project_type_enum'),
    nullable=True,
    index=True
)
```

**Exit Criteria:**
- [ ] Migration file created
- [ ] Migration runs successfully locally
- [ ] Column exists in database
- [ ] Tests pass

---

### Phase 2: Data Backfill

**Goal:** Populate `project_type` for existing 48 projects

**Backfill Heuristics:**
- `organization = 'DRW'` → `Work`
- `path LIKE '%/Learning/%'` → `Learning`
- `classification = 'archive'` → `Inactive`
- Remaining → `Personal` (default)

**Key Tasks:**
1. Create backfill script with heuristics
2. Run backfill in dry-run mode first
3. Execute backfill
4. Validate results and document corrections

**Exit Criteria:**
- [ ] Backfill script created
- [ ] All 48 projects have `project_type` populated
- [ ] Results validated

---

### Phase 3: API Updates

**Goal:** Enable API filtering and update documentation

**Key Tasks:**
1. Add `project_type` query parameter to GET `/api/projects`
2. Update OpenAPI spec with field and parameter
3. Update mapping script to populate `project_type`
4. Add/update tests

**API Change:**
```
GET /api/projects?project_type=Work
GET /api/projects?project_type=Personal
GET /api/projects?project_type=Learning
```

**Exit Criteria:**
- [ ] API filtering works
- [ ] OpenAPI spec updated
- [ ] Mapping script updated
- [ ] Tests pass

---

## ⚠️ Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Migration fails | Test locally first, backup database |
| Heuristics incorrect | Review results, allow manual corrections |
| API breaks proj-cli | Additive change only, coordinate with proj-cli |

---

## 📊 Requirements Traceability

| Requirement | Satisfied By |
|-------------|--------------|
| FR-2: Project Type Classification | All phases |
| FR-2a: Field Addition | Phase 1 |
| FR-2b: Required for New Projects | Phase 3 |
| FR-2c: Mapping Script Update | Phase 3 |
| FR-2d: API Filtering | Phase 3 |
| FR-2e: Data Backfill | Phase 2 |
| NFR-2: Migration Safety | Phase 1 (nullable first) |

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Feature Plan](feature-plan.md)
- [Phase 1: Schema Migration](phase-1.md)
- [Phase 2: Data Backfill](phase-2.md)
- [Phase 3: API Updates](phase-3.md)
- [ADR-003](../../../../../dev-infra/admin/decisions/project-model-definition/adr-003-add-project-type-field.md)

---

**Last Updated:** 2025-12-23


