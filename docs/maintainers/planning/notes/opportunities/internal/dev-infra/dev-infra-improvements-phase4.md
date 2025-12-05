# Dev-Infra Improvements - Phase 4

**Source:** Phase 4 (Search & Filter Projects) + Fix Batch System  
**Target:** ~/Projects/dev-infra template  
**Status:** 🟡 Pending  
**Date:** 2025-12-05

---

## Introduction

Phase 4 introduced search and filtering capabilities, but more importantly, established a comprehensive fix batch system for managing deferred issues. This document captures actionable improvements for the dev-infra template based on Phase 4 learnings.

**Why improvements matter:**
- Fix tracking system prevents technical debt accumulation
- PR-based organization scales with many PRs
- Combined workflows reduce friction
- Clear templates ensure consistency

**How discovered:**
- Deferred issues accumulated across phases
- Flat fix directory became unmanageable
- Multiple workflow steps needed automation
- Manual processes were error-prone

**What problem they solve:**
- Lost or forgotten deferred issues
- Unmanageable fix directory structure
- Inconsistent fix implementation workflow
- Manual tracking updates

---

## Pre-Project Setup

### Fix Tracking System Structure

- [ ] **Create fix directory structure**
  - **Location:** `docs/maintainers/planning/features/[feature]/fix/`
  - **Action:** Create hub-and-spoke structure with PR subdirectories
  - **Prevents/Enables:** Scalable fix tracking, prevents lost issues
  - **Content/Example:**
    ```
    fix/
    ├── README.md (main hub)
    ├── pr##/ (PR directories)
    │   ├── README.md (PR hub)
    │   └── batch-*.md (fix batch plans)
    └── archived/ (completed PRs)
        ├── README.md (archive hub)
        └── pr##/ (archived PR directories)
    ```
  - **Expected Impact:** Fix tracking scales well, easy to find fixes for specific PRs
  - **Priority:** HIGH
  - **Effort:** MEDIUM

### Fix Plan Template

- [ ] **Create fix plan template**
  - **Location:** `docs/maintainers/planning/features/[feature]/fix/pr##/batch-template.md`
  - **Action:** Template for fix batch plans with all required sections
  - **Prevents/Enables:** Consistent fix plans, clear implementation steps
  - **Content/Example:**
    ```markdown
    # Fix Plan: PR ## Batch [Priority] [Effort] - Batch [Number]

    **PR:** ##
    **Batch:** [priority]-[effort]-[batch-number]
    **Priority:** [Priority]
    **Effort:** [Effort]
    **Status:** 🔴 Not Started
    **Created:** YYYY-MM-DD
    **Issues:** [N] issue(s)

    ## Issues in This Batch

    | Issue | Priority | Impact | Effort | Description |
    |-------|----------|--------|--------|-------------|

    ## Issue Details

    ### Issue PR##-#N: [Title]

    **Location:** `file:line-range`
    **Sourcery Comment:** Comment #N
    **Priority:** [Priority] | **Impact:** [Impact] | **Effort:** [Effort]

    **Description:**
    [Description]

    **Current Code:**
    ```[language]
    [code snippet]
    ```

    **Proposed Solution:**
    [Solution description]

    ## Implementation Steps

    1. [Step 1]
       - [ ] Sub-step
       - [ ] Sub-step

    ## Definition of Done

    - [ ] All issues fixed
    - [ ] Tests passing
    - [ ] Code reviewed
    - [ ] Ready for PR
    ```
  - **Expected Impact:** Consistent fix plans, easier implementation
  - **Priority:** HIGH
  - **Effort:** LOW

---

## Project Structure

### Fix Directory Hub Templates

- [ ] **Create PR hub README template**
  - **Location:** `docs/maintainers/planning/features/[feature]/fix/pr##/README.md.template`
  - **Action:** Template for PR fix tracking hubs
  - **Prevents/Enables:** Consistent PR hubs, clear fix tracking
  - **Content/Example:**
    ```markdown
    # PR ## Fix Tracking

    **PR:** ## - [PR Title]
    **Date:** YYYY-MM-DD
    **Status:** 🟡 Planned
    **Last Updated:** YYYY-MM-DD

    ## 📋 Quick Links

    ### Fix Batches

    - **[batch-name.md](batch-name.md)** - [Description] ([Priority], [Effort], [N] issues)

    ## 📊 Summary

    **Total Issues:** [N]
    **Batches:** [M]
    **Status:** 🟡 Planned

    ## 📋 Deferred Issues

    **Date:** YYYY-MM-DD
    **Review:** PR ## Sourcery feedback
    **Status:** 🟡 **DEFERRED** / ✅ **NONE**

    [Deferred issues list or "NONE" note]
    ```
  - **Expected Impact:** Consistent PR hubs, easy navigation
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## Configuration

### Sourcery Review Path Configuration

- [ ] **Document dt-review path parameter**
  - **Location:** `.cursor/commands/pr-validation.md`
  - **Action:** Document path parameter usage for dt-review
  - **Prevents/Enables:** Correct review file locations, no extra directories
  - **Content/Example:**
    ```bash
    # Run review with custom path
    ~/Projects/dev-toolkit/bin/dt-review [pr-number] \
      docs/maintainers/feedback/sourcery/pr##.md
    ```
  - **Expected Impact:** Reviews saved to correct location, no cleanup needed
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## Documentation

### Manual Testing Guide Template

