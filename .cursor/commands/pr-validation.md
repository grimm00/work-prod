# PR Validation & Review Command

Use this command when a PR is already open to run manual testing, update documentation, and perform code review in one workflow.

---

## Workflow Overview

**When to use:**
- PR is already created and open
- Need to validate features with manual testing
- Need to run Sourcery review (dt-review)
- Want to update manual testing guide with scenarios

**Key principle:** Combines manual testing execution, documentation updates, and code review into a single workflow.

---

## Usage

**Command:** `/pr-validation [pr-number] [phase-number]`

**Examples:**
- `/pr-validation 12 4` - Validate PR #12 for Phase 4
- `/pr-validation 10 3` - Validate PR #10 for Phase 3

---

## Step-by-Step Process

### 1. Verify PR Status

**Check PR exists and is open:**

```bash
gh pr view [pr-number] --json state,title,headRefName
```

**Expected:**
- PR state: `OPEN`
- PR title matches phase
- Head branch exists

---

### 1a. Restore Unrelated Files (Cursor IDE Bug Fix)

**Issue:** Cursor IDE may modify unrelated files when opening them. These should be restored before proceeding.

**Process:**

1. **Check modified files:**
   ```bash
   git status --short
   ```

2. **Identify Phase-related files:**
   - Review what files should actually be modified for this phase
   - Keep only files that are part of the phase implementation

3. **Restore unrelated files:**
   ```bash
   # Restore all unrelated files (adjust paths as needed)
   git restore [unrelated-file-1] [unrelated-file-2] ...
   
   # Or restore all modified files except phase-specific ones
   git restore $(git diff --name-only | grep -v "phase-[N]\.md\|projects\.py\|test_projects\.py\|list_cmd\.py")
   ```

4. **Verify only phase files remain:**
   ```bash
   git status --short
   ```

**Common unrelated files to restore:**
- `__init__.py` files (often just whitespace changes)
- Documentation files unrelated to the phase
- Frontend files (if backend phase)
- Inventory/script files
- Config files (`.gitignore`, `pytest.ini`, `requirements.txt`) unless actually changed

**After restoration:**
- [ ] Only phase-related files remain modified
- [ ] No accidental changes to unrelated code
- [ ] Ready to proceed with validation

---

### 2. Update Manual Testing Guide (MANDATORY)

**File:** `docs/maintainers/planning/features/projects/manual-testing.md`

**IMPORTANT:** This step is MANDATORY for all PRs. Always check and update the manual testing guide, even if scenarios already exist.

**Process:**

1. **Review PR changes to identify new features:**
   - Check what endpoints/commands were added/modified
   - Identify all user-facing functionality
   - Note any validation or error handling changes

2. **Check if scenarios exist:**
   - Search manual testing guide for relevant scenarios
   - Check if all new features are covered
   - Verify scenarios match current implementation

3. **Add missing scenarios:**
   - If scenarios are missing, add them using the template below
   - For phase PRs: Add scenarios for all new functionality
   - For fix PRs: Add scenarios if validation/error handling changed
   - Use consistent format and numbering

4. **Update header if needed:**
   - Add PR number to header if not already listed
   - Update "Last Updated" date
   - Note which scenarios were added for this PR

5. **Update acceptance criteria:**
   - Add checkboxes for new functionality
   - Ensure all new features are covered

**Scenario Template:**
```markdown
### Scenario N: [Feature Name] - [Test Type]

**Test:** [Brief description]

**Prerequisites:** [Any setup needed]

**[API/CLI] Test:**
```bash
[Command or curl example]
# Expected: [Expected result]
```

**Verification:**
```bash
[Verification command]
# Expected: [What to verify]
```

**Expected Result:** ✅ [Success criteria]
```

**Common scenarios to add:**

**For Filtering Features:**
- Filter by each filter type (status, organization, classification)
- Multiple filters combined
- Invalid filter values
- Empty results
- CLI filter flags

**For Search Features:**
- Search by name
- Search by description
- Case-insensitive search
- Partial match
- No results found
- Combined with filters
- CLI search flag

**For New Endpoints:**
- Basic functionality (happy path)
- Error cases (404, 400, validation)
- Edge cases
- CLI equivalent (if applicable)

**After updating:**
- [ ] Scenarios added for all new functionality
- [ ] Header updated with PR number
- [ ] Acceptance criteria updated
- [ ] Scenarios committed to PR branch
- [ ] Note which scenarios were added

---

### 3. Run Manual Testing Scenarios

**Location:** `docs/maintainers/planning/features/projects/manual-testing.md`

**Prerequisites:**
- Backend server running: `cd backend && python run.py`
- Server accessible at `http://localhost:5000`
- Health check passes: `curl http://localhost:5000/api/health`

**Process:**

1. **Identify scenarios to test:**
   - Review manual testing guide
   - Find scenarios for this phase
   - Note scenario numbers (e.g., "Scenarios 16-28 for Phase 4")

2. **Run scenarios in order:**
   - Some scenarios depend on previous state
   - Run each scenario completely
   - Document results (✅ pass / ❌ fail)

