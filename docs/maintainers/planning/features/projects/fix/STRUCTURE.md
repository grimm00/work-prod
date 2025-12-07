# Fix Directory Structure Proposal

**Status:** 🟡 Proposed  
**Date:** 2025-12-04

---

## Problem

Current fix directory has all files flat:
- 14+ files already
- Mix of individual issues and batches
- No organization by PR
- Will grow significantly with more phases
- Doesn't follow hub-and-spoke pattern

---

## Proposed Structure

```
fix/
├── README.md                    # 📍 HUB - Main fix tracking hub
├── pr01/                        # PR #1 fixes
│   ├── README.md                # PR #1 hub
│   ├── issue-01-logging-config.md
│   ├── issue-02-cors-security.md
│   └── issue-03-flask-env-deprecated.md
├── pr02/                        # PR #2 fixes
│   ├── README.md                # PR #2 hub
│   └── issue-03-cli-imports.md
├── pr12/                        # PR #12 fixes
│   ├── README.md                # PR #12 hub
│   ├── batch-medium-low-01.md
│   ├── batch-medium-medium-01.md
│   └── batch-low-low-01.md
└── archived/                    # Completed/old fixes
    ├── README.md                # Archive hub
    ├── pr01/                    # Archived PR #1 fixes
    │   └── (completed files)
    └── pr08/                    # Archived PR #8 fixes
        └── (completed files)
```

---

## Benefits

1. **Hub-and-Spoke Pattern:**
   - Main README.md links to PR directories
   - Each PR directory has its own README.md hub
   - Fix plans are spokes within PR directories

2. **Scalability:**
   - Easy to add new PRs (just create directory)
   - Each PR directory stays manageable
   - Archive old PRs when complete

3. **Organization:**
   - Clear separation by PR
   - Easy to find fixes for specific PR
   - Archive keeps active directory clean

4. **Git Management:**
   - Keep active fixes in git (planning artifacts)
   - Archive completed ones (still in git for reference)
   - Optionally gitignore very old archived (6+ months)

---

## Migration Plan

1. Create PR subdirectories (pr01/, pr02/, pr12/, etc.)
2. Move existing fix files to appropriate PR directories
3. Create README.md hub for each PR directory
4. Update main README.md with new structure
5. Update commands to use new paths

---

## Gitignore Strategy

**Option 1: Keep Everything in Git**
- All fix plans tracked
- Archive completed ones but keep in git
- Pros: Full history, easy reference
- Cons: More files in repo

**Option 2: Gitignore Old Archived**
- Keep active fixes in git
- Archive completed ones
- Gitignore archived files older than 6 months
- Pros: Cleaner repo, still have recent history
- Cons: Lose very old reference material

**Recommendation:** Option 1 (keep everything) - Fix plans are planning artifacts and should be tracked. Archive keeps active directory clean without losing history.

**Alternative:** Option 3 - Gitignore completed batches only (not individual issues)
- Keep individual issue fix plans in git (reference material)
- Gitignore completed batch files (they're implementation artifacts)
- Keep README.md tracking in git
- Pros: Reduces clutter, keeps important reference material
- Cons: Lose batch implementation details

**My Recommendation:** Keep everything in git but organize better. Fix plans are valuable planning artifacts that document decision-making process. The organization structure (by PR) will keep things manageable even with many files.

---

## Implementation

Would require:
1. Restructuring existing files
2. Updating `/fix-plan` command paths
3. Updating `/fix-implement` command paths
4. Updating `/fix-review` command paths
5. Updating main README.md

