# Dev-Infra Template Improvements

**Source:** work-prod Phase 1 learnings  
**Target:** ~/Projects/dev-infra project template  
**Status:** 🟡 Pending Application  
**Last Updated:** 2025-12-03

---

## 📋 Introduction

This document captures actionable improvements for the dev-infra project template, informed by real implementation experience in work-prod. These improvements were discovered during Phase 0 (Development Environment) and Phase 1 (Projects API + CLI) implementation.

**Why these improvements matter:**

- **Reduce setup friction** - Automate manual steps that trip up new projects
- **Encode best practices** - Bake in patterns that worked well
- **Prevent common mistakes** - Address issues we encountered
- **Accelerate delivery** - Start new projects with proven patterns

**How they were discovered:**

- Pain points during setup (missing directories, unclear patterns)
- External code review feedback (Sourcery AI)
- Process gaps (PR discipline, fix tracking)
- Successful patterns (TDD, documentation structure)

**What problem they solve:**

- New projects don't repeat our mistakes
- Proven patterns propagate automatically
- Setup is faster and more reliable
- Quality gates are built-in from day 1

---

## Section 1: Pre-Project Setup

### Narrative: Why Upfront Decisions Save Time Later

The biggest delays in Phase 0 came from decisions that should have been made during Week 1 research. Testing strategy (pytest vs unittest) was chosen during implementation rather than as part of tech stack research. This could have led to suboptimal choices or late refactoring.

**Key insight:** Architectural decisions should be researched and documented (ADRs) before any implementation begins.

### Actionable Items

- [ ] **Add testing strategy to Week 1 research template**

  - **Location:** `templates/research/week-1-checklist.md`
  - **Add section:** "Testing Infrastructure"
  - **Include:** Framework comparison (pytest vs unittest), coverage tools, fixture patterns
  - **Deliverable:** Research document + ADR for testing approach

- [ ] **Include tech stack research checklist with testing**

  - **Location:** `templates/research/tech-stack-template.md`
  - **Add items:**
    - Testing framework selection
    - Code coverage tool
    - Mocking/stubbing approach
    - Integration testing strategy
  - **Reference:** `docs/maintainers/research/tech-stack/testing-strategy.md` format

- [ ] **Create decision record template for test frameworks**
  - **Location:** `templates/decisions/adr-testing-framework.md`
  - **Include sections:**
    - Context (why testing matters)
    - Evaluated options (pytest, unittest, nose)
    - Decision criteria (fixture support, plugins, readability)
    - Consequences (learning curve, tooling)

**Expected Impact:** Testing approach decided upfront, no mid-project pivot needed.

---

## Section 2: Project Structure

### Narrative: Directory Structure That Scales From Day 1

Manual directory creation (`backend/instance/`) caused a cryptic SQLite error during first database operation. Pre-creating key directories with explanatory comments would prevent this friction.

**Key insight:** Template should include all necessary directories with .gitkeep files and comments explaining their purpose.

### Actionable Items

- [ ] **Pre-create backend/instance/ directory**

  - **Location:** Template project structure
  - **Action:** Create `backend/instance/` in template
  - **Prevents:** SQLite "unable to open database file" error

- [ ] **Add .gitkeep to instance/ with comment explaining SQLite storage**

  - **Location:** `backend/instance/.gitkeep`
  - **Content:**
    ```
    # SQLite Database Storage
    #
    # This directory stores SQLite database files in development and production.
    # Database files are ignored by git (see .gitignore) to prevent committing data.
    #
    # Files in this directory:
    # - work_prod_dev.db (development database)
    # - work_prod_test.db (test database, if not using :memory:)
    # - work_prod.db (production database)
    ```

- [ ] **Include scripts/[project]\_cli/ structure template**

  - **Location:** `templates/scripts/project_cli/`
  - **Structure:**
    ```
    scripts/
      project_cli/
        README.md          # CLI usage documentation
        proj               # Executable (template with shebang)
        commands/          # Command modules
          __init__.py
        config.py          # API base URL configuration
        api_client.py      # HTTP client template
    ```
  - **Include:** Example command file with Click + Rich

- [ ] **Document where different tool types belong**
  - **Location:** `templates/docs/project-structure.md`
  - **Add section:** "Scripts Organization"
  - **Explain:**
    - `scripts/[project]_cli/` - User-facing CLI tools
    - `scripts/dev/` - Development automation
    - `scripts/ci/` - CI/CD automation
    - `scripts/data/` - Data processing/migration

