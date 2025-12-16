# Post Release Command

Handles post-release cleanup including merging main back to develop, cleaning up the release branch, and preparing for the next development cycle. Customize this command for your project's release workflow.

---

## Configuration

**Path Detection:**

- Releases: `docs/maintainers/planning/releases/[version]/`

**Version Format:** `vX.Y.Z` (e.g., `v0.2.0`)

---

## Workflow Overview

**When to use:**

- After release is merged to main
- After tag is created
- To clean up and prepare for next development cycle

**Workflow Position:**

```
/pr --release (merged)
         │
         ▼
   Tag created (vX.Y.Z)
         │
         ▼
   GitHub release published (optional)
         │
         ▼
┌─────────────────────────────────────┐
│   /post-release vX.Y.Z              │  ◄── This command
│                                     │
│   1. Merge main to develop          │
│   2. Clean up release branch        │
│   3. Update release docs (optional) │
│   4. Prepare for next cycle         │
└─────────────────────────────────────┘
         │
         ▼
   Ready for next development cycle
```

---

## Usage

**Command:** `/post-release [version] [options]`

**Examples:**

- `/post-release v0.2.0` - Full post-release workflow
- `/post-release v0.2.0 --dry-run` - Preview changes
- `/post-release v0.2.0 --keep-branch` - Don't delete release branch

**Options:**

- `--dry-run` - Show what would be done without executing
- `--keep-branch` - Keep release branch (don't delete)

---

## Step-by-Step Process

### 1. Validate Release Complete

**Verify release:**

```bash
# Check tag exists
git tag -l "vX.Y.Z"

# Check main has release changes
git log main --oneline -5
```

### 2. Merge Main to Develop

**Sync develop with main:**

```bash
git checkout develop
git pull origin develop
git merge origin/main --no-edit
git push origin develop
```

**Handle conflicts (if any):**

- Resolve in favor of main for release-specific changes
- Keep develop changes for ongoing work

### 3. Clean Up Release Branch

**Delete release branch:**

```bash
# Delete local
git branch -d release/vX.Y.Z

# Delete remote
git push origin --delete release/vX.Y.Z
```

### 4. Update Release Documentation (Optional)

**Mark release as published:**

```markdown
# In RELEASE-NOTES.md
**Status:** ✅ Published

# In RELEASE-READINESS.md (if exists)
**Status:** ✅ Released
```

### 5. Summary Report

```markdown
## ✅ Post-Release Complete

**Version:** vX.Y.Z

### Actions Completed

- [x] Main merged to develop
- [x] Release branch deleted
- [x] Release docs updated

### Next Steps

1. Start next development cycle
2. Plan v(X.Y+1).0 features
3. Create new feature branches from develop
```

---

## Customization

**This is a scaffold command.** Customize it for your project:

- Add release retrospective creation
- Add release announcement steps
- Add deployment verification
- Add metrics/analytics updates

---

**Last Updated:** 2025-12-16  
**Status:** 🟠 Scaffold - Customize for your project

