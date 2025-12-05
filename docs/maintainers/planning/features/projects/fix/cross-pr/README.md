# Cross-PR Fix Batches

**Purpose:** Fix batches created from fix-review reports across multiple PRs  
**Status:** ✅ Active  
**Last Updated:** 2025-12-05

---

## 📋 Quick Links

### Active Batches

- **[quick-wins-low-low-01.md](quick-wins-low-low-01.md)** - Quick Wins Batch 1 (✅ Complete, PR #14)
- **[quick-wins-low-low-02.md](quick-wins-low-low-02.md)** - Quick Wins Batch 2 (🔴 Not Started, 7 issues)
- **[test-quality-medium-low-01.md](test-quality-medium-low-01.md)** - Test Quality (🟡 MEDIUM, 🟢 LOW, 4 issues)

---

## 📊 Summary

**Total Batches:** 3 (1 complete, 2 active)  
**Total Issues:** 18 (7 complete, 11 active)  
**Source PRs:** #1, #2, #8, #12, #13, #16, #18, #19

**Priority Breakdown:**

- 🟡 MEDIUM: 5 issues (1 MEDIUM/LOW batch + 1 in Quick Wins Batch 2)
- 🟢 LOW: 13 issues (2 Quick Wins batches)

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

- **Status:** 🔴 Not Started
- **Issues:** 7 issues (5 LOW/LOW + 2 MEDIUM/LOW)
- **File:** [quick-wins-low-low-02.md](quick-wins-low-low-02.md)
- **Estimated:** 1-2 hours
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

### Test Quality Batch

- **Status:** 🔴 Not Started
- **Issues:** 4 MEDIUM/LOW issues
- **File:** [test-quality-medium-low-01.md](test-quality-medium-low-01.md)
- **Estimated:** 2-3 hours
- **Source PRs:** #2 (2 issues), #8 (1 issue), #13 (1 issue)

**Issues:**
- PR02-#4: Test null path serialization
- PR02-#8: Test updated_at changes
- PR08-#3: Missing test: empty JSON body
- PR13-#1: Strengthen test assertions

---

## 🚀 Next Steps

1. Review fix plans in this directory
2. Use `/fix-implement` command to implement batches
3. Start with Quick Wins batch (lower priority, builds momentum)
4. Then implement Test Quality batch (improves test coverage)

---

**Last Updated:** 2025-12-05

