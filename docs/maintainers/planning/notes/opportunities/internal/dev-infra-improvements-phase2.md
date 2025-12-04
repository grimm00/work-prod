# Dev-Infra Template Improvements - Phase 2

**Source:** work-prod Phase 2 learnings  
**Target:** ~/Projects/dev-infra project template  
**Status:** 🟡 Pending Application  
**Last Updated:** 2025-12-04

---

## 📋 Introduction

This document captures actionable improvements for the dev-infra project template, informed by real implementation experience in work-prod Phase 2. These improvements were discovered during Phase 2 (Create & Update Projects) implementation, critical security fixes, and process improvements.

**Why these improvements matter:**

- **Prevent security vulnerabilities** - Catch issues before they reach production
- **Encode review processes** - Make quality gates mandatory and clear
- **Improve developer workflow** - Reduce friction in common tasks
- **Scale documentation** - Patterns that work as projects grow

**How they were discovered:**

- Security vulnerability found in Sourcery review (exception leak)
- Process gaps (missing pre-merge review checkpoint)
- Documentation scaling issues (manual testing location)
- Successful patterns (deferred issues backlog, fast-track fixes)

**What problem they solve:**

- Security issues caught before production
- Consistent quality gates across all PRs
- Scalable documentation patterns
- Clear process for urgent fixes

---

## Section 1: Pre-Project Setup

### Narrative: Mandatory Security Review from Day 1

Phase 2 revealed that even well-tested code can have security vulnerabilities that only external review catches. The exception leak issue wasn't obvious to the developer but was immediately flagged by Sourcery. Making security review mandatory from the start prevents these issues.

**Key insight:** Security review should be a non-negotiable quality gate, not optional.

### Actionable Items

- [ ] **Add Sourcery integration to project setup checklist**

  - **Location:** `templates/setup/ci-cd-checklist.md`
  - **Action:** Add step: "Set up Sourcery AI code review"
  - **Content:**
    ```markdown
    ## Code Review Setup
    
    - [ ] Install Sourcery CLI: `pip install sourcery-cli`
    - [ ] Configure Sourcery API key in environment
    - [ ] Add `dt-review` command to dev-toolkit (or document manual process)
    - [ ] Test Sourcery review on first PR
    ```
  - **Prevents:** Security issues reaching production
  - **Expected Impact:** Catch 100% of critical security issues before merge
  - **Priority:** CRITICAL
  - **Effort:** LOW

- [ ] **Create enum handling decision template**

  - **Location:** `templates/research/data-model-patterns.md`
  - **Action:** Add section: "Enum Handling Strategy"
  - **Content:**
    ```markdown
    ## Enum Handling Strategy
    
    For categorical fields (status, classification, type), decide:
    
    **Option 1: SQLAlchemy Enum**
    - DB-level validation
    - Type safety at ORM level
    - Migration creates enum type
    - Recommended for: Status, classification, fixed categories
    
    **Option 2: Custom Validation**
    - API-level only
    - More flexible
    - No DB constraint
    - Recommended for: User-defined categories
    
    **Decision Criteria:**
    - Fixed set of values → SQLAlchemy Enum
    - User-defined → Custom validation
    - Need DB constraint → SQLAlchemy Enum
    ```
  - **Prevents:** Mid-implementation decisions
  - **Expected Impact:** Faster model implementation, consistent patterns
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## Section 2: Testing Infrastructure

### Narrative: Manual Testing That Scales

Manual testing documentation started at top-level but quickly became unwieldy. Moving to feature-specific locations and adding clear state management notes solved scaling issues and prevented false bug reports.

**Key insight:** Manual testing guides should be feature-specific and include state management.

### Actionable Items

- [ ] **Add manual testing guide template**

  - **Location:** `templates/testing/manual-testing-guide.md`
  - **Action:** Create comprehensive manual testing template
  - **Content:**
    ```markdown
    # [Feature Name] - Manual Testing Guide
    
    **Feature:** [Feature description]
    **Last Updated:** [Date]
    
    ## Important Notes
    
    ⚠️ **Run scenarios in order** - Some scenarios depend on previous ones
    ⚠️ **Database state matters** - Reset database between test sessions
    ⚠️ **Prerequisites** - Check prerequisites before each scenario
    
    ## Prerequisites
    
    - [ ] Backend server running (`python run.py`)
    - [ ] Database migrated to latest version
    - [ ] Clean database state (or note current state)
    
    ## Test Scenarios
    
    ### Scenario 1: [Test Name]
    
    **Test:** [What you're testing]
    **Prerequisites:** [Any required setup]
    
    **Steps:**
    ```bash
    # curl command or CLI command
    ```
    
    **Expected Result:**
    - Status code: [code]
    - Response: [what to expect]
    
    **Verification:**
    ```bash
    # How to verify the result
    ```
    
    ## Acceptance Criteria
    
    - [ ] All scenarios pass
    - [ ] Edge cases tested
    - [ ] Error cases verified
    ```
  - **Prevents:** False bug reports, unclear test procedures
  - **Expected Impact:** User verification catches integration issues
  - **Priority:** HIGH
  - **Effort:** MEDIUM

