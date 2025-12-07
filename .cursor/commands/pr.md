# PR Command

Centralized command for creating pull requests for phases and fix batches. Provides consistent PR creation workflow with appropriate templates and validation.

---

## Workflow Overview

**When to use:**

- After completing a phase (use `--phase`)
- After implementing a fix batch (use `--fix`)
- After completing release transition steps (use `--release`)
- To create PRs with consistent formatting and validation

**Key principle:** Single command for all PR creation, with context-specific templates and workflows.

---

## Usage

**Command:** `@pr [--phase|--fix|--release] [identifier] [options]`

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

3. **Release PR:** `@pr --release [version]`
   - Example: `@pr --release v0.1.0`
   - Creates PR for release transition
   - Uses release-specific template

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
- `--release` flag → Release PR mode
- Neither flag → Show usage/help

**Checklist:**

- [ ] Mode determined
- [ ] Identifier provided (phase number, batch name, or version)
- [ ] Current branch matches expected (phase branch, fix branch, or release branch)

---

## Phase PR Mode (`--phase`)

### 1. Pre-PR Validation Checklist

**Run these checks before proceeding:**

#### Automated Testing
- [ ] Run full test suite: `pytest tests/ -v`
- [ ] All tests passing (no failures)
- [ ] Coverage maintained or improved
- [ ] Check coverage report: `pytest --cov --cov-report=html`
- [ ] No test warnings (except known deprecations)

#### Code Quality
- [ ] Run linter: `pylint backend/` or `flake8 backend/`
- [ ] No linter errors
- [ ] Code follows project patterns
- [ ] No TODO/FIXME comments left behind

#### Manual Testing
- [ ] Check if manual testing guide exists: `docs/maintainers/planning/features/[feature]/manual-testing.md`
- [ ] **REQUIRED:** Add new scenarios for phase features (see step 1a)
- [ ] If guide exists, run ALL scenarios in order
- [ ] Document any issues found during manual testing
- [ ] Fix any bugs found before proceeding
- [ ] Update manual testing guide if scenarios need adjustment

**Manual Testing Location:**
- Feature-specific: `docs/maintainers/planning/features/[feature]/manual-testing.md`
- Run scenarios in order (some may depend on previous state)
- Note database state requirements

#### Documentation
- [ ] Phase document updated (all tasks marked complete: `- [x]`)
- [ ] README files updated (API docs, CLI docs)
- [ ] No broken links in documentation
- [ ] Code comments added where needed

#### Git State
- [ ] All changes committed to feature branch
- [ ] Feature branch is up-to-date with `develop`
- [ ] No uncommitted changes
- [ ] Commit messages follow conventional format

---

### 1a. Add Manual Testing Scenarios

**File:** `docs/maintainers/planning/features/[feature]/manual-testing.md`

**When to add scenarios:**
- New API endpoints added
- New CLI commands added
- New features that need user verification
- Filtering/search capabilities
- Any user-facing functionality

**Checklist:**
- [ ] Review phase features and identify what needs manual testing
- [ ] Check current scenario count (last scenario number)
- [ ] Add scenarios for each new feature
- [ ] Number scenarios sequentially (continue from last number)
- [ ] Include both curl and CLI examples (if applicable)
- [ ] Add verification steps
- [ ] Note any prerequisites or dependencies
- [ ] Update "Phases" field in document header if needed

**Scenario Template:**

```markdown
### Scenario N: [Feature Name] - [Method]

**Test:** [What this scenario tests]

**Prerequisites:** [Any required setup or previous scenarios]

**API Test (if applicable):**
```bash
# curl command
curl [endpoint] [options]
# Expected: [expected response]
```

**CLI Test (if applicable):**
```bash
# CLI command
./proj [command] [options]
# Expected Output:
# [example output]
```

**Verification:**
```bash
# Commands to verify the result
# Expected: [expected result]
```

**Expected Result:** ✅ [Success criteria]
```

**Common Scenario Types:**

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

**After adding scenarios:**
- [ ] Update scenario count in document header if needed
- [ ] Verify scenarios are numbered sequentially
- [ ] Check that prerequisites are clear
- [ ] Ensure scenarios can be run in order (or note dependencies)
- [ ] Test at least one scenario manually to verify format

---