**Expected Impact:** Zero manual directory creation, clear conventions for scripts organization.

---

## Section 3: Flask Backend Patterns

### Narrative: Application Factory Pattern Benefits and Setup

Flask's application factory pattern enabled easy testing with different configurations and clean separation of concerns. However, the pattern isn't obvious from Flask documentation, and model imports for Flask-Migrate require a non-intuitive pattern.

**Key insight:** Template should include complete, working application factory with all necessary patterns (config, extensions, model imports, blueprints).

### Actionable Items

- [ ] **Add Flask application factory template**

  - **Location:** `templates/backend/app/__init__.py`
  - **Include:**
    - Extension initialization (db, migrate, CORS)
    - Configuration loading from config object
    - Model import in app context (for Flask-Migrate)
    - Blueprint registration pattern
  - **Key code:**
    ```python
    def create_app(config_name='default'):
        app = Flask(__name__)
        app.config.from_object(config[config_name])
        config[config_name].init_app(app)

        # Initialize extensions
        db.init_app(app)
        migrate.init_app(app, db)
        CORS(app, origins=app.config.get('CORS_ORIGINS', []))

        # CRITICAL: Import models for Flask-Migrate detection
        with app.app_context():
            from app import models

        # Register blueprints
        from app.api.health import health_bp
        app.register_blueprint(health_bp, url_prefix='/api')

        return app
    ```

- [ ] **Include config.py with environment classes**

  - **Location:** `templates/backend/config.py`
  - **Include:**
    - Base `Config` class
    - `DevelopmentConfig` (with debug, local DB)
    - `TestingConfig` (with in-memory DB)
    - `ProductionConfig` (with environment variables)
    - `init_app()` method for prod logging setup
  - **Reference:** work-prod `config.py` as template

- [ ] **Document **init**.py patterns for packages**

  - **Location:** `templates/docs/flask-patterns.md`
  - **Add section:** "Python Package Initialization"
  - **Explain:**
    - `__init__.py` makes directories importable
    - Application factory pattern in `app/__init__.py`
    - Model re-exporting in `app/models/__init__.py`
    - Benefits: cleaner imports, encapsulation

- [ ] **Add model import pattern to template**

  - **Location:** `templates/backend/app/models/__init__.py`
  - **Pattern:**
    ```python
    # Import all models here for Flask-Migrate detection
    from .project import Project
    # Add future models:
    # from .user import User
    # from .task import Task
    ```
  - **Comment explaining:** Flask-Migrate scans this file

- [ ] **Include CORS configuration examples**
  - **Location:** `templates/backend/config.py`
  - **Add to each config class:**

    ```python
    class DevelopmentConfig(Config):
        CORS_ORIGINS = [
            'http://localhost:5173',  # Vite dev server
            'http://localhost:3000',  # Alternative port
        ]

    class ProductionConfig(Config):
        # Production reads from environment variable
        CORS_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
    ```

  - **Document:** Security rationale in comments

**Expected Impact:** Working Flask app structure out of the box, no "discovery through error" needed.

---

## Section 4: Documentation Templates

### Narrative: Hub-and-Spoke Pattern Effectiveness

The hub-and-spoke documentation pattern (README hubs linking to spoke documents) made navigation effortless. Progressive disclosure kept overviews clean while detailed documents were one click away. This pattern should be standard in every feature.

**Key insight:** Consistent documentation structure across all features reduces cognitive load and makes information easy to find.

### Actionable Items

- [ ] **Add feature plan template (with phase documents)**

  - **Location:** `templates/docs/features/feature-template/`
  - **Include:**
    - `README.md` (hub with Quick Links)
    - `feature-plan.md` (high-level overview)
    - `status-and-next-steps.md` (tracking)
    - `phase-0.md` (foundation template)
    - `phase-1.md` (first feature template)
  - **Reference:** work-prod Projects feature structure

- [ ] **Include status-and-next-steps.md template**

  - **Location:** `templates/docs/features/status-and-next-steps.md`
  - **Sections:**
    - Current Phase
    - Last Updated
    - Completed Milestones
    - In Progress
    - Next Steps
    - Phase Completion Table

- [ ] **Add fix plan template with pr##-issue-## naming**

  - **Location:** `templates/docs/features/fix/issue-template.md`
  - **Filename format:** `pr##-issue-##-[short-name].md`
  - **Sections:**
    - Sourcery Issue (PR, comment number)
    - Problem Description
    - Priority Assessment (Priority, Impact, Effort)
    - Solution Approach
    - Implementation Steps
    - Testing Requirements
    - Related ADRs

