# Fix Plan Command

Analyzes Sourcery review for a PR, batches issues by priority and effort, and creates fix plans ready for implementation.

---

## Workflow Overview

**When to use:**
- After PR is merged and Sourcery review is available
- To organize deferred issues into implementable batches
- Before implementing fixes

**Key principle:** Batch issues intelligently by priority first, then by effort, creating manageable fix plans.

---

## Usage

**Command:** `@fix-plan [pr-number] [options]`

**Examples:**
- `@fix-plan` - Analyze last merged PR (default)
- `@fix-plan 12` - Analyze PR #12
- `@fix-plan 12 --max-batch-size 3` - Custom batch size
- `@fix-plan 12 --priority MEDIUM` - Only plan MEDIUM priority issues
- `@fix-plan --review-old` - Review and plan old deferred issues
- `@fix-plan --archive-completed` - Archive completed fix plans

**Options:**
- `--max-batch-size N` - Maximum issues per batch (default: 5 for MEDIUM/LOW, 3 for HIGH/CRITICAL)
- `--priority LEVEL` - Only plan issues of this priority (CRITICAL, HIGH, MEDIUM, LOW)
- `--min-effort LEVEL` - Only plan issues with at least this effort (LOW, MEDIUM, HIGH)
- `--dry-run` - Show batching plan without creating fix plan files
- `--review-old` - Review old deferred issues (see "Reviewing Old Issues" section)
- `--archive-completed` - Archive completed fix plans to `fix/archived/`

---

## Step-by-Step Process

### 1. Identify PR and Review File

**Default behavior:**
- Find last merged PR (check git log or GitHub)
- Locate Sourcery review file: `docs/maintainers/feedback/sourcery/pr##.md`

**Manual specification:**
- Use provided PR number
- Verify review file exists

**Commands:**
```bash
# Find last merged PR
gh pr list --state merged --limit 1 --json number,title,mergedAt

# Check if review file exists
ls docs/maintainers/feedback/sourcery/pr##.md
```

**Checklist:**
- [ ] PR number identified (or using default)
- [ ] Review file exists and is readable
- [ ] Priority matrix is filled out in review file

---

### 2. Parse Sourcery Review

**Extract from review file:**
- All individual comments
- Priority matrix assessments
- Overall comments (if applicable)
- File locations and descriptions

**Parse priority matrix:**
- Extract Priority, Impact, Effort for each comment
- Identify which issues are deferred (MEDIUM/LOW priority)
- Note CRITICAL/HIGH issues that need immediate attention

**Example parsing:**
```markdown
| Comment | Priority | Impact | Effort | Notes |
|---------|----------|--------|--------|-------|
| #1 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Use click.Choice for CLI validation |
| #2 | 🟡 MEDIUM | 🟢 LOW | 🟢 LOW | Tighten test expectations |
| #3 | 🟡 MEDIUM | 🟢 LOW | 🟡 MEDIUM | Avoid conditionals in tests |
```

**Checklist:**
- [ ] All comments parsed
- [ ] Priority/Impact/Effort extracted
- [ ] Deferred issues identified

---

### 3. Check for Already-Fixed Issues

**Check fix tracking:**
- Review `docs/maintainers/planning/features/projects/fix/README.md`
- Check individual fix plan files
- Verify GitHub PRs for fixes

**Mark fixed issues:**
- If issue was fixed in a previous PR, mark as "✅ Complete" in review file
- Update fix tracking to reflect completion
- Archive fix plan if exists

**Archive completed issues:**
- Move fix plan to `fix/archived/` directory (if exists)
- Update fix tracking to remove from active list
- Note completion date and PR number

**Default behavior:**
- Include all deferred issues (MEDIUM/LOW priority)
- Skip CRITICAL/HIGH if already fixed
- Skip issues marked as "✅ Complete" in fix tracking
- Skip issues in archived fix plans

**Checklist:**
- [ ] Fix tracking reviewed for completed issues
- [ ] Already-fixed issues marked/archived
- [ ] Only unfixed issues included in planning

---

### 4. Batch Issues by Priority and Effort

**Batching Strategy:**

1. **Group by Priority** (highest first):
   - 🔴 CRITICAL
   - 🟠 HIGH
   - 🟡 MEDIUM
   - 🟢 LOW