- [ ] **Create manual testing scenario template**
  - **Location:** `docs/maintainers/planning/features/[feature]/manual-testing.md.template`
  - **Action:** Template for manual testing scenarios
  - **Prevents/Enables:** Consistent scenarios, complete coverage
  - **Content/Example:**
    ```markdown
    ### Scenario N: [Feature Name] - [Test Case]

    **Type:** API / CLI
    **Prerequisites:** [Any setup needed]

    **API Test:**
    ```bash
    curl [endpoint] [options]
    ```

    **Expected Response:**
    - Status: [code]
    - Body: [description]

    **CLI Test:**
    ```bash
    ./proj [command] [options]
    ```

    **Expected Output:**
    - [Description]

    **Verification:**
    - [ ] Status code correct
    - [ ] Response body matches expected
    - [ ] No errors in logs
    ```
  - **Expected Impact:** Consistent scenarios, easier to add new ones
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## Development Workflow

### Fix Planning Command

- [ ] **Include /fix-plan command**
  - **Location:** `.cursor/commands/fix-plan.md`
  - **Action:** Complete command template for creating fix batches
  - **Prevents/Enables:** Systematic batching of deferred issues
  - **Content/Example:**
    ```markdown
    # Fix Plan Command

    [Complete command template with:
    - PR detection
    - Issue parsing
    - Batching logic
    - Fix plan creation
    - PR hub updates]
    ```
  - **Expected Impact:** Consistent fix batching, no lost issues
  - **Priority:** HIGH
  - **Effort:** MEDIUM

### Fix Implementation Command

- [ ] **Include /fix-implement command**
  - **Location:** `.cursor/commands/fix-implement.md`
  - **Action:** Complete command template for implementing fix batches
  - **Prevents/Enables:** Systematic fix implementation with TDD workflow
  - **Content/Example:**
    ```markdown
    # Fix Implement Command

    [Complete command template with:
    - Fix plan loading
    - Branch creation
    - TDD workflow
    - Tracking updates
    - PR creation]
    ```
  - **Expected Impact:** Consistent fix implementation, clear workflow
  - **Priority:** HIGH
  - **Effort:** MEDIUM

### Fix Review Command

- [ ] **Include /fix-review command**
  - **Location:** `.cursor/commands/fix-review.md`
  - **Action:** Complete command template for reviewing old deferred issues
  - **Prevents/Enables:** Periodic review of accumulated issues
  - **Content/Example:**
    ```markdown
    # Fix Review Command

    [Complete command template with:
    - Issue scanning
    - Accumulation detection
    - Quick win identification
    - Review report generation]
    ```
  - **Expected Impact:** Proactive technical debt management
  - **Priority:** MEDIUM
  - **Effort:** MEDIUM

### PR Validation Command

- [ ] **Include /pr-validation command**
  - **Location:** `.cursor/commands/pr-validation.md`
  - **Action:** Complete command template for combined PR validation
  - **Prevents/Enables:** Single command for complete PR validation
  - **Content/Example:**
    ```markdown
    # PR Validation Command

    [Complete command template with:
    - Unrelated file restoration
    - Manual testing guide updates
    - Manual testing execution
    - Sourcery review
    - Priority matrix filling]
    ```
  - **Expected Impact:** Complete validation in one command, nothing missed
  - **Priority:** HIGH
  - **Effort:** MEDIUM

---

## CLI/Tooling

### Query Parameter Filtering Pattern

- [ ] **Document query parameter filtering pattern**
  - **Location:** `backend/app/api/[resource].py.template`
  - **Action:** Include pattern for dynamic query building
  - **Prevents/Enables:** Consistent filtering implementation
  - **Content/Example:**
    ```python
    def list_resources():
        """List all resources with optional filtering."""
        query = Resource.query

        # Apply filters
        if 'status' in request.args:
            status = request.args['status']
            if status in VALID_STATUSES:
                query = query.filter_by(status=status)

        # Apply search
        if 'search' in request.args:
            search_term = f"%{request.args['search']}%"
            query = query.filter(
                or_(
                    Resource.field1.ilike(search_term),
                    Resource.field2.ilike(search_term)
                )
            )

        resources = query.order_by(Resource.id).all()
        return jsonify([resource.to_dict() for resource in resources]), 200
    ```
  - **Expected Impact:** Consistent filtering across resources
  - **Priority:** MEDIUM
  - **Effort:** LOW

### Case-Insensitive Search Pattern

- [ ] **Document case-insensitive search pattern**
  - **Location:** `backend/app/api/[resource].py.template`
  - **Action:** Include pattern for case-insensitive text search
  - **Prevents/Enables:** User-friendly search functionality
  - **Content/Example:**
    ```python
    from sqlalchemy import or_

    if 'search' in request.args:
        search_term = f"%{request.args['search']}%"
        query = query.filter(
            or_(
                Model.field1.ilike(search_term),
                Model.field2.ilike(search_term)
            )
        )
    ```
  - **Expected Impact:** Consistent search implementation
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## Summary

### High Priority Items

1. **Fix tracking system structure** - Scales well, prevents lost issues
2. **Fix plan template** - Consistent plans, clear implementation
3. **Fix planning command** - Systematic batching
4. **Fix implementation command** - Clear workflow
5. **PR validation command** - Complete validation

### Medium Priority Items

1. **PR hub template** - Consistent hubs
2. **Manual testing scenario template** - Consistent scenarios
3. **Query parameter filtering pattern** - Consistent filtering
4. **Case-insensitive search pattern** - Consistent search
5. **Fix review command** - Proactive debt management

### Low Priority Items

1. **Sourcery review path documentation** - Correct file locations

---

**Last Updated:** 2025-12-05  
**Status:** 🟡 Pending  
**Next:** Apply to dev-infra template

