# Projects Feature - Fix Tracking

**Purpose:** Track fixes identified through code review (Sourcery, manual review, etc.)  
**Status:** ✅ Active  
**Last Updated:** 2025-12-05  
**Progress:** 17/23 complete (74%) - Quick Wins batch complete via PR #14, PR02-#3 fixed via PR #15

**Note:** This directory uses hub-and-spoke organization by PR number. Completed PRs are archived to `archived/` directory.

---

## 📋 Quick Links

### Active PRs

- **[PR #2](pr02/README.md)** - Phase 1: List & Get Projects (🟡 Partial - 4 MEDIUM issues planned)
- **[PR #12](pr12/README.md)** - Phase 4: Search & Filter Projects (🟡 Partial - 2/3 batches complete via PR #13, #19)
- **[PR #16](pr16/README.md)** - Phase 5: Import Projects from JSON (✅ Complete - 1 HIGH fixed, 11 deferred)
- **[PR #18](pr18/README.md)** - CLI table display improvements (✅ Complete - 2 issues fixed, 2 deferred)
- **[PR #19](pr19/README.md)** - Fix Batch: pr12-batch-medium-low-01 (✅ Complete - 1 issue fixed, 1 deferred)
- **[PR #20](pr20/README.md)** - Fix Batch: test-quality-medium-low-01 (✅ Complete - 9 issues fixed, 5 deferred)
- **[PR #21](pr21/README.md)** - Fix Batch: quick-wins-low-low-02 (✅ Complete - 7 issues fixed, 0 deferred)
- **[PR #22](pr22/README.md)** - Fix Batch: code-refactoring-medium-medium-01 (✅ Complete - 2 issues fixed, 6 deferred)
- **[PR #24](pr24/README.md)** - Phase 6: CLI Enhancement & Daily Use Tools (✅ Complete - All tasks complete, 16 deferred)

### User-Reported Issues

- **[CLI Table Display Issue](user-reported-01-cli-table-display.md)** - Table columns truncate, missing `--wide` flag (✅ Complete - 2025-12-05, PR #18)

### Cross-PR Batches

- **[Cross-PR Batches](cross-pr/README.md)** - Batches from fix-review reports (2 complete, 2 active, 18 issues)
  - ✅ **Quick Wins Batch 1** (PR #14) - 7 LOW/LOW issues fixed
  - ✅ **Test Quality Improvements Batch** (PR #20) - 9 issues fixed (5 MEDIUM/LOW + 4 LOW/MEDIUM)
  - ✅ **Quick Wins Batch 2** (PR #21) - 7 issues fixed (5 LOW/LOW + 2 MEDIUM/LOW)
  - ✅ **Code Refactoring Batch** (PR #22) - 2 MEDIUM/MEDIUM issues fixed

### Archived PRs

- **[Archived](archived/README.md)** - Completed PRs (PR #1, #4, #8)

---

## 📊 Overview

This directory tracks fixes identified through code review processes including:
- Sourcery AI code review
- Manual code review
- Security audits
- Performance analysis

**Organization:** Fix plans are organized by PR number in subdirectories. Each PR directory has its own README.md hub linking to fix plan files (spokes).

---

## 📁 Directory Structure

```
fix/
├── README.md                    # 📍 HUB - This file
├── pr02/                        # PR #2 fixes
│   ├── README.md                # PR #2 hub
│   └── issue-*.md               # Individual fix plans
├── pr12/                        # PR #12 fixes
│   ├── README.md                # PR #12 hub
│   └── batch-*.md               # Fix batch plans
├── cross-pr/                    # Cross-PR batches
│   ├── README.md                # Cross-PR hub
│   └── *.md                     # Batch fix plans
└── archived/                    # Completed PRs
    ├── README.md                # Archive hub
    ├── pr01/                    # Archived PR #1
    ├── pr04/                    # Archived PR #4
    └── pr08/                    # Archived PR #8
```

---

## 🔧 Fix Branch Strategy

### For Multiple Related Fixes

- Create `fix/pr##-sourcery-issues` branch from develop
- Implement all CRITICAL and HIGH priority fixes
- Create single PR with all fixes
- Group by priority in commit messages

**Example:**
```bash
git checkout develop
git pull
git checkout -b fix/pr12-medium-low-batch-01
# Implement fixes from pr12/batch-medium-low-01.md
git commit -m "fix(cli): use click.Choice for validation (PR12-#1, #2)"
```

### For Individual Urgent Fixes

- Create `fix/issue-[number]-[short-name]` branch
- Implement single fix
- Fast-track PR if CRITICAL

---

## 📝 Current Status

### Active PRs

#### PR #2 (Phase 1)
- **Status:** 🟡 Partial
- **Issues:** 1 HIGH priority issue not fixed
- **Hub:** [pr02/README.md](pr02/README.md)

#### PR #12 (Phase 4)
- **Status:** 🟡 Partial
- **Batches:** 2/3 batches complete via PR #13, #19
- **Hub:** [pr12/README.md](pr12/README.md)

### Cross-PR Batches

#### Quick Wins Batch
- **Status:** 🔴 Not Started
- **Issues:** 7 LOW/LOW issues
- **Hub:** [cross-pr/README.md](cross-pr/README.md)

#### Test Quality Batch
- **Status:** 🔴 Not Started
- **Issues:** 4 MEDIUM/LOW issues
- **Hub:** [cross-pr/README.md](cross-pr/README.md)

### Archived PRs

#### PR #1 (Phase 0)
- **Status:** ✅ Complete (3/5 issues fixed)
- **Hub:** [archived/pr01/README.md](archived/pr01/README.md)

#### PR #4 (Config Fixes)
- **Status:** ✅ Complete (All issues fixed)
- **Hub:** [archived/pr04/README.md](archived/pr04/README.md)

#### PR #8 (Phase 2)
- **Status:** ✅ Critical Issues Fixed (2/6 fixed)
- **Hub:** [archived/pr08/README.md](archived/pr08/README.md)

---

## 📈 Summary Statistics

**Total Issues:** 25 across 7 PRs (including PR #13, #18, #19)  
**Status Breakdown:**
- ✅ Complete/Fixed: 12 (PRs #1, #4, #8, PR12-#3 via PR #13, PR12-#1 via PR #18, PR12-#2 via PR #19, PR18 user-reported)
- ✅ Resolved: 2 (PR #2 - fixed in Phase 2)
- 🔴 Not Fixed: 1 (PR #2 - HIGH priority)
- 🟡 Planned: 2 (PR #12 - remaining batch)
- 🟡 Deferred: 9 (Various PRs, including PR #13, PR #18)

**Priority Breakdown:**
- 🔴 CRITICAL: 0 (all fixed!)
- 🟠 HIGH: 1 (PR02-#3 - CLI imports, can defer)
- 🟡 MEDIUM: 8 (can defer, including PR13-#1, PR18-Overall-#2)
- 🟢 LOW: 6 (can defer, including PR18-Overall-#1)
- ✅ Complete/Resolved/Fixed: 11

---

## 🚦 Priority Guidelines

### Priority Levels
- 🔴 **CRITICAL**: Security, stability, or core functionality issues
- 🟠 **HIGH**: Bug risks or significant maintainability issues
- 🟡 **MEDIUM**: Code quality and maintainability improvements
- 🟢 **LOW**: Nice-to-have improvements

### Impact Levels
- 🔴 **CRITICAL**: Affects core functionality
- 🟠 **HIGH**: User-facing or significant changes
- 🟡 **MEDIUM**: Developer experience improvements
- 🟢 **LOW**: Minor improvements

### Effort Levels
- 🟢 **LOW**: Simple, quick changes
- 🟡 **MEDIUM**: Moderate complexity
- 🟠 **HIGH**: Complex refactoring
- 🔴 **VERY_HIGH**: Major rewrites

---

## 🎯 Recommended Action Plan

### 🔴 Immediate Priority

**PR #2 - HIGH Priority Issue:**
- **PR02-#3:** CLI import ambiguity (HIGH priority, LOW effort)
- **File:** [pr02/issue-03-cli-imports.md](pr02/issue-03-cli-imports.md)
- **Action:** Should be fixed before next CLI work

### 🟡 Next: PR #12 Batches

**Batch 1: MEDIUM/LOW** (2 issues) ✅ Complete
- **File:** [pr12/batch-medium-low-01.md](pr12/batch-medium-low-01.md)
- **Issues:** CLI validation, test expectations
- **Completed:** PR #19 (2025-12-05)

**Batch 2: MEDIUM/MEDIUM** (1 issue)
- **File:** [pr12/batch-medium-medium-01.md](pr12/batch-medium-medium-01.md)
- **Issues:** Avoid conditionals in tests
- **Estimated:** 1-2 hours

**Batch 3: LOW/LOW** (2 issues)
- **File:** [pr12/batch-low-low-01.md](pr12/batch-low-low-01.md)
- **Issues:** Named expression, raise from error
- **Estimated:** 30 min - 1 hour

---

## 📋 Workflow

1. **Sourcery Review** - Code review identifies issues
2. **Priority Assessment** - Fill priority matrix in `docs/maintainers/feedback/sourcery/pr##.md`
3. **Create Fix Plans** - Use `/fix-plan` command to create batches
4. **Fix Plans Created** - Plans saved in `pr##/` directory
5. **Implement Fixes** - Use `/fix-implement` command with batch name
6. **Test Thoroughly** - Run all tests, verify no regressions
7. **Create PR** - Link to fix plans in PR description
8. **Review & Merge** - Merge to develop after approval
9. **Archive** - Move completed PR to `archived/` directory

---

## 📚 Related Documentation

**Sourcery Feedback Files:** `docs/maintainers/feedback/sourcery/pr##.md`

**Commands:**
- `/fix-plan` - Create fix plans from PR review
- `/fix-implement` - Implement fixes from a batch
- `/fix-review` - Review old deferred issues

---

**Last Updated:** 2025-12-05  
**Status:** ✅ Active  
**Next:** Review cross-PR batches, implement Quick Wins batch, then Test Quality batch

---

## Recent Completions

### PR #18 (2025-12-05)
- ✅ CLI table display improvements (user-reported)
- ✅ click.Choice validation (PR12-#1 via PR #18)
- ✅ Test expectations tightened (PR12-#2 via PR #19)
- 🟡 1 remaining batch (LOW/LOW priority)
