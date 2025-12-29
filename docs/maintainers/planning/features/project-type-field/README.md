# Project Type Field - Feature Hub

**Purpose:** Add `project_type` field for project type classification  
**Status:** 🟠 In Progress  
**Created:** 2025-12-23  
**Last Updated:** 2025-12-23  
**Owner:** work-prod

---

## 📋 Quick Links

- **[Feature Plan](feature-plan.md)** - Feature overview and goals
- **[Transition Plan](transition-plan.md)** - Implementation transition plan
- **[Phase 1: Schema Migration](phase-1.md)** - Database schema changes (✅ Complete - PR #40)
- **[Phase 1 Review](phase-1-review.md)** - Pre-implementation readiness review
- **[Phase 2: Data Backfill](phase-2.md)** - Backfill existing data
- **[Phase 3: API Updates](phase-3.md)** - API and documentation updates

### Related ADRs (dev-infra)

- **[ADR-001: Tier 1 API Validation](../../../../../dev-infra/admin/decisions/project-model-definition/adr-001-tier-1-api-validation.md)** - API readiness confirmed
- **[ADR-003: Add project_type Field](../../../../../dev-infra/admin/decisions/project-model-definition/adr-003-add-project-type-field.md)** - Decision to add field

### Related Requirements

- **[Requirements Document](../../../../../dev-infra/admin/research/project-model-definition/requirements.md)** - FR-2, FR-2a through FR-2e

---

## 🎯 Feature Overview

Add a new `project_type` enum field to classify projects by type: `Work`, `Personal`, `Learning`, `Inactive`.

**Problem:** Current `classification` field represents priority, not type. Cannot answer "What kind of project is this?"

**Solution:** Add `project_type` field (additive, non-breaking change).

---

## 📊 Feature Status

| Phase | Name | Status | Effort |
|-------|------|--------|--------|
| Phase 1 | Schema Migration | ✅ Complete | ~2 hours |
| Phase 2 | Data Backfill | 🔴 Not Started | ~2 hours |
| Phase 3 | API Updates | 🔴 Not Started | ~3 hours |

**Total Estimated Effort:** ~7 hours

---

## 🏢 Ownership

| Arm | Role | Responsibilities |
|-----|------|------------------|
| **work-prod** | Schema Owner | Implements field, migration, API filtering |
| **proj-cli** | Consumer | Updates client to support project_type parameter |

---

## 🚀 Next Steps

1. ~~Review feature plan and transition plan~~ ✅
2. ~~Pre-phase review for Phase 1~~ ✅
3. ~~Phase 1: Schema Migration~~ ✅ (PR #40, 2025-12-29)
4. Begin Phase 2: Data Backfill with `/task-phase 2`

---

## 📝 Completed Milestones

- **Phase 1: Schema Migration** ✅ (PR #40, 2025-12-29)
  - Added `project_type` enum column to Project model
  - Created Flask-Migrate migration
  - Added index for filtering performance
  - Unit tests added (4 tests)
  - 126 tests passing, 97% coverage

---

**Last Updated:** 2025-12-29  
**Phase 1 Complete:** 2025-12-29 (PR #40)
