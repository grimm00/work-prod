# Projects Feature - Fix Tracking

**Purpose:** Track fixes identified through code review (Sourcery, manual review, etc.)  
**Status:** ✅ PR #8 CRITICAL ISSUES FIXED  
**Last Updated:** 2025-12-04  
**Progress:** 7/22 complete (32%)

---

## ✅ PR #8 Critical Issues - RESOLVED

**Date:** 2025-12-04  
**Review:** PR #8 (Phase 2) Sourcery feedback  
**Status:** ✅ **FIXED in PR #9**

**Security Issue:** ✅ FIXED - Exception details no longer leaked to clients
**Validation Bug:** ✅ FIXED - Null status properly rejected with 400

**PR #9 Status:** Merged to develop - Critical fixes deployed
**Remaining Issues:** 4 LOW/MEDIUM priority items for future improvement

---

## 📋 PR #12 Deferred Issues (Phase 4)

**Date:** 2025-12-04  
**Review:** PR #12 (Phase 4) Sourcery feedback  
**Status:** 🟡 **DEFERRED** - All MEDIUM/LOW priority, can be handled opportunistically

**Deferred Issues:**

- **PR12-#1:** Use `click.Choice` for CLI validation (MEDIUM priority, LOW effort) - Improves UX by catching invalid values early
- **PR12-#2:** Tighten test expectations for invalid status (MEDIUM priority, LOW effort) - Test quality improvement
- **PR12-#3:** Avoid conditionals in tests (MEDIUM priority, MEDIUM effort) - Code quality improvement, requires test refactoring
- **PR12-#4:** Use named expression (LOW priority, LOW effort) - Minor code quality improvement
- **PR12-#5:** Raise from previous error (LOW priority, LOW effort) - Minor code quality improvement

**Action Plan:** These can be handled opportunistically during future phases or in a dedicated code quality improvement PR.

---

## 📋 Overview

