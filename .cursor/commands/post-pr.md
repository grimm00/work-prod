# Post-PR Documentation Update Command

Use this command after a PR is merged to update all relevant documentation. This ensures phase completion status, feature milestones, and next steps are properly documented.

---

## Workflow Overview

**When to use:**
- After PR is merged to `develop`
- Before starting next phase
- To ensure documentation stays in sync with code

**Key principle:** Documentation updates happen in a separate `docs` branch, then merged directly to `develop` (no PR needed for docs-only changes).

---

## Usage

**Command:** `@post-pr [pr-number] [phase-number]`

**Examples:**
- `@post-pr 10 3` - Update docs after PR #10 (Phase 3) merge
- `@post-pr 11 4` - Update docs after PR #11 (Phase 4) merge

---

## Step-by-Step Process

### 1. Validate Inputs

**Check before proceeding:**
- [ ] PR number is valid (check GitHub)
- [ ] Phase number is valid (phase document exists)
- [ ] PR is merged to `develop` (or user confirms it will be merged)
- [ ] Current branch is `develop` (or can switch to it)

**Validation commands:**
```bash
# Check current branch
git branch --show-current

# Verify PR is merged (check GitHub or git log)
gh pr view [pr-number] --json merged
```

---

### 2. Create Docs Branch

**Branch naming:**
- Format: `docs/post-pr##-phase##-complete`
- Example: `docs/post-pr10-phase3-complete`

**Steps:**
```bash
# Ensure we're on develop
git checkout develop
git pull origin develop

# Create docs branch
git checkout -b docs/post-pr[##]-phase[##]-complete
```

**Checklist:**
- [ ] Branch created from `develop`
- [ ] Branch name follows convention
- [ ] Local `develop` is up-to-date with remote

---

### 3. Update Phase Document

**File:** `docs/maintainers/planning/features/projects/phase-N.md`

**Updates to make:**

1. **Status Field**
   - Change from current status to: `**Status:** ✅ Complete`
   - If already marked complete, verify it's correct

2. **Completion Date**
   - Add completion date if not present
   - Format: `**Completed:** YYYY-MM-DD`
   - Use today's date

