# Task Release Command

Use this command to implement release transition tasks step-by-step, following the release transition plan and ensuring proper release preparation.

---

## Workflow Overview

**Pattern:**
1. Release transition plan has multiple steps (documentation, verification, tagging, etc.)
2. **Step Grouping:** Related steps are grouped together (e.g., documentation steps)
3. Implement the step group completely
4. Commit the work
5. Stop and wait for user to invoke command again for next step group
6. Create PR only after completing ALL steps in release transition (use `/pr --release [version]` command)

**Step Grouping Rules:**
- **Group together:** Related documentation steps (e.g., Step 1 + Step 4)
- **Separate:** Different step types (e.g., documentation vs verification vs tagging)
- **Separate:** Large/complex steps that benefit from review

**Examples:**
- Step 1 (Finalize Documentation) + Step 4 (Update Documentation) = **One invocation**
- Step 2 (Pre-Release Verification) = **Separate invocation** (verification)
- Step 3 (Version Tagging) = **Separate invocation** (critical step)

**When to create PR:**
- After completing the LAST step in the release transition
- Use `/pr --release [version]` command for complete PR workflow
- Before marking release as complete
- After all verification steps pass

**Key Principle:** Group related steps, but separate different step types. Complete the step group, commit it, then stop. User will invoke command again for the next step group.

---

## Usage

**Command:** `/task-release [version] [step-number]`

**Examples:**
- `/task-release v0.1.0 1` - Implement Release v0.1.0, Steps 1-4 (Documentation steps)
- `/task-release v0.1.0 2` - Implement Release v0.1.0, Step 2 (Pre-Release Verification)
- `/task-release v0.1.0 3` - Implement Release v0.1.0, Step 3 (Version Tagging)

**Step Grouping:**
- When you specify a documentation step (e.g., Step 1), automatically include related documentation steps (Step 4)
- Different step types (documentation vs verification vs tagging) are separate invocations
- Check transition plan document to identify natural groupings

**Important:** 
- This command handles **one step group at a time** (typically related steps)
- After completing a step group, stop and wait for user to invoke again for next group
- Do NOT continue to next step group automatically
- Use `/pr --release [version]` command when all steps are complete to create PR

---

## Step-by-Step Process

### 1. Start a Release Task

**What to do:**
1. Read the transition plan document: `docs/maintainers/planning/releases/[version]/transition-plan.md`
2. Identify the current step (numbered in the document)
3. Check prerequisites (previous steps, release status)
4. Create feature branch if starting release: `release/[version]`

**Branch naming:**
- First step: `release/[version]` (e.g., `release/v0.1.0`)
- Subsequent steps: Use same branch

**Checklist:**
- [ ] Transition plan document read and understood
- [ ] Prerequisites met (previous steps complete)
- [ ] Feature branch created (if first step)
- [ ] Current step identified and understood

---

### 2. Implement Step Group

**Step-specific patterns:**

#### Documentation Steps (Steps 1, 4)

**Step 1: Finalize Release Documentation**
- [ ] Review release checklist for completeness
- [ ] Review release notes for accuracy
- [ ] Verify all metrics are current
- [ ] Check all links in release notes are valid
- [ ] Verify technical details are accurate
- [ ] Update release date when ready
- [ ] Commit: `docs(release): finalize release documentation for [version]`

**Step 4: Update Release Documentation**
- [ ] Update release hub (releases/README.md) with release status
- [ ] Update version hub ([version]/README.md) with release date
- [ ] Update release checklist with completion status
- [ ] Update release notes with final release date
- [ ] Create release history entry (if history.md exists)
- [ ] Commit: `docs(release): update release documentation for [version]`

#### Verification Steps (Step 2)

**Step 2: Complete Pre-Release Verification**
- [ ] Verify all tests still passing (`pytest backend/`)
- [ ] Verify test coverage still > 80% (`pytest --cov`)
- [ ] Verify 0 linting errors (`flake8 backend/`)
- [ ] Verify all examples in documentation work
- [ ] Verify production startup script works
- [ ] Verify deployment guide steps are accurate
- [ ] Verify OpenAPI specification is accurate
- [ ] Commit: `chore(release): complete pre-release verification for [version]`

#### Tagging Steps (Step 3)

