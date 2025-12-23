# Release Checklist - v0.2.0

**Version:** v0.2.0  
**Status:** 🔴 Not Started  
**Created:** 2025-12-23  
**Type:** Minor Release (Architectural Change)

---

## Pre-Release

### Code Quality

- [ ] All tests passing
- [ ] Test coverage maintained (97% from v0.1.0)
- [ ] 0 linting errors maintained
- [ ] All HIGH priority issues addressed
- [ ] Critical bugs fixed

### Documentation

- [ ] Documentation reviewed and accurate
- [ ] README updated to point to proj-cli
- [ ] scripts/README.md redirects to proj-cli
- [ ] All CLI references updated

### Migration Verification

- [ ] proj-cli v0.1.0 released and functional
- [ ] proj-cli can connect to work-prod API
- [ ] All previous CLI commands available in proj-cli
- [ ] Inventory commands available in proj-cli

### Release Preparation

- [x] Release directory structure created ✅
- [x] Release checklist complete (this file)
- [ ] Release notes prepared
- [ ] Version number determined (v0.2.0)
- [ ] CHANGELOG updated

---

## Release

### Version Management

- [ ] Version tagged in git (`git tag v0.2.0`)
- [ ] Tag pushed to remote (`git push origin v0.2.0`)
- [ ] Version number updated in documentation

### Release Documentation

- [ ] Release notes finalized
- [ ] CHANGELOG merged
- [ ] Documentation updated with version number

### Release Artifacts

- [ ] Release notes published
- [ ] Documentation links verified

---

## Post-Release

### Git Cleanup

- [ ] Main merged to develop
- [ ] Release branch deleted (local)
- [ ] Release branch deleted (remote)

### Communication

- [ ] Release notes published
- [ ] Note about proj-cli migration included

### Follow-up

- [ ] Post-release monitoring active
- [ ] Issues tracked (if any)
- [ ] Next release planned

---

## Release Summary

**Version:** v0.2.0 - API-Only Architecture  
**Target Date:** 2025-12-23  
**Status:** 🔴 Draft

**Key Changes:**
- Removed CLI tool (migrated to proj-cli)
- Removed inventory scripts (migrated to proj-cli)
- work-prod is now API-only

**Related:**
- Source: proj-cli feature (ADR-0007)
- PRs: #38 (cleanup)
- Replacement: proj-cli v0.1.0

---

**Last Updated:** 2025-12-23