- [ ] **Create fix/README.md template with priority matrix**

  - **Location:** `templates/docs/features/fix/README.md`
  - **Include:**
    - Fix tracking workflow
    - Priority matrix explanation
    - Current fixes table
    - Branch strategy
    - Reference to Sourcery reviews

- [ ] **Include opportunities/internal and external structure**
  - **Location:** `templates/docs/planning/notes/opportunities/`
  - **Structure:**
    ```
    opportunities/
      README.md           # Parent hub
      internal/
        README.md         # Export hub
      external/
        README.md         # Import hub
    ```
  - **Purpose:** Knowledge transfer between projects

**Expected Impact:** Consistent documentation structure, easy navigation, systematic fix tracking.

---

## Section 5: Git Flow & PR Workflow

### Narrative: Discipline Prevents Mistakes

Prematurely merging PRs #1 and #2 without review caused us to fix the same issues retroactively. Adding PR review discipline to Cursor rules prevented future mistakes. This workflow should be default in every project.

**Key insight:** Automated reminders and checklists in tools (Cursor rules, PR templates) enforce discipline better than relying on memory.

### Actionable Items

- [ ] **Add default .cursor/rules/main.mdc with PR review workflow**

  - **Location:** `templates/.cursor/rules/main.mdc`
  - **Include section:** "Pull Request Review Workflow"
  - **Content:**
    - NEVER merge without review
    - External review workflow (dt-review)
    - Priority matrix assessment
    - Fix plan creation
    - User approval requirement
  - **Reference:** work-prod Cursor rules PR section

- [ ] **Include branch protection rule documentation**

  - **Location:** `templates/docs/git-workflow.md`
  - **Add section:** "Branch Protection"
  - **Explain:**
    - `main` and `develop` are protected
    - `feat/*` and `fix/*` require PRs
    - `docs/*` can push directly (with discipline)
    - How to configure GitHub branch protection

- [ ] **Add PR template with review checklist**

  - **Location:** `templates/.github/pull_request_template.md`
  - **Include:**
    - Description section
    - Review checklist (external review, priority matrix, tests)
    - Link to Sourcery review file
    - Related issues
    - Breaking changes warning

- [ ] **Document Sourcery integration workflow**

  - **Location:** `templates/docs/code-review-workflow.md`
  - **Sections:**
    - Setting up Sourcery
    - Running dt-review
    - Filling priority matrix
    - Creating fix plans
    - Batch-by-priority strategy

- [ ] **Include fix plan workflow in Cursor rules**
  - **Location:** `templates/.cursor/rules/main.mdc`
  - **Add reminder:** After Sourcery review, create fix plans before merging
  - **Template fix plan command:** (optional automation)

**Expected Impact:** No premature merges, systematic issue tracking, consistent code review process.

---

## Section 6: Testing Infrastructure

### Narrative: TDD From Day 1 With Proper Setup

Test-driven development (TDD) with pytest's vertical slice approach gave us confidence to refactor and prevented integration surprises. But pytest configuration and fixtures took time to set up correctly. Template should include working test infrastructure from the start.

**Key insight:** Testing infrastructure (fixtures, coverage, markers) set up before Phase 0 enables TDD from first line of code.

### Actionable Items

- [ ] **Add pytest.ini template with coverage settings**

  - **Location:** `templates/backend/pytest.ini`
  - **Include:**
    ```ini
    [pytest]
    testpaths = tests
    python_files = test_*.py
    python_classes = Test*
    python_functions = test_*
    addopts =
        --cov=app
        --cov-report=term-missing
        --cov-report=html
        --verbose
    markers =
        unit: Unit tests
        integration: Integration tests
    ```

- [ ] **Include conftest.py with common fixtures**

  - **Location:** `templates/backend/tests/conftest.py`
  - **Include fixtures:**
    - `app` - Flask application instance
    - `client` - Test client
    - `db_session` - Database session with rollback
    - `runner` - CLI test runner
  - **Reference:** work-prod conftest.py

- [ ] **Add test directory structure (unit/integration/e2e)**

  - **Location:** Template project structure
  - **Create:**
    ```
    backend/tests/
      conftest.py
      unit/
        models/
          __init__.py
        utils/
          __init__.py
      integration/
        api/
          __init__.py
    tests/ (top-level for E2E)
      e2e/
        __init__.py
    ```
  - **Include:** Example test in each directory