- [ ] **Document monkeypatch auto-cleanup pattern**

  - **Location:** `templates/testing/pytest-patterns.md`
  - **Action:** Add section: "Fixture Cleanup"
  - **Content:**
    ```markdown
    ## Fixture Cleanup
    
    pytest automatically restores monkeypatched attributes after each test.
    Manual cleanup is unnecessary.
    
    ✅ **Good:**
    ```python
    def test_something(client, monkeypatch):
        monkeypatch.setattr(db.session, 'commit', mock_commit)
        # Test code
        # No manual restore needed
    ```
    
    ❌ **Unnecessary:**
    ```python
    def test_something(client, monkeypatch):
        original = db.session.commit
        monkeypatch.setattr(db.session, 'commit', mock_commit)
        # Test code
        monkeypatch.setattr(db.session, 'commit', original)  # Not needed!
    ```
    ```
  - **Prevents:** Unnecessary manual cleanup code
  - **Expected Impact:** Cleaner, more maintainable tests
  - **Priority:** LOW
  - **Effort:** LOW

---

## Section 3: Development Workflow

### Narrative: Quality Gates That Prevent Security Issues

PR #8 merged with a CRITICAL security issue because Sourcery review wasn't part of the merge checklist. Adding it as a mandatory checkpoint ensures all code PRs get security review before merge.

**Key insight:** Quality gates must be explicit checkpoints, not optional steps.

### Actionable Items