3. **Verify Tasks**
   - Check all task checkboxes are marked: `- [x]`
   - If any are incomplete, note them (shouldn't happen if PR merged)

4. **Last Updated**
   - Update `**Last Updated:**` field to today's date

**Example updates:**
```markdown
**Phase:** 3 - Projects API - Delete & Archive (Backend + CLI)  
**Duration:** 1 day  
**Status:** ✅ Complete  
**Completed:** 2025-12-04
**Prerequisites:** Phase 2 complete
```

**Checklist:**
- [ ] Status marked as complete
- [ ] Completion date added
- [ ] All tasks verified complete
- [ ] Last Updated date refreshed

---

### 4. Update Feature Status Document

**File:** `docs/maintainers/planning/features/projects/status-and-next-steps.md`

**Updates to make:**

1. **Current Phase Field**
   - Update to reflect completed phase
   - Example: `**Current Phase:** Phase 3 Complete`

2. **Overall Progress**
   - Calculate new percentage
   - Format: `X/8 phases complete (XX%)`
   - Example: `3/8 phases complete (37.5%)`

3. **Completed Milestones Section**
   - Add new entry for completed phase
   - Include PR number
   - Include completion date
   - Brief summary of what was accomplished

4. **What's Happening Now**
   - Update to reflect current state
   - Mark completed phase with ✅
   - Update next phase status

5. **Immediate Next Steps**
   - Update to next phase
   - Remove completed phase items
   - Add next phase tasks

6. **Progress Tracking Table**
   - Update phase row status to "✅ Complete"
   - Add end date
   - Calculate duration

7. **Last Updated**
   - Update to today's date

**Example milestone entry:**
```markdown
- ✅ **Phase 3: Delete & Archive Complete** (2025-12-04)
  - DELETE /api/projects/<id> endpoint implemented
  - PUT /api/projects/<id>/archive endpoint implemented
  - CLI `proj delete` and `proj archive` commands added
  - 49 tests passing with 92% coverage
  - Merged via PR #10
```

**Checklist:**
- [ ] Current phase updated
- [ ] Progress percentage calculated
- [ ] Milestone entry added
- [ ] Next steps updated
- [ ] Progress table updated
- [ ] Last Updated refreshed

---

### 5. Document Deferred Issues

**IMPORTANT:** Always check for deferred issues, even if none exist. This ensures tracking is complete.

**Process:**

1. **Check Sourcery Review File**
   - Location: `docs/maintainers/feedback/sourcery/pr##.md`
   - Review priority matrix for all comments
   - Identify MEDIUM/LOW priority issues that were deferred

2. **Create/Update PR Directory**
   - Create PR directory if it doesn't exist: `docs/maintainers/planning/features/projects/fix/pr##/`
   - Create or update PR hub: `docs/maintainers/planning/features/projects/fix/pr##/README.md`

3. **If Deferred Issues Exist:**
   - Add deferred issues section to PR hub README.md
   - Include date, review source, and status
   - List each deferred issue with:
     - Comment number (e.g., PR12-#1)
     - Brief description
     - Priority and effort levels
     - Action plan (deferred to next phase, future PR, etc.)
   - Update main fix tracking README.md to link to PR hub

4. **If No Deferred Issues:**
   - Note in PR hub that review was checked
   - All issues were CRITICAL/HIGH and addressed, or no issues found
   - Update main fix tracking README.md

**PR Hub Entry (with deferred issues):**
**File:** `docs/maintainers/planning/features/projects/fix/pr##/README.md`

```markdown
## 📋 Deferred Issues

**Date:** 2025-12-04  
**Review:** PR #12 (Phase 4) Sourcery feedback  
**Status:** 🟡 **DEFERRED** - All MEDIUM/LOW priority, can be handled opportunistically

**Deferred Issues:**

- **PR12-#1:** Use `click.Choice` for CLI validation (MEDIUM priority, LOW effort) - Improves UX by catching invalid values early
- **PR12-#2:** Tighten test expectations for invalid status (MEDIUM priority, LOW effort) - Test quality improvement
- **PR12-#3:** Avoid conditionals in tests (MEDIUM priority, MEDIUM effort) - Code quality improvement, requires test refactoring
- **PR12-#4:** Use named expression (LOW priority, LOW effort) - Minor code quality improvement
- **PR12-#5:** Raise from previous error (LOW priority, LOW effort) - Minor code quality improvement

**Action Plan:** These can be handled opportunistically during future phases or in a dedicated code quality improvement PR.
```

**PR Hub Entry (no deferred issues):**
**File:** `docs/maintainers/planning/features/projects/fix/pr##/README.md`

```markdown
## 📋 Deferred Issues

**Date:** YYYY-MM-DD  
**Review:** PR #N (Phase N) Sourcery feedback  
**Status:** ✅ **NONE** - All issues were CRITICAL/HIGH priority and addressed in PR, or no issues found
```

**Update Main Fix Tracking:**
**File:** `docs/maintainers/planning/features/projects/fix/README.md`

Add PR to active PRs section (if not already there):
```markdown
### Active PRs

- **[PR ##](pr##/README.md)** - [PR Title] ([Status])
```

**Checklist:**
- [ ] PR directory created (if needed)
- [ ] PR hub README.md created/updated
- [ ] Sourcery review file checked for deferred issues
- [ ] Deferred issues section added to PR hub (if issues exist)
- [ ] Each issue documented with priority, effort, and action plan
- [ ] No deferred issues noted in PR hub (if none exist)
- [ ] Main fix tracking README.md updated with PR link

---

### 6. Commit Changes

**Commit message format:**
```
docs(phase-N): update post-merge documentation

Post-PR #N documentation updates:
- Mark Phase N as complete with date
- Update feature status milestones
- Update progress to X/8 phases (XX%)
- Update next steps to Phase N+1
- Document deferred issues (if any)

Related: PR #N
```

**Steps:**
```bash
# Stage all documentation changes
git add docs/

# Commit with proper message
git commit -m "docs(phase-N): update post-merge documentation

Post-PR #N documentation updates:
- Mark Phase N as complete with date
- Update feature status milestones
- Update progress to X/8 phases (XX%)
- Update next steps to Phase N+1
- Document deferred issues (if any)

Related: PR #N"
```

**Checklist:**
- [ ] All relevant files staged
- [ ] Commit message follows conventional format
- [ ] PR number included in commit body

---

### 7. Merge Directly to Develop

**Since this is documentation-only, merge directly to develop (no PR needed):**

```bash
# Switch to develop
git checkout develop
git pull origin develop

# Merge docs branch
git merge docs/post-pr[##]-phase[##]-complete --no-edit

# Push to remote
git push origin develop

# Clean up local branch
git branch -d docs/post-pr[##]-phase[##]-complete

# Clean up remote branch
git push origin --delete docs/post-pr[##]-phase[##]-complete
```

**Checklist:**
- [ ] Merged to `develop` locally
- [ ] Pushed to remote `develop`
- [ ] Local branch deleted
- [ ] Remote branch deleted

**Note:** Documentation-only changes can be merged directly to `develop` without a PR, following Git Flow pattern for `docs/*` branches.

---

### 8. Clean Up Merged PR Branch

**IMPORTANT:** Clean up the merged PR branch (both local and remote) to keep repository clean.

**Process:**

1. **Verify PR is merged:**
   ```bash
   gh pr view [pr-number] --json state,mergedAt
   ```
   - Should show `state: "MERGED"` and `mergedAt` timestamp

2. **Check if branch exists locally:**
   ```bash
   git branch --list [branch-name]
   ```

3. **Check if branch exists remotely:**
   ```bash
   git branch -r --list origin/[branch-name]
   ```

4. **Delete local branch (if exists):**
   ```bash
   # Try normal delete first (only works if merged locally)
   git branch -d [branch-name]
   
   # If that fails (branch merged via GitHub, not locally), force delete
   # This is safe if PR is confirmed merged on GitHub
   git branch -D [branch-name]
   ```
   
   **Note:** If branch was merged via GitHub PR (not locally), `git branch -d` may fail even though the branch is merged. Use `git branch -D` in this case, but only after confirming PR is merged on GitHub.

5. **Delete remote branch (if exists):**
   ```bash
   git push origin --delete [branch-name]
   ```

**Branch naming patterns:**
- Feature branches: `feat/phase-N-[description]`
- Fix branches: `fix/[description]` or `fix/pr##-[description]`
- Docs branches: `docs/[description]`

**Example cleanup:**
```bash
# For PR #12 (feat/phase-4-search-filter)
git branch -d feat/phase-4-search-filter
git push origin --delete feat/phase-4-search-filter

# For PR #13 (fix/pr12-batch-medium-medium-01)
git branch -d fix/pr12-batch-medium-medium-01
git push origin --delete fix/pr12-batch-medium-medium-01
```

**Safety checks:**
- Only delete branches that are merged
- Verify branch name matches PR head branch
- Check that branch is not currently checked out
- Confirm deletion before proceeding

**Checklist:**
- [ ] PR verified as merged
- [ ] Local branch deleted (if existed)
- [ ] Remote branch deleted (if existed)
- [ ] No errors during cleanup

---

## Auto-Detection Features

### Detect Next Phase

**Logic:**
- Current phase number + 1
- Check if phase document exists
- If last phase, note completion

**Example:**
- Phase 3 complete → Next: Phase 4
- Phase 8 complete → Next: MVP Complete

### Calculate Progress

**Formula:**
- Completed phases / Total phases × 100
- Total phases: 8 (for Projects feature)
- Round to 1 decimal place

**Example:**
- 3 phases complete → 3/8 = 37.5%
- 5 phases complete → 5/8 = 62.5%

### Find Phase Document

**Path pattern:**
- `docs/maintainers/planning/features/projects/phase-N.md`
- Verify file exists before updating

---

## Validation Checks

### Before Starting

- [ ] PR number is valid (exists in GitHub)
- [ ] Phase number is valid (phase document exists)
- [ ] PR is merged (or user confirms merge)
- [ ] Current branch is `develop` or can switch

### During Updates

- [ ] Phase document exists and is readable
- [ ] Status document exists and is readable
- [ ] Fix tracking document exists and is readable
- [ ] Sourcery review file checked for deferred issues
- [ ] All required fields can be updated
- [ ] No conflicting changes in files

### After Updates

- [ ] All files updated correctly
- [ ] Dates are correct (today's date)
- [ ] Progress percentage is accurate
- [ ] Next phase is correct
- [ ] Commit message is proper
- [ ] Merged PR branch cleaned up (local and remote)

---

## Error Handling

### Missing Files

**If phase document doesn't exist:**
- Error: "Phase N document not found at [path]"
- Suggest: Check phase number or create document first

**If status document doesn't exist:**
- Error: "Status document not found at [path]"
- Suggest: Check feature directory structure

### Invalid PR Number

**If PR doesn't exist:**
- Error: "PR #N not found"
- Suggest: Verify PR number or check if merged

### Branch Conflicts

**If branch already exists:**
- Error: "Branch docs/post-pr##-phase##-complete already exists"
- Options:
  - Use existing branch
  - Delete and recreate
  - Use different branch name

### Merge Conflicts

**If conflicts when merging:**
- Resolve conflicts manually
- Re-commit resolved files
- Continue with PR creation

---

## Integration with Other Commands

### Command Sequence

**Complete workflow:**
1. `/phase-task` - Implement individual tasks
2. `/phase-pr` - Complete phase and create PR
3. PR merged (manual GitHub action)
4. `/post-pr` - Update documentation ← **You are here**
5. `/int-opp` - Capture phase learnings (optional)

### Related Commands

- **`/phase-task`** - Individual task implementation
- **`/phase-pr`** - Phase completion and PR workflow
- **`/post-pr`** - Post-merge documentation updates (this command)
- **`/int-opp`** - Document phase learnings (run after post-pr)

---

## Common Scenarios

### Scenario 1: Standard Phase Completion

**Situation:** Phase 3 complete, PR #10 merged

**Steps:**
1. Run `/post-pr 10 3`
2. Updates phase-3.md (mark complete, add date)
3. Updates status-and-next-steps.md (milestone, progress, next steps)
4. Creates docs branch and PR
5. Merge docs PR

**Result:** Documentation reflects Phase 3 completion, ready for Phase 4

---

### Scenario 2: First Phase Completion

**Situation:** Phase 0 complete, PR #1 merged

**Steps:**
1. Run `/post-pr 1 0`
2. Updates phase-0.md
3. Updates status (first milestone entry)
4. Progress: 1/8 = 12.5%
5. Next steps: Phase 1

**Result:** First milestone documented, progress tracking started

---

### Scenario 3: Last Phase Completion

**Situation:** Phase 8 complete, PR #20 merged

**Steps:**
1. Run `/post-pr 20 8`
2. Updates phase-8.md
3. Updates status (final milestone)
4. Progress: 8/8 = 100%
5. Next steps: MVP Complete / Production Ready

**Result:** Feature complete, all documentation updated

---

### Scenario 4: Phase with Deferred Issues

**Situation:** Phase 4 complete, PR #12 had deferred MEDIUM/LOW issues

**Steps:**
1. Run `/post-pr 12 4`
2. Updates phase and status documents
3. Checks Sourcery review file (`pr12.md`)
4. Updates fix tracking with deferred issues section
5. Documents all 5 deferred issues with priority/effort
6. Notes action plan (opportunistic handling)

**Result:** Documentation complete, deferred issues tracked for future handling

---

## Tips

### Before Running Command

- Verify PR is actually merged (check GitHub)
- Ensure `develop` branch is up-to-date
- Have PR number and phase number ready
- Check if any special updates needed (deferred issues, etc.)

### During Updates

- Review each file change before committing
- Verify dates are correct (today's date)
- Double-check progress percentage calculation
- Ensure next phase number is correct
- Check Sourcery review for deferred issues
- Document deferred issues even if none exist (note "NONE")

### After Updates

- Review PR description before creating
- Verify all files updated correctly
- Check that next phase is ready to start
- Clean up merged PR branch (local and remote)
- Consider running `/int-opp` to capture learnings

---

## Reference

**Phase Documents:**
- `docs/maintainers/planning/features/projects/phase-N.md`

**Feature Planning:**
- `docs/maintainers/planning/features/projects/feature-plan.md`
- `docs/maintainers/planning/features/projects/status-and-next-steps.md`

**Fix Tracking:**
- `docs/maintainers/planning/features/projects/fix/README.md`

**Related Commands:**
- `/phase-task` - Individual task implementation
- `/phase-pr` - Phase completion and PR workflow
- `/int-opp` - Document phase learnings

**Workflow:**
- Git Flow: `docs/maintainers/planning/notes/projects-first-strategy.md`
- PR Review: Cursor rules (Pull Request Review Workflow section)

---

**Last Updated:** 2025-12-04  
**Status:** ✅ Active  
**Next:** Use after each PR merge to keep documentation current