### 2. Load Phase Information

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
- [ ] Pre-PR validation checklist complete

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

### 3. Update Feature Documentation

**Files to check:**

**API Documentation:**
- `backend/README.md` - Add new endpoints
- Update endpoint list
- Add request/response examples

**CLI Documentation:**
- `scripts/project_cli/README.md` - Add new commands
- Update command examples
- Add usage notes

**Manual Testing Guide:**
- `docs/maintainers/planning/features/[feature]/manual-testing.md`
- **REQUIRED:** Add new scenarios for phase features (see step 1a)
- Update scenario numbering
- Add prerequisites/notes

---

### 4. Final Test Run

**Before creating PR, run:**

```bash
# Full test suite
cd backend && pytest tests/ -v

# Coverage check
pytest --cov --cov-report=term-missing

# Linter check
pylint backend/ || flake8 backend/
```

**Expected:**
- All tests pass
- Coverage maintained/improved
- No linter errors

---

### 5. Create Phase PR

**PR Title:**

```
feat: [Phase N Description] (Phase N)
```

**Examples:**
- `feat: Delete & Archive Projects (Phase 3)`
- `feat: Create & Update Projects (Phase 2)`

**Steps:**

```bash
# Verify branch
git branch --show-current

# Push branch (if not already pushed)
git push origin feat/phase-[N]-[name]

# Create PR using GitHub CLI
# Option A: Use temporary file (auto-cleaned)
cat > /tmp/pr-description-phase[N].md << 'EOF'
[paste PR description content]
EOF

gh pr create --title "feat: [Phase N Description] (Phase N)" \
             --body-file /tmp/pr-description-phase[N].md \
             --base develop \
             --head feat/phase-[N]-[name]

# Clean up
rm /tmp/pr-description-phase[N].md
```

**Note:** PR description files are gitignored (`pr-description*.md`) to prevent accidental commits.

**After PR creation:**

1. **Get PR number from output** (e.g., `#12`)
2. **STOP HERE - Present PR link to user**
   - DO NOT auto-merge
   - DO NOT proceed to Sourcery review yet
   - Wait for user acknowledgment

**Checklist:**

- [ ] Branch pushed
- [ ] PR created
- [ ] Description includes all tasks
- [ ] Related docs linked
- [ ] PR link presented to user
- [ ] User acknowledges PR creation

---

### 6. Present PR to User

**After PR is created:**

1. **Display PR information:**
   - PR number and URL
   - PR title
   - Branch information

2. **Next steps:**
   - Use `/pr-validation` command to run manual testing, Sourcery review, and update documentation
   - Or proceed with manual review and testing

**Note:** Sourcery review (`dt-review`) is handled by the `/pr-validation` command, not during PR creation.

---

### 7. Address Critical Issues (If Any)

**If CRITICAL/HIGH issues found:**

1. **Create fix branch:**
   ```bash
   git checkout -b fix/pr##-critical-issues
   ```

2. **Implement fixes:**
   - Use `/fix-implement` command with fix batch name
   - Follow fix plans
   - Write tests for fixes
   - Run full test suite
   - Commit fixes

3. **Update PR:**
   - Push fix branch
   - Update PR description with fixes
   - Re-run `/pr-validation` if needed (includes Sourcery review)

**If only LOW/MEDIUM issues:**
- Document in fix tracking
- Can be deferred to future PR
- Proceed with merge approval

---

### 8. Get User Approval

**Before merging:**

- [ ] PR created and link presented to user
- [ ] `/pr-validation` command run (includes manual testing and Sourcery review)
- [ ] Manual testing completed
- [ ] CRITICAL/HIGH issues addressed (if any)
- [ ] User explicitly approves merge

**DO NOT auto-merge** - Always wait for explicit user approval.

**After merge:**
- Use `/post-pr` command to update documentation

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

## Release PR Mode (`--release`)

### 1. Load Release Information

**Parse version:**
- Extract version (e.g., `v0.1.0`)
- Verify version format (should match semantic versioning)

**Load transition plan:**
- `docs/maintainers/planning/releases/[version]/transition-plan.md`

**Extract information:**
- Version number
- Release steps completed
- Release checklist status
- Release notes status
- Tagging status
- Post-release verification status

**Verify:**
- Transition plan exists
- All steps marked complete
- Release checklist complete
- Release notes finalized
- Current branch is release branch (e.g., `release/[version]`)

