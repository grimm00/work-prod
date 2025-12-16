# Task Phase Command

Use this command to implement phase tasks step-by-step, following TDD workflow and creating PRs at the right time.

---

## Workflow Overview

**Pattern:**
1. Phase has multiple tasks (usually TDD: RED → GREEN cycles)
2. **Task Grouping:** RED + GREEN phases are grouped together (tightly coupled TDD cycle)
3. Implement the task group completely (RED → GREEN → REFACTOR)
4. Commit the work
5. Stop and wait for user to invoke command again for next task group
6. Create PR only after completing ALL tasks in phase (use `/pr --phase [N]` command)

**Task Grouping Rules:**
- **Group together:** RED test task + GREEN implementation task (e.g., Task 1 + Task 2)
- **Separate:** Different task types (e.g., API tasks vs CLI tasks)
- **Separate:** Large/complex tasks that benefit from review

**Examples:**
- Task 1 (Write Filter Tests - RED) + Task 2 (Implement Filtering - GREEN) = **One invocation**
- Task 3 (Write Search Tests - RED) + Task 4 (Implement Search - GREEN) = **One invocation**
- Task 5 (Enhance CLI) = **Separate invocation** (different component)

**When to create PR:**
- After completing the LAST task in the phase
- Use `/pr --phase [N]` command for complete PR workflow
- Before marking phase as complete
- After all tests pass
- After manual testing (if applicable)

**Key Principle:** Group related TDD cycles (RED+GREEN), but separate different components. Complete the task group, commit it, then stop. User will invoke command again for the next task group.

---

## Usage

**Command:** `/task-phase [phase-number] [task-number]`

**Examples:**
- `/task-phase 4 1` - Implement Phase 4, Tasks 1-2 (RED + GREEN for filtering)
- `/task-phase 4 3` - Implement Phase 4, Tasks 3-4 (RED + GREEN for search)
- `/task-phase 4 5` - Implement Phase 4, Task 5 (CLI enhancement)

**Task Grouping:**
- When you specify a RED task (e.g., Task 1), automatically include the next GREEN task (Task 2)
- Different task types (API vs CLI) are separate invocations
- Check phase document to identify natural groupings

**Important:** 
- This command handles **one task group at a time** (typically RED+GREEN pair)
- After completing a task group, stop and wait for user to invoke again for next group
- Do NOT continue to next task group automatically
- Use `/pr --phase [N]` command when all tasks are complete to create PR

---

## Pre-Task Branch Validation (BLOCKING)

**CRITICAL:** This validation MUST pass before any work begins. Do NOT proceed if validation fails.

### Validation Steps

1. **Check Current Branch:**
   ```bash
   git branch --show-current
   ```
   
2. **Expected Pattern:** `feat/[feature-name]-phase-N-*` or `feat/phase-N-*`

3. **Validation Logic:**
   - If on `develop` or `main` → **ERROR: Wrong branch**
   - If on different feature branch → **ERROR: Wrong feature**
   - If branch in worktree elsewhere → **ERROR: Worktree conflict**

### Error Handling

**Wrong Branch Error:**
```
❌ BLOCKING: Currently on 'develop', expected 'feat/[feature]-phase-N-*'
   
   Resolution:
   1. Check out the correct feature branch: git checkout feat/[feature]-phase-N-[desc]
   2. If branch exists in worktree, work from that worktree instead
   3. If starting new phase, create branch: git checkout -b feat/[feature]-phase-N-[desc]
```

**Worktree Conflict Error:**
```
❌ BLOCKING: Branch 'feat/...' is checked out in worktree at '/path/to/worktree'
   
   Resolution:
   1. Work from the worktree: cd /path/to/worktree
   2. Or delete the worktree: git worktree remove /path/to/worktree
   3. Then checkout: git checkout feat/...
```

### Enforcement

- This check runs at the START of every `/task-phase` invocation
- If validation fails, the command STOPS immediately
- No code changes should be made until validation passes

---

## Step-by-Step Process

### 1. Start a Phase Task

**What to do:**
1. **Branch validation passed** (checked above)
2. Read the phase document: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
3. Identify the current task (numbered in the document)
4. Check prerequisites (previous tasks, phase status)
5. Create feature branch if starting phase: `feat/[feature-name]-phase-N-[description]` or `feat/phase-N-[description]`

