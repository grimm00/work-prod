# PR #40 Fix Tracking - Phase 1: Schema Migration

**PR:** #40  
**Phase:** Phase 1 - Schema Migration  
**Date:** 2025-12-29  
**Status:** 🟢 All issues LOW priority - deferred to future cleanup

---

## 📋 Deferred Issues

**Date:** 2025-12-29  
**Review:** [PR #40 Sourcery Review](../../../feedback/sourcery/pr40.md)  
**Status:** 🟢 **DEFERRED** - All LOW priority, can be handled opportunistically

### Deferred Issues:

| ID | Description | Priority | Impact | Effort | Action |
|----|-------------|----------|--------|--------|--------|
| PR40-#1 | Use pytest.mark.parametrize for valid values test | 🟢 LOW | 🟢 LOW | 🟢 LOW | Defer |
| PR40-Overall-#1 | Enum type cleanup on Postgres downgrade | 🟢 LOW | 🟢 LOW | 🟢 LOW | N/A (SQLite) |
| PR40-Overall-#2 | Rollback after commit is no-op in test | 🟢 LOW | 🟢 LOW | 🟢 LOW | Defer |

### Issue Details:

**PR40-#1: Use pytest.mark.parametrize**
- **Location:** `backend/tests/unit/models/test_project.py:239-248`
- **Description:** Suggestion to use pytest.mark.parametrize instead of loop with manual rollback
- **Why Deferred:** Test works correctly as-is. Nice improvement but not urgent.

**PR40-Overall-#1: Enum type cleanup on downgrade**
- **Description:** Drop `project_type_enum` type on Postgres downgrade
- **Why Deferred:** N/A for SQLite (our database). Only relevant if migrating to Postgres.

**PR40-Overall-#2: Rollback after commit**
- **Description:** db.session.rollback() after commit is effectively a no-op
- **Why Deferred:** Test semantics work correctly. Minor clarity improvement.

---

## 📊 Action Plan

**Decision:** All issues deferred to future code cleanup.

**Rationale:**
- All issues are LOW priority
- No impact on functionality
- Test coverage is at 97%
- No security or stability concerns

**Future Handling:**
- Can be addressed opportunistically during future phases
- Or in a dedicated code quality improvement PR

---

**Last Updated:** 2025-12-29

