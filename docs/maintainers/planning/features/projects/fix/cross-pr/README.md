# Cross-PR Fix Batches

**Purpose:** Fix batches created from fix-review reports across multiple PRs  
**Status:** ✅ Active  
**Last Updated:** 2025-12-05

---

## 📋 Quick Links

### Active Batches

- **[quick-wins-low-low-01.md](quick-wins-low-low-01.md)** - Quick Wins Batch 1 (✅ Complete, PR #14)
- **[quick-wins-low-low-02.md](quick-wins-low-low-02.md)** - Quick Wins Batch 2 (🔴 Not Started, 7 issues)
- **[test-quality-medium-low-01.md](test-quality-medium-low-01.md)** - Test Quality Improvements (🔴 Not Started, 9 issues)
- **[code-refactoring-medium-medium-01.md](code-refactoring-medium-medium-01.md)** - Code Refactoring (🔴 Not Started, 2 issues)

---

## 📊 Summary

**Total Batches:** 4 (2 complete, 2 active)  
**Total Issues:** 20 (14 complete, 6 active)  
**Source PRs:** #1, #2, #8, #12, #13, #16, #18, #19

**Note:** Quick Wins Batch 2 completed via PR #21 (2025-12-05)

**Priority Breakdown:**

- 🟡 MEDIUM: 11 issues (Test Quality batch + Code Refactoring batch + 1 in Quick Wins Batch 2)
- 🟢 LOW: 9 issues (2 Quick Wins batches)

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

## 🚀 Next Steps

1. Review fix plans in this directory
2. Use `/fix-implement` command to implement batches
3. Start with Quick Wins Batch 2 (lower priority, builds momentum)
4. Then implement Test Quality Improvements batch (improves test coverage)
5. Finally implement Code Refactoring batch (improves code organization)

---

**Last Updated:** 2025-12-05

