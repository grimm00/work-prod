# Fix Implement Command

Implements fixes from a fix plan batch. Handles TDD workflow, testing, and PR creation for fix batches.

---

## Workflow Overview

**When to use:**
- After fix plans are created with `/fix-plan`
- To implement a specific batch of fixes
- When ready to address deferred issues

**Key principle:** Follow TDD workflow, implement all issues in batch, test thoroughly, create PR.

---

## Usage

**Command:** `@fix-implement [batch-name] [options]`

**Examples:**
- `@fix-implement pr12-batch-medium-low-01` - Implement specific batch
- `@fix-implement pr12-batch-medium-low-01 --skip-tests` - Skip test writing (not recommended)
- `@fix-implement pr12-batch-medium-low-01 --dry-run` - Show implementation plan without executing

**Options:**
- `--skip-tests` - Skip writing tests (not recommended, use only for trivial fixes)
- `--dry-run` - Show what would be implemented without making changes
- `--no-pr` - Implement fixes but don't create PR (for testing)

---

## Step-by-Step Process

### 1. Load Fix Plan

**File:** `docs/maintainers/planning/features/projects/fix/[batch-name].md`

**Extract information:**
- PR number
- Issues in batch
- Priority and effort levels
- File locations
- Implementation steps
- Testing requirements

**Verify:**
- Fix plan exists and is readable
- All issues are documented
- Implementation steps are clear

**Checklist:**
- [ ] Fix plan file found
- [ ] All issues identified
- [ ] Implementation steps reviewed
- [ ] Testing requirements understood

---

### 2. Create Fix Branch

**Branch naming:**
- Format: `fix/[batch-name]`
- Example: `fix/pr12-batch-medium-low-01`

**Steps:**
```bash
# Ensure on develop
git checkout develop
git pull origin develop

# Create fix branch
git checkout -b fix/[batch-name]
```

**Checklist:**
- [ ] Branch created from develop
- [ ] Branch name follows convention
- [ ] Local develop is up-to-date

---

### 3. Implement Each Issue (TDD Workflow)

**For each issue in the batch:**

#### 3a. Write Tests First (RED)

**If tests don't exist:**
- Write failing tests that demonstrate the issue
- Test should fail with current implementation
- Document expected behavior

**If tests exist but need updating:**
- Update tests to reflect desired behavior
- Ensure tests fail initially

**Example:**
```python
def test_cli_uses_click_choice_for_status(client):
    """Test that CLI validates status using click.Choice."""
    runner = CliRunner()
    # This should fail with invalid status
    result = runner.invoke(cli, ['list', '--status', 'invalid'])
    assert result.exit_code != 0
    assert 'invalid choice' in result.output.lower()
```

#### 3b. Implement Fix (GREEN)

**Follow implementation steps from fix plan:**
- Make minimal changes to pass tests
- Follow code style and patterns
- Add comments if needed

**Example:**
```python
@click.option(
    '--status', '-s',
    type=click.Choice(['active', 'paused', 'completed', 'cancelled'], case_sensitive=False),
    help='Filter by project status'
)
```

#### 3c. Refactor (If Needed)

**After tests pass:**
- Improve code quality
- Remove duplication
- Improve readability
- Ensure no regressions

#### 3d. Verify Fix

**Run tests:**
```bash
# Run specific test
pytest backend/tests/path/to/test_file.py::test_name -v

# Run all tests
pytest backend/tests/ -v

# Check coverage
pytest --cov --cov-report=term-missing
```

**Manual testing (if applicable):**
- Test the fix manually
- Verify expected behavior
- Check for regressions

**Checklist:**
- [ ] Tests written (RED)
- [ ] Implementation done (GREEN)
- [ ] Tests passing
- [ ] Refactored if needed
- [ ] No regressions

---

### 4. Commit Each Issue

**Commit message format:**
```
fix(scope): [brief description] (PR##-#N)

[Longer description if needed]

Fixes: PR##-#N
Part of: [batch-name]
```

**Example:**
```bash
git commit -m "fix(cli): use click.Choice for status validation (PR12-#1)

Replace free-form status input with click.Choice to validate
status values at CLI level, improving UX by catching invalid
values early.

Fixes: PR12-#1
Part of: pr12-batch-medium-low-01"
```

**Checklist:**
- [ ] Commit message follows format
- [ ] Issue number referenced
- [ ] Batch name included
- [ ] Changes committed

---

### 5. Complete Batch Implementation

**After all issues in batch are fixed:**

1. **Run full test suite:**
   ```bash
   pytest backend/tests/ -v
   ```

2. **Check coverage:**
   ```bash
   pytest --cov --cov-report=html
   ```

3. **Run linter:**
   ```bash
   pylint backend/ || flake8 backend/
   ```

4. **Verify all issues addressed:**
   - Check fix plan checklist
   - Verify all implementation steps completed
   - Ensure all tests pass

**Checklist:**
- [ ] All issues in batch fixed
- [ ] All tests passing
- [ ] Coverage maintained/improved
- [ ] No linter errors
- [ ] Manual testing complete (if applicable)

---

### 6. Update Fix Plan Status

**File:** `docs/maintainers/planning/features/projects/fix/[batch-name].md`

