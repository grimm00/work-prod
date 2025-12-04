# Projects Feature - Fix Tracking

**Purpose:** Track fixes identified through code review (Sourcery, manual review, etc.)  
**Status:** 🔴 CRITICAL ISSUES IN PR #8  
**Last Updated:** 2025-12-04  
**Progress:** 5/18 complete (28%)

---

## 🚨 URGENT: Critical Issues in PR #8

**Date:** 2025-12-04  
**Review:** PR #8 (Phase 2) Sourcery feedback  
**Status:** 🔴 **MUST FIX BEFORE MERGE**

**Security Issue Alert:** PR #8 has a CRITICAL security issue - exception details are leaked to clients, potentially exposing database schema and internal implementation details.

**High Priority Bug:** Null status validation causes confusing 409 errors instead of proper 400 validation errors.

**Action Required:** 
1. Fix PR08-#1 (CRITICAL - security)
2. Fix PR08-#2 (HIGH - validation bug)
3. Then merge PR #8

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

### PR #8 Sourcery Review (Phase 2) - **🔴 URGENT**

| Issue | Priority | Impact | Effort | Status | File |
|-------|----------|--------|--------|--------|------|
| PR08-#1 | 🔴 CRITICAL | 🔴 CRITICAL | 🟡 MEDIUM | 🔴 **BLOCKS MERGE** | [pr08-issue-01-exception-leak.md](pr08-issue-01-exception-leak.md) |
| PR08-#2 | 🟠 HIGH | 🟠 HIGH | 🟡 MEDIUM | 🔴 **BLOCKS MERGE** | [pr08-issue-02-null-status-validation.md](pr08-issue-02-null-status-validation.md) |
| PR08-#3 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | 🟡 Deferred | Missing test: empty JSON body |
| PR08-#14 | 🟡 MEDIUM | 🟢 LOW | 🟢 LOW | 🟡 Deferred | Bare except in CLI |
| PR08-Overall | 🟡 MEDIUM | 🟠 HIGH | 🟠 HIGH | 🟡 Deferred | Code duplication (validation, errors, CLI) |
| PR08-#4-#15 | 🟢 LOW | 🟢 LOW | 🟢 LOW | 🟡 Deferred | Style improvements (12 issues) |

**Note:** PR #8 cannot be merged until PR08-#1 and PR08-#2 are fixed.

---

## 📊 Summary Statistics

**Total Issues:** 24 across 5 PRs  
**Status Breakdown:**
- ✅ Complete/Fixed: 8 (PRs #1, #4, #6)
- ✅ Resolved: 2 (PR #2 - fixed in Phase 2)
- 🔴 **BLOCKS MERGE:** 2 (PR #8 - **URGENT**)
- 🔴 Not Fixed: 4 (PRs #2, #3)
- 🟡 Deferred: 6 (PR #8 - MEDIUM/LOW)
- 🟡 Planned: 2 (PR #1 - LOW priority)

**Priority Breakdown:**
- 🔴 CRITICAL: 1 (PR08-#1 - **BLOCKS PR #8 MERGE**)
- 🟠 HIGH: 1 (PR08-#2 - **BLOCKS PR #8 MERGE**)
- 🟠 HIGH (other): 1 (PR02-#3 - can defer)
- 🟡 MEDIUM: 8 (can defer)
- 🟢 LOW: 13 (can defer)
- ✅ Complete/Resolved/Fixed: 10

**Effort Estimate for PR #8 Blocking Issues:**
- CRITICAL (1 issue): 30 minutes (PR08-#1 - Exception leak fix)
- HIGH (1 issue): 20 minutes (PR08-#2 - Null validation fix)
- **Total: 50 minutes to unblock PR #8**

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

### 🔴 URGENT: Fix PR #8 Blocking Issues (50 minutes)

**Note:** PR #8 has been merged to `develop`, but contains CRITICAL security issue. Fix must be applied immediately.

**Branch:** `fix/pr08-critical-security-validation` from `develop`

**MUST FIX IMMEDIATELY (PR #8 is already merged):**
1. 🔴 PR08-#1 - Exception leak security issue (30 min) - **SECURITY**
2. 🟠 PR08-#2 - Null status validation bug (20 min)

**Process:**
1. Create fix branch from `develop`
2. Implement both fixes with tests
3. Create PR, fast-track review
4. Merge immediately (docs/* or with approval)

### Future: Test Improvements PR

**Branch:** `feat/test-improvements`

**Issues to Fix:**
- 🟡 PR02-#4 - Test null path serialization
- 🟡 PR02-#6-#7 - Use IntegrityError in tests
- 🟡 PR02-#8 - Test updated_at changes
- 🟡 PR03-#1 - CORS parsing robustness

**Timing:** After Phase 2 merges

### Opportunistic: Code Quality

**Issues:**
- 🟢 PR01-#5-#6 - Test improvements and README
- 🟢 PR02-#5, #9-#11 - Test and error handling improvements

**Timing:** Fix when touching related code

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

**Last Updated:** 2025-12-03  
**Status:** ⚠️ CRITICAL ISSUES FOUND - MUST FIX BEFORE PHASE 2  
**Next:** Create `fix/critical-config-logging-issues` branch and implement fixes