3. **For each scenario:**

   **API Tests:**
   ```bash
   # Run curl command from scenario
   curl [endpoint] [options]
   
   # Verify response matches expected
   # Check status code, JSON structure, values
   ```

   **CLI Tests:**
   ```bash
   cd /Users/cdwilson/Projects/work-prod/scripts/project_cli
   
   # Run CLI command from scenario
   ./proj [command] [options]
   
   # Verify output matches expected
   # Check formatting, values, error messages
   ```

4. **Document results and check off scenarios:**
   - For each scenario that passes, check off its checkboxes in the manual testing guide
   - Change `- [ ]` to `- [x]` for each verification item that passes
   - Mark "Expected Result:" line with ✅ if all checks pass
   - Note any failures or issues (keep checkboxes unchecked if scenario fails)
   - Update acceptance criteria checklist at the end of the guide

**Common Issues:**

- **Database state:** If scenarios fail due to missing data, check prerequisites
- **Server not running:** Ensure backend is running before testing
- **Port conflicts:** Verify port 5000 is available
- **CLI path:** Ensure you're in the correct directory for CLI commands

**After manual testing:**
- [ ] All scenarios passed
- [ ] Checkboxes checked off (`- [ ]` → `- [x]`) for passing scenarios
- [ ] Expected Result lines marked with ✅ for passing scenarios
- [ ] Any failures documented (keep checkboxes unchecked)
- [ ] Acceptance criteria updated
- [ ] Results committed to PR branch

---

### 4. Run Sourcery Review (dt-review)

**Important:** 
- Run from the work-prod directory to ensure review is for the correct repository
- Use the path parameter to save directly to the project's documentation structure
- This avoids creating an `admin/` directory at the root level
- **Note:** If review is not available or fails, that's okay - continue without review

**Process:**

1. **Navigate to work-prod:**
   ```bash
   cd /Users/cdwilson/Projects/work-prod
   ```

2. **Ensure output directory exists:**
   ```bash
   mkdir -p docs/maintainers/feedback/sourcery
   ```

3. **Run review with custom path:**
   ```bash
   dt-review [pr-number] docs/maintainers/feedback/sourcery/pr##.md
   ```

   **Example:**
   ```bash
   dt-review 19 docs/maintainers/feedback/sourcery/pr19.md
   ```

   **Note:** The `dt-review` command is available in PATH at `/usr/local/bin/dt-review`, so it can be called directly without the full path.

   **If review fails or is not available:**
   - This is acceptable - some PRs may not have reviews available
   - Continue with validation workflow
   - Note in summary that review was skipped
   - Can run review manually later if needed

4. **Review will be saved directly to:**
   `docs/maintainers/feedback/sourcery/pr##.md`

**Note:** The `dt-review` command accepts a second argument for the output path. This saves directly to the project's documentation structure instead of creating an `admin/` directory at the root level. The dev-toolkit will be updated in the future to use the new docs structure by default.

**Expected:**
- Review file created/updated (if available)
- Contains Sourcery comments and suggestions (if review succeeded)
- Organized by file/line number
- **If review not available:** Continue without review - this is acceptable

---

### 5. Fill Out Priority Matrix (If Review Available)

**File:** `docs/maintainers/feedback/sourcery/pr##.md`

**Skip this step if:**
- Sourcery review file doesn't exist
- Review failed to generate
- No comments in review file

**If review is available:**

**For each Sourcery comment:**

Add priority assessment after the comment:

```markdown
**Priority:** CRITICAL 🔴 / HIGH 🟠 / MEDIUM 🟡 / LOW 🟢
**Impact:** CRITICAL 🔴 / HIGH 🟠 / MEDIUM 🟡 / LOW 🟢
**Effort:** LOW 🟢 / MEDIUM 🟡 / HIGH 🟠 / VERY_HIGH 🔴
**Action:** Fix now / Defer to next PR / Document for future
```

**Priority Guidelines:**

**CRITICAL 🔴:**
- Security vulnerabilities
- Data loss risks
- Breaking API changes
- Test failures

**HIGH 🟠:**
- Performance issues
- Code quality problems
- Maintainability concerns
- Missing error handling

**MEDIUM 🟡:**
- Code style improvements
- Refactoring opportunities
- Documentation gaps
- Minor optimizations

**LOW 🟢:**
- Naming suggestions
- Style preferences
- Minor readability improvements
- Optional enhancements

**After priority matrix (if review available):**
- [ ] All comments assessed
- [ ] CRITICAL/HIGH items identified
- [ ] Action plan documented
- [ ] Matrix committed to PR branch

**If review not available:**
- [ ] Note in summary that review was skipped
- [ ] Continue with validation workflow

---

### 6. Address Critical Issues (If Any)

**If CRITICAL 🔴 or HIGH 🟠 issues found:**

1. **Create fix branch (if not already on PR branch):**
   ```bash
   git checkout feat/phase-N-[description]
   ```

2. **Implement fixes:**
   - Follow fix plans
   - Write tests for fixes
   - Run full test suite
   - Commit fixes

3. **Update PR:**
   - Push fixes to PR branch
   - Update PR description with fixes
   - Re-run manual testing if needed