- [ ] **Add Sourcery review checkpoint to PR template**

  - **Location:** `templates/github/pull_request_template.md`
  - **Action:** Add mandatory checklist section
  - **Content:**
    ```markdown
    ## Pre-Merge Checklist
    
    - [ ] All automated tests passing
    - [ ] Code coverage maintained
    - [ ] **Sourcery review completed** (run `dt-review` from dev-toolkit)
    - [ ] Priority matrix filled out in `docs/maintainers/feedback/sourcery/pr##.md`
    - [ ] CRITICAL/HIGH issues addressed (if any)
    - [ ] Fix plans created for outstanding CRITICAL/HIGH issues
    - [ ] Manual testing completed (if applicable)
    ```
  - **Prevents:** Merging PRs without security review
  - **Expected Impact:** 100% PR coverage with Sourcery review
  - **Priority:** CRITICAL
  - **Effort:** LOW

- [ ] **Create fast-track process for CRITICAL fixes**

  - **Location:** `templates/workflow/git-flow-guide.md`
  - **Action:** Add section: "Fast-Track Process for CRITICAL Fixes"
  - **Content:**
    ```markdown
    ## Fast-Track Process for CRITICAL Fixes
    
    When a CRITICAL security or stability issue is found:
    
    1. **Create fix branch immediately**
       ```bash
       git checkout develop
       git pull
       git checkout -b fix/pr##-critical-[issue-name]
       ```
    
    2. **Implement fix with comprehensive tests**
       - Fix the issue
       - Add tests that verify the fix
       - Ensure all tests pass
    
    3. **Create PR marked CRITICAL priority**
       - Title: `fix: critical [issue description]`
       - Mark as CRITICAL in PR description
       - Reference fix plan document
    
    4. **Fast-track review and merge**
       - Same-day merge expected for security issues
       - Can skip normal review cycle if urgent
       - Still requires tests and fix plan
    
    **Naming Convention:**
    - `fix/pr##-critical-[issue-name]`
    - Example: `fix/pr08-critical-exception-leak`
    ```
  - **Prevents:** Delays on security fixes
  - **Expected Impact:** Reduce security vulnerability window to < 1 hour
  - **Priority:** HIGH
  - **Effort:** LOW

- [ ] **Document deferred issues backlog pattern**

  - **Location:** `templates/workflow/fix-tracking-system.md`
  - **Action:** Add section: "Deferred Issues Backlog"
  - **Content:**
    ```markdown
    ## Deferred Issues Backlog
    
    Organize non-blocking issues for future work:
    
    ### Structure
    
    ```markdown
    ## 📦 Deferred Issues Backlog
    
    **Total:** [N] deferred issues (can be addressed in future PRs)
    
    #### Test Improvements ([N] issues, [X] hours)
    - Issue description
    - Priority, effort, impact
    
    #### Code Quality & Refactoring ([N] issues, [X] hours)
    - Issue description
    
    #### Style Improvements ([N] items, [X] hours)
    - Issue description
    
    **Total estimated effort:** [X-Y] hours
    ```
    
    ### Categories
    
    - **Test Improvements:** Missing tests, test quality improvements
    - **Code Quality:** Refactoring, duplication reduction
    - **Style Improvements:** Code style, formatting, minor refactors
    
    ### Benefits
    
    - Prevents decision paralysis
    - Clear roadmap for future work
    - Realistic effort planning
    - Can address opportunistically or in dedicated PRs
    ```
  - **Prevents:** Decision paralysis on non-blocking issues
  - **Expected Impact:** Clear future roadmap, realistic planning
  - **Priority:** MEDIUM
  - **Effort:** MEDIUM

- [ ] **Clarify all PRs need approval rule**

  - **Location:** `templates/workflow/git-flow-guide.md`
  - **Action:** Emphasize in "Pull Request Review Workflow" section
  - **Content:**
    ```markdown
    ## Pull Request Review Workflow
    
    ⚠️ **CRITICAL:** Do NOT merge pull requests automatically.
    
    **ALL PRs require explicit user approval:**
    - Code PRs: External review required
    - Docs-only PRs: User approval required
    - Fix PRs: User approval required
    - **NO EXCEPTIONS**
    
    Even docs-only PRs benefit from review and should wait for approval.
    ```
  - **Prevents:** Accidental merges
  - **Expected Impact:** Better PR discipline, no auto-merge mistakes
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## Section 4: CLI/Tooling

### Narrative: Robust CLI Imports

CLI import errors occurred when using relative imports. Switching to package-qualified imports made the CLI robust in any execution context.

**Key insight:** CLI tools need package-qualified imports for reliability.

### Actionable Items

- [ ] **Add package-qualified imports pattern**

  - **Location:** `templates/cli/cli-structure.md`
  - **Action:** Add section: "Import Pattern"
  - **Content:**
    ```markdown
    ## Import Pattern
    
    Always use package-qualified imports in CLI tools:
    
    ✅ **Good:**
    ```python
    from project_cli.config import Config
    from project_cli.api_client import APIClient
    from project_cli.commands.list_cmd import list_projects
    ```
    
    ❌ **Avoid:**
    ```python
    from .config import Config
    from .api_client import APIClient
    from .commands.list_cmd import list_projects
    ```
    
    **Why:**
    - Works in any execution context
    - No ImportError when script run directly
    - Consistent across all modules
    - Easier debugging
    
    **Pattern:**
    - Use `from package.module import` not relative imports
    - Apply consistently across all CLI modules
    ```
  - **Prevents:** ImportError in different execution contexts
  - **Expected Impact:** Robust CLI tools that work anywhere
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## Section 5: Documentation

### Narrative: Feature-Specific Documentation That Scales

Top-level manual testing file became unwieldy with multiple features. Moving to feature-specific locations scales better and keeps documentation organized.

**Key insight:** Feature-specific documentation scales better than top-level files.

### Actionable Items

- [ ] **Create feature-specific manual testing location**

  - **Location:** `templates/docs/feature-directory-structure.md`
  - **Action:** Add `manual-testing.md` to feature directory structure
  - **Content:**
    ```markdown
    ## Feature Directory Structure
    
    ```
    docs/maintainers/planning/features/[feature-name]/
    ├── README.md              # Feature hub
    ├── feature-plan.md        # High-level plan
    ├── phase-N.md             # Phase details
    ├── manual-testing.md      # Feature-specific manual testing guide
    ├── deliverables/          # Planning outputs
    └── fix/                    # Fix tracking
    ```
    
    **Why feature-specific:**
    - Scales better than top-level file
    - Keeps testing docs with feature docs
    - Prevents unwieldy single file
    - Clear organization
    ```
  - **Prevents:** Top-level manual testing file becoming unwieldy
  - **Expected Impact:** Scalable testing documentation pattern
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## Summary

### Total Improvements: 10

**By Priority:**
- 🔴 CRITICAL: 2 (Sourcery integration, PR template checkpoint)
- 🟠 HIGH: 1 (Manual testing guide template)
- 🟡 MEDIUM: 6 (Enum decision, deferred backlog, CLI imports, feature docs, etc.)
- 🟢 LOW: 1 (Monkeypatch cleanup docs)

**By Category:**
- Pre-Project Setup: 2
- Testing Infrastructure: 2
- Development Workflow: 4
- CLI/Tooling: 1
- Documentation: 1

**Total Estimated Effort:** 4-6 hours

**Expected Impact:**
- 100% security review coverage
- Zero security vulnerabilities reaching production
- Scalable documentation patterns
- Clear process for urgent fixes
- Robust CLI tools

---

**Last Updated:** 2025-12-04  
**Status:** 🟡 Pending Application  
**Next:** Apply to dev-infra template when updating for Phase 2 patterns

