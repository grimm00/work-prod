# PR Command

Centralized command for creating pull requests for phases and fix batches. Provides consistent PR creation workflow with appropriate templates and validation.

---

## Workflow Overview

**When to use:**

- After completing a phase (use `--phase`)
- After implementing a fix batch (use `--fix`)
- To create PRs with consistent formatting and validation

**Key principle:** Single command for all PR creation, with context-specific templates and workflows.

---

## Usage

**Command:** `@pr [--phase|--fix] [identifier] [options]`

**Modes:**

1. **Phase PR:** `@pr --phase [phase-number]`
   - Example: `@pr --phase 4`
   - Creates PR for completed phase
   - Uses phase-specific template

2. **Fix PR:** `@pr --fix [batch-name]`
   - Example: `@pr --fix pr12-batch-medium-low-01`
   - Example: `@pr --fix quick-wins-low-low-01` (cross-PR batch)
   - Creates PR for fix batch
   - Uses fix-specific template

**Options:**

- `--dry-run` - Show PR description without creating PR
- `--no-push` - Create PR description but don't push branch or create PR
- `--body-file [path]` - Use custom body file instead of generating
- `--title [title]` - Override default PR title

---

## Step-by-Step Process

### Mode Selection

**Determine mode:**

- `--phase` flag → Phase PR mode
- `--fix` flag → Fix PR mode
- Neither flag → Show usage/help

**Checklist:**

- [ ] Mode determined
- [ ] Identifier provided (phase number or batch name)
- [ ] Current branch matches expected (phase branch or fix branch)

---

## Phase PR Mode (`--phase`)

### 1. Load Phase Information

**Parse phase number:**

- Extract phase number (e.g., `--phase 4` → Phase 4)
- Load phase document: `docs/maintainers/planning/features/[feature]/phase-[N].md`
- Verify phase is complete (status: ✅ Complete)

**Extract information:**

- Phase number and name
- Completion date
- Tasks completed
- Deliverables
- Related PRs (if any)

**Verify:**

- Phase document exists
- Phase marked as complete
- All tasks completed
- Branch name matches phase (e.g., `feat/phase-[N]-...`)

**Checklist:**

- [ ] Phase document found
- [ ] Phase marked complete
- [ ] Current branch is phase branch

---

### 2. Generate PR Description (Phase)

**Template:**

```markdown
## Phase [N]: [Phase Name]

**Status:** ✅ Complete  
**Completed:** YYYY-MM-DD

---

## Summary

[Brief description of what was accomplished in this phase]

---

## Tasks Completed

- [x] Task 1
- [x] Task 2
- [x] Task 3

---

## Changes

### [Category 1]

**Files Modified:**
- `[file1]` - [description]
- `[file2]` - [description]

**Key Changes:**
- [Change description]
- [Change description]

### [Category 2]

[Similar format]

---

## Testing

- [x] All tests passing ([N] tests)
- [x] Coverage maintained/improved ([X]%)
- [x] Manual testing completed
- [x] No regressions introduced

---

## Deliverables

- [Deliverable 1]
- [Deliverable 2]

---

## Related

- **Phase Plan:** `docs/maintainers/planning/features/[feature]/phase-[N].md`
- **Feature Status:** `docs/maintainers/planning/features/[feature]/status-and-next-steps.md`
- **Manual Testing:** `docs/maintainers/planning/features/[feature]/manual-testing.md`
```

**Checklist:**

- [ ] PR description generated
- [ ] All tasks listed
- [ ] Changes documented
- [ ] Testing status included
- [ ] Related docs linked

---

### 3. Create Phase PR

**PR Title:**

```
feat: Phase [N] - [Phase Name]
```

**Steps:**

```bash
# Verify branch
git branch --show-current

# Push branch (if not already pushed)
git push origin feat/phase-[N]-[name]

# Create PR
gh pr create --title "feat: Phase [N] - [Phase Name]" \
             --body-file /tmp/pr-description-phase[N].md \
             --base develop \
             --head feat/phase-[N]-[name]
```