**Branch naming:**
- First task: `feat/[feature-name]-phase-N-[description]` (e.g., `feat/projects-phase-3-delete-archive`)
- Or: `feat/phase-N-[description]` if no feature name
- Subsequent tasks: Use same branch

**Status Update (Start of Phase):**

**Auto-Update Phase Status:**

When starting a phase (first task of the phase), automatically update status:

1. **Read phase document:**
   - Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
   - Project-wide: `docs/maintainers/planning/phases/phase-N.md`

2. **Check current status:**
   - If status is "🔴 Not Started" or missing, update to "🟠 In Progress"
   - If status is already "🟠 In Progress", leave as is (may be resuming)
   - If status is "✅ Complete", warn user (shouldn't happen)

3. **Update phase document:**
   - Change `**Status:** 🔴 Not Started` to `**Status:** 🟠 In Progress`
   - Update `**Last Updated:**` field to today's date

4. **Update feature status document (if first phase):**
   - File: `docs/maintainers/planning/features/[feature-name]/status-and-next-steps.md`
   - Update `**Status:**` to "🟠 In Progress" if still "🔴 Not Started"
   - Update `**Current Phase:**` to reflect starting phase
   - Update `**Last Updated:**` field

5. **Commit status updates:**
   - Commit message: `docs(phase-N): update phase status to In Progress`
   - Include both phase document and feature status document if updated
   - Commit immediately after updating (before starting work)

**Note:** Status updates are committed immediately at phase start to ensure status is current from the beginning.

**Checklist:**
- [ ] Branch validation passed
- [ ] Phase document read and understood
- [ ] Prerequisites met (previous phase complete)
- [ ] Feature branch created (if first task)
- [ ] Current task identified and understood
- [ ] Phase status auto-updated to "🟠 In Progress" (if starting phase)
- [ ] Feature status auto-updated (if first phase)
- [ ] Status updates committed

---

### 2. Implement Task Group Following TDD

**TDD Pattern (RED → GREEN → REFACTOR):**

**If task group includes RED + GREEN:**

#### RED Phase (Write Tests First)
- [ ] Write failing tests for the task
- [ ] Run tests to confirm they fail
- [ ] Commit: `test(phase-N): add tests for [task description]`

#### GREEN Phase (Implement to Pass)
- [ ] Implement minimum code to pass tests
- [ ] Run tests to confirm they pass
- [ ] Commit: `feat(phase-N): implement [task description]`

#### REFACTOR Phase (Improve Code)
- [ ] Refactor if needed (with tests still passing)
- [ ] Commit: `refactor(phase-N): improve [task description]` (if needed)

**If task group is standalone (e.g., CLI task):**
- [ ] Implement the task completely
- [ ] Test manually
- [ ] Commit: `feat(phase-N): implement [task description]`

**Task-specific patterns:**

**Model Changes:**
1. Write model tests (RED)
2. Update model (GREEN)
3. Create migration: `flask db migrate -m "Description"`
4. Apply migration: `flask db upgrade`
5. Run tests (should pass)

**API Endpoints:**
1. Write integration tests (RED)
2. Implement endpoint (GREEN)
3. Test with curl/CLI manually
4. Run full test suite

**CLI Commands:**
1. Write CLI tests (if applicable)
2. Implement command
3. Test manually
4. Update CLI README

---

### 3. Commit Strategy

**Commit after each logical unit:**

**Small commits are better:**
- One commit per test file
- One commit per implementation
- One commit per migration
- One commit per CLI command

**Commit message format:**
```
type(scope): brief description

Longer explanation if needed

Related: Phase N, Task M
```

**Types:**
- `test` - Adding tests
- `feat` - New feature/functionality
- `fix` - Bug fix
- `refactor` - Code improvement
- `docs` - Documentation only
- `chore` - Maintenance

**Examples:**
```bash
git commit -m "test(phase-3): add DELETE endpoint tests"
git commit -m "feat(phase-3): implement DELETE endpoint"
git commit -m "feat(phase-3): add proj delete CLI command"
```

---

### 4. Check Task Completion

**After implementing a task:**

- [ ] All tests for this task pass
- [ ] Code follows project patterns
- [ ] No linter errors
- [ ] Manual testing done (if applicable)
- [ ] Task checklist items completed
- [ ] Committed to feature branch

**Update phase document:**
- Mark task items as complete: `- [x]` instead of `- [ ]`
- Don't commit phase doc changes until phase complete

**Auto-Status Update (MANDATORY):**

After task implementation is complete, AUTOMATICALLY:

1. **Update Phase Document:**
   - Mark task checkboxes as complete: `- [ ]` → `- [x]`
   - Update Last Updated field

2. **Commit Status Update:**
   ```bash
   git add [phase-document]
   git commit -m "docs(phase-N): mark Task M complete"
   ```

3. **Verify Commit Location:**
   ```bash
   # Confirm commit is on feature branch, NOT develop
   git branch --show-current  # Should be feat/...
   git log --oneline -1       # Should show status commit
   ```

---

### 5. Stop After Task Group Completion

**After completing a task group:**

- [ ] Task group fully implemented and tested
- [ ] All commits made to feature branch
- [ ] Tests passing
- [ ] **STOP - Do NOT proceed to next task group**
- [ ] Present completion summary to user
- [ ] Indicate which tasks were completed (e.g., "Tasks 1-2 complete: Filter tests + implementation")
- [ ] Wait for user to invoke command again for next task group

**Important:** This command handles ONE task group at a time (typically RED+GREEN pair). The user will invoke the command again with the next task number when ready to continue.

---

### 6. Complete All Tasks - Create PR

**When ALL tasks in phase are done:**

**Pre-PR Checklist:**
- [ ] All tasks completed
- [ ] All tests passing
- [ ] Coverage maintained/improved
- [ ] Manual testing complete (if applicable)
- [ ] Phase document updated (all tasks marked complete)
- [ ] README/docs updated (if needed)
- [ ] No linter errors

**Status Update (Phase Completion):**

**Auto-Update Phase Status:**

When all tasks in phase are complete, automatically update status:

1. **Read phase document:**
   - Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
   - Project-wide: `docs/maintainers/planning/phases/phase-N.md`

2. **Verify all tasks complete:**
   - Check all task checkboxes are marked `- [x]`
   - Verify no incomplete tasks remain

3. **Update phase document:**
   - Change `**Status:** 🟠 In Progress` to `**Status:** ✅ Complete`
   - Add completion date: `**Completed:** YYYY-MM-DD`
   - Update `**Last Updated:**` field

4. **Update feature status document:**
   - File: `docs/maintainers/planning/features/[feature-name]/status-and-next-steps.md`
   - Update `**Current Phase:**` to reflect completed phase
   - Update `**Progress:**` percentage (calculate based on completed phases)
   - Add completed milestone entry
   - Update `**Last Updated:**` field

5. **Commit status updates:**
   - Commit message: `docs(phase-N): update phase status to Complete`
   - Include both phase document and feature status document
   - Commit before creating PR

**Note:** Status updates are committed before PR creation to ensure status is current.

**Checklist:**
- [ ] Phase status auto-updated to "✅ Complete"
- [ ] Completion date added to phase document
- [ ] Feature status document updated with phase completion
- [ ] Progress tracking updated
- [ ] Status updates committed

**Create PR:**
1. Push final commits to feature branch
2. Run Sourcery review: `dt-review` from dev-toolkit
3. Fill out priority matrix in `docs/maintainers/feedback/sourcery/pr##.md`
4. Address any CRITICAL/HIGH issues before PR
5. Create PR with comprehensive description

**PR Title Format:**
```
feat: [Phase N Description] (Phase N)
```

**PR Description Template:**
```markdown
## Phase N: [Phase Name]

[Brief description of what was implemented]

---

## What's Included

### [Component 1]
- Feature/change description
- Tests added
- Files modified

### [Component 2]
- Feature/change description
- Tests added
- Files modified

---

## Testing

- [ ] All automated tests passing
- [ ] Coverage: [X]%
- [ ] Manual testing complete (if applicable)
- [ ] Sourcery review completed

---

## Related

- **Phase Plan:** `docs/maintainers/planning/features/projects/phase-N.md`
- **Feature Plan:** `docs/maintainers/planning/features/projects/feature-plan.md`
```

**After PR Created:**
- [ ] Present PR link to user (DO NOT auto-merge)
- [ ] Wait for external review (dt-review)
- [ ] Address CRITICAL/HIGH issues
- [ ] Get user approval before merge

---

## Task Detection Logic

**How to identify tasks:**

Tasks are typically numbered in phase documents:
- `#### 1. Write DELETE Endpoint Tests (TDD - RED)`
- `#### 2. Implement DELETE Endpoint (TDD - GREEN)`
- `#### 3. Write Archive Tests (TDD - RED)`
- etc.

**Task boundaries:**
- Each numbered section is a task
- Tasks may have sub-items (checkboxes)
- Complete all sub-items before moving to next task

**Last task detection:**
- Check if there are more numbered tasks after current
- Look for "Completion Criteria" section (comes after all tasks)
- If no more tasks, it's time to create PR

---

## Common Patterns

### Pattern 1: Model Extension Task

**Task:** "Extend Project Model"

**Steps:**
1. Write model tests (RED)
2. Update model file
3. Create migration
4. Apply migration
5. Update `to_dict()` method
6. Run tests (GREEN)
7. Commit

**Files typically modified:**
- `backend/tests/unit/models/test_project.py`
- `backend/app/models/project.py`
- `backend/migrations/versions/XXX_*.py` (new)

### Pattern 2: API Endpoint Task

**Task:** "Implement DELETE Endpoint"

**Steps:**
1. Write integration tests (RED)
2. Add route to `backend/app/api/projects.py`
3. Implement handler function
4. Add error handling
5. Run tests (GREEN)
6. Test manually with curl
7. Commit

**Files typically modified:**
- `backend/tests/integration/api/test_projects.py`
- `backend/app/api/projects.py`
- `backend/README.md` (update API docs)

### Pattern 3: CLI Command Task

**Task:** "Add proj delete command"

**Steps:**
1. Create command file: `scripts/project_cli/commands/delete_cmd.py`
2. Implement command with Click
3. Add Rich formatting
4. Register in `scripts/project_cli/proj`
5. Test manually
6. Update CLI README
7. Commit

**Files typically modified:**
- `scripts/project_cli/commands/delete_cmd.py` (new)
- `scripts/project_cli/proj`
- `scripts/project_cli/README.md`

---

## Error Handling

**If tests fail:**
- Debug the failure
- Fix the issue
- Re-run tests
- Don't move to next task until tests pass

**If migration fails:**
- Check migration file
- May need to reset database: `rm backend/instance/*.db`
- Re-run migration: `flask db upgrade`

**If linter errors:**
- Fix linter issues
- Re-run linter
- Don't commit until clean

---

## Phase Completion Checklist

**Before marking phase complete:**

- [ ] All tasks completed
- [ ] All tests passing
- [ ] Coverage maintained
- [ ] Manual testing done
- [ ] Documentation updated
- [ ] PR created and reviewed
- [ ] Sourcery review completed
- [ ] CRITICAL/HIGH issues addressed
- [ ] PR merged to develop
- [ ] Phase document status updated to "✅ Complete"
- [ ] Feature status updated (if needed)

---

## Tips

**While implementing:**
- Focus on ONE task group (typically RED+GREEN pair)
- Keep phase document open for reference
- Check off items as you complete them
- Don't skip tests (TDD discipline)
- Commit frequently (small commits)
- Push to branch regularly

**Task grouping:**
- RED + GREEN phases naturally belong together
- Complete the full TDD cycle before stopping
- Different components (API vs CLI) are separate

**After completing task group:**
- **STOP - Do NOT continue to next task group**
- Present summary of what was accomplished
- Indicate which tasks were completed (e.g., "Tasks 1-2 complete")
- Wait for user to invoke command again

**Important reminders:**
- One task group per invocation (typically RED+GREEN pair)
- Complete task group fully before stopping
- Don't proceed to next task group automatically
- Use `/pr --phase [N]` when all tasks done

---

## Reference

**Phase Documents:**
- `docs/maintainers/planning/features/projects/phase-N.md`

**Feature Planning:**
- `docs/maintainers/planning/features/projects/feature-plan.md`
- `docs/maintainers/planning/features/projects/status-and-next-steps.md`

**Testing:**
- `docs/maintainers/planning/features/projects/manual-testing.md`

**Workflow:**
- Git Flow: `docs/maintainers/planning/notes/projects-first-strategy.md`
- PR Review: Cursor rules (Pull Request Review Workflow section)

