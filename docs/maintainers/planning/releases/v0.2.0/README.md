# Release v0.2.0 - API-Only Architecture

**Version:** v0.2.0  
**Status:** 🔴 Draft  
**Target Date:** 2025-12-23  
**Created:** 2025-12-23  
**Source:** proj-cli feature development (PR #38)  
**Type:** Minor Release (Architectural Change)

---

## 📋 Quick Links

- **[Release Checklist](checklist.md)** - Release preparation checklist
- **[Release Notes](release-notes.md)** - Release notes and changelog
- **[CHANGELOG Draft](CHANGELOG-DRAFT.md)** - CHANGELOG draft for review
- **[Transition Plan](transition-plan.md)** - API-only transition planning

---

## 📊 Release Summary

**Version:** v0.2.0 - API-Only Architecture  
**Target Date:** 2025-12-23  
**Status:** 🔴 Draft

**Key Changes:**
- **Removed:** CLI tool (`scripts/project_cli/`) - Now in separate proj-cli repo
- **Removed:** Inventory scripts (`scripts/inventory/`) - Now in proj-cli
- **Changed:** work-prod is now API-only; use proj-cli for CLI functionality
- **Added:** Command usage tracking documentation

**Development:**
- PRs: 1 (PR #38 - cleanup)
- Related Release: proj-cli v0.1.0 (replacement CLI)
- Breaking: Yes (CLI removed, but replacement available)

---

## ✅ Release Checklist Status

**Pre-Release:**
- [ ] All tests passing
- [ ] Coverage maintained (97%)
- [ ] 0 linting errors maintained
- [ ] Documentation reviewed
- [ ] Release checklist complete
- [ ] Release notes prepared
- [ ] CHANGELOG updated

**Release:**
- [ ] Version tagged in git
- [ ] Release notes finalized
- [ ] Documentation updated with version

**Post-Release:**
- [ ] Main merged to develop
- [ ] Release branch cleaned up
- [ ] Release docs updated

---

## 🔗 Related

- **Release Checklist:** [checklist.md](checklist.md)
- **Release Notes:** [release-notes.md](release-notes.md)
- **Transition Plan:** [transition-plan.md](transition-plan.md)
- **CHANGELOG Draft:** [CHANGELOG-DRAFT.md](CHANGELOG-DRAFT.md)
- **proj-cli Feature:** `docs/maintainers/planning/features/proj-cli/`
- **proj-cli v0.1.0:** https://github.com/grimm00/proj-cli/releases/tag/v0.1.0

---

**Last Updated:** 2025-12-23