**Checklist:**

- [ ] Branch pushed
- [ ] PR created
- [ ] Description includes all tasks
- [ ] Related docs linked
- [ ] PR link presented to user

---

## Fix PR Mode (`--fix`)

### 1. Load Fix Batch Information

**Parse batch name:**

- Extract batch name (e.g., `quick-wins-low-low-01`)
- Determine batch type:
  - PR-Specific: Starts with `pr##-batch-`
  - Cross-PR: Does NOT start with `pr##-batch-`

**Load fix plan:**

- PR-Specific: `docs/maintainers/planning/features/[feature]/fix/pr##/[batch-name].md`
- Cross-PR: `docs/maintainers/planning/features/[feature]/fix/cross-pr/[batch-name].md`

**Extract information:**

- Batch name and type
- Issues fixed
- Source PR(s)
- Files modified
- Testing status
- Completion date

**Verify:**

- Fix plan exists
- Batch marked as complete
- All issues fixed
- Tests passing
- Current branch is fix branch (e.g., `fix/[batch-name]`)

**Checklist:**

- [ ] Batch type determined
- [ ] Fix plan found
- [ ] Batch marked complete
- [ ] Current branch is fix branch

---

### 2. Generate PR Description (Fix)

**For PR-Specific Batches:**

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

- [x] All existing tests passing ([N] tests)
- [x] New tests added for fixes
- [x] Coverage maintained/improved ([X]%)
- [x] Manual testing completed (if applicable)
- [x] No regressions introduced

---

## Related

- **Fix Plan:** `docs/maintainers/planning/features/[feature]/fix/pr##/[batch-name].md`
- **Sourcery Review:** `docs/maintainers/feedback/sourcery/pr##.md`
- **Original PR:** #[number]
```

**For Cross-PR Batches:**

```markdown
## Fix Batch: [batch-name] (Cross-PR)

Fixes [N] issues from multiple PRs' Sourcery reviews.

**Source PRs:** PR #[number], PR #[number], ...

---

## Issues Fixed

- **PR##-#N:** [Description] ([Priority], [Effort]) - Source: PR #[number]
- **PR##-#M:** [Description] ([Priority], [Effort]) - Source: PR #[number]

---

## Changes

### [Issue PR##-#N] (from PR #[number])

**File:** `[file]`

[Description of changes]

**Tests:**

- [Test file] - [What was tested]

### [Issue PR##-#M] (from PR #[number])

[Similar format]

---

## Testing

- [x] All existing tests passing ([N] tests)
- [x] New tests added for fixes
- [x] Coverage maintained/improved ([X]%)
- [x] Manual testing completed (if applicable)
- [x] No regressions introduced

---

## Related

- **Fix Plan:** `docs/maintainers/planning/features/[feature]/fix/cross-pr/[batch-name].md`
- **Fix Review Report:** `docs/maintainers/planning/features/[feature]/fix/fix-review-report-YYYY-MM-DD.md`
- **Source PRs:** PR #[number], PR #[number], ...
- **Sourcery Reviews:**
  - `docs/maintainers/feedback/sourcery/pr##.md`
  - `docs/maintainers/feedback/sourcery/pr##.md`
```

**Checklist:**

- [ ] PR description generated
- [ ] All issues listed
- [ ] Changes documented
- [ ] Testing status included
- [ ] Related docs linked
- [ ] Source PRs listed (for cross-PR batches)

---

### 3. Create Fix PR

**PR Title:**

**For PR-Specific Batches:**
```
fix: [Batch Description] ([batch-name])
```

**For Cross-PR Batches:**
```
fix: [Batch Description] ([batch-name], cross-PR batch)
```

**Steps:**

```bash
# Verify branch
git branch --show-current

# Push branch (if not already pushed)
git push origin fix/[batch-name]