- [ ] **Document vertical slice TDD approach**

  - **Location:** `templates/docs/testing-guide.md`
  - **Sections:**
    - TDD cycle (RED-GREEN-REFACTOR)
    - Vertical slice pattern (Model → API → UI)
    - When to write unit vs integration tests
    - Coverage discipline (aim for >95%)
    - Test naming conventions

- [ ] **Include test naming conventions**
  - **Location:** `templates/docs/testing-guide.md`
  - **Conventions:**
    - `test_[function_name]_[condition]_[expected_result]`
    - Example: `test_create_project_with_valid_data_returns_201`
    - Be descriptive, not terse

**Expected Impact:** TDD possible from day 1, consistent test structure, high coverage expected.

---

## Section 7: CLI Tool Pattern

### Narrative: CLI-First for Backend-Only MVP

The CLI tool (using Click + Rich) provided immediate user value without frontend complexity. It became a powerful development tool and interim MVP solution. This pattern should be easy to adopt in future projects.

**Key insight:** CLI-first approach reduces cognitive load, accelerates backend development, and delivers user value faster than full-stack approach.

### Actionable Items

- [ ] **Add Click-based CLI template**

  - **Location:** `templates/scripts/project_cli/proj`
  - **Include:**
    - Shebang pointing to venv Python
    - Click group setup
    - Command registration pattern
    - Help text examples
  - **Template:**

    ```python
    #!/path/to/venv/bin/python
    import click
    from scripts.project_cli.commands.list_cmd import list_items
    from scripts.project_cli.commands.get_cmd import get_item

    @click.group()
    def cli():
        """CLI tool for [project name]."""
        pass

    cli.add_command(list_items)
    cli.add_command(get_item)

    if __name__ == '__main__':
        cli()
    ```

- [ ] **Include Rich formatting examples**

  - **Location:** `templates/scripts/project_cli/commands/list_cmd.py`
  - **Show:**
    - Table creation with columns
    - Color/style usage
    - Console printing
    - Error formatting
  - **Reference:** work-prod list_cmd.py

- [ ] **Document API client pattern**

  - **Location:** `templates/scripts/project_cli/api_client.py`
  - **Include:**
    - Base URL configuration
    - GET/POST/PUT/DELETE methods
    - Error handling (requests.exceptions)
    - JSON response parsing
  - **Template:** work-prod api_client.py

- [ ] **Add command structure template**

  - **Location:** `templates/scripts/project_cli/commands/`
  - **Include:**
    - `list_cmd.py` - List resources
    - `get_cmd.py` - Get single resource
    - `create_cmd.py` - Create resource
    - Each with Click decorators + Rich output

- [ ] **Include shebang pattern for direct execution**
  - **Location:** `templates/docs/cli-development.md`
  - **Explain:**
    - Shebang must point to venv Python
    - File must be executable (`chmod +x`)
    - Can run as `./scripts/project_cli/proj`
    - Add to PATH for `proj` command

**Expected Impact:** CLI tools easy to add, consistent formatting, backend-first MVP viable option.

---

## Section 8: Automation Scripts

### Narrative: Automate the Predictable

Manual steps (creating instance directory, initializing database, setting up virtual environment) are predictable and should be automated. Setup scripts reduce friction for new developers and eliminate forgotten steps.

**Key insight:** First-run automation (setup.sh) gets developers productive faster and ensures environment consistency.

### Actionable Items

- [ ] **Add setup.sh for initial project setup**

  - **Location:** `templates/scripts/setup.sh`
  - **Actions:**
    - Check Python version
    - Create virtual environment
    - Install dependencies
    - Create necessary directories
    - Initialize database
    - Create .env from template
  - **Make executable:** `chmod +x scripts/setup.sh`

- [ ] **Include instance directory creation in setup**

  - **Add to setup.sh:**
    ```bash
    # Create necessary directories
    mkdir -p backend/instance
    echo "# SQLite database storage directory" > backend/instance/.gitkeep
    ```

- [ ] **Add database initialization script**

  - **Location:** `templates/scripts/init_db.sh`
  - **Actions:**
    - Run migrations (`flask db upgrade`)
    - Optionally seed data
    - Verify database created
  - **Reference from setup.sh**

- [ ] **Include virtual environment setup automation**

  - **Add to setup.sh:**
    ```bash
    # Create and activate virtual environment
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r backend/requirements.txt
    ```