**Checklist:**
- [ ] Version format valid
- [ ] Transition plan found
- [ ] All steps complete
- [ ] Current branch is release branch

---

### 2. Generate PR Description (Release)

**PR Title:**
```
chore: Release [version]
```

**PR Description Template:**

```markdown
## Release [version]

[Brief description of release - e.g., "MVP Release" or "First production release"]

---

## What's Included

### Release Preparation
- Release checklist completed
- Release notes finalized
- Pre-release verification complete
- Version tagged: [version]
- Release documentation updated

### Verification
- All tests passing ([N] tests)
- Test coverage: [X]%
- Production readiness verified
- Deployment guide reviewed
- Post-release verification complete (if applicable)

### Release Steps Completed
- [x] Step 1: Finalize Release Documentation
- [x] Step 2: Complete Pre-Release Verification
- [x] Step 3: Version Tagging and Release
- [x] Step 4: Update Release Documentation
- [x] Step 5: Post-Release Verification
- [x] Step 6: Release Communication

---

## Testing

- [x] All automated tests passing ([N] tests)
- [x] Coverage: [X]% (maintained/improved)
- [x] Pre-release verification complete
- [x] Post-release verification complete (if applicable)
- [ ] Sourcery review completed (if code changes)

---

## Release Artifacts

- **Release Checklist:** `docs/maintainers/planning/releases/[version]/checklist.md`
- **Release Notes:** `docs/maintainers/planning/releases/[version]/release-notes.md`
- **Transition Plan:** `docs/maintainers/planning/releases/[version]/transition-plan.md`

---

## Related

- **Transition Plan:** `docs/maintainers/planning/releases/[version]/transition-plan.md`
- **Release Checklist:** `docs/maintainers/planning/releases/[version]/checklist.md`
- **Release Notes:** `docs/maintainers/planning/releases/[version]/release-notes.md`
- **Release Hub:** `docs/maintainers/planning/releases/README.md`
```

---

### 3. Pre-PR Validation (Release)

**Before creating PR:**

- [ ] All release steps completed
- [ ] Release checklist complete
- [ ] Release notes finalized
- [ ] Version tagged (if Step 3 complete)
- [ ] All verification steps passed
- [ ] Release documentation updated
- [ ] Transition plan updated (all steps marked complete)
- [ ] Current branch is release branch
- [ ] All changes committed

**Verification commands:**
```bash
# Verify tag exists
git tag -l [version]

# Verify branch
git branch --show-current

# Verify tests passing
pytest backend/ -v
```

**Checklist:**
- [ ] On release branch
- [ ] No uncommitted changes
- [ ] All verification steps passed
- [ ] Release documentation complete

---

### 4. Create PR (Release)

**Steps:**

1. **Push release branch:**
   ```bash
   git push origin release/[version]
   ```

2. **Create PR using GitHub CLI:**
   ```bash
   gh pr create --title "chore: Release [version]" \
                --body-file /tmp/pr-description-release-[version].md \
                --base develop \
                --head release/[version]
   ```

3. **Get PR number from output** (e.g., `#36`)

4. **STOP HERE - Present PR link to user**
   - DO NOT auto-merge
   - DO NOT proceed to Sourcery review yet
   - Wait for user acknowledgment

---

### 5. Sourcery Review (Release)

**After PR created and user acknowledges:**

- Run Sourcery review if code changes exist: `dt-review`
- Review feedback saved to: `docs/maintainers/feedback/sourcery/pr##.md`
- Fill out priority matrix (if review run)
- Address CRITICAL/HIGH issues before merge (if any)

**Note:** Release PRs may have minimal code changes (mostly documentation), so Sourcery review may be optional.

---

### 6. Post-Merge (Release)

**After merge:**
- Use `/post-pr --release [version]` command to update documentation

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

1. `/task-phase` - Implement phase tasks
2. `/task-release` - Implement release transition tasks
2. `/pr --phase [N]` - Create phase PR
3. `/post-pr` - Update documentation after merge

### Fix Workflow

1. `/fix-plan` - Create fix plans
2. `/fix-implement [batch-name]` - Implement fixes
3. `/pr --fix [batch-name]` - Create fix PR
4. `/post-pr --fix [batch-name]` - Update documentation after merge