**Step 3: Version Tagging and Release**
- [ ] Determine final commit for release (current HEAD or specific commit)
- [ ] Create git tag: `git tag -a [version] -m "[Version] Release"`
- [ ] Push tag to remote: `git push origin [version]`
- [ ] Verify tag created correctly: `git tag -l [version]`
- [ ] **Create GitHub Release:** `gh release create [version] --title "[version] [Description]" --notes-file docs/maintainers/planning/releases/[version]/release-notes.md`
- [ ] Verify GitHub Release page accessible
- [ ] Update release notes with actual release date
- [ ] Update release checklist with release date
- [ ] Commit: `chore(release): tag release [version]`

#### Post-Release Steps (Steps 5, 6)

**Step 5: Post-Release Verification**
- [ ] Verify production deployment (if deploying)
- [ ] Verify health checks passing (if deployed)
- [ ] Verify monitoring active (if deployed)
- [ ] Verify logging configured correctly (if deployed)
- [ ] Test release artifacts (tag, release notes, documentation)
- [ ] Verify release notes accessible
- [ ] Verify documentation links work
- [ ] Commit: `chore(release): complete post-release verification for [version]`

**Step 6: Release Communication**
- [ ] Publish release notes (if applicable)
- [ ] Notify team (if applicable)
- [ ] Notify users (if applicable)
- [ ] Update project status documentation
- [ ] Update feature status (mark MVP complete)
- [ ] Commit: `docs(release): complete release communication for [version]`

---

### 3. Commit Strategy

**Commit after each logical unit:**
- One commit per step group
- One commit per verification run
- One commit per documentation update

**Commit message format:**
```
type(scope): brief description

Longer explanation if needed

Related: Release [version], Step [N]
```

**Types:**
- `docs` - Documentation updates
- `chore` - Release tasks, tagging, verification
- `fix` - Bug fixes found during verification

**Examples:**
```bash
git commit -m "docs(release): finalize release documentation for v0.1.0"
git commit -m "chore(release): complete pre-release verification for v0.1.0"
git commit -m "chore(release): tag release v0.1.0"
```

---

### 4. Check Step Completion

**After implementing a step:**

- [ ] All tasks for this step complete
- [ ] Verification steps passed (if applicable)
- [ ] Documentation updated (if applicable)
- [ ] Step checklist items completed
- [ ] Committed to release branch

**Update transition plan document:**
- Mark step items as complete: `- [x]` instead of `- [ ]`
- Don't commit transition plan doc changes until release complete

---

### 5. Stop After Step Group Completion

**After completing a step group:**

- [ ] Step group fully implemented and verified
- [ ] All commits made to release branch
- [ ] Verification steps passed (if applicable)
- [ ] **STOP - Do NOT proceed to next step group**
- [ ] Present completion summary to user
- [ ] Indicate which steps were completed (e.g., "Steps 1-4 complete: Documentation finalized and updated")
- [ ] Wait for user to invoke command again for next step group

**Important:** This command handles ONE step group at a time (typically related steps). The user will invoke the command again with the next step number when ready to continue.

---

### 6. Complete All Steps - Create PR

**When ALL steps in release transition are done:**

**Pre-PR Checklist:**
- [ ] All steps completed
- [ ] All verification steps passed
- [ ] Release tagged (if Step 3 complete)
- [ ] Release documentation complete
- [ ] Transition plan document updated (all steps marked complete)
- [ ] Release notes finalized
- [ ] No critical issues found

**Create PR:**
1. Push final commits to release branch
2. Run Sourcery review: `dt-review` from dev-toolkit (if code changes)
3. Fill out priority matrix in `docs/maintainers/feedback/sourcery/pr##.md` (if review run)
4. Address any CRITICAL/HIGH issues before PR (if any)
5. Create PR with comprehensive description

**PR Title Format:**
```
chore: Release [version]
```

**PR Description Template:**
```markdown
## Release [version]

[Brief description of release]

---

## What's Included

### Release Preparation
- Release checklist completed
- Release notes finalized
- Pre-release verification complete
- Version tagged: [version]
- Release documentation updated

### Verification
- All tests passing
- Test coverage: [X]%
- Production readiness verified
- Deployment guide reviewed

---

## Testing

- [x] All automated tests passing
- [x] Coverage: [X]%
- [x] Pre-release verification complete
- [x] Post-release verification complete (if applicable)
- [ ] Sourcery review completed (if code changes)

---

## Related

- **Transition Plan:** `docs/maintainers/planning/releases/[version]/transition-plan.md`
- **Release Checklist:** `docs/maintainers/planning/releases/[version]/checklist.md`
- **Release Notes:** `docs/maintainers/planning/releases/[version]/release-notes.md`
```