2. **Within each priority, group by Effort** (lowest first):
   - 🟢 LOW effort
   - 🟡 MEDIUM effort
   - 🟠 HIGH effort
   - 🔴 VERY_HIGH effort

3. **Create batches within each priority/effort group:**
   - **CRITICAL/HIGH:** Max 3 issues per batch (urgent, need careful review)
   - **MEDIUM/LOW:** Max 5 issues per batch (can handle more at once)
   - **VERY_HIGH effort:** 1 issue per batch (complex, needs focus)

**Batch Naming:**
- Format: `pr##-batch-[priority]-[effort]-[batch-number]`
- Examples:
  - `pr12-batch-medium-low-01` - PR #12, MEDIUM priority, LOW effort, batch 1
  - `pr12-batch-low-low-01` - PR #12, LOW priority, LOW effort, batch 1
  - `pr12-batch-critical-low-01` - PR #12, CRITICAL priority, LOW effort, batch 1

**Example Batching:**

**PR #12 Issues:**
- PR12-#1: MEDIUM, LOW effort
- PR12-#2: MEDIUM, LOW effort
- PR12-#3: MEDIUM, MEDIUM effort
- PR12-#4: LOW, LOW effort
- PR12-#5: LOW, LOW effort

**Batches Created:**
- `pr12-batch-medium-low-01`: PR12-#1, PR12-#2 (2 issues)
- `pr12-batch-medium-medium-01`: PR12-#3 (1 issue)
- `pr12-batch-low-low-01`: PR12-#4, PR12-#5 (2 issues)

**Checklist:**
- [ ] Issues grouped by priority
- [ ] Within priority, grouped by effort
- [ ] Batches created with appropriate sizes
- [ ] Batch names follow convention

---

### 5. Create Fix Plan Files

**Location:** `docs/maintainers/planning/features/projects/fix/`

**File naming:**
- Format: `pr##-batch-[priority]-[effort]-[batch-number].md`
- Example: `pr12-batch-medium-low-01.md`

**Fix Plan Template:**

```markdown
# Fix Plan: PR ## Batch [Priority] [Effort] - Batch [Number]

**PR:** ##  
**Batch:** [priority]-[effort]-[batch-number]  
**Priority:** [Priority Level]  
**Effort:** [Effort Level]  
**Status:** 🔴 Not Started  
**Created:** YYYY-MM-DD  
**Issues:** [N] issues

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR##-#N | [Priority] | [Impact] | [Effort] | [Description] |

---

## Overview

This batch contains [N] [priority] priority issues with [effort] effort. These issues are related to [common theme if applicable].

**Estimated Time:** [X] hours  
**Files Affected:** [list of files]

---

## Issues Details

### Issue PR##-#N: [Short Description]

**Location:** `[file]:[line]`  
**Sourcery Comment:** Comment #N  
**Priority:** [Priority] | **Impact:** [Impact] | **Effort:** [Effort]

**Description:**
[Full description from Sourcery review]

**Current Code:**
```[language]
[code snippet]
```

**Proposed Solution:**
[Solution description or code]

---

## Implementation Steps

1. **Issue PR##-#N**
   - [ ] Step 1
   - [ ] Step 2
   - [ ] Step 3

2. **Issue PR##-#M**
   - [ ] Step 1
   - [ ] Step 2

---

## Testing

- [ ] All existing tests pass
- [ ] New tests added (if applicable)
- [ ] Manual testing completed
- [ ] No regressions introduced

---

## Files to Modify

- `[file1]` - [reason]
- `[file2]` - [reason]

---

## Definition of Done

- [ ] All issues in batch fixed
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Documentation updated (if needed)
- [ ] Ready for PR

---

**Batch Rationale:**
These issues are batched together because they:
- Share similar priority and effort levels
- May affect related code areas
- Can be implemented together efficiently
```

**Checklist:**
- [ ] Fix plan file created for each batch
- [ ] All issues documented in batch files
- [ ] Implementation steps outlined
- [ ] Testing requirements specified

---

### 6. Update Fix Tracking

**File:** `docs/maintainers/planning/features/projects/fix/README.md`

**Add batch tracking section:**

