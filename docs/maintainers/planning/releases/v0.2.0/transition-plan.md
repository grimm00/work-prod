# Transition Plan - v0.2.0

**Version:** v0.2.0 - API-Only Architecture  
**Status:** 🔴 Draft  
**Created:** 2025-12-23

---

## 📋 Overview

This release transitions work-prod from a full-stack application (API + CLI) to an API-only backend. CLI functionality has been migrated to the separate proj-cli repository.

**Transition Type:** Architectural Decoupling

---

## 🎯 Goals

1. **Clean Architecture:** Separate API backend from CLI frontend
2. **Independent Evolution:** Allow CLI and API to version separately
3. **User Continuity:** Ensure users have replacement CLI available
4. **Zero Downtime:** API functionality unchanged

---

## 📝 Pre-Release Tasks

- [x] proj-cli repository created
- [x] proj-cli v0.1.0 released with all commands
- [x] work-prod CLI removed (PR #38)
- [x] work-prod README updated
- [ ] Verify proj-cli works with work-prod API
- [ ] Release checklist completed
- [ ] Release notes finalized

---

## 🚀 Release Tasks

- [ ] Create release branch
- [ ] Final documentation review
- [ ] Tag v0.2.0
- [ ] Push tag to remote
- [ ] Create GitHub release
- [ ] Update CHANGELOG.md

---

## 📦 Post-Release Tasks

- [ ] Merge main to develop
- [ ] Delete release branch
- [ ] Update release documentation status
- [ ] Announce migration path (if applicable)

---

## ⚠️ Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Users don't know about proj-cli | Medium | README clearly documents migration |
| proj-cli has bugs | Medium | proj-cli v0.1.0 tested and released |
| API breaks | Low | No API changes in this release |
| Documentation gaps | Low | Comprehensive release notes |

---

## 📊 Verification Checklist

### Before Release

- [ ] `proj list` works against work-prod API
- [ ] `proj get 1` returns project details
- [ ] `proj inv scan github` works
- [ ] `proj inv export api` exports to work-prod
- [ ] All 15 commands verified functional

### After Release

- [ ] README links work
- [ ] proj-cli installation instructions work
- [ ] No broken references in documentation

---

## 🔗 Related

- **proj-cli v0.1.0:** https://github.com/grimm00/proj-cli/releases/tag/v0.1.0
- **ADR-0007:** `docs/maintainers/decisions/ADR-0007-inventory-system-cli-tool-architecture.md`
- **PR #38:** Remove CLI and inventory scripts

---

**Last Updated:** 2025-12-23