**Update status:**
```markdown
**Status:** ✅ Complete  
**Completed:** YYYY-MM-DD  
**PR:** #[number]
```

**Update Definition of Done:**
- Mark all items complete
- Add completion notes if needed

**Mark individual issues in Sourcery review:**
- Update review file: `docs/maintainers/feedback/sourcery/pr##.md`
- Mark each issue as "✅ Fixed" in priority matrix
- Add PR number reference

**Example:**
```markdown
| Comment | Priority | Impact | Effort | Status | Notes |
|---------|----------|--------|--------|--------|-------|
| #1 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | ✅ Fixed | Fixed in PR #15 (pr12-batch-medium-low-01) |
```

**Checklist:**
- [ ] Fix plan status updated
- [ ] Definition of Done marked complete
- [ ] Completion date added
- [ ] Individual issues marked in Sourcery review
- [ ] PR number referenced

---

### 7. Update Fix Tracking

**File:** `docs/maintainers/planning/features/projects/fix/README.md`

**Update batch status:**
```markdown
| Batch | Priority | Effort | Issues | Status | File |
|-------|----------|--------|--------|--------|------|
| pr##-batch-medium-low-01 | 🟡 MEDIUM | 🟢 LOW | 2 | ✅ Complete | [pr##-batch-medium-low-01.md](pr##-batch-medium-low-01.md) |
```

**Add completion note:**
```markdown
**Completed:** YYYY-MM-DD via PR #[number]
```

**Checklist:**
- [ ] Batch status updated to "Complete"
- [ ] PR number added
- [ ] Completion date added

---

### 8. Create PR

**PR Title Format:**
```
fix: [Batch Description] ([batch-name])
```

**Example:**
```
fix: CLI validation and test improvements (pr12-batch-medium-low-01)
```

**PR Description Template:**

```markdown
## Fix Batch: [batch-name]

Fixes [N] issues from PR #[number] Sourcery review.

---

## Issues Fixed

- **PR##-#N:** [Description] ([Priority], [Effort])
- **PR##-#M:** [Description] ([Priority], [Effort])

---

## Changes

### [Issue PR##-#N]

**File:** `[file]`

[Description of changes]

**Tests:**
- [Test file] - [What was tested]

### [Issue PR##-#M]

[Similar format]

---

## Testing

- [x] All existing tests passing
- [x] New tests added for fixes
- [x] Coverage maintained/improved ([X]%)
- [x] Manual testing completed (if applicable)
- [x] No regressions introduced

---

## Related

- **Fix Plan:** `docs/maintainers/planning/features/projects/fix/[batch-name].md`
- **Sourcery Review:** `docs/maintainers/feedback/sourcery/pr##.md`
- **Original PR:** #[number]
```

**Create PR:**
```bash
# Push branch
git push origin fix/[batch-name]

# Create PR
gh pr create --title "fix: [Batch Description] ([batch-name])" \
             --body-file /tmp/pr-description.md \
             --base develop \
             --head fix/[batch-name]
```

**Checklist:**
- [ ] PR created
- [ ] Description includes all issues
- [ ] Fix plan linked
- [ ] Tests documented
- [ ] PR link presented to user

---

## TDD Workflow Reminder

**For each issue:**

1. **RED:** Write failing test
   - Test demonstrates the issue
   - Test fails with current code

2. **GREEN:** Implement fix
   - Minimal changes to pass test
   - Test now passes

3. **REFACTOR:** Improve code
   - Clean up implementation
   - Remove duplication
   - Improve readability
   - Ensure tests still pass

---

## Common Issues

### Issue: Tests Fail After Fix

**Solution:**
- Review test expectations
- Check if fix changed behavior
- Update tests if behavior change is correct
- Verify no regressions

### Issue: Multiple Files Affected

**Solution:**
- Implement changes file by file
- Test after each file change
- Commit incrementally if helpful
- Ensure all files updated consistently

### Issue: Fix Conflicts with Recent Changes

**Solution:**
- Rebase on latest develop
- Resolve conflicts
- Re-test after rebase
- Verify fix still works

### Issue: Batch Too Large

**Solution:**
- Can split batch into smaller PRs
- Implement subset of issues
- Create PR for partial batch
- Continue with remaining issues

---

## Tips

### Before Starting

- Review fix plan thoroughly
- Understand all issues in batch
- Check if any dependencies exist
- Ensure test environment ready

### During Implementation

- Follow TDD workflow strictly
- Commit frequently (per issue)
- Test after each change
- Keep commits focused

### After Implementation

- Run full test suite
- Check coverage
- Review code changes
- Update documentation

---

## Reference

**Fix Plans:**
- `docs/maintainers/planning/features/projects/fix/[batch-name].md`

**Fix Tracking:**
- `docs/maintainers/planning/features/projects/fix/README.md`

**Sourcery Reviews:**
- `docs/maintainers/feedback/sourcery/pr##.md`

**Related Commands:**
- `/fix-plan` - Create fix plans from PR review
- `/fix-review` - Review old deferred issues
- `/phase-task` - Individual task implementation (similar workflow)

---

**Last Updated:** 2025-12-04  
**Status:** ✅ Active  
**Next:** Use after `/fix-plan` to implement batches