**If only LOW/MEDIUM issues:**
- Document in fix tracking
- Can be deferred to future PR
- Proceed with merge approval

---

### 7. Update PR Description (If Needed)

**If manual testing or review revealed issues:**

Update PR description to include:
- Manual testing results
- Sourcery review summary
- Critical issues addressed
- Deferred issues documented

**PR Description Updates:**

```markdown
## Testing

- [x] All automated tests passing ([N] tests)
- [x] Coverage: [X]% (maintained/improved)
- [x] Manual testing complete ([N] scenarios)
- [x] Sourcery review complete ([N] comments)

## Review Summary

**Sourcery Review:**
- Total comments: [N]
- CRITICAL: [N] (all addressed)
- HIGH: [N] (all addressed)
- MEDIUM: [N] (deferred to next PR)
- LOW: [N] (documented for future)

**Manual Testing:**
- Scenarios tested: [N]
- All scenarios passed: ✅
- Checkboxes checked off: ✅ (all passing scenarios marked)
- Expected Result lines marked: ✅ (all passing scenarios)
- Issues found: [None / List issues]
```

---

### 8. Summary Report

**Present to user:**

```markdown
## PR Validation Complete

**PR:** #[pr-number] - [PR Title]

### Manual Testing
- ✅ Scenarios tested: [N]
- ✅ All scenarios passed
- ✅ Checkboxes checked off for passing scenarios
- ✅ Expected Result lines marked with ✅
- ⚠️ Issues found: [None / List]

### Code Review
- ✅ Sourcery review complete (or ⚠️ Review not available - skipped)
- ✅ Priority matrix filled out (or ⚠️ Skipped - no review)
- ⚠️ Critical issues: [N] (all addressed) or [None - no review]
- ⚠️ Deferred issues: [N] or [None - no review]

### Next Steps
- [ ] User review PR changes
- [ ] User approve merge (if ready)
- [ ] Merge PR
- [ ] Run `/post-pr` command for documentation updates
```

---

## Common Issues

### Issue: Manual Testing Scenarios Missing

**Solution:**
- Review PR changes to identify features
- Add scenarios using template from `/phase-pr` command
- Ensure scenarios cover all new functionality
- Test at least one scenario to verify format

### Issue: Backend Server Not Running

**Solution:**
```bash
cd backend
source ../venv/bin/activate
python run.py
```

Verify with:
```bash
curl http://localhost:5000/api/health
```

### Issue: dt-review Not Found

**Solution:**
- The `dt-review` command should be available in PATH at `/usr/local/bin/dt-review`
- Try calling it directly: `dt-review [pr-number] [output-path]`
- Verify it's in PATH: `which dt-review` (should show `/usr/local/bin/dt-review`)
- If not found, check if dev-toolkit is installed and `dt-review` is symlinked to `/usr/local/bin/`

### Issue: Sourcery Review File Not Created

**Solution:**
- **This is acceptable** - some PRs may not have reviews available
- Check if review completed successfully
- Verify PR number is correct
- Ensure output directory exists: `mkdir -p docs/maintainers/feedback/sourcery`
- Verify the path parameter is correct: `docs/maintainers/feedback/sourcery/pr##.md`
- Check that you're running from the work-prod directory
- **If review is not available:** Continue without review - this is acceptable for the workflow

### Issue: Manual Testing Fails

**Solution:**
- Check database state (may need to reset)
- Verify prerequisites for scenarios
- Check server logs for errors
- Ensure all dependencies installed
- Document failures and fix before proceeding

---

## Checklist Summary

**Before running command:**
- [ ] PR is open and accessible
- [ ] Backend server is running
- [ ] Manual testing guide exists
- [ ] dev-toolkit is available

**During execution:**
- [ ] Manual testing guide updated with scenarios (MANDATORY)
- [ ] All scenarios tested and passed
- [ ] Checkboxes checked off (`- [ ]` → `- [x]`) for passing scenarios
- [ ] Expected Result lines marked with ✅ for passing scenarios
- [ ] Sourcery review completed
- [ ] Priority matrix filled out
- [ ] Critical issues addressed (if any)

**After execution:**
- [ ] Results documented
- [ ] PR description updated (if needed)
- [ ] Summary presented to user
- [ ] Ready for user review/approval

---

## Tips

**Manual Testing:**
- Run scenarios in order (some depend on previous state)
- Document results immediately
- Take screenshots if helpful
- Note any unexpected behavior

**Code Review:**
- Be thorough with priority assessment
- Don't skip LOW priority items (document them)
- Address CRITICAL items before merge
- Document deferred items clearly

**Workflow:**
- This command combines multiple steps for efficiency
- Can be run multiple times if PR is updated
- Always verify results before proceeding
- Present clear summary to user

---

## Reference

**Manual Testing:**
- `docs/maintainers/planning/features/projects/manual-testing.md`

**Code Review:**
- `docs/maintainers/feedback/sourcery/pr##.md`

**PR Management:**
- GitHub CLI: `gh pr view [number]`
- PR description updates

**Related Commands:**
- `/phase-pr` - Create PR and initial validation
- `/post-pr` - Post-merge documentation updates
- `/int-opp` - Document phase learnings