- [ ] **Document common automation patterns**
  - **Location:** `templates/docs/automation-guide.md`
  - **Include:**
    - Setup scripts (setup.sh)
    - Database scripts (init_db.sh, seed_db.sh)
    - Test runners (run_tests.sh)
    - Deployment scripts
    - When to automate vs. document

**Expected Impact:** One command (`./scripts/setup.sh`) gets project running, zero forgotten setup steps.

---

## Appendix: Priority Assessment

### Template Update Priority Matrix

| Improvement                         | Priority  | Effort    | Impact    | Apply When  |
| ----------------------------------- | --------- | --------- | --------- | ----------- |
| Testing strategy (Section 1)        | 🔴 HIGH   | 🟢 LOW    | 🔴 HIGH   | Immediately |
| Flask patterns (Section 3)          | 🔴 HIGH   | 🟡 MEDIUM | 🔴 HIGH   | Next update |
| Project structure (Section 2)       | 🟠 MEDIUM | 🟢 LOW    | 🟠 MEDIUM | Next update |
| Documentation templates (Section 4) | 🟠 MEDIUM | 🟡 MEDIUM | 🟠 MEDIUM | Next update |
| Cursor rules (Section 5)            | 🟠 MEDIUM | 🟢 LOW    | 🟠 MEDIUM | Next update |
| Testing infrastructure (Section 6)  | 🟠 MEDIUM | 🟡 MEDIUM | 🟠 MEDIUM | When needed |
| CLI template (Section 7)            | 🟡 LOW    | 🟡 MEDIUM | 🟡 MEDIUM | When needed |
| Automation scripts (Section 8)      | 🟢 NICE   | 🟠 HIGH   | 🟡 MEDIUM | Future      |

### Application Strategy

**Phase 1: High Priority (Apply Immediately)**

- Testing strategy in Week 1 research
- Flask application factory template
- CORS configuration examples
- PR review workflow in Cursor rules

**Phase 2: Medium Priority (Next Template Update)**

- Instance directory pre-creation
- Fix plan templates
- Hub-and-spoke documentation structure
- Branch protection documentation

**Phase 3: Low Priority (When Needed)**

- CLI tool templates
- Automation scripts
- Python package patterns guide

**Phase 4: Nice to Have (Future)**

- Advanced automation
- Additional CLI examples
- Performance optimization patterns

### Effort Estimation

| Section                           | Effort    | Time Estimate |
| --------------------------------- | --------- | ------------- |
| Section 1: Pre-Project Setup      | 🟢 LOW    | 2 hours       |
| Section 2: Project Structure      | 🟢 LOW    | 2 hours       |
| Section 3: Flask Backend          | 🟡 MEDIUM | 4 hours       |
| Section 4: Documentation          | 🟡 MEDIUM | 3 hours       |
| Section 5: Git Flow & PR          | 🟢 LOW    | 2 hours       |
| Section 6: Testing Infrastructure | 🟡 MEDIUM | 4 hours       |
| Section 7: CLI Tool Pattern       | 🟡 MEDIUM | 3 hours       |
| Section 8: Automation Scripts     | 🟠 HIGH   | 6 hours       |
| **Total**                         | -         | **26 hours**  |

**Recommended approach:** Apply in phases (Phase 1: 8 hours, Phase 2: 10 hours, Phase 3: 6 hours, Phase 4: 6 hours)

---

## 🔄 Next Steps

### Before Applying to dev-infra

- [ ] Review this checklist with dev-infra stakeholders
- [ ] Prioritize items based on upcoming projects
- [ ] Schedule template update session
- [ ] Test updated template with new project

### During Application

- [ ] Work through each section sequentially
- [ ] Test each change in isolation
- [ ] Update dev-infra documentation
- [ ] Version the template (tag release)

### After Application

- [ ] Create new test project from updated template
- [ ] Verify all improvements work as expected
- [ ] Document any issues discovered
- [ ] Share updated template with team

### Continuous Improvement

- [ ] Capture learnings from Phase 2+ in work-prod
- [ ] Update this checklist as new patterns emerge
- [ ] Review checklist completion quarterly
- [ ] Iterate on template based on feedback

---

**Last Updated:** 2025-12-03  
**Status:** 🟡 Pending Application  
**Next:** Schedule review session for template updates  
**Related:** [Phase 1 Learnings](phase-1-learnings.md)