### Release Workflow

1. `/reflection-artifacts --type release` - Generate release artifacts
2. `/transition-plan --from-artifacts` - Create transition plan
3. `/task-release [version] [step]` - Implement release steps
4. `/pr --release [version]` - Create release PR
5. `/post-pr --release [version]` - Update documentation after merge

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

## Common Issues

### Issue: Manual Testing Guide Doesn't Exist

**Solution:**
- Create manual testing guide for this phase
- Add scenarios for all new features
- Document prerequisites and execution order
- Location: `docs/maintainers/planning/features/[feature]/manual-testing.md`

### Issue: Tests Fail After Manual Testing

**Solution:**
- Manual testing may have changed database state
- Reset test database: `rm backend/instance/*.db`
- Re-run migrations: `flask db upgrade`
- Re-run tests

### Issue: Coverage Dropped

**Solution:**
- Check which files have lower coverage
- Add tests for uncovered code paths
- May need to add edge case tests
- Don't proceed until coverage maintained

### Issue: Sourcery Review Not Available

**Solution:**
- Sourcery review is handled by `/pr-validation` command, not during PR creation
- Run `/pr-validation` after PR is created to get Sourcery review
- Can proceed with PR creation, review will be done via `/pr-validation`

---

## Pre-PR Checklist Summary

**Before creating PR, ensure:**

- [ ] All tasks completed
- [ ] All automated tests passing
- [ ] Coverage maintained/improved
- [ ] **Manual testing complete** (if applicable)
- [ ] Manual testing scenarios added for new features
- [ ] Phase document updated (tasks marked complete)
- [ ] README/docs updated
- [ ] No linter errors
- [ ] All changes committed
- [ ] Feature branch pushed

**After PR created:**

- [ ] PR link presented to user
- [ ] `/pr-validation` command run (includes Sourcery review)
- [ ] Priority matrix filled out
- [ ] CRITICAL/HIGH issues addressed
- [ ] User approval obtained
- [ ] PR merged
- [ ] Post-merge cleanup done (use `/post-pr`)

---

## Tips

**Before PR:**
- **Don't skip adding manual testing scenarios** - Required for new features
- Don't skip manual testing - it catches real bugs
- Run full test suite one more time before PR
- Review all changes in diff view
- Ensure commit messages are clear
- Check that documentation is accurate
- Verify manual testing scenarios are complete and numbered correctly

**During PR:**
- Present PR link clearly to user
- Don't auto-merge without approval
- Run `/pr-validation` to fill out Sourcery matrix (if review available)
- Be honest about issues found
- Prioritize fixes appropriately

**After PR:**
- Use `/post-pr` command for documentation updates
- Clean up branches promptly
- Capture learnings while fresh
- Celebrate completion! 🎉

---

## Reference

**Phase Documents:**

- `docs/maintainers/planning/features/[feature]/phase-[N].md`

**Fix Plans:**

- PR-Specific: `docs/maintainers/planning/features/[feature]/fix/pr##/[batch-name].md`
- Cross-PR: `docs/maintainers/planning/features/[feature]/fix/cross-pr/[batch-name].md`

**Feature Planning:**

- `docs/maintainers/planning/features/[feature]/feature-plan.md`
- `docs/maintainers/planning/features/[feature]/status-and-next-steps.md`

**Testing:**

- `docs/maintainers/planning/features/[feature]/manual-testing.md`

**Review Workflow:**

- `docs/maintainers/feedback/sourcery/pr##.md`
- `docs/maintainers/planning/features/[feature]/fix/README.md` (main hub)
- `docs/maintainers/planning/features/[feature]/fix/pr##/README.md` (PR hub)

**Related Commands:**

- `/task-phase` - Implement phase tasks
- `/task-release` - Implement release transition tasks
- `/fix-implement` - Implement fix batches
- `/fix-plan` - Create fix plans from Sourcery reviews
- `/pr-validation` - Validate PR (manual testing + Sourcery review)
- `/post-pr` - Post-merge documentation updates
- `/int-opp` - Document phase learnings

---

**Last Updated:** 2025-12-07  
**Status:** ✅ Active  
**Next:** Use `/pr --phase [N]` for phase PRs, `/pr --fix [batch-name]` for fix PRs, `/pr --release [version]` for release PRs

