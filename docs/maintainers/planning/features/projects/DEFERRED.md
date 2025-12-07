# Projects Feature - Deferred Tasks

**Purpose:** Track tasks and issues intentionally postponed to future phases  
**Status:** ✅ Active  
**Last Updated:** 2025-12-03

---

## 📋 Overview

This document tracks tasks, fixes, and features that have been identified but deliberately postponed to future phases. These are not forgotten - they're strategically deferred to maintain focus and momentum.

---

## 🔮 Deferred to Phase 8 (Frontend Learning Project)

### Issue #4: Frontend CSS Layout

**Source:** Sourcery PR #1, Comment #4  
**Location:** `frontend/src/index.css:25-30`  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Issue:**
Using `display: flex` and `place-items: center` on `body` turns the whole viewport into a centered flex container. This works for the health-check view but may conflict with future layouts (scrolling content, sidebars, etc.).

**Recommendation:**
Move the centering styles into a specific wrapper (e.g., `#root` or a layout component) and keep `body` styles minimal.

**Why Deferred:**
- Phase 0-7 use backend-first approach with CLI tools
- Frontend is deferred to Phase 8 as a learning project
- This issue will be addressed during frontend refactoring
- No impact on current backend MVP development

**Related:**
- [frontend/README-DEFERRED.md](../../../../frontend/README-DEFERRED.md)
- [docs/maintainers/planning/mvp-roadmap.md](../../mvp-roadmap.md) - Phase 8 section

---

## 📊 Deferred Items by Category

### Code Quality (Phase 8)
| Item | Priority | Reason | Target Phase |
|------|----------|--------|--------------|
| Frontend CSS Layout | 🟢 LOW | Frontend deferred to learning project | Phase 8 |

### Future Enhancements (Post-MVP)
_No items yet_

### Research Required (TBD)
_No items yet_

---

## 🎯 Review Process

**When to Add Items:**
1. Code review identifies low-priority improvements
2. Feature requests outside current phase scope
3. Technical debt that doesn't block progress
4. Enhancements requiring research or design

**When to Promote Items:**
1. Deferred issue becomes blocking
2. Related work brings item into scope
3. Priority changes based on new information
4. Natural opportunity arises during related work

---

## 📝 Adding New Deferred Items

Use this template:

```markdown
### [Item Name]

**Source:** [Sourcery PR #X / User Request / etc.]  
**Location:** [file path or feature area]  
**Priority:** [🔴/🟠/🟡/🟢] | **Impact:** [🔴/🟠/🟡/🟢] | **Effort:** [🟢/🟡/🟠/🔴]

**Issue:**
[Clear description of the issue or enhancement]

**Recommendation:**
[What should be done]

**Why Deferred:**
- [Reason 1]
- [Reason 2]

**Related:**
- [Links to related documents]
```

---

## 🔄 Workflow

```
┌─────────────┐
│ Issue Found │
└──────┬──────┘
       │
       ▼
┌──────────────┐      ┌────────────────┐
│ Priority     │──────│ High Priority? │──► Create Fix Plan
│ Assessment   │      │ Blocks MVP?    │
└──────┬───────┘      └────────────────┘
       │ Low Priority/
       │ Out of Scope
       ▼
┌──────────────┐
│ Add to       │
│ DEFERRED.md  │
└──────┬───────┘
       │
       ▼
┌──────────────┐      ┌────────────────┐
│ Review       │──────│ Still Deferred?│──► Keep in DEFERRED.md
│ at Phase End │      │                │
└──────────────┘      └────────┬───────┘
                               │ Promote
                               ▼
                      ┌────────────────┐
                      │ Create Fix Plan│
                      │ for Next Phase │
                      └────────────────┘
```

---

## 📌 Notes

- **Not Forgotten:** Deferred ≠ Ignored. Items are tracked and reviewed regularly.
- **Strategic Focus:** Deferring allows focus on critical path for MVP delivery.
- **Flexibility:** Items can be promoted if priority changes or blocking issues arise.
- **Learning Opportunity:** Some items (like Frontend CSS) deferred to support learning goals.

---

**Last Updated:** 2025-12-03  
**Status:** ✅ Active  
**Next Review:** End of Phase 2

