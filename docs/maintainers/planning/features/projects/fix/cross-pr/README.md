# Cross-PR Fix Batches

**Purpose:** Fix batches created from fix-review reports across multiple PRs  
**Status:** ✅ Active  
**Last Updated:** 2025-12-05

---

## 📋 Quick Links

### Active Batches

- **[quick-wins-low-low-01.md](quick-wins-low-low-01.md)** - Quick Wins (🟢 LOW, 🟢 LOW, 7 issues)
- **[test-quality-medium-low-01.md](test-quality-medium-low-01.md)** - Test Quality (🟡 MEDIUM, 🟢 LOW, 4 issues)

---

## 📊 Summary

**Total Batches:** 2  
**Total Issues:** 11  
**Source PRs:** #1, #2, #8, #12, #13

**Priority Breakdown:**

- 🟡 MEDIUM: 4 issues (1 batch)
- 🟢 LOW: 7 issues (1 batch)

---

## 🟡 Active Batches

### Quick Wins Batch

- **Status:** 🔴 Not Started
- **Issues:** 7 LOW/LOW issues
- **File:** [quick-wins-low-low-01.md](quick-wins-low-low-01.md)
- **Estimated:** 2-3 hours
- **Source PRs:** #1 (2 issues), #2 (4 issues), #12 (1 issue)

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

