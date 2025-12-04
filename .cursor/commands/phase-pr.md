# Phase PR Creation Command

Use this command after completing ALL tasks in a phase, before creating the PR. This ensures proper pre-PR validation, manual testing, documentation updates, and Sourcery review workflow.

---

## Workflow Overview

**When to use:**
- After completing the LAST task in a phase
- Before creating the PR
- After all automated tests pass
- Before marking phase as complete

**Key principle:** Manual testing happens BEFORE PR creation, not after.

---

## Usage

**Command:** `@phase-pr [phase-number]`

**Examples:**
- `@phase-pr 3` - Complete Phase 3 and create PR

---

## Step-by-Step Process

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
- [ ] Check if manual testing guide exists: `docs/maintainers/planning/features/projects/manual-testing.md`
- [ ] **REQUIRED:** Add new scenarios for phase features (see step 3a)
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

### 2. Update Phase Document

**File:** `docs/maintainers/planning/features/projects/phase-N.md`

**What to update:**
- Mark all task checkboxes as complete: `- [x]`
- Update status if there's a status field
- Add completion date if applicable
- Don't commit yet (will commit with PR)

**Example:**
```markdown
#### 1. Write DELETE Endpoint Tests (TDD - RED)
- [x] Test DELETE returns 204 No Content
- [x] Test DELETE removes from database
- [x] Test DELETE on non-existent returns 404
- [x] Tests pass ✅
```

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
- `docs/maintainers/planning/features/projects/manual-testing.md`
- **REQUIRED:** Add new scenarios for phase features
- Update scenario numbering
- Add prerequisites/notes
- See "3a. Add Manual Testing Scenarios" below for details

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

### 5. Create PR Description

**PR Title Format:**
```
feat: [Phase N Description] (Phase N)
```

**Examples:**
- `feat: Delete & Archive Projects (Phase 3)`
- `feat: Create & Update Projects (Phase 2)`

**PR Description Template:**

```markdown
## Phase N: [Phase Name]

[Brief 1-2 sentence description of what was implemented]

---

## What's Included

### [Component 1: e.g., DELETE Endpoint]
- **Feature:** DELETE /api/projects/<id> endpoint
- **Tests:** 4 integration tests added
- **Files Modified:**
  - `backend/app/api/projects.py` - Added delete_project function
  - `backend/tests/integration/api/test_projects.py` - Added DELETE tests
- **Documentation:** Updated `backend/README.md` with DELETE endpoint

### [Component 2: e.g., Archive Endpoint]
- **Feature:** PUT /api/projects/<id>/archive endpoint
- **Tests:** 3 integration tests added
- **Files Modified:**
  - `backend/app/api/projects.py` - Added archive_project function
  - `backend/tests/integration/api/test_projects.py` - Added archive tests
- **Documentation:** Updated API docs

### [Component 3: e.g., CLI Commands]
- **Feature:** `proj delete <id>` and `proj archive <id>` commands
- **Files Modified:**
  - `scripts/project_cli/commands/delete_cmd.py` (new)
  - `scripts/project_cli/commands/archive_cmd.py` (new)
  - `scripts/project_cli/proj` - Registered commands
  - `scripts/project_cli/README.md` - Updated docs

---

## Testing

- [x] All automated tests passing (46 tests)
- [x] Coverage: 93% (maintained)
- [x] Manual testing complete (14 scenarios)
- [ ] Sourcery review pending (will run after PR creation)

---

## Related

- **Phase Plan:** `docs/maintainers/planning/features/projects/phase-N.md`
- **Feature Plan:** `docs/maintainers/planning/features/projects/feature-plan.md`
- **Manual Testing:** `docs/maintainers/planning/features/projects/manual-testing.md`
```

---

### 6. Create PR

**Steps:**

1. **Push feature branch:**
   ```bash
   git push origin feat/phase-N-[description]
   ```

2. **Create PR using GitHub CLI:**
   
   **Option A: Use temporary file (auto-cleaned):**
   ```bash
   # Create description file in /tmp (auto-cleaned by OS)
   cat > /tmp/pr-description-phase-N.md << 'EOF'
   [paste PR description content]
   EOF
   
   gh pr create --title "feat: [Phase N Description] (Phase N)" \
                --body-file /tmp/pr-description-phase-N.md \
                --base develop \
                --head feat/phase-N-[description]
   
   # Clean up
   rm /tmp/pr-description-phase-N.md
   ```
   
   **Option B: Use inline body (simpler):**
   ```bash
   gh pr create --title "feat: [Phase N Description] (Phase N)" \
                --body "$(cat << 'EOF'
   [paste PR description content]
   EOF
   )" \
                --base develop \
                --head feat/phase-N-[description]
   ```
   
   **Option C: Use GitHub web UI** (paste description manually)

   **Note:** PR description files are gitignored (`pr-description*.md`) to prevent accidental commits.

3. **Get PR number from output** (e.g., `#12`)