**After PR Created:**
- [ ] Present PR link to user (DO NOT auto-merge)
- [ ] Wait for external review (dt-review, if applicable)
- [ ] Address CRITICAL/HIGH issues (if any)
- [ ] Get user approval before merge

---

## Step Detection Logic

**How to identify steps:**

Steps are numbered in transition plan documents:
- `### Step 1: Finalize Release Documentation`
- `### Step 2: Complete Pre-Release Verification`
- `### Step 3: Version Tagging and Release`
- etc.

**Step boundaries:**
- Each numbered section is a step
- Steps may have sub-items (checkboxes)
- Complete all sub-items before moving to next step

**Last step detection:**
- Check if there are more numbered steps after current
- Look for "Post-Transition" section (comes after all steps)
- If no more steps, it's time to create PR

---

## Common Patterns

### Pattern 1: Documentation Steps

**Steps:** 1 (Finalize) + 4 (Update)

**Steps:**
1. Review release checklist
2. Review release notes
3. Verify metrics and links
4. Update release hubs
5. Update release checklist
6. Update release notes
7. Commit

**Files typically modified:**
- `docs/maintainers/planning/releases/[version]/checklist.md`
- `docs/maintainers/planning/releases/[version]/release-notes.md`
- `docs/maintainers/planning/releases/[version]/README.md`
- `docs/maintainers/planning/releases/README.md`

### Pattern 2: Verification Steps

**Step:** 2 (Pre-Release Verification)

**Steps:**
1. Run test suite
2. Check coverage
3. Run linter
4. Verify documentation examples
5. Verify production scripts
6. Commit

**Commands:**
```bash
pytest backend/ -v
pytest --cov
flake8 backend/
```

### Pattern 3: Tagging Steps

**Step:** 3 (Version Tagging)

**Steps:**
1. Determine release commit
2. Create git tag
3. Push tag to remote
4. Verify tag
5. Update release date in docs
6. Commit

**Commands:**
```bash
git tag -a v0.1.0 -m "MVP Release v0.1.0"
git push origin v0.1.0
git tag -l v0.1.0
```

---

## Error Handling

**If verification fails:**
- Debug the failure
- Fix the issue
- Re-run verification
- Don't move to next step until verification passes

**If tagging fails:**
- Check if tag already exists
- Verify remote access
- Check tag format
- Re-try tagging

**If documentation issues found:**
- Fix documentation
- Re-verify links
- Update release notes
- Don't proceed until documentation accurate

---

## Release Completion Checklist

**Before marking release complete:**

- [ ] All steps completed
- [ ] All verification steps passed
- [ ] Release tagged
- [ ] Release documentation complete
- [ ] PR created and reviewed
- [ ] Sourcery review completed (if code changes)
- [ ] CRITICAL/HIGH issues addressed (if any)
- [ ] PR merged to develop
- [ ] Transition plan document status updated to "✅ Complete"
- [ ] Release hub updated with release date

---

## Tips

**While implementing:**
- Focus on ONE step group (typically related steps)
- Keep transition plan document open for reference
- Check off items as you complete them
- Don't skip verification steps
- Commit frequently (small commits)
- Push to branch regularly

**Step grouping:**
- Documentation steps naturally belong together
- Verification steps are separate (critical)
- Tagging step is separate (critical)
- Complete the full step group before stopping

**After completing step group:**
- **STOP - Do NOT continue to next step group**
- Present summary of what was accomplished
- Indicate which steps were completed (e.g., "Steps 1-4 complete")
- Wait for user to invoke command again

**Important reminders:**
- One step group per invocation (typically related steps)
- Complete step group fully before stopping
- Don't proceed to next step group automatically
- Use `/pr --release [version]` when all steps done

---

## Reference

**Transition Plan Documents:**
- `docs/maintainers/planning/releases/[version]/transition-plan.md`

**Release Planning:**
- `docs/maintainers/planning/releases/[version]/checklist.md`
- `docs/maintainers/planning/releases/[version]/release-notes.md`
- `docs/maintainers/planning/releases/[version]/README.md`
- `docs/maintainers/planning/releases/README.md`

**Related Commands:**
- `/pr --release [version]` - Create PR for release
- `/post-pr --release [version]` - Update documentation after release PR merge
- `/task-phase` - Implement phase tasks (similar workflow)

---

**Last Updated:** 2025-12-07  
**Status:** ✅ Active  
**Next:** Use `/pr --release [version]` when all steps complete, or `/task-release [version] [step]` for next step group

--- End Command ---

