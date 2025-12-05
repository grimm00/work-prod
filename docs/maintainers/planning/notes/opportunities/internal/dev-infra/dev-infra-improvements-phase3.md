# Dev-Infra Template Improvements - Phase 3

**Source:** work-prod Phase 3 learnings  
**Target:** ~/Projects/dev-infra project template  
**Status:** 🟡 Pending Application  
**Last Updated:** 2025-12-04

---

## 📋 Introduction

This document captures actionable improvements for the dev-infra project template, informed by real implementation experience in work-prod Phase 3. These improvements were discovered during Phase 3 (Delete & Archive Projects) implementation, workflow automation, and process refinement.

**Why these improvements matter:**

- **Automate repetitive tasks** - Reduce manual documentation work
- **Clarify workflows** - Distinguish between code PRs and docs updates
- **Improve CLI patterns** - Template confirmation and display patterns
- **Document archive strategies** - Help developers choose right approach

**How they were discovered:**

- Post-PR documentation workflow automation need
- Direct merge pattern for docs-only changes
- CLI confirmation pattern for destructive operations
- Archive implementation simplicity (status-based vs soft-delete)

**What problem they solve:**

- Manual documentation updates are error-prone
- Unclear when PRs are needed vs direct merge
- Inconsistent CLI patterns across commands
- Unclear archive/soft-delete decision criteria

---

## Section 1: Pre-Project Setup

### Narrative: Archive Strategy Decision Guide

Phase 3 revealed that archive patterns can be simpler than expected. Status-based archive (using existing fields) worked perfectly and required no migration. A decision guide would help developers choose the right pattern upfront.

**Key insight:** Not all archives need soft-delete. Status-based archive is simpler and sufficient for most cases.

### Actionable Items

- [ ] **Add archive strategy decision guide**

  - **Location:** `templates/research/data-model-patterns.md`
  - **Action:** Add section: "Archive and Soft-Delete Strategies"
  - **Content:**
    ```markdown
    ## Archive and Soft-Delete Strategies
    
    ### Option 1: Status-Based Archive (Recommended for Most Cases)
    
    **When to use:**
    - Simple archive needs (hide from active lists)
    - No audit trail requirements
    - Existing status/classification fields available
    
    **Implementation:**
    - Use existing status or classification field
    - Set status='archived' or classification='archive'
    - No schema changes needed
    - Archived items still queryable
    
    **Example:**
    ```python
    # Archive endpoint
    project.status = 'archived'
    project.classification = 'archive'
    db.session.commit()
    ```
    
    **Pros:**
    - No migration needed
    - Simple queries (no filtering)
    - Easy to unarchive
    
    **Cons:**
    - No deletion timestamp
    - No audit trail
    
    ### Option 2: Soft Delete (For Audit Requirements)
    
    **When to use:**
    - Need deletion timestamp
    - Audit trail required
    - Compliance requirements
    
    **Implementation:**
    - Add `deleted_at` timestamp field
    - Filter deleted items in queries
    - Migration required
    
    **Example:**
    ```python
    # Model
    deleted_at = db.Column(db.DateTime, nullable=True, index=True)
    
    # Query (exclude deleted)
    projects = Project.query.filter(Project.deleted_at.is_(None)).all()
    ```
    
    **Pros:**
    - Audit trail
    - Deletion timestamp
    - Compliance-friendly
    
    **Cons:**
    - Schema change required
    - More complex queries
    - Harder to unarchive
    ```
  - **Prevents:** Over-engineering archive solutions
  - **Expected Impact:** Choose right pattern from start, avoid unnecessary migrations
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## Section 2: Project Structure

### Narrative: Manual Testing Documentation Location

Phase 3 revealed that top-level manual testing docs don't scale. Feature-specific guides are better. Template should establish this pattern from the start.

**Key insight:** Manual testing docs should be feature-specific, not project-wide.

### Actionable Items

- [ ] **Add manual-testing.md to feature directory template**

  - **Location:** `templates/docs/maintainers/planning/features/[feature-name]/manual-testing.md`
  - **Action:** Create template file with structure
  - **Content:**
    ```markdown
    # [Feature Name] - Manual Testing Guide
    
    **Feature:** [Feature Name]  
    **Last Updated:** [Date]  
    **Status:** ✅ Active
    
    ---
    
    ## Overview
    
    This guide provides step-by-step manual testing scenarios for [Feature Name].
    
    **Prerequisites:**
    - Backend server running (`flask run`)
    - Database initialized (`flask db upgrade`)
    - CLI tool installed (`pip install -e scripts/`)
    
    **Important:** Run scenarios in order. Some scenarios depend on previous ones.
    
    ---
    
    ## Scenario N: [Scenario Name]
    
    **Purpose:** [What this tests]
    
    **Steps:**
    1. [Step 1]
    2. [Step 2]
    
    **Expected Result:**
    - [Expected outcome 1]
    - [Expected outcome 2]
    
    **Verification:**
    ```bash
    # Verification commands
    ```
    
    ---
    
    ## Notes
    
    - Database state: [Clean/Seeded/Stateful]
    - Dependencies: [Any prerequisites]
    ```
  - **Prevents:** Documentation fragmentation, scaling issues
  - **Expected Impact:** Consistent manual testing documentation location
  - **Priority:** MEDIUM
  - **Effort:** LOW

