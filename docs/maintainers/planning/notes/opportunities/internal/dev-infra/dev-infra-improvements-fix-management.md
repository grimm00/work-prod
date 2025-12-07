# Dev-Infra Improvements: Fix Management System

**Source:** Fix Management System Learnings (2025-12-05)  
**Target:** ~/Projects/dev-infra template  
**Status:** 🟡 Pending  
**Why:** Comprehensive fix management system proven effective in work-prod  
**How discovered:** Built and refined over 2 days implementing PR #14 and #15  
**Problem solved:** Efficient handling of code review feedback, deferred issues, and fix tracking

---

## Introduction

The fix management system evolved from simple tracking to a comprehensive workflow supporting both PR-specific and cross-PR fix batches. This document provides actionable improvements for the dev-infra template based on lessons learned.

**Key Components:**
- Fix tracking with hub-and-spoke organization
- Cross-PR batch system
- Automated fix workflow commands
- Fix review and batching
- Graceful handling of missing reviews

---

## Pre-Project Setup

### Fix Tracking Structure

- [ ] **Create fix tracking directory structure**
  - **Location:** `docs/maintainers/planning/features/[feature]/fix/`
  - **Action:** Pre-create directory structure with hub-and-spoke pattern
  - **Prevents/Enables:** Consistent fix organization, easy navigation
  - **Content/Example:**
    ```
    fix/
    ├── README.md                    # Main hub
    ├── pr##/                        # PR-specific fixes
    │   ├── README.md                # PR hub
    │   └── [fix-plans].md          # Individual fixes/batches
    ├── cross-pr/                    # Cross-PR batches
    │   ├── README.md                # Cross-PR hub
    │   └── [batch-plans].md        # Cross-PR batches
    └── archived/                    # Completed PRs
        └── README.md                # Archive hub
    ```
  - **Expected Impact:** Consistent fix organization across all projects
  - **Priority:** HIGH
  - **Effort:** LOW

- [ ] **Include fix tracking hub templates**
  - **Location:** `docs/maintainers/planning/features/[feature]/fix/README.md`
  - **Action:** Provide hub template with quick links, summary, and navigation
  - **Prevents/Enables:** Consistent hub structure, easy fix discovery
  - **Content/Example:**
    ```markdown
    # [Feature] Feature - Fix Tracking

    **Purpose:** Track fixes identified through code review  
    **Status:** ✅ Active  
    **Last Updated:** YYYY-MM-DD  
    **Progress:** X/Y complete (Z%)

    ## 📋 Quick Links

    ### Active PRs
    - **[PR ##](pr##/README.md)** - [Description] ([Status])

    ### Cross-PR Batches
    - **[Cross-PR Batches](cross-pr/README.md)** - [Description]

    ## 📊 Summary
    [Progress breakdown]
    ```
  - **Expected Impact:** Standardized fix tracking hubs
  - **Priority:** HIGH
  - **Effort:** LOW

---

## Project Structure

### Fix Plan Templates

- [ ] **Create fix plan template**
  - **Location:** `.cursor/templates/fix-plan-template.md`
  - **Action:** Provide template for individual fix plans
  - **Prevents/Enables:** Consistent fix plan structure, clear implementation guidance
  - **Content/Example:**
    ```markdown
    # Fix Plan: PR ## Issue #N - [Title]

    **PR:** ##  
    **Sourcery Comment:** #N  
    **Status:** 🔴 Not Started  
    **Created:** YYYY-MM-DD  
    **Priority:** [Priority] | **Impact:** [Impact] | **Effort:** [Effort]

    ## Issue Details

    **Location:** `[file]:[line]`

    **Description:**
    [Full description]

    **Current Code:**
    ```[language]
    [code snippet]
    ```

    **Proposed Solution:**
    ```[language]
    [fixed code]
    ```

    ## Implementation Steps

    1. [ ] Step 1
    2. [ ] Step 2

    ## Testing

    - [ ] All existing tests pass
    - [ ] New tests added (if applicable)

    ## Definition of Done

    - [ ] Issue fixed
    - [ ] Tests passing
    - [ ] Code reviewed
    ```
  - **Expected Impact:** Consistent fix plans, clear implementation guidance
  - **Priority:** HIGH
  - **Effort:** LOW