4. **STOP HERE - Present PR link to user**
   - DO NOT auto-merge
   - DO NOT proceed to Sourcery review yet
   - Wait for user acknowledgment

---

### 7. Sourcery Review Workflow

**After PR is created and user acknowledges:**

1. **Run Sourcery review:**
   ```bash
   cd ~/Projects/dev-toolkit
   dt-review
   ```

2. **Review feedback saved to:**
   `docs/maintainers/feedback/sourcery/pr##.md`

3. **Fill out priority matrix:**
   - For each Sourcery comment, assess:
     - **Priority:** CRITICAL 🔴 / HIGH 🟠 / MEDIUM 🟡 / LOW 🟢
     - **Impact:** CRITICAL 🔴 / HIGH 🟠 / MEDIUM 🟡 / LOW 🟢
     - **Effort:** LOW 🟢 / MEDIUM 🟡 / HIGH 🟠 / VERY_HIGH 🔴

4. **Identify critical issues:**
   - Review all CRITICAL 🔴 items
   - Review all HIGH 🟠 items
   - Determine if fixes needed before merge

5. **Create fix plans (if needed):**
   - Location: `docs/maintainers/planning/features/projects/fix/`
   - Format: `pr##-issue-##-[short-name].md`
   - Reference Sourcery comment number
   - Include priority, impact, effort assessment

6. **Update fix tracking:**
   - Update `docs/maintainers/planning/features/projects/fix/README.md`
   - Add new issues to tracking table

---

### 8. Address Critical Issues (If Any)

**If CRITICAL/HIGH issues found:**

1. **Create fix branch:**
   ```bash
   git checkout -b fix/pr##-critical-issues
   ```

2. **Implement fixes:**
   - Follow fix plans
   - Write tests for fixes
   - Run full test suite
   - Commit fixes

3. **Update PR:**
   - Push fix branch
   - Update PR description with fixes
   - Re-run Sourcery review if needed

**If only LOW/MEDIUM issues:**
- Document in fix tracking
- Can be deferred to future PR
- Proceed with merge approval

---

### 9. Get User Approval

**Before merging:**

- [ ] PR created and link presented to user
- [ ] Sourcery review completed
- [ ] Priority matrix filled out
- [ ] CRITICAL/HIGH issues addressed (if any)
- [ ] User explicitly approves merge

**DO NOT auto-merge** - Always wait for explicit user approval.

---

### 10. Post-Merge Cleanup

**After PR merged:**

1. **Update phase document status:**
   - Mark phase as "✅ Complete"
   - Add completion date
   - Commit to develop branch

2. **Update feature status:**
   - `docs/maintainers/planning/features/projects/status-and-next-steps.md`
   - Update completed milestones
   - Update next steps

3. **Branch cleanup:**
   ```bash
   git checkout develop
   git pull origin develop
   git branch -d feat/phase-N-[description]
   git push origin --delete feat/phase-N-[description]
   ```

4. **Document learnings (optional):**
   - Use `/int-opp` command to capture phase learnings
   - Update dev-infra improvements checklist

---

## Common Issues

### Issue: Manual Testing Guide Doesn't Exist

**Solution:**
- Create manual testing guide for this phase
- Add scenarios for all new features
- Document prerequisites and execution order
- Location: `docs/maintainers/planning/features/projects/manual-testing.md`

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
- Check if `dt-review` is installed
- May need to run from `~/Projects/dev-toolkit`
- Can proceed with PR creation, review later
- Document in PR description that review pending

---

## Pre-PR Checklist Summary

**Before creating PR, ensure:**

- [ ] All tasks completed
- [ ] All automated tests passing
- [ ] Coverage maintained/improved
- [ ] **Manual testing complete** (if applicable)
- [ ] Phase document updated (tasks marked complete)
- [ ] README/docs updated
- [ ] No linter errors
- [ ] All changes committed
- [ ] Feature branch pushed

**After PR created:**

- [ ] PR link presented to user
- [ ] Sourcery review run (dt-review)
- [ ] Priority matrix filled out
- [ ] CRITICAL/HIGH issues addressed
- [ ] User approval obtained
- [ ] PR merged
- [ ] Post-merge cleanup done

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
- Fill out Sourcery matrix thoroughly
- Be honest about issues found
- Prioritize fixes appropriately

**After PR:**
- Clean up branches promptly
- Update documentation status
- Capture learnings while fresh
- Celebrate completion! 🎉

---

## Reference

**Phase Documents:**
- `docs/maintainers/planning/features/projects/phase-N.md`

**Feature Planning:**
- `docs/maintainers/planning/features/projects/feature-plan.md`
- `docs/maintainers/planning/features/projects/status-and-next-steps.md`

**Testing:**
- `docs/maintainers/planning/features/projects/manual-testing.md`

**Review Workflow:**
- `docs/maintainers/feedback/sourcery/pr##.md`
- `docs/maintainers/planning/features/projects/fix/README.md`

**Related Commands:**
- `/phase-task` - Individual task implementation
- `/int-opp` - Document phase learnings

