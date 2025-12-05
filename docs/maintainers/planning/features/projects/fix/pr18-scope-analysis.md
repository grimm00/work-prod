# PR #18 Scope Analysis

**PR:** #18 - fix: CLI table display - add --wide flag for full columns  
**Date:** 2025-12-05  
**Status:** 🟡 Needs Scope Clarification

---

## 📋 Original Scope (From Fix Plan)

**Fix Plan:** `user-reported-01-cli-table-display.md`

**Original Issues:**
1. ✅ Add `--wide` flag to show all columns
2. ✅ Auto-show filtered columns (user feedback during testing)
3. ✅ Auto-show Description column when searching (user feedback)
4. ✅ Add `click.Choice` validation for status/classification (PR12-#1, batched)

**Expected Changes:**
- `scripts/project_cli/commands/list_cmd.py` - CLI improvements only
- Manual testing guide updates
- Documentation updates

---

## 🔍 Actual Changes in PR #18

### ✅ In Scope (Original Intent)

1. **CLI Table Display Improvements:**
   - `--wide` flag implementation
   - Auto-show filtered columns (Status/Org/Classification when filtering)
   - Auto-show Description column when searching
   - `click.Choice` validation for status/classification
   - Full-width table layout
   - Column wrapping

2. **Documentation:**
   - Manual testing scenarios (24, 27, 27a, 27b, 27c)
   - User feedback documentation
   - Sourcery review processing

**Files Changed (In Scope):**
- `scripts/project_cli/commands/list_cmd.py` ✅
- `docs/maintainers/planning/features/projects/manual-testing.md` ✅
- `docs/maintainers/feedback/user/pr18-table-column-visibility.md` ✅
- `docs/maintainers/feedback/sourcery/pr18.md` ✅
- `docs/maintainers/planning/features/projects/fix/user-reported-01-cli-table-display.md` ✅

### ⚠️ Out of Scope (Accumulated During Development)

**Issue:** During Scenario 32 testing, discovered import endpoint validation gaps and database enum issues.

**Changes Added (Should Be Separate PR):**

1. **Import Endpoint Validation:**
   - `backend/app/api/projects.py` - Validate classification/status in import
   - `backend/tests/integration/api/test_projects_import.py` - Tests for invalid enum values
   - Related to Scenario 32 testing, not PR #18 scope

2. **Database Error Handling:**
   - Multiple commits trying to handle LookupError for invalid enum values
   - Eventually reverted after fixing database directly
   - Related to Scenario 32 testing issue, not PR #18 scope

**Files Changed (Out of Scope):**
- `backend/app/api/projects.py` ⚠️ (import validation + error handling)
- `backend/app/models/project.py` ⚠️ (error handling, later reverted)
- `backend/tests/integration/api/test_projects_import.py` ⚠️ (import validation tests)

---

## 🎯 Recommendation: Split PR

### Option 1: Keep Current PR, Document Scope (Recommended)

**Keep in PR #18:**
- ✅ All CLI table display improvements
- ✅ Documentation updates
- ✅ Manual testing scenarios

**Defer to Next PR:**
- ⚠️ Import endpoint validation improvements (Scenario 32 related)
- ⚠️ Any remaining database error handling (if needed)

**Action:**
1. Update PR description to clarify scope
2. Note that import validation was discovered during testing
3. Create separate fix plan for import validation
4. Merge PR #18 with current scope
5. Create new PR for import validation fixes

### Option 2: Split Commits (More Work)

**Create Two PRs:**
1. **PR #18:** Only CLI improvements (revert import/database commits)
2. **PR #19:** Import validation and database fixes

**Pros:**
- Clean separation of concerns
- Easier to review
- Better git history

**Cons:**
- More work to split commits
- May need to recreate some work
- Import validation already tested and working

---

## 📊 Commit Analysis

**Total Commits:** 25

**In Scope (CLI Improvements):** ~15 commits
- CLI table display fixes
- User feedback implementations
- Documentation updates
- Manual testing scenarios

**Out of Scope (Import/Database):** ~10 commits
- Import validation fixes
- Database error handling attempts
- Reverts of complex error handling

---

## 💡 Recommended Action Plan

### Immediate (PR #18)

1. **Update PR Description:**
   - Clarify that import validation was discovered during testing
   - Note it's included but was not original scope
   - Document what's in scope vs discovered during testing

2. **Create Fix Plan for Import Validation:**
   - New fix plan: `pr18-discovered-import-validation.md`
   - Document Scenario 32 testing discovery
   - Mark as separate concern

3. **Merge PR #18:**
   - All changes are tested and working
   - Import validation is a good addition
   - Can document scope in PR description

### Future (Post-Merge)

1. **Create Separate PR for Remaining Issues:**
   - Any additional import validation improvements
   - Database error handling refinements (if needed)
   - Keep PRs focused on single concerns

---

## ✅ Decision

**Recommendation:** Keep current PR #18 as-is, but document scope clearly.

**Rationale:**
- All changes are tested and working
- Import validation is a valuable addition discovered during testing
- Splitting would require significant work
- Can document scope in PR description
- Future PRs can be more focused

**Action Items:**
1. Update PR description with scope clarification
2. Create fix plan documenting discovered issues
3. Merge PR #18
4. Use `/post-pr` to update documentation
5. Create separate PR for any future import/database improvements

---

**Last Updated:** 2025-12-05  
**Status:** Ready for merge with scope documentation

