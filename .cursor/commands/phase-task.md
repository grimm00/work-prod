# Phase Task Implementation Command

Use this command to implement phases task-by-task, following TDD workflow and creating PRs at the right time.

---

## Workflow Overview

**Pattern:**
1. Phase has multiple tasks (usually TDD: RED → GREEN cycles)
2. Implement each task incrementally
3. Commit after each task (or logical group)
4. Create PR after completing ALL tasks in phase
5. Run Sourcery review before PR creation

**When to create PR:**
- After completing the LAST task in the phase
- Before marking phase as complete
- After all tests pass
- After manual testing (if applicable)

---

## Usage

**Command:** `@phase-task [phase-number] [task-number]`

**Examples:**
- `@phase-task 3 1` - Start Phase 3, Task 1
- `@phase-task 3 2` - Continue Phase 3, Task 2
- `@phase-task 3 pr` - Create PR after all tasks complete

---

## Step-by-Step Process

### 1. Start a Phase Task

**What to do:**
1. Read the phase document: `docs/maintainers/planning/features/projects/phase-N.md`
2. Identify the current task (numbered in the document)
3. Check prerequisites (previous tasks, phase status)
4. Create feature branch if starting phase: `feat/phase-N-[description]`

**Branch naming:**
- First task: `feat/phase-N-[description]` (e.g., `feat/phase-3-delete-archive`)
- Subsequent tasks: Use same branch

**Checklist:**
- [ ] Phase document read and understood
- [ ] Prerequisites met (previous phase complete)
- [ ] Feature branch created (if first task)
- [ ] Current task identified and understood

---

### 2. Implement Task Following TDD

**TDD Pattern (RED → GREEN → REFACTOR):**

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
- [ ] Commit: `refactor(phase-N): improve [task description]`

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

---

### 5. Move to Next Task

**Before starting next task:**

- [ ] Previous task fully complete
- [ ] All commits pushed to feature branch
- [ ] Tests still passing
- [ ] Ready for next task

**Repeat steps 2-4 for next task**

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
- Keep phase document open for reference
- Check off items as you complete them
- Don't skip tests (TDD discipline)
- Commit frequently (small commits)
- Push to branch regularly

**Before PR:**
- Review all changes
- Run full test suite
- Check coverage report
- Update any relevant docs
- Ensure phase doc reflects completion

**After PR:**
- Don't auto-merge (wait for approval)
- Address review feedback promptly
- Update fix tracking if issues found
- Mark phase complete after merge

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

