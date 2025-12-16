# Infrastructure Planning

**Purpose:** Track infrastructure improvements and migrations  
**Status:** ✅ Active  
**Last Updated:** 2025-12-16

---

## 📋 Quick Links

### Active Improvements

- **[Inventory Repository Separation](inventory-repository-separation/README.md)** - Separate inventory POC to standalone repo (✅ Planned)
- **[SQLAlchemy 2.0 Migration](sqlalchemy-migration/improvement-plan.md)** - Migrate to SQLAlchemy 2.0 patterns (🔴 Not Started)

### Checklists

- **[Public Repo Checklist](public-repo-checklist.md)** - Public repository preparation (✅ Complete)

---

## 📊 Summary

| Improvement | Priority | Status | Effort |
|-------------|----------|--------|--------|
| Inventory Repository Separation | Medium | ✅ Planned | High |
| SQLAlchemy 2.0 Migration | Low | 🔴 Not Started | Medium |
| Public Repo Checklist | High | ✅ Complete | Low |

---

## 🎯 Current Focus

### SQLAlchemy 2.0 Migration

**Status:** 🔴 Not Started  
**Priority:** Low  
**Source:** reflection-work-prod-integration-2025-12-16.md

Migrate from `Query.get()` to `Session.get()` pattern to eliminate deprecation warnings and prepare for SQLAlchemy 2.x upgrade.

**Plan:** [sqlalchemy-migration/improvement-plan.md](sqlalchemy-migration/improvement-plan.md)

---

## 📅 Timeline

| Phase | Status | Target |
|-------|--------|--------|
| Public Repo Prep | ✅ Complete | Done |
| Inventory Separation | ✅ Planned | When prioritized |
| SQLAlchemy Migration | 🔴 Not Started | When prioritized |

---

## 🔗 Related

- **Reflections:** `docs/maintainers/planning/notes/reflections/`
- **Release Process:** `docs/maintainers/planning/releases/PROCESS.md`
- **Backend Rules:** `.cursor/rules/backend.mdc`

---

**Last Updated:** 2025-12-16  
**Status:** ✅ Active

