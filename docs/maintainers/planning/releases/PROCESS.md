# Release Process Documentation

**Purpose:** Standardized release process for work-prod  
**Status:** ✅ Active  
**Created:** 2025-12-16  
**Source:** reflection-work-prod-integration-2025-12-16.md

---

## 📋 Quick Links

- **[Releases Hub](README.md)** - All releases overview
- **[v0.1.0 Release](v0.1.0/README.md)** - MVP Release (2025-12-07)

---

## Overview

This document describes the standard release process for work-prod. It follows Git Flow conventions and integrates with the Cursor command system.

---

## Release Types

### Major Release (vX.0.0)

**When:** Breaking changes, major new features, or significant architectural changes.

**Process:**
1. Full `/release-prep` workflow
2. Transition plan required
3. Full testing cycle
4. Comprehensive release notes
5. User migration guide (if needed)

### Minor Release (vX.Y.0)

**When:** New features, non-breaking improvements, or significant enhancements.

**Process:**
1. Standard `/release-prep` workflow
2. Transition plan optional
3. Standard testing cycle
4. Detailed release notes

### Patch Release (vX.Y.Z)

**When:** Bug fixes, security patches, or minor improvements.

**Process:**
1. `/release-prep --skip-transition` workflow
2. No transition plan needed
3. Focused testing on fixes
4. Brief release notes

---

## Release Workflow

### Phase 1: Preparation

**Commands:** `/release-prep vX.Y.Z`

1. **Create Release Branch:**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b release/vX.Y.Z
   ```

2. **Create Release Directory:**
   ```
   docs/maintainers/planning/releases/vX.Y.Z/
   ├── README.md          # Release hub
   ├── checklist.md       # Pre-release checklist
   ├── release-notes.md   # Release notes draft
   └── transition-plan.md # Migration plan (if needed)
   ```

3. **Update Version References:**
   - `CHANGELOG.md` - Add release entry
   - `backend/openapi.yaml` - Update version
   - Documentation version references

4. **Run Pre-Release Checks:**
   - All tests passing
   - Test coverage > 80%
   - Linting clean
   - Documentation reviewed

### Phase 2: Finalization

**Commands:** `/release-finalize vX.Y.Z`

1. **Finalize Release Notes:**
   - Review and polish release notes
   - Add any late additions
   - Verify changelog accuracy

2. **Complete Checklist:**
   - All checklist items verified
   - No outstanding blockers
   - Ready for merge

3. **Merge to Main:**
   ```bash
   git checkout main
   git pull origin main
   git merge release/vX.Y.Z --no-ff -m "chore: Release vX.Y.Z"
   git push origin main
   ```

4. **Tag Release:**
   ```bash
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git push origin vX.Y.Z
   ```

5. **Create GitHub Release:**
   ```bash
   gh release create vX.Y.Z --title "vX.Y.Z" --notes-file docs/maintainers/planning/releases/vX.Y.Z/release-notes.md
   ```

### Phase 3: Post-Release

**Commands:** `/post-release vX.Y.Z`

1. **Merge Back to Develop:**
   ```bash
   git checkout develop
   git pull origin develop
   git merge main --no-ff -m "chore: Merge vX.Y.Z release back to develop"
   git push origin develop
   ```

2. **Clean Up:**
   - Delete release branch
   - Archive release documentation
   - Update status documents

3. **Update Documentation:**
   - Update releases hub with completion status
   - Archive release directory if desired
   - Update project README with new version

---

## Pre-Release Checklist

### Code Quality

- [ ] All tests passing (backend + CLI)
- [ ] Test coverage > 80% (target: >90%)
- [ ] Linting clean (flake8, no errors)
- [ ] No CRITICAL or HIGH priority bugs
- [ ] SQLAlchemy deprecation warnings acceptable

### Documentation

- [ ] CHANGELOG.md updated
- [ ] Release notes complete
- [ ] README.md current
- [ ] API documentation current (OpenAPI spec)

### Deployment

- [ ] Production configuration verified
- [ ] Deployment guide current
- [ ] Startup scripts working
- [ ] Environment variables documented

### Testing

- [ ] Manual testing scenarios passed
- [ ] Edge case tests passing
- [ ] Performance tests acceptable
- [ ] Integration tests passing

---

## Release Notes Format

```markdown
# Release Notes - vX.Y.Z

**Release Date:** YYYY-MM-DD  
**Status:** Stable

---

## What's New

- Feature 1
- Feature 2

## Improvements

- Improvement 1
- Improvement 2

## Bug Fixes

- Fix 1
- Fix 2

## Breaking Changes

- None (or list changes)

## Upgrade Notes

- Any special instructions for upgrading
```

---

## Changelog Format

```markdown
## [vX.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing features

### Fixed
- Bug fixes

### Deprecated
- Features that will be removed

### Removed
- Removed features

### Security
- Security fixes
```

---

## Troubleshooting

### Merge Conflicts

1. Resolve conflicts locally
2. Re-run tests after resolution
3. Document any non-obvious resolutions

### Failed Tests

1. Investigate and fix before release
2. If hotfix needed, apply to release branch
3. Re-run full test suite

### Version Mismatch

1. Verify version in all locations
2. Update any missed references
3. Re-tag if needed

---

## Related Commands

- `/release-prep` - Prepare release artifacts
- `/release-finalize` - Complete release process
- `/post-release` - Post-release cleanup
- `/reflect` - Create release reflection

---

**Last Updated:** 2025-12-16  
**Status:** ✅ Active