This directory tracks fixes identified through code review processes including:
- Sourcery AI code review
- Manual code review
- Security audits
- Performance analysis

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
git checkout -b fix/critical-config-logging-issues
# Implement fixes from PRs #2, #4
git commit -m "fix(critical): add FLASK_ENV fallback and fix logging config"
```

### For Individual Urgent Fixes

- Create `fix/issue-[number]-[short-name]` branch
- Implement single fix
- Fast-track PR if CRITICAL

---

## 📝 Current Fixes

### PR #1 Sourcery Review (Phase 0)

| Issue | Priority | Impact | Effort | Status | File |
|-------|----------|--------|--------|--------|------|
| PR01-#1 | 🟠 HIGH | 🟡 MEDIUM | 🟢 LOW | ✅ Complete | [pr01-issue-01-logging-config.md](pr01-issue-01-logging-config.md) |
| PR01-#2 | 🔴 CRITICAL | 🔴 CRITICAL | 🟢 LOW | ✅ Complete | [pr01-issue-02-cors-security.md](pr01-issue-02-cors-security.md) |
| PR01-#3 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | ✅ Complete | [pr01-issue-03-flask-env-deprecated.md](pr01-issue-03-flask-env-deprecated.md) |
| PR01-#5 | 🟢 LOW | 🟢 LOW | 🟢 LOW | 🟡 Planned | [pr01-issue-05-test-improvements.md](pr01-issue-05-test-improvements.md) |
| PR01-#6 | 🟢 LOW | 🟢 LOW | 🟢 LOW | 🟡 Planned | [pr01-issue-06-readme-typo.md](pr01-issue-06-readme-typo.md) |

### PR #2 Sourcery Review (Phase 1) - **NEW**

| Issue | Priority | Impact | Effort | Status | File |
|-------|----------|--------|--------|--------|------|
| PR02-#1 | ✅ RESOLVED | - | - | Phase 2 | Overlapping routes fixed in Phase 2 |
| PR02-#2 | ✅ RESOLVED | - | - | Phase 2 | ValueError handler removed in Phase 2 |
| PR02-#3 | 🟠 HIGH | 🟠 HIGH | 🟢 LOW | 🔴 Not Fixed | [pr02-issue-03-cli-imports.md](pr02-issue-03-cli-imports.md) |
| PR02-#4 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | 🔴 Not Fixed | Test null path serialization |
| PR02-#5 | 🟢 LOW | 🟢 LOW | 🟢 LOW | 🔴 Not Fixed | Test error message content |
| PR02-#6 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | 🔴 Not Fixed | Use IntegrityError in test |
| PR02-#7 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | 🔴 Not Fixed | Use IntegrityError in test |
| PR02-#8 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | 🔴 Not Fixed | Test updated_at changes |
| PR02-#9 | 🟢 LOW | 🟢 LOW | 🟡 MEDIUM | 🔴 Not Fixed | Avoid loop in tests |
| PR02-#10 | 🟢 LOW | 🟢 LOW | 🟢 LOW | 🔴 Not Fixed | Raise from previous error (get) |
| PR02-#11 | 🟢 LOW | 🟢 LOW | 🟢 LOW | 🔴 Not Fixed | Raise from previous error (list) |

### PR #3 Sourcery Review (CORS Fix) - **NEW**

| Issue | Priority | Impact | Effort | Status | File |
|-------|----------|--------|--------|--------|------|
| PR03-#1 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | 🔴 Not Fixed | CORS parsing whitespace handling |

### PR #4 Sourcery Review (Config Fixes) - **NEW**

| Issue | Priority | Impact | Effort | Status | File |
|-------|----------|--------|--------|--------|------|
| PR04-#1 | 🟠 HIGH | 🟠 HIGH | 🟢 LOW | ✅ Fixed (PR #6) | [pr04-issue-01-02-logging-setup.md](pr04-issue-01-02-logging-setup.md) |
| PR04-#2 | 🟠 HIGH | 🟠 HIGH | 🟢 LOW | ✅ Fixed (PR #6) | [pr04-issue-01-02-logging-setup.md](pr04-issue-01-02-logging-setup.md) |
| PR04-#3 | 🔴 CRITICAL | 🔴 CRITICAL | 🟢 LOW | ✅ Fixed (PR #6) | [pr04-issue-03-flask-env-fallback.md](pr04-issue-03-flask-env-fallback.md) |

### PR #8 Sourcery Review (Phase 2) - ✅ **FIXED**

| Issue | Priority | Impact | Effort | Status | File |
|-------|----------|--------|--------|--------|------|
| PR08-#1 | 🔴 CRITICAL | 🔴 CRITICAL | 🟡 MEDIUM | ✅ Fixed (PR #9) | [pr08-issue-01-exception-leak.md](pr08-issue-01-exception-leak.md) |
| PR08-#2 | 🟠 HIGH | 🟠 HIGH | 🟡 MEDIUM | ✅ Fixed (PR #9) | [pr08-issue-02-null-status-validation.md](pr08-issue-02-null-status-validation.md) |
| PR08-#3 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | 🟡 Deferred | Missing test: empty JSON body |
| PR08-#14 | 🟡 MEDIUM | 🟢 LOW | 🟢 LOW | 🟡 Deferred | Bare except in CLI |
| PR08-Overall | 🟡 MEDIUM | 🟠 HIGH | 🟠 HIGH | 🟡 Deferred | Code duplication (validation, errors, CLI) |
| PR08-#4-#15 | 🟢 LOW | 🟢 LOW | 🟢 LOW | 🟡 Deferred | Style improvements (12 issues) |

### PR #9 Sourcery Review (Security Fixes) - 🟢 **CLEAN**

| Issue | Priority | Impact | Effort | Status | File |
|-------|----------|--------|--------|--------|------|
| PR09-#1 | 🟢 LOW | 🟡 MEDIUM | 🟢 LOW | 🟡 Deferred | Test: Assert exact error messages |
| PR09-#2 | 🟢 LOW | 🟢 LOW | 🟢 LOW | 🟡 Deferred | Test: Remove redundant monkeypatch restore |
| PR09-Overall-1 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 Deferred | Extract status validation helper |
| PR09-Overall-2 | 🟢 LOW | 🟡 MEDIUM | 🟢 LOW | 🟡 Deferred | Test improvements (same as #1) |

**Note:** PR #9 has no blocking issues. All items are LOW/MEDIUM priority improvements.

---

## 📊 Summary Statistics

**Total Issues:** 28 across 6 PRs  
**Status Breakdown:**
- ✅ Complete/Fixed: 12 (PRs #1, #4, #6, #9)
- ✅ Resolved: 2 (PR #2 - fixed in Phase 2)
- 🔴 Not Fixed: 4 (PRs #2, #3)
- 🟡 Deferred: 10 (PRs #8, #9 - MEDIUM/LOW improvements)
- 🟡 Planned: 2 (PR #1 - LOW priority)

**Priority Breakdown:**
- 🔴 CRITICAL: 0 (all fixed!)
- 🟠 HIGH: 1 (PR02-#3 - CLI imports, can defer)
- 🟡 MEDIUM: 10 (can defer)
- 🟢 LOW: 15 (can defer)
- ✅ Complete/Resolved/Fixed: 14

**Recent Fixes (PR #9):**
- ✅ PR08-#1 (CRITICAL): Exception leak security fix
- ✅ PR08-#2 (HIGH): Null status validation fix
- **Time to fix:** 50 minutes (as estimated)

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

### ✅ COMPLETED: PR #8 Critical Issues Fixed

**Branch:** `fix/pr08-critical-security-validation` (merged via PR #9)

**Fixes Applied:**
1. ✅ PR08-#1 - Exception leak security issue (30 min) - **FIXED**
2. ✅ PR08-#2 - Null status validation bug (20 min) - **FIXED**

**Result:**
- PR #9 merged to `develop`
- All CRITICAL and HIGH issues resolved
- 4 new tests added, all passing
- Coverage maintained at 94%

### 📦 Deferred Issues Backlog

**Total:** 14 deferred issues (can be addressed in future PRs)

#### Test Improvements (7 issues)

| Issue | Priority | Effort | Description |
|-------|----------|--------|-------------|
| PR09-#1 | 🟢 LOW | 🟢 LOW | Assert exact error messages in tests |
| PR09-#2 | 🟢 LOW | 🟢 LOW | Remove redundant monkeypatch restore |
| PR08-#3 | 🟡 MEDIUM | 🟢 LOW | Add test for empty JSON body on POST |
| PR02-#4 | 🟡 MEDIUM | 🟢 LOW | Test null path serialization |
| PR02-#6-#7 | 🟡 MEDIUM | 🟢 LOW | Use IntegrityError in tests (2 places) |
| PR02-#8 | 🟡 MEDIUM | 🟢 LOW | Test updated_at timestamp changes |
| PR01-#5 | 🟢 LOW | 🟢 LOW | Improve health check tests |

**Estimated effort:** 2-3 hours for all test improvements

#### Code Quality & Refactoring (5 issues)

| Issue | Priority | Effort | Description |
|-------|----------|--------|-------------|
| PR09-Overall-1 | 🟡 MEDIUM | 🟡 MEDIUM | Extract status validation helper (reduce duplication) |
| PR08-Overall | 🟡 MEDIUM | 🟠 HIGH | Reduce duplication in validation, errors, and CLI |
| PR08-#14 | 🟡 MEDIUM | 🟢 LOW | Replace bare except in CLI with Exception |
| PR03-#1 | 🟡 MEDIUM | 🟢 LOW | Improve CORS origin parsing robustness |
| PR02-#3 | 🟠 HIGH | 🟢 LOW | Use package-qualified imports in CLI (partially done) |

**Estimated effort:** 3-4 hours for refactoring work

#### Style Improvements (12 individual items from PR08)

| Category | Count | Effort | Description |
|----------|-------|--------|-------------|
| Merge nested ifs | 4 | 🟢 LOW | Simplify validation conditions (#6, #7, #8, #9) |
| Avoid loops in tests | 2 | 🟢 LOW | Refactor enum validation tests (#10, #11) |
| Use walrus operator | 2 | 🟢 LOW | Simplify assignment + conditional (#12, #13) |
| Documentation | 1 | 🟢 LOW | Fix typo in manual testing guide (#4) |
| Test coverage | 1 | 🟢 LOW | Add 404 test scenario (#5) |
| Remove unnecessary code | 2 | 🟢 LOW | Remove .keys() call, simplify dict access (#15) |

**Estimated effort:** 1-2 hours for all style improvements

#### Summary by Priority

- 🟠 **HIGH:** 1 issue (CLI imports - can defer)
- 🟡 **MEDIUM:** 8 issues (test improvements, refactoring)
- 🟢 **LOW:** 17 issues (style, documentation)

**Total estimated effort:** 6-9 hours across all deferred items

#### Recommended Approach

1. **Short-term (opportunistic):** Fix style improvements when touching related code
2. **Medium-term (dedicated PR):** Test improvements bundle (2-3 hours)
3. **Long-term (Phase 4+):** Code quality refactoring (extract helpers, reduce duplication)

---

## Deferred from PR #10 (Phase 3)

**Date:** 2025-12-04  
**Review:** PR #10 (Phase 3) Sourcery feedback  
**Status:** 🟡 **DEFERRED to Phase 4**

**Issues to handle opportunistically in Phase 4:**

- **PR10-#1:** Test assertion improvement - tighten 404 assertions (MEDIUM, LOW effort)
- **PR10-#3:** Bare except in archive_cmd.py (MEDIUM, LOW effort)
- **PR10-#4:** Bare except in delete_cmd.py (MEDIUM, LOW effort)
- **PR10-Overall-1:** Use Enum values instead of raw strings (MEDIUM, MEDIUM effort)
- **PR10-Overall-2:** Extract error handling helper for CLI commands (MEDIUM, MEDIUM effort)

**Total:** 5 MEDIUM priority issues, estimated 2-3 hours

**Plan:** Address these during Phase 4 implementation when touching related code (CLI commands, test improvements).

---

## 📋 Workflow

1. **Sourcery Review** - Code review identifies issues
2. **Priority Assessment** - Fill priority matrix in `docs/maintainers/feedback/sourcery/pr##-fixed.md`
3. **Create Fix Plans** - Document each fix in this directory
4. **Create Fix Branch** - Branch from develop
5. **Implement Fixes** - Follow fix plan implementation steps
6. **Test Thoroughly** - Run all tests, verify no regressions
7. **Create PR** - Link to fix plans in PR description
8. **Review & Merge** - Merge to develop after approval
9. **Mark Complete** - Update fix plan status

---

## 📚 Related Documentation

- **Sourcery Feedback Files:** `docs/maintainers/feedback/sourcery/pr0X-fixed.md`
- **Cross-Reference Analysis:** `docs/maintainers/planning/notes/sourcery-cross-reference.md`
- **Review Summary:** `docs/maintainers/planning/notes/sourcery-feedback-review-summary.md`

---

**Last Updated:** 2025-12-04  
**Status:** ✅ All CRITICAL issues resolved - 14 deferred improvements tracked  
**Next:** Address deferred items opportunistically or in dedicated improvement PRs