- [ ] **Create batch fix plan template**
  - **Location:** `.cursor/templates/batch-fix-plan-template.md`
  - **Action:** Provide template for fix batch plans
  - **Prevents/Enables:** Consistent batch structure, clear batch organization
  - **Content/Example:**
    ```markdown
    # Fix Plan: PR ## Batch [Priority] [Effort] - Batch [Number]

    **PR:** ##  
    **Batch:** [priority]-[effort]-[batch-number]  
    **Priority:** [Priority]  
    **Effort:** [Effort]  
    **Status:** 🔴 Not Started  
    **Created:** YYYY-MM-DD  
    **Issues:** [N] issues

    ## Issues in This Batch

    | Issue   | Priority   | Impact   | Effort   | Description   |
    | ------- | ---------- | -------- | -------- | ------------- |
    | PR##-#N | [Priority] | [Impact] | [Effort] | [Description] |

    ## Issue Details

    [For each issue...]

    ## Implementation Steps

    [For each issue...]

    ## Definition of Done

    - [ ] All issues in batch fixed
    - [ ] Tests passing
    - [ ] Ready for PR
    ```
  - **Expected Impact:** Consistent batch plans, clear batch organization
  - **Priority:** HIGH
  - **Effort:** LOW

---

## Configuration

### Fix Management Commands

- [ ] **Include fix management command suite**
  - **Location:** `.cursor/commands/`
  - **Action:** Include all fix management commands
  - **Prevents/Enables:** Standardized fix workflow, automated fix tracking
  - **Content/Example:**
    - `fix-plan.md` - Create fix plans from reviews
    - `fix-implement.md` - Implement fixes from batches
    - `fix-review.md` - Review old deferred issues
    - `pr-validation.md` - Validate PRs (handles missing reviews)
    - `post-pr.md` - Update docs after PR merge
  - **Expected Impact:** Consistent fix workflow across projects
  - **Priority:** CRITICAL
  - **Effort:** MEDIUM

- [ ] **Document fix workflow**
  - **Location:** `docs/maintainers/planning/notes/fix-workflow.md`
  - **Action:** Document complete fix management workflow
  - **Prevents/Enables:** Clear understanding of fix process, onboarding
  - **Content/Example:**
    ```markdown
    # Fix Management Workflow

    ## Overview

    1. PR merged → Sourcery review available
    2. `/fix-plan` → Creates fix batches
    3. `/fix-implement [batch]` → Implements fixes
    4. `/pr --fix [batch]` → Creates PR
    5. PR merged → `/post-pr` → Updates docs

    ## Commands

    - `/fix-plan` - Create fix plans
    - `/fix-implement` - Implement fixes
    - `/fix-review` - Review deferred issues
    - `/pr-validation` - Validate PRs
    - `/post-pr` - Update docs
    ```
  - **Expected Impact:** Clear fix workflow documentation
  - **Priority:** HIGH
  - **Effort:** LOW

---

## Testing Infrastructure

### Fix Testing Patterns

- [ ] **Document fix testing requirements**
  - **Location:** `docs/maintainers/planning/notes/fix-testing.md`
  - **Action:** Document TDD workflow for fixes
  - **Prevents/Enables:** Consistent fix quality, proper testing
  - **Content/Example:**
    ```markdown
    # Fix Testing Requirements

    ## TDD Workflow

    1. **RED:** Write failing test
    2. **GREEN:** Implement fix
    3. **REFACTOR:** Improve code

    ## Testing Checklist

    - [ ] All existing tests pass
    - [ ] New tests added (if applicable)
    - [ ] Coverage maintained/improved
    - [ ] No regressions introduced
    ```
  - **Expected Impact:** Consistent fix quality
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## Documentation

### Fix Tracking Documentation

