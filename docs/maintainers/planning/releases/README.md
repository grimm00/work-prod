# Release Management

**Purpose:** Track and manage project releases  
**Status:** ✅ Active  
**Last Updated:** 2025-12-07

---

## 📋 Quick Links

### Process

- **[Release Process](PROCESS.md)** - Standard release workflow and documentation

### Releases

- **[v0.2.0](v0.2.0/README.md)** - API-Only Architecture (🟡 Ready for Release)
- **[v0.1.0](v0.1.0/README.md)** - MVP Release (✅ Released 2025-12-07)

---

## 📊 Summary

**Total Releases:** 1 released, 1 ready  
**Latest Release:** v0.1.0 (MVP) - Released 2025-12-07  
**Next Release:** v0.2.0 (API-Only) - Ready for release  
**Status:** 🟡 v0.2.0 ready for release

---

## 🎯 Release Process

### Release Lifecycle

1. **Planning** - Create release directory with checklist
2. **Preparation** - Complete checklist items
3. **Release** - Deploy and document
4. **Post-Release** - Update history and roadmap

### Release Checklist

Each release includes:
- `checklist.md` - Release preparation checklist
- `release-notes.md` - Release notes and changelog

---

## 📅 Release Timeline

| Version | Status | Release Date | Type | Description |
|---------|--------|--------------|------|-------------|
| v0.2.0 | 🟡 Ready | 2025-12-23 | Minor | API-Only Architecture |
| v0.1.0 | ✅ Released | 2025-12-07 | MVP | Backend MVP Release |

---

## 🚀 Upcoming Releases

### v0.2.0 - API-Only Architecture

**Status:** 🟡 Ready for Release  
**Release Date:** 2025-12-23  
**Created:** 2025-12-23  
**Source:** proj-cli feature (ADR-0007, PR #38)

**Key Changes:**
- CLI removed (migrated to proj-cli)
- Inventory scripts removed (migrated to proj-cli)
- work-prod is now API-only
- Documentation updated

**Checklist:** [v0.2.0/checklist.md](v0.2.0/checklist.md)  
**Release Notes:** [v0.2.0/release-notes.md](v0.2.0/release-notes.md)  
**Transition Plan:** [v0.2.0/transition-plan.md](v0.2.0/transition-plan.md)

---

## 📝 Release History

### v0.1.0 - MVP Release (2025-12-07)

**Status:** ✅ Released  
**PR:** #37  
**Type:** MVP Release

**Key Features:**
- Full CRUD API
- Search and filter
- Bulk import
- CLI tool
- Production ready
- 97% test coverage

**Release Notes:** [v0.1.0/release-notes.md](v0.1.0/release-notes.md)

---

## 🔗 Related

- **Feature Status:** `docs/maintainers/planning/features/projects/status-and-next-steps.md`
- **Reflection:** `docs/maintainers/planning/notes/reflections/reflection-2025-12-07-mvp-complete.md`
- **Production Guide:** `backend/PRODUCTION.md`
- **Deployment Guide:** `backend/DEPLOYMENT.md`

---

**Last Updated:** 2025-12-23  
**Next Release:** v0.2.0 (API-Only Architecture) - In preparation

