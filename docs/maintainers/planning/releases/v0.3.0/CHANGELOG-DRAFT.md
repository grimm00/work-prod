# CHANGELOG Draft - v0.3.0

**Draft Created:** 2025-12-29  
**Status:** 📝 Draft - Needs Review

---

## [0.3.0] - 2025-12-29

### Added

- **Project Type Field** - New `project_type` enum for classifying projects (PR #40, #41, #42)
  - Valid types: `Work`, `Personal`, `Learning`, `Inactive`
  - Database column with index for filtering performance
  - API query parameter: `GET /api/projects?project_type=Work`
  - Invalid values return 400 error with clear message

- **Backfill Script** - One-time script to classify existing projects (`scripts/backfill_project_type.py`)
  - Heuristic-based classification
  - Dry-run mode by default
  - Detailed results reporting

- **Manual Testing Guide** - Test scenarios for project-type-field feature
  - 5 scenarios covering API filtering
  - Located in feature documentation

### Changed

- **Project Model** - Added `project_type` field to `to_dict()` output
- **OpenAPI Specification** - Updated with `project_type` field in all relevant schemas

### Documentation

- **Feature Hub** - Complete documentation for project-type-field feature
- **Phase Documents** - Detailed implementation plans for all 3 phases
- **Fix Tracking** - Deferred issues documented (10 issues across PRs #40-42)

---

## PRs Included

| PR | Title | Merged |
|----|-------|--------|
| #40 | feat: Add project_type enum field schema migration (Phase 1) | 2025-12-29 |
| #41 | feat: Data Backfill for project_type (Phase 2) | 2025-12-29 |
| #42 | feat: API Updates for project_type (Phase 3) | 2025-12-29 |

---

## Review Checklist

- [x] All PRs listed
- [x] Categorization correct
- [x] Descriptions accurate
- [ ] Breaking changes noted (if any) - None
- [ ] Ready to merge into CHANGELOG.md

---

**Last Updated:** 2025-12-29

