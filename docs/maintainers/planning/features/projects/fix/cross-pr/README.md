# Cross-PR Fix Batches

**Purpose:** Fix batches created from fix-review reports across multiple PRs  
**Status:** ✅ Active  
**Last Updated:** 2025-12-05

---

## 📋 Quick Links

### Active Batches

- **[quick-wins-low-low-01.md](quick-wins-low-low-01.md)** - Quick Wins Batch 1 (✅ Complete, PR #14)
- **[quick-wins-low-low-02.md](quick-wins-low-low-02.md)** - Quick Wins Batch 2 (✅ Complete, PR #21)
- **[test-quality-medium-low-01.md](test-quality-medium-low-01.md)** - Test Quality Improvements (✅ Complete, PR #20)
- **[code-refactoring-medium-medium-01.md](code-refactoring-medium-medium-01.md)** - Code Refactoring (✅ Complete, PR #22)
- **[bug-risk-fixes-medium-low-01.md](bug-risk-fixes-medium-low-01.md)** - Bug Risk Fixes (🔴 Not Started, 3 issues)
- **[quick-wins-low-low-03.md](quick-wins-low-low-03.md)** - Quick Wins Batch 3 (🔴 Not Started, 9 issues from PR #24)
- **[configuration-improvements-medium-medium-01.md](configuration-improvements-medium-medium-01.md)** - Configuration Improvements (✅ Complete, PR #27)
- **[test-quality-improvements-medium-low-02.md](test-quality-improvements-medium-low-02.md)** - Test Quality Improvements Batch 2 (🟡 MEDIUM, 🟢 LOW, 9 issues) ✅ **Complete** (PR #33, merged 2025-12-07)
- **[test-quality-improvements-medium-low-03.md](test-quality-improvements-medium-low-03.md)** - Test Quality Improvements Batch 3 (🔴 Not Started, 1 issue from PR #19)

---

## 📊 Summary

**Total Batches:** 9 (5 complete, 4 active)  
**Total Issues:** 57 (21 complete, 36 active)  
**Source PRs:** #1, #2, #8, #12, #13, #16, #18, #19, #20, #22, #24, #27

**Notes:**
- Quick Wins Batch 2 completed via PR #21 (2025-12-05)
- Code Refactoring Batch completed via PR #22 (2025-12-06)
- Configuration Improvements Batch completed via PR #27 (2025-12-06)

**Priority Breakdown:**

- 🟡 MEDIUM: 16 issues (Bug Risk batch: 1, Test Quality batches: 10, Code Refactoring: 2, Quick Wins Batch 2: 1, Test Quality Batch 2: 2)
- 🟢 LOW: 35 issues (Quick Wins batches: 16, Test Quality: 1, Code Refactoring: 3, Bug Risk: 1)

---

## 🟡 Active Batches

### Quick Wins Batch 1

- **Status:** ✅ Complete
- **Issues:** 7 LOW/LOW issues (6 fixed, 1 already fixed)
- **File:** [quick-wins-low-low-01.md](quick-wins-low-low-01.md)
- **Completed:** 2025-12-05
- **PR:** #14
- **Source PRs:** #1 (2 issues), #2 (4 issues), #12 (1 issue)

### Quick Wins Batch 2

- **Status:** ✅ Complete
- **Issues:** 7 issues (5 LOW/LOW + 2 MEDIUM/LOW)
- **File:** [quick-wins-low-low-02.md](quick-wins-low-low-02.md)
- **Completed:** 2025-12-05 via PR #21
- **Source PRs:** #12 (2 issues), #16 (3 issues), #18 (1 issue), #19 (1 issue)

**Issues:**
- PR12-#4: Use named expression
- PR12-#5: Raise from previous error
- PR16-#8: Swap if expression
- PR16-#9: Remove duplicate dict key
- PR16-#12: Raise from previous error (3 instances)
- PR18-Overall-#1: Consistency of missing-value handling
- PR19-Overall-#1: Use @pytest.mark.parametrize

**Issues:**
- PR01-#5: Test improvements
- PR01-#6: README typo
- PR02-#5: Test error message content
- PR02-#9: Avoid loop in tests
- PR02-#10: Raise from previous error (get)
- PR02-#11: Raise from previous error (list)
- PR12-#5: Raise from previous error

---

### Test Quality Improvements Batch

- **Status:** ✅ Complete
- **Issues:** 9 issues (5 MEDIUM/LOW + 4 LOW/MEDIUM)
- **File:** [test-quality-medium-low-01.md](test-quality-medium-low-01.md)
- **Completed:** 2025-12-05 via PR #20
- **Source PRs:** #2 (4 issues), #13 (1 issue), #16 (4 issues)

**Issues:**
- PR02-#4: Test null path serialization ✅
- PR02-#6: Use IntegrityError in name test ✅
- PR02-#7: Use IntegrityError in path test ✅
- PR02-#8: Test updated_at changes ✅
- PR13-#1: Strengthen test assertions ✅
- PR16-#4, #5, #6, #7: Avoid loops in tests (4 instances, use parametrize) ✅

### Code Refactoring Batch

- **Status:** ✅ Complete
- **Issues:** 2 MEDIUM/MEDIUM issues
- **File:** [code-refactoring-medium-medium-01.md](code-refactoring-medium-medium-01.md)
- **Completed:** 2025-12-05 via PR #22
- **Source PRs:** #16 (1 issue), #18 (1 issue)

**Issues:**
- PR16-#10: Extract duplicate code into method (validation logic) ✅
- PR18-Overall-#2: Factor column configuration into helper (table building) ✅

---

## 🟡 Active Batches

### Bug Risk Fixes Batch

- **Status:** ✅ Complete
- **Issues:** 3 MEDIUM/LOW issues
- **File:** [bug-risk-fixes-medium-low-01.md](bug-risk-fixes-medium-low-01.md)
- **Completed:** 2025-12-06 via PR #25
- **Source PRs:** #22 (1 issue), #24 (2 issues)

**Issues:**
- PR24-#1: Guard against invalid `display.max_rows` values
- PR24-#3: Fix health URL construction
- PR22-#1: Use `.get()` for path to avoid KeyError

### Quick Wins Batch 3

- **Status:** 🔴 Not Started
- **Issues:** 9 LOW/LOW issues
- **File:** [quick-wins-low-low-03.md](quick-wins-low-low-03.md)
- **Estimated:** 1-2 hours
- **Source PRs:** #24 (9 issues)
- **Created:** 2025-12-07 from fix-review-report-2025-12-07.md

**Issues:**
- PR24-#4: Remove unused parameter
- PR24-#5: Fix unreachable branch
- PR24-#6: Merge nested if conditions
- PR24-#7, #12, #13: Use `except Exception:` instead of bare `except:` (3 instances)
- PR24-#8: Use named expression
- PR24-#9: Convert for loop to dict comprehension
- PR24-#10: Merge assignment and augmented assignment (2 instances)

### Configuration Improvements Batch

- **Status:** ✅ Complete
- **Issues:** 3 MEDIUM/MEDIUM issues
- **File:** [configuration-improvements-medium-medium-01.md](configuration-improvements-medium-medium-01.md)
- **Completed:** 2025-12-06 via PR #27
- **Source PRs:** #24 (3 issues)

**Issues:**
- PR24-#2: Use configured API base URL in error messages
- PR24-Overall #1: Config defaults visibility
- PR24-Overall #2: Hardcoded URLs

### Test Quality Improvements Batch 2

- **Status:** 🔴 Not Started
- **Issues:** 9 MEDIUM/LOW issues (1 deferred)
- **File:** [test-quality-improvements-medium-low-02.md](test-quality-improvements-medium-low-02.md)
- **Estimated:** 3-4 hours
- **Source PRs:** #16 (2 issues), #19 (1 issue), #20 (4 issues), #22 (2 issues, 1 deferred)

**Issues:**
- Test coverage improvements (3 issues)
- Test reliability improvements (1 issue)
- Test duplication reduction (1 issue)
- Request validation improvements (2 issues)
- API simplification (1 issue)
- Architectural improvement (1 issue - deferred)

### Test Quality Improvements Batch 3

- **Status:** 🔴 Not Started
- **Issues:** 1 MEDIUM/LOW issue
- **File:** [test-quality-improvements-medium-low-03.md](test-quality-improvements-medium-low-03.md)
- **Estimated:** 30 minutes - 1 hour
- **Source PRs:** #19 (1 issue)
- **Created:** 2025-12-07 from fix-review-report-2025-12-07.md

**Issues:**
- PR19-#1: Strengthen test assertions

---

## 🚀 Next Steps

1. Review fix plans in this directory
2. Use `/fix-implement` command to implement batches
3. **Recommended order:**
   - Start with Bug Risk Fixes Batch (highest priority)
   - Then Quick Wins Batch 3 (builds momentum)
   - Then Configuration Improvements Batch (improves UX)
   - Finally Test Quality Improvements Batch 2 (improves test coverage)

---

**Last Updated:** 2025-12-07