- [ ] **Update feature directory README template**

  - **Location:** `templates/docs/maintainers/planning/features/[feature-name]/README.md`
  - **Action:** Add manual testing link to Quick Links
  - **Content:**
    ```markdown
    ## 📋 Quick Links
    
    ### Planning
    - [Feature Plan](feature-plan.md)
    - [Status & Next Steps](status-and-next-steps.md)
    
    ### Implementation
    - [Phase N](phase-N.md)
    
    ### Testing
    - [Manual Testing Guide](manual-testing.md)  # <-- Add this
    
    ### Troubleshooting
    - [Fix Tracking](fix/README.md)
    ```
  - **Prevents:** Missing manual testing documentation
  - **Expected Impact:** Easy to find testing guides
  - **Priority:** LOW
  - **Effort:** LOW

---

## Section 3: Development Workflow

### Narrative: Git Flow Patterns for Documentation

Phase 3 established that docs-only changes can merge directly to develop without PRs. This speeds up workflow and follows Git Flow principles. Template should document this clearly.

**Key insight:** Different workflows for different change types improve efficiency.

### Actionable Items

- [ ] **Document Git Flow patterns for docs branches**

  - **Location:** `templates/docs/maintainers/planning/notes/git-flow-patterns.md`
  - **Action:** Add section: "Documentation Branch Workflow"
  - **Content:**
    ```markdown
    ## Documentation Branch Workflow
    
    ### When to Use Direct Merge
    
    **Docs-only branches** (`docs/*`) can merge directly to `develop`:
    - No code changes
    - Documentation updates only
    - Low risk
    - High frequency
    
    **Workflow:**
    ```bash
    # Create docs branch
    git checkout develop
    git pull
    git checkout -b docs/[description]
    
    # Make documentation changes
    # ... edit docs ...
    
    # Commit
    git add docs/
    git commit -m "docs(...): ..."
    
    # Merge directly (no PR)
    git checkout develop
    git merge docs/[description] --no-edit
    git push origin develop
    
    # Cleanup
    git branch -d docs/[description]
    ```
    
    ### When to Use PR
    
    **Code branches** (`feat/*`, `fix/*`) require PRs:
    - Code changes
    - Need review
    - Higher risk
    - Lower frequency
    
    **Workflow:**
    ```bash
    # Create feature branch
    git checkout develop
    git pull
    git checkout -b feat/[feature]
    
    # Make code changes
    # ... implement feature ...
    
    # Commit
    git add .
    git commit -m "feat(...): ..."
    
    # Push and create PR
    git push origin feat/[feature]
    gh pr create --base develop --head feat/[feature]
    
    # Wait for review and merge
    ```
    
    ### Decision Tree
    
    ```
    Changes include code?
    ├─ Yes → Create PR
    └─ No → Direct merge (if docs-only)
    ```
    ```
  - **Prevents:** Unnecessary PRs for docs updates
  - **Expected Impact:** Faster documentation workflow
  - **Priority:** MEDIUM
  - **Effort:** LOW

- [ ] **Add post-PR documentation command template**

  - **Location:** `templates/.cursor/commands/post-pr.md`
  - **Action:** Create command template
  - **Content:** (See work-prod `.cursor/commands/post-pr.md` as example)
  - **Prevents:** Manual documentation updates, missed updates
  - **Expected Impact:** Automated, consistent documentation updates
  - **Priority:** HIGH
  - **Effort:** MEDIUM

---

## Section 4: CLI/Tooling

### Narrative: CLI Patterns for Destructive Operations

Phase 3 established confirmation prompt pattern for DELETE operations. This should be templated for consistency across CLI commands.

**Key insight:** Destructive operations need safety checks. Template the pattern.

### Actionable Items

- [ ] **Add CLI confirmation prompt template**

  - **Location:** `templates/scripts/cli/patterns/confirmation-prompt.md`
  - **Action:** Create pattern documentation
  - **Content:**
    ```markdown
    # CLI Confirmation Prompt Pattern
    
    ## When to Use
    
    Use confirmation prompts for:
    - Destructive operations (delete, remove, destroy)
    - Irreversible actions
    - Operations that affect multiple resources
    - High-risk operations
    
    ## Pattern
    
    ```python
    import click
    from rich.console import Console
    from rich.prompt import Confirm
    from project_cli.api_client import APIClient
    
    @click.command()
    @click.argument('resource_id', type=int)
    @click.option('--yes', '-y', is_flag=True, help='Skip confirmation prompt')
    def delete_resource(resource_id, yes):
        """Delete a resource permanently."""
        console = Console()
        
        try:
            # Get resource details first
            client = APIClient()
            resource = client.get_resource(resource_id)
            
            # Confirm unless --yes flag is used
            if not yes:
                console.print(
                    f"[yellow]Warning: This will permanently delete "
                    f"{resource['name']} (ID: {resource_id})[/yellow]"
                )
                if not Confirm.ask("Are you sure you want to delete this resource?", default=False):
                    console.print("[yellow]Deletion cancelled.[/yellow]")
                    return
            
            # Perform deletion
            client.delete_resource(resource_id)
            console.print(f"[green]✓ Deleted {resource['name']}[/green]")
            
        except Exception as e:
            # Error handling
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    if 'error' in error_data:
                        error_msg = error_data['error']
                except:
                    pass
            console.print(f"[red]✗ Error: {error_msg}[/red]")
            raise click.Abort()
    ```
    
    ## Key Elements
    
    1. **Get resource details first** - Show user what they're deleting
    2. **Warning message** - Clear yellow warning with resource name
    3. **Default to "no"** - Safer default (default=False)
    4. **--yes flag** - Allow skipping for automation
    5. **Clear success message** - Green checkmark with resource name
    6. **Error handling** - Extract error message from API response
    
    ## Variations
    
    ### Multiple Resources
    ```python
    if not yes:
        console.print(f"[yellow]Warning: This will delete {len(resources)} resources[/yellow]")
        if not Confirm.ask(f"Delete {len(resources)} resources?", default=False):
            return
    ```
    
    ### With Preview
    ```python
    # Show what will be deleted
    table = Table(title="Resources to Delete")
    for resource in resources:
        table.add_row(str(resource['id']), resource['name'])
    console.print(table)
    
    if not Confirm.ask("Delete these resources?", default=False):
        return
    ```
    ```
  - **Prevents:** Accidental deletions, inconsistent UX
  - **Expected Impact:** Consistent safety checks across CLI commands
  - **Priority:** HIGH
  - **Effort:** LOW

- [ ] **Add Rich table display pattern**

  - **Location:** `templates/scripts/cli/patterns/rich-table-display.md`
  - **Action:** Create pattern documentation
  - **Content:**
    ```markdown
    # Rich Table Display Pattern
    
    ## When to Use
    
    Use Rich tables for:
    - Displaying state changes (archive, update)
    - Showing resource details
    - Multi-field displays
    - Professional presentation
    
    ## Pattern
    
    ```python
    from rich.console import Console
    from rich.table import Table
    
    @click.command()
    @click.argument('resource_id', type=int)
    def update_resource(resource_id):
        """Update a resource."""
        console = Console()
        
        client = APIClient()
        resource = client.update_resource(resource_id, data)
        
        # Success message
        console.print(f"[green]✓ Updated {resource['name']}[/green]")
        
        # Display updated state in table
        table = Table(title="Updated Resource", show_header=False)
        table.add_column("Field", style="cyan", justify="right")
        table.add_column("Value", style="green")
        
        # Add rows (only non-empty fields)
        table.add_row("ID", str(resource['id']))
        table.add_row("Name", resource['name'])
        if resource.get('status'):
            table.add_row("Status", resource['status'])
        if resource.get('description'):
            table.add_row("Description", resource['description'])
        
        console.print(table)
    ```
    
    ## Key Elements
    
    1. **Title** - Descriptive title for context
    2. **No header** - Cleaner for key-value displays
    3. **Styled columns** - Cyan for labels, green for values
    4. **Right-justified labels** - Professional alignment
    5. **Conditional rows** - Only show non-empty fields
    6. **Formatted values** - Format dates, numbers appropriately
    
    ## Variations
    
    ### With Header
    ```python
    table = Table(title="Resources", show_header=True)
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Status", style="yellow")
    
    for resource in resources:
        table.add_row(str(resource['id']), resource['name'], resource['status'])
    ```
    
    ### Compact Display
    ```python
    table = Table(show_header=False, box=None)  # No box for compact
    table.add_column("", style="cyan", width=15)
    table.add_column("", style="green")
    ```
    ```
  - **Prevents:** Inconsistent CLI displays
  - **Expected Impact:** Professional, consistent CLI UX
  - **Priority:** MEDIUM
  - **Effort:** LOW

- [ ] **Add CLI error handling pattern**

  - **Location:** `templates/scripts/cli/patterns/error-handling.md`
  - **Action:** Create pattern documentation
  - **Content:**
    ```markdown
    # CLI Error Handling Pattern
    
    ## Pattern
    
    ```python
    import click
    from rich.console import Console
    
    @click.command()
    def command():
        console = Console()
        
        try:
            # Command logic
            result = client.do_something()
            console.print(f"[green]✓ Success[/green]")
            
        except Exception as e:  # Explicit exception type
            # Extract error message
            error_msg = str(e)
            
            # Try to get API error message
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    if 'error' in error_data:
                        error_msg = error_data['error']
                except:
                    pass  # Fall back to str(e)
            
            # Display error
            console.print(f"[red]✗ Error: {error_msg}[/red]")
            raise click.Abort()
    ```
    
    ## Key Elements
    
    1. **Explicit exception type** - `except Exception as e:` not bare `except:`
    2. **Extract API error** - Try to get error message from API response
    3. **Fallback** - Use str(e) if API error extraction fails
    4. **User-friendly display** - Red error message with ✗ symbol
    5. **Abort on error** - `raise click.Abort()` to exit cleanly
    
    ## Common Error Types
    
    ### API Errors (requests library)
    ```python
    except requests.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                error_msg = error_data.get('error', str(e))
            except:
                error_msg = str(e)
    ```
    
    ### Validation Errors
    ```python
    except ValueError as e:
        console.print(f"[red]✗ Validation Error: {e}[/red]")
        raise click.Abort()
    ```
    
    ### Not Found Errors
    ```python
    except NotFoundError as e:
        console.print(f"[red]✗ Not Found: {e}[/red]")
        raise click.Abort()
    ```
    ```
  - **Prevents:** Bare except clauses, inconsistent error handling
  - **Expected Impact:** Consistent, user-friendly error messages
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## Section 5: Documentation

### Narrative: Post-PR Documentation Automation

Phase 3 created `/post-pr` command to automate documentation updates after PR merges. This prevents missed updates and ensures consistency.

**Key insight:** Automate repetitive documentation tasks to prevent errors.

### Actionable Items

- [ ] **Add post-PR command template**

  - **Location:** `templates/.cursor/commands/post-pr.md`
  - **Action:** Copy from work-prod as template
  - **Prevents:** Missed documentation updates
  - **Expected Impact:** Automated, consistent documentation
  - **Priority:** HIGH
  - **Effort:** MEDIUM (copy and adapt)

- [ ] **Document command creation pattern**

  - **Location:** `templates/.cursor/commands/README.md`
  - **Action:** Create guide for command creation
  - **Content:**
    ```markdown
    # Cursor Command Templates
    
    ## Purpose
    
    Cursor commands automate repetitive workflows and reduce cognitive load.
    
    ## When to Create Commands
    
    Create commands for:
    - Repetitive workflows (post-PR updates, phase completion)
    - Multi-step processes (testing, deployment)
    - Error-prone tasks (documentation updates)
    
    ## Command Structure
    
    ```markdown
    # Command Name
    
    Use this command to [purpose].
    
    ## Workflow Overview
    
    **When to use:** [scenarios]
    **Key principle:** [principle]
    
    ## Usage
    
    **Command:** `@command-name [args]`
    
    ## Step-by-Step Process
    
    ### 1. Step Name
    - [ ] Checklist item
    - [ ] Another item
    
    ## Success Criteria
    - [ ] Criterion 1
    - [ ] Criterion 2
    ```
    
    ## Examples
    
    - `/phase-task` - Task-by-task phase implementation
    - `/phase-pr` - Phase completion and PR workflow
    - `/post-pr` - Post-merge documentation updates
    - `/int-opp` - Document internal opportunities
    ```
  - **Prevents:** Inconsistent command structure
  - **Expected Impact:** Reusable command patterns
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## Summary

### Priority Breakdown

- **HIGH Priority (3 items):**
  - CLI confirmation prompt template
  - Post-PR command template
  - CLI error handling pattern

- **MEDIUM Priority (4 items):**
  - Archive strategy decision guide
  - Git Flow patterns documentation
  - Rich table display pattern
  - Command creation pattern

- **LOW Priority (2 items):**
  - Manual testing template
  - Feature README update

### Estimated Effort

- **Total:** 6-8 hours
- **High priority:** 3-4 hours
- **Medium priority:** 2-3 hours
- **Low priority:** 1 hour

### Expected Impact

- **Automation:** Post-PR command reduces manual work
- **Consistency:** CLI patterns ensure uniform UX
- **Clarity:** Archive guide helps choose right pattern
- **Efficiency:** Git Flow docs speed up workflow

---

**Last Updated:** 2025-12-04  
**Status:** 🟡 Pending Application  
**Next:** Apply improvements to dev-infra template