- [ ] **Include fix tracking README template**
  - **Location:** `docs/maintainers/planning/features/[feature]/fix/README.md`
  - **Action:** Provide template for fix tracking hub
  - **Prevents/Enables:** Consistent fix tracking, easy navigation
  - **Content/Example:** See "Fix Tracking Structure" section above
  - **Expected Impact:** Standardized fix tracking
  - **Priority:** HIGH
  - **Effort:** LOW

- [ ] **Document cross-PR batch system**
  - **Location:** `docs/maintainers/planning/notes/cross-pr-batches.md`
  - **Action:** Document cross-PR batch creation and management
  - **Prevents/Enables:** Efficient handling of deferred issues
  - **Content/Example:**
    ```markdown
    # Cross-PR Fix Batches

    ## Overview

    Cross-PR batches group related fixes from multiple PRs into
    single implementable batches.

    ## Batch Naming

    Format: `[name]-[priority]-[effort]-[batch-number]`
    Example: `quick-wins-low-low-01`

    ## Creation

    Use `/fix-review` to identify deferred issues, then `/fix-plan
    --from-review-report` to create batches.
    ```
  - **Expected Impact:** Efficient deferred issue handling
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## Development Workflow

### Fix Review Process

- [ ] **Include fix review command**
  - **Location:** `.cursor/commands/fix-review.md`
  - **Action:** Provide command for reviewing old deferred issues
  - **Prevents/Enables:** Proactive fix management, batch creation
  - **Content/Example:** See fix-review command documentation
  - **Expected Impact:** Better deferred issue management
  - **Priority:** MEDIUM
  - **Effort:** MEDIUM

- [ ] **Document review handling**
  - **Location:** `.cursor/commands/pr-validation.md`
  - **Action:** Document graceful handling of missing reviews
  - **Prevents/Enables:** Workflow doesn't break on missing reviews
  - **Content/Example:**
    ```markdown
    ### 4. Run Sourcery Review (dt-review)

    **Note:** If review is not available or fails, that's okay -
    continue without review

    **If review fails:**
    - This is acceptable - some PRs may not have reviews available
    - Continue with validation workflow
    - Note in summary that review was skipped
    ```
  - **Expected Impact:** Robust validation workflow
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## CLI/Tooling

### Fix Management Automation

- [ ] **Include fix progress calculation script**
  - **Location:** `scripts/calculate-fix-progress.sh`
  - **Action:** Automate fix tracking progress calculation
  - **Prevents/Enables:** Accurate progress tracking, reduced manual work
  - **Content/Example:**
    ```bash
    #!/bin/bash
    # Calculate fix tracking progress from fix tracking files
    # Updates progress in fix/README.md
    ```
  - **Expected Impact:** Automated progress tracking
  - **Priority:** LOW
  - **Effort:** MEDIUM

- [ ] **Include branch cleanup script**
  - **Location:** `scripts/cleanup-merged-branches.sh`
  - **Action:** Clean up merged branches automatically
  - **Prevents/Enables:** Clean repository, reduced manual cleanup
  - **Content/Example:**
    ```bash
    #!/bin/bash
    # Clean up merged branches (local and remote)
    # Verify merge status before cleanup
    ```
  - **Expected Impact:** Automated branch cleanup
  - **Priority:** LOW
  - **Effort:** LOW

---

## Summary

**Total Improvements:** 12  
**Priority Breakdown:**
- CRITICAL: 1 (fix management commands)
- HIGH: 5 (structure, templates, workflow)
- MEDIUM: 5 (review, testing, documentation)
- LOW: 1 (automation scripts)

**Expected Impact:**
- Consistent fix management across projects
- Reduced documentation overhead
- Standardized fix workflow
- Efficient deferred issue handling
- Robust validation process

**Implementation Order:**
1. Fix tracking structure (HIGH, LOW effort)
2. Fix management commands (CRITICAL, MEDIUM effort)
3. Fix plan templates (HIGH, LOW effort)
4. Workflow documentation (HIGH, LOW effort)
5. Automation scripts (LOW priority, can defer)

---

**Last Updated:** 2025-12-05  
**Status:** 🟡 Pending  
**Next:** Apply improvements to dev-infra template