```markdown
## 📋 PR ## Fix Batches

**Date:** YYYY-MM-DD  
**Review:** PR ## Sourcery feedback  
**Status:** 🟡 **PLANNED** - Fix plans created, ready for implementation

**Batches:**

| Batch | Priority | Effort | Issues | Status | File |
|-------|----------|--------|--------|--------|------|
| pr##-batch-medium-low-01 | 🟡 MEDIUM | 🟢 LOW | 2 | 🔴 Not Started | [pr##-batch-medium-low-01.md](pr##-batch-medium-low-01.md) |
| pr##-batch-medium-medium-01 | 🟡 MEDIUM | 🟡 MEDIUM | 1 | 🔴 Not Started | [pr##-batch-medium-medium-01.md](pr##-batch-medium-medium-01.md) |
| pr##-batch-low-low-01 | 🟢 LOW | 🟢 LOW | 2 | 🔴 Not Started | [pr##-batch-low-low-01.md](pr##-batch-low-low-01.md) |

**Total:** [N] batches, [M] issues
```

**Checklist:**
- [ ] Fix tracking updated with batch information
- [ ] Batch table added
- [ ] Status tracking initialized

---

### 7. Summary Report

**Present to user:**

```markdown
## Fix Plan Complete

**PR:** #N - [PR Title]

### Issues Analyzed
- Total issues: [N]
- Deferred issues: [M]
- Already fixed: [K]

### Batches Created
- [N] batches created
- Priority breakdown:
  - CRITICAL: [X] batches
  - HIGH: [Y] batches
  - MEDIUM: [Z] batches
  - LOW: [W] batches

### Next Steps
1. Review fix plans in `docs/maintainers/planning/features/projects/fix/`
2. Use `/fix-implement` command to implement batches
3. Start with CRITICAL/HIGH batches first
```

---

## Batching Logic Details

### Batch Size Guidelines

**CRITICAL Priority:**
- Max 1-2 issues per batch (urgent, need careful attention)
- Each issue may need separate PR

**HIGH Priority:**
- Max 2-3 issues per batch
- Can combine related issues

**MEDIUM Priority:**
- Max 3-5 issues per batch
- Group by related functionality if possible

**LOW Priority:**
- Max 5 issues per batch
- Can handle larger batches

**Effort Considerations:**
- VERY_HIGH effort: Always 1 issue per batch
- HIGH effort: Max 2 issues per batch
- MEDIUM effort: Max 3-4 issues per batch
- LOW effort: Can batch up to max size

### Related Issue Grouping

**If issues affect same files:**
- Prefer grouping in same batch
- Reduces file switching overhead

**If issues are similar (e.g., all test improvements):**
- Can batch together even if different files
- Creates cohesive PR

---

## Common Issues

### Issue: No Review File Found

**Solution:**
- Check if PR number is correct
- Verify review was run (`dt-review` command)
- May need to run review first

### Issue: Priority Matrix Not Filled

**Solution:**
- Fill priority matrix in review file first
- Use `/pr-validation` command to ensure matrix is complete

### Issue: All Issues Already Fixed

**Solution:**
- Check fix tracking document
- Update review file status if needed
- No batches needed

### Issue: Too Many Issues in One Batch

**Solution:**
- Reduce `--max-batch-size` parameter
- Manually split batches if needed
- Consider creating separate batches for different file areas

---

## Tips

### Before Running

- Ensure Sourcery review is complete
- Verify priority matrix is filled out
- Check if any issues were already fixed

### During Planning

- Review batching logic makes sense
- Consider related issues grouping
- Adjust batch sizes if needed

### After Planning

- Review fix plan files for accuracy
- Verify batch sizes are manageable
- Consider implementation order (CRITICAL first)

---

## Reference

**Review Files:**
- `docs/maintainers/feedback/sourcery/pr##.md`

**Fix Plans:**
- `docs/maintainers/planning/features/projects/fix/pr##-batch-*.md`

**Fix Tracking:**
- `docs/maintainers/planning/features/projects/fix/README.md`

**Related Commands:**
- `/fix-implement` - Implement fixes from a batch
- `/fix-review` - Review old deferred issues for addressing
- `/pr-validation` - Run Sourcery review and fill priority matrix

---

**Last Updated:** 2025-12-04  
**Status:** ✅ Active  
**Next:** Use `/fix-implement` to implement batches or `/fix-review` to review old issues

