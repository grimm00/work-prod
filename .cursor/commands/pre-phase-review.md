# Pre-Phase Review Command

Review and align phase documentation before starting a new phase. Ensures scope clarity, documentation consistency, and readiness for implementation.

---

## Workflow Overview

**When to use:**

- Before starting a new phase
- After completing a phase (to prepare for next)
- When scope is unclear or documentation inconsistent
- To verify prerequisites are met

**Key principle:** Catch scope mismatches, documentation inconsistencies, and missing prerequisites before starting work. Prevents confusion and rework.

---

## Usage

**Command:** `/pre-phase-review [phase-number] [options]`

**Examples:**

- `/pre-phase-review 6` - Review Phase 6 before starting
- `/pre-phase-review 6 --fix` - Review Phase 6 and fix inconsistencies
- `/pre-phase-review --current` - Review current phase (from status doc)
- `/pre-phase-review --all` - Review all remaining phases

**Options:**

- `--fix` - Automatically fix inconsistencies found
- `--dry-run` - Show what would be fixed without making changes
- `--strict` - Fail if any inconsistencies found
- `--check-prerequisites` - Verify prerequisites are met

---

## Step-by-Step Process

### 1. Identify Phase Documents

**Find all phase-related documents:**

1. **Phase document:** `docs/maintainers/planning/features/[feature]/phase-[N].md`
2. **Status document:** `docs/maintainers/planning/features/[feature]/status-and-next-steps.md`
3. **Feature plan:** `docs/maintainers/planning/features/[feature]/feature-plan.md`
4. **Feature README:** `docs/maintainers/planning/features/[feature]/README.md`

**Checklist:**

- [ ] Phase document found
- [ ] Status document found
- [ ] Feature plan found
- [ ] Feature README found

---

### 2. Extract Phase Scope

**Read phase document and extract:**

- Phase title/name
- Phase description/overview
- Goals
- Tasks
- Duration estimate
- Prerequisites
- Success criteria

**Checklist:**

- [ ] Phase title extracted
- [ ] Description extracted
- [ ] Goals identified
- [ ] Tasks listed
- [ ] Duration noted
- [ ] Prerequisites checked

---

### 3. Check Documentation Consistency

**Compare phase scope across documents:**

1. **Phase Document vs. Status Document:**
   - Does status document mention correct phase name?
   - Does "Next Steps" section match phase goals?
   - Is phase listed correctly in progress tracking?

2. **Phase Document vs. Feature Plan:**
   - Does feature plan mention correct phase name?
   - Does phase description match?
   - Are goals aligned?

3. **Phase Document vs. Feature README:**
   - Does README link to correct phase document?
   - Is phase description consistent?
   - Is status indicator correct?

**Checklist:**

- [ ] Phase name consistent across all docs
- [ ] Description consistent
- [ ] Goals aligned
- [ ] Duration matches
- [ ] Prerequisites match

---

### 4. Verify Prerequisites

**Check if prerequisites are met:**

1. **Previous phases complete:**
   - Are all prerequisite phases marked complete?
   - Are PRs merged?
   - Are tests passing?

2. **Dependencies ready:**
   - Are required features implemented?
   - Are APIs available?
   - Are tools installed?

3. **Documentation ready:**
   - Are research documents complete?
   - Are ADRs created?
   - Are patterns documented?

**Checklist:**

- [ ] Prerequisites met
- [ ] Dependencies available
- [ ] Documentation ready
- [ ] No blockers

---

### 5. Identify Inconsistencies

**Document all inconsistencies found:**

**Common inconsistencies:**

1. **Scope Mismatch:**
   - Phase document says "X" but status says "Y"
   - Different phase names in different docs
   - Conflicting goals

2. **Status Mismatch:**
   - Phase marked complete in one doc but not another
   - Different status indicators
   - Missing completion dates

3. **Timeline Mismatch:**
   - Different duration estimates
   - Conflicting start/end dates
   - Timeline inconsistencies

4. **Prerequisite Mismatch:**
   - Different prerequisites listed
   - Missing prerequisites
   - Outdated prerequisites

**Format:**

```markdown
## Inconsistencies Found

### 1. Scope Mismatch: Phase 6

**Location:** `status-and-next-steps.md` vs `phase-6.md`

**Issue:**
- `status-and-next-steps.md` says: "Projects API - Relationships"
- `phase-6.md` says: "CLI Enhancement & Daily Use Tools"

**Impact:** Confusion about what Phase 6 actually includes

**Fix:** Update `status-and-next-steps.md` to match `phase-6.md`

**Priority:** 🔴 High
```

**Checklist:**

- [ ] All inconsistencies documented
- [ ] Impact assessed
- [ ] Fix identified
- [ ] Priority assigned

---

### 6. Fix Inconsistencies (If --fix)

**Apply fixes:**

1. **Update status document:**
   - Fix phase name/description
   - Update "Next Steps" section
   - Correct progress tracking

2. **Update feature plan:**
   - Align phase description
   - Update goals if needed
   - Fix timeline if needed

3. **Update feature README:**
   - Fix phase link/description
   - Update status indicator
   - Correct phase order

**Checklist:**