# Create PR
gh pr create --title "fix: [Batch Description] ([batch-name])" \
             --body-file /tmp/pr-description-fix-[batch-name].md \
             --base develop \
             --head fix/[batch-name]
```

**Checklist:**

- [ ] Branch pushed
- [ ] PR created
- [ ] Description includes all issues
- [ ] Fix plan linked
- [ ] Tests documented
- [ ] PR link presented to user

---

## Common Workflow Steps

### Pre-PR Validation

**For both modes:**

1. **Verify branch:**
   ```bash
   git branch --show-current
   ```

2. **Check uncommitted changes:**
   ```bash
   git status --short
   ```

3. **Verify tests pass:**
   ```bash
   cd backend && pytest -v
   ```

4. **Check coverage:**
   ```bash
   pytest --cov --cov-report=term-missing
   ```

**Checklist:**

- [ ] On correct branch
- [ ] No uncommitted changes
- [ ] All tests passing
- [ ] Coverage acceptable

---

## Options

### `--dry-run`

**Behavior:**

- Generate PR description
- Display to user
- Do NOT push branch
- Do NOT create PR

**Use case:**

- Preview PR description before creating
- Verify template formatting
- Check for missing information

---

### `--no-push`

**Behavior:**

- Generate PR description
- Save to file
- Do NOT push branch
- Do NOT create PR

**Use case:**

- Generate description for manual PR creation
- Review before pushing
- Custom PR creation workflow

---

### `--body-file [path]`

**Behavior:**

- Use provided file as PR body
- Skip description generation
- Still validate branch and mode

**Use case:**

- Custom PR descriptions
- Pre-written descriptions
- Template variations

---

### `--title [title]`

**Behavior:**

- Override default PR title
- Still use generated body (unless `--body-file` used)

**Use case:**

- Custom titles
- Special formatting
- Consistency requirements

---

## Integration with Other Commands

### Phase Workflow

1. `/phase-task` - Implement phase tasks
2. `/pr --phase [N]` - Create phase PR
3. `/post-pr` - Update documentation after merge

### Fix Workflow

1. `/fix-plan` - Create fix plans
2. `/fix-implement [batch-name]` - Implement fixes
3. `/pr --fix [batch-name]` - Create fix PR
4. `/post-pr` - Update documentation after merge

---

## Common Issues

### Issue: Branch Name Mismatch

**Solution:**

- Verify current branch matches expected
- For phases: Should be `feat/phase-[N]-...`
- For fixes: Should be `fix/[batch-name]`
- Create branch if needed

### Issue: Phase/Fix Not Complete

**Solution:**

- Verify phase/fix plan marked complete
- Check all tasks/issues completed
- Update status if needed
- Re-run command after completion

### Issue: Missing Information

**Solution:**

- Check phase/fix plan completeness
- Verify all required fields present
- Update documentation if needed
- Re-run command

---

## Tips

### Before Creating PR

- Review generated description
- Verify all information correct
- Check related documentation links
- Ensure tests passing

### After Creating PR

- Share PR link with team
- Update tracking documents
- Monitor PR status
- Use `/post-pr` after merge

---

## Reference

**Phase Documents:**

- `docs/maintainers/planning/features/[feature]/phase-[N].md`

**Fix Plans:**

- PR-Specific: `docs/maintainers/planning/features/[feature]/fix/pr##/[batch-name].md`
- Cross-PR: `docs/maintainers/planning/features/[feature]/fix/cross-pr/[batch-name].md`

**Related Commands:**

- `/phase-task` - Implement phase tasks
- `/phase-pr` - Legacy phase PR command (use `/pr --phase` instead)
- `/fix-implement` - Implement fix batches
- `/post-pr` - Post-merge documentation updates

---

**Last Updated:** 2025-12-05  
**Status:** ✅ Active  
**Next:** Use `/pr --phase [N]` for phase PRs, `/pr --fix [batch-name]` for fix PRs

