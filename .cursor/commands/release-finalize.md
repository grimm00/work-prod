# Release Finalize Command

Finalizes release preparation by merging CHANGELOG draft, completing release notes, and preparing for the release PR. Customize this command for your project's release workflow.

---

## Configuration

**Path Detection:**

- Releases: `docs/maintainers/planning/releases/[version]/`
- CHANGELOG: `CHANGELOG.md` (root)

**Version Format:** `vX.Y.Z` (e.g., `v0.2.0`)

---

## Workflow Overview

**When to use:**

- After `/release-prep` has generated draft documents
- After reviewing and approving draft content
- Before creating the release PR

**Workflow Position:**

```
/release-prep vX.Y.Z
         │
         ▼
   Review Drafts (manual)
         │
         ▼
┌─────────────────────────────────────┐
│   /release-finalize vX.Y.Z          │  ◄── This command
│                                     │
│   1. Merge CHANGELOG draft          │
│   2. Finalize release notes         │
│   3. Update version references      │
│   4. Commit to release branch       │
└─────────────────────────────────────┘
         │
         ▼
   /pr --release (create PR to main)
```

---

## Usage

**Command:** `/release-finalize [version] [options]`

**Examples:**

- `/release-finalize v0.2.0` - Full finalization
- `/release-finalize v0.2.0 --dry-run` - Preview changes
- `/release-finalize v0.2.0 --date 2025-12-20` - Set release date

**Options:**

- `--dry-run` - Show what would be done without executing
- `--date YYYY-MM-DD` - Set release date (default: today)

---

## Step-by-Step Process

### 1. Validate Prerequisites

**Required files:**

```
docs/maintainers/planning/releases/vX.Y.Z/CHANGELOG-DRAFT.md
docs/maintainers/planning/releases/vX.Y.Z/RELEASE-NOTES.md
CHANGELOG.md
```

### 2. Merge CHANGELOG Draft

**Process:**

1. Read `CHANGELOG-DRAFT.md`
2. Insert version section into `CHANGELOG.md` (after Unreleased or at top)
3. Set release date

**Example:**

```markdown
## [Unreleased]
...

## [0.2.0] - 2025-12-16    ◄── Inserted

### Added
- ...

## [0.1.0] - 2025-12-07    ◄── Existing
```

### 3. Finalize Release Notes

**Update `RELEASE-NOTES.md`:**

```markdown
# Before
**Release Date:** YYYY-MM-DD
**Status:** 🔴 Draft

# After
**Release Date:** 2025-12-16
**Status:** ✅ Final
```

### 4. Update Version References (Optional)

**Files to check:**

- `package.json` (if exists) - `"version": "X.Y.Z"`
- `pyproject.toml` (if exists) - `version = "X.Y.Z"`
- README badges
- Any hardcoded version strings

### 5. Commit Changes

```bash
git add CHANGELOG.md
git add docs/maintainers/planning/releases/vX.Y.Z/
git commit -m "docs(release): finalize vX.Y.Z release documents

- Merged CHANGELOG draft into CHANGELOG.md
- Finalized release notes
- Updated version references"
```

### 6. Summary Report

```markdown
## ✅ Release Finalization Complete

**Version:** vX.Y.Z
**Date:** YYYY-MM-DD

### Changes Made

- CHANGELOG merged
- Release notes finalized
- Version references updated

### Next Steps

1. Run `/pr --release` to create PR to main
2. Get review
3. Merge and tag
```

---

## Customization

**This is a scaffold command.** Customize it for your project:

- Add automated version bumping
- Add version reference scanning
- Add release validation steps
- Add CI/CD integration

---

**Last Updated:** 2025-12-16  
**Status:** 🟠 Scaffold - Customize for your project