- [ ] Status document updated
- [ ] Feature plan updated
- [ ] Feature README updated
- [ ] All fixes applied

---

### 7. Generate Review Report

**Create review report:**

```markdown
# Pre-Phase Review: Phase [N]

**Phase:** [Phase Name]  
**Date:** [Date]  
**Reviewer:** [Name/AI]  
**Status:** ✅ Ready / 🟡 Needs Fixes / 🔴 Not Ready

---

## 📋 Phase Scope

**Title:** [Phase Title]  
**Description:** [Phase Description]  
**Duration:** [Estimate]  
**Prerequisites:** [List]

**Goals:**
- Goal 1
- Goal 2

**Tasks:**
- Task 1
- Task 2

---

## ✅ Documentation Consistency

### Phase Document
- **File:** `phase-[N].md`
- **Title:** [Title]
- **Status:** ✅ Consistent

### Status Document
- **File:** `status-and-next-steps.md`
- **Mention:** [What it says]
- **Status:** ✅ Consistent / 🟡 Inconsistent

### Feature Plan
- **File:** `feature-plan.md`
- **Mention:** [What it says]
- **Status:** ✅ Consistent / 🟡 Inconsistent

### Feature README
- **File:** `README.md`
- **Mention:** [What it says]
- **Status:** ✅ Consistent / 🟡 Inconsistent

---

## 🔍 Inconsistencies Found

### [Inconsistency 1]

**Location:** [Files]
**Issue:** [Description]
**Impact:** [Impact]
**Fix:** [Fix]
**Priority:** [Priority]

---

## ✅ Prerequisites Check

### Previous Phases
- [ ] Phase [N-1] complete
- [ ] Phase [N-2] complete (if needed)

### Dependencies
- [ ] Feature X implemented
- [ ] API Y available
- [ ] Tool Z installed

### Documentation
- [ ] Research complete
- [ ] ADRs created
- [ ] Patterns documented

---

## 🎯 Readiness Assessment

**Overall Status:** ✅ Ready / 🟡 Needs Fixes / 🔴 Not Ready

**Blockers:**
- [List any blockers]

**Recommendations:**
- [Recommendation 1]
- [Recommendation 2]

---

## 📝 Action Items

1. [ ] Fix inconsistency 1
2. [ ] Verify prerequisite 1
3. [ ] Update document X

---

**Last Updated:** [Date]  
**Next Review:** [When to review again]
```

**Checklist:**

- [ ] Review report generated
- [ ] Inconsistencies documented
- [ ] Prerequisites checked
- [ ] Readiness assessed
- [ ] Action items listed

---

### 8. Commit Changes

**If fixes applied:**

```bash
git add docs/maintainers/planning/features/[feature]/
git commit -m "docs(phase-[N]): align phase scope across documentation

- Fixed scope mismatch in status-and-next-steps.md
- Updated feature plan to match phase document
- Aligned feature README with phase scope
- Verified prerequisites met"
```

**Checklist:**

- [ ] Changes committed
- [ ] Commit message follows format
- [ ] Documentation updated

---

## Common Scenarios

### Scenario 1: Scope Mismatch

**Situation:** Phase document says "CLI Enhancement" but status says "Relationships"

**Action:**
1. Run `/pre-phase-review 6 --fix`
2. Review inconsistencies found
3. Apply fixes to align documentation
4. Commit changes

**Result:** Documentation aligned, clear scope for Phase 6

---

### Scenario 2: Missing Prerequisites

**Situation:** Phase 6 requires Phase 5 complete, but Phase 5 not marked complete

**Action:**
1. Run `/pre-phase-review 6 --check-prerequisites`
2. Verify Phase 5 actually complete
3. Update status if needed
4. Proceed if prerequisites met

**Result:** Prerequisites verified, ready to start

---

### Scenario 3: Multiple Inconsistencies

**Situation:** Phase scope inconsistent across 3+ documents

**Action:**
1. Run `/pre-phase-review 6 --dry-run`
2. Review all inconsistencies
3. Determine source of truth (usually phase document)
4. Run `/pre-phase-review 6 --fix` to apply fixes

**Result:** All documentation aligned

---

## Tips

### Source of Truth

- **Phase Document** (`phase-[N].md`) is usually the source of truth
- Update other documents to match phase document
- If phase document is wrong, update it first

### When to Review

- **Before starting:** Always review before beginning a phase
- **After completion:** Review next phase after completing current
- **When confused:** If scope unclear, run review

### Fix Strategy

- **Fix immediately:** High-priority inconsistencies
- **Document:** Medium-priority for later
- **Note:** Low-priority for awareness

---

## Reference

**Phase Documents:**

- `docs/maintainers/planning/features/[feature]/phase-[N].md`
- `docs/maintainers/planning/features/[feature]/status-and-next-steps.md`
- `docs/maintainers/planning/features/[feature]/feature-plan.md`
- `docs/maintainers/planning/features/[feature]/README.md`

**Related Commands:**

- `/reflect --phase` - Reflect on completed phase
- `/pr --phase [N]` - Create PR for phase completion
- `/post-pr` - Update documentation after PR merge

---

**Last Updated:** 2025-12-05  
**Status:** ✅ Active  
**Next:** Use before starting Phase 6

