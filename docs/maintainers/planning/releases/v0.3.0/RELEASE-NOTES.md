# Release Notes - v0.3.0

**Version:** v0.3.0  
**Release Date:** 2025-12-29  
**Status:** ✅ Published (GitHub Release)

---

## 🎉 Highlights

This release introduces the **Project Type Field** feature, enabling classification of projects by type (Work, Personal, Learning, Inactive). This is an additive, non-breaking change that enhances project organization and filtering capabilities.

**Key Benefits:**
- Filter projects by type via API
- Clear distinction between work-related and personal projects
- Track learning projects separately
- Archive inactive projects with proper classification

---

## ✨ New Features

### Project Type Field

Classify projects using the new `project_type` enum field.

**Valid Types:**
- `Work` - Professional/job-related projects
- `Personal` - Personal projects and hobbies
- `Learning` - Educational and skill-building projects
- `Inactive` - Archived or dormant projects

**API Filtering:**

```bash
# Filter by project type
curl "http://localhost:5000/api/projects?project_type=Work"

# Combine with other filters
curl "http://localhost:5000/api/projects?project_type=Work&status=active"

# Invalid type returns 400 error
curl "http://localhost:5000/api/projects?project_type=InvalidType"
# {"error": "Invalid project_type. Must be one of: Work, Personal, Learning, Inactive"}
```

**Response:**

All project responses now include the `project_type` field:

```json
{
  "id": 1,
  "name": "My Project",
  "project_type": "Work",
  "status": "active",
  ...
}
```

---

## 🔧 Improvements

- **OpenAPI Specification** - Updated to document `project_type` field and filtering
- **Test Coverage** - 14 new tests added, maintaining 97% coverage

---

## 📚 Documentation

- Complete feature documentation in `docs/maintainers/planning/features/project-type-field/`
- Manual testing guide with 5 API test scenarios
- Fix tracking for deferred Sourcery review items

---

## ⚠️ Breaking Changes

None in this release. The `project_type` field is additive and nullable.

---

## 🔄 Migration Guide

No migration required. Existing projects will have `project_type: null` until explicitly set or until the backfill script is run.

**Optional:** Run the backfill script to classify existing projects:

```bash
# Preview changes (dry-run)
python scripts/backfill_project_type.py

# Apply changes
python scripts/backfill_project_type.py --execute
```

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| PRs Merged | 3 |
| Tests Added | 14 |
| Test Coverage | 97% |
| Total Tests | 130 |

---

## 🔗 Related

- **proj-cli Integration:** The `proj-cli` project has a planned `project-type-support` feature to consume this new field.

---

**Full Changelog:** [v0.2.0...v0.3.0](https://github.com/grimm00/work-prod/compare/v0.2.0...v0.3.0)

---

**Last Updated:** 2025-12-29

