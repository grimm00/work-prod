# PR #41 - Deferred Issues

**Feature:** Project Type Field  
**Phase:** 2 (Data Backfill)  
**PR:** #41  
**Date:** 2025-12-29  
**Status:** 🟡 **DEFERRED** - All LOW/MEDIUM priority, one-time script

---

## 📋 Overview

This document lists the low-priority issues identified during the Sourcery review of PR #41 (Phase 2: Data Backfill). These issues are deferred because:

1. This is a one-time backfill script (already executed)
2. The main heuristic logic is fully tested
3. Current scale is 31 projects (not a memory concern)
4. Constants are documented in ADR-003

---

## 📝 Deferred Issues

### PR41-#1: Add Tests for backfill() Function

- **Source:** Sourcery Comment #1
- **Location:** `scripts/tests/test_backfill_project_type.py:20-29`
- **Priority:** 🟡 MEDIUM
- **Impact:** 🟡 MEDIUM
- **Effort:** 🟡 MEDIUM
- **Description:** Add tests that exercise the `backfill()` function behavior (dry-run vs execute, DB updates, and filtering). Currently only `classify_project` is covered.
- **Action:** Defer - heuristics are the main logic and are fully tested. The backfill function is straightforward orchestration.

### PR41-Overall-#1: sys.path Modification

- **Source:** Sourcery Overall Comment #1
- **Location:** `scripts/backfill_project_type.py`
- **Priority:** 🟢 LOW
- **Impact:** 🟢 LOW
- **Effort:** 🟡 MEDIUM
- **Description:** The backfill script and tests both modify `sys.path` using relative paths; consider turning `scripts` into a proper package or using existing application entrypoints.
- **Action:** Defer - one-time backfill script, works fine as-is.

### PR41-Overall-#2: Memory Concerns (Batched Iteration)

- **Source:** Sourcery Overall Comment #2
- **Location:** `scripts/backfill_project_type.py`
- **Priority:** 🟢 LOW
- **Impact:** 🟢 LOW
- **Effort:** 🟡 MEDIUM
- **Description:** The `backfill` function loads all projects with `project_type IS NULL` into memory at once; consider batched iteration for larger datasets.
- **Action:** Defer - current scale is 31 projects, not a concern.

### PR41-Overall-#3: Hard-Coded Strings

- **Source:** Sourcery Overall Comment #3
- **Location:** `scripts/backfill_project_type.py`
- **Priority:** 🟢 LOW
- **Impact:** 🟢 LOW
- **Effort:** 🟡 MEDIUM
- **Description:** Classification heuristics rely on hard-coded string values (e.g., `'DRW'`, `'/Learning/'`, `'archive'`); consider centralizing in enums or constants.
- **Action:** Defer - one-time script, constants are documented in ADR-003.

---

## 🚀 Next Steps

- These issues are low priority for a one-time backfill script
- Consider addressing if scripts/ is expanded to a reusable package
- Monitor if project count grows significantly (for memory concern)

---

**Last Updated:** 2025-12-29

