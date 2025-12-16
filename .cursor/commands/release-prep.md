# Release Prep Command

Orchestrates release preparation by creating documentation drafts and optionally creating the release branch. Customize this command for your project's release workflow.

---

## Configuration

**Path Detection:**

- Releases: `docs/maintainers/planning/releases/[version]/`
- CHANGELOG: `CHANGELOG.md` (root)

**Version Format:** `vX.Y.Z` (e.g., `v0.2.0`)

---

## Workflow Overview

**When to use:**

- When starting release preparation
- After feature development is complete
- To generate all release documentation

**Workflow Position:**

```
Feature Development Complete
         │
         ▼
┌─────────────────────────────────────┐
│   /release-prep vX.Y.Z              │  ◄── This command
│                                     │
│   1. Create release directory       │
│   2. Run readiness check (optional) │
│   3. Create CHANGELOG draft         │
│   4. Create release notes draft     │
│   5. Create release branch (opt)    │
└─────────────────────────────────────┘
         │
         ▼
   Manual review of drafts
         │
         ▼
   /release-finalize vX.Y.Z
```

---

## Usage

**Command:** `/release-prep [version] [options]`

**Examples:**

- `/release-prep v0.2.0` - Full release preparation
- `/release-prep v0.2.0 --dry-run` - Show what would be done
- `/release-prep v0.2.0 --skip-branch` - Prepare but don't create branch

**Options:**

- `--dry-run` - Show what would be done without executing
- `--skip-branch` - Skip release branch creation
- `--force` - Continue despite warnings

---

## Step-by-Step Process

### 1. Create Release Directory

```bash
mkdir -p docs/maintainers/planning/releases/vX.Y.Z/
```

### 2. Run Readiness Check (Optional)

**Manual checklist:**

- [ ] All tests passing
- [ ] No blocking issues
- [ ] Critical bugs fixed
- [ ] Documentation complete

### 3. Create CHANGELOG Draft

**File:** `docs/maintainers/planning/releases/vX.Y.Z/CHANGELOG-DRAFT.md`

**Gather changes:**

```bash
# Get commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Get merged PRs
gh pr list --state merged --limit 50 --json number,title,mergedAt
```

**Template:**

```markdown
# CHANGELOG Draft - vX.Y.Z

**Draft Created:** YYYY-MM-DD  
**Status:** 🔴 Draft - Needs Review

---

## [X.Y.Z] - YYYY-MM-DD

### Added

- **[Feature]** - Description (PR #XX)

### Changed

- **[Change]** - Description (PR #XX)

### Fixed

- **[Fix]** - Description (PR #XX)

---

## Review Checklist

- [ ] All PRs listed
- [ ] Categorization correct
- [ ] Ready to merge into CHANGELOG.md
```

### 4. Create Release Notes Draft

**File:** `docs/maintainers/planning/releases/vX.Y.Z/RELEASE-NOTES.md`

**Template:**

```markdown
# Release Notes - vX.Y.Z

**Version:** vX.Y.Z  
**Release Date:** YYYY-MM-DD  
**Status:** 🔴 Draft - Needs Review

---

## 🎉 Highlights

[Executive summary of key features]

---

## ✨ New Features

### [Feature Name]

[Description]

---

## 🔧 Improvements

- [Improvement]

---

## 🐛 Bug Fixes

- [Fix] (PR #XX)

---

## ⚠️ Breaking Changes

None in this release.

---

**Full Changelog:** [vPREV...vX.Y.Z](compare-link)
```

### 5. Create Release Branch (Optional)

```bash
git checkout develop
git pull origin develop
git checkout -b release/vX.Y.Z

git add docs/maintainers/planning/releases/vX.Y.Z/
git commit -m "docs(release): initialize vX.Y.Z release preparation"
```

### 6. Summary Report

```markdown
## ✅ Release Preparation Complete

**Version:** vX.Y.Z

### Documents Created

- CHANGELOG-DRAFT.md
- RELEASE-NOTES.md

### Next Steps

1. Review drafts
2. Run `/release-finalize vX.Y.Z`
3. Create release PR
```

---

## Customization

**This is a scaffold command.** Customize it for your project:

- Add project-specific readiness checks
- Add automated version bumping
- Add changelog generation from commits
- Add release scripts

---

**Last Updated:** 2025-12-16  
**Status:** 🟠 Scaffold - Customize for your project

