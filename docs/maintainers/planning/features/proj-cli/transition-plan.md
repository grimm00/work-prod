# Feature Transition Plan - proj-cli

**Feature:** Unified CLI Tool (`proj`)  
**Status:** 🔴 Not Started  
**Created:** 2025-12-16  
**Source:** [ADR-0007](../../../decisions/ADR-0007-inventory-system-cli-tool-architecture.md)  
**Type:** Feature

---

## Overview

Build a unified CLI tool named `proj` as a proper Python package in a separate repository (`proj-cli`). This CLI consolidates:

- **Project management:** Existing `proj` commands (list, get, create, update, delete, search, import)
- **Inventory management:** New `proj inv` subcommands (scan, analyze, dedupe, export)

After migration, work-prod becomes **API-only**.

---

## Transition Goals

From ADR-0007 success criteria:

- [ ] Single entry point CLI command (`proj`)
- [ ] All existing project commands migrated and working
- [ ] New inventory commands functional as subcommands
- [ ] Configuration support (YAML + Pydantic + XDG)
- [ ] Pip installable from local or GitHub
- [ ] work-prod becomes API-only

---

## Pre-Transition Checklist

- [ ] ADR-0007 reviewed and approved ✅
- [ ] Requirements document reviewed
- [ ] `dev-infra` project template available
- [ ] work-prod API running (for testing)
- [ ] GitHub token available (for inventory scanning)

---

## Transition Steps

### Phase 1: Repository Setup

**Goal:** Create `proj-cli` repository with package structure and basic Typer app.

**Estimated Effort:** ~2-3 hours

**Prerequisites:**

- [ ] `dev-infra/new-project.sh` script available
- [ ] GitHub repository creation access

**Tasks:**

1. **Create repository:**
   - Run `dev-infra/new-project.sh proj-cli`
   - Initialize Git repository
   - Create basic README

2. **Create package structure:**
   ```
   proj-cli/
   ├── pyproject.toml
   ├── requirements.txt
   ├── README.md
   ├── src/
   │   └── proj/
   │       ├── __init__.py
   │       ├── __main__.py
   │       ├── cli.py
   │       ├── config.py
   │       └── commands/
   │           └── __init__.py
   └── tests/
   ```

3. **Create pyproject.toml:**
   - Package metadata
   - `proj` entry point via `[project.scripts]`
   - Dependencies: typer[all], pyyaml, pydantic-settings, requests

4. **Create Pydantic config:**
   - XDG paths for config/data
   - Environment variable overrides (`PROJ_*`)
   - Default config creation

5. **Create basic Typer app:**
   - Main CLI with `--version` and `--help`
   - Placeholder command groups

**Deliverables:**

- `proj --version` works
- `proj --help` shows structure
- Config loads from XDG paths

**Definition of Done:**

- [ ] Repository created and pushed
- [ ] Package installable via `pip install -e .`
- [ ] `proj --help` shows app structure
- [ ] Config loading works

---

### Phase 2: Migrate Project Commands

**Goal:** Move existing `proj` commands from work-prod to new CLI with Typer.

**Estimated Effort:** ~3-4 hours

**Prerequisites:**

- [ ] Phase 1 complete
- [ ] work-prod API running

**Tasks:**

1. **Migrate API client:**
   - Copy `scripts/project_cli/api_client.py` → `src/proj/api_client.py`
   - Update imports
   - Add config integration for API URL

2. **Create projects command group:**
   - Create `src/proj/commands/projects.py`
   - Convert argparse to Typer for each command

3. **Migrate commands:**
   - `proj list` - List all projects
   - `proj get <id>` - Get project details
   - `proj create` - Create new project
   - `proj update <id>` - Update existing project
   - `proj delete <id>` - Delete project
   - `proj search <query>` - Search projects
   - `proj import <file>` - Import from JSON

4. **Test all commands:**
   - Verify feature parity with current CLI
   - Test against running work-prod API

**Deliverables:**

- All `proj` commands working
- API client migrated
- Feature parity verified

**Definition of Done:**

- [ ] All 7 project commands functional
- [ ] Output matches current CLI
- [ ] API client works with configurable URL

---

### Phase 3: Add Inventory Commands

**Goal:** Add `proj inv` subcommand group wrapping inventory scripts.

**Estimated Effort:** ~3-4 hours

**Prerequisites:**

- [ ] Phase 2 complete
- [ ] GitHub token available

**Tasks:**

1. **Create inventory command group:**
   - Create `src/proj/commands/inventory.py`
   - Register as `proj inv` subcommand group

2. **Create scanners module:**
   - Create `src/proj/scanners/` directory
   - GitHub scanner (wrap `fetch-github-repos.sh`)
   - Local scanner (wrap `scan-local-projects.sh`)

3. **Implement scan commands:**
   - `proj inv scan github` - Scan GitHub repos
   - `proj inv scan local` - Scan local directories

4. **Implement analysis commands:**
   - `proj inv analyze` - Analyze tech stack (wrap `analyze-tech-stack.py`)
   - `proj inv dedupe` - Deduplicate results (wrap `deduplicate-projects.py`)

5. **Implement export commands:**
   - `proj inv export json` - Export to JSON file
   - `proj inv export api` - Push to work-prod API (wrap `map_inventory_to_projects.py`)

6. **Add status command:**
   - `proj inv status` - Show inventory state (data files, last scan, etc.)

**Deliverables:**

- All `proj inv` commands working
- Inventory workflows functional
- Error handling in place

**Definition of Done:**

- [ ] `proj inv scan github/local` functional
- [ ] `proj inv analyze/dedupe` functional
- [ ] `proj inv export json/api` functional
- [ ] Basic error handling

---

### Phase 4: Polish & Cleanup

**Goal:** Testing, documentation, Rich UI, and work-prod cleanup.

**Estimated Effort:** ~2-3 hours

**Prerequisites:**

- [ ] Phase 3 complete

**Tasks:**

1. **Add tests:**
   - Unit tests for config
   - Integration tests for commands
   - Test fixtures

2. **Add Rich UI enhancements:**
   - Progress bars for long operations
   - Colored output
   - Table formatting

3. **First-run experience:**
   - Create default config if none exists
   - Show helpful message

4. **Documentation:**
   - Update README with usage
   - Add command examples

5. **Work-prod cleanup:**
   - Remove `scripts/project_cli/` directory
   - Update work-prod README to reference `proj-cli`
   - Update any documentation referencing `proj`

**Deliverables:**

- Tests passing
- Polish complete
- work-prod cleaned up

**Definition of Done:**

- [ ] Basic tests passing
- [ ] Rich UI enhancements in place
- [ ] work-prod `scripts/project_cli/` removed
- [ ] work-prod README updated
- [ ] proj-cli README complete

---

## Post-Transition

After all phases complete:

- [ ] `proj-cli` repository tagged with v0.1.0
- [ ] work-prod API-only (no CLI code)
- [ ] Documentation updated in both repos
- [ ] Announcement of new CLI location

---

## Definition of Done (Overall)

- [ ] All 4 phases complete
- [ ] All project commands migrated and working
- [ ] All inventory commands working
- [ ] Tests passing
- [ ] work-prod cleaned up
- [ ] Documentation complete

---

## Source Code Migration Map

| Source (work-prod) | Destination (proj-cli) |
|--------------------|------------------------|
| `scripts/project_cli/cli.py` | `src/proj/commands/projects.py` |
| `scripts/project_cli/api_client.py` | `src/proj/api_client.py` |
| `scripts/project_cli/commands/*.py` | `src/proj/commands/projects.py` |
| `scripts/inventory/fetch-github-repos.sh` | `src/proj/scanners/github.py` (subprocess) |
| `scripts/inventory/scan-local-projects.sh` | `src/proj/scanners/local.py` (subprocess) |
| `scripts/inventory/analyze-tech-stack.py` | `src/proj/commands/inventory.py` |
| `scripts/inventory/classify-projects.py` | `src/proj/commands/inventory.py` |
| `scripts/inventory/deduplicate-projects.py` | `src/proj/commands/inventory.py` |
| `scripts/map_inventory_to_projects.py` | `src/proj/commands/inventory.py` |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| API changes during migration | Low | Medium | Test against stable API |
| Shell script compatibility | Medium | Low | Keep scripts, wrap with subprocess |
| Config migration confusion | Low | Low | Document migration path |

---

## References

- [Feature Plan](feature-plan.md)
- [ADR-0007](../../../decisions/ADR-0007-inventory-system-cli-tool-architecture.md)
- [Requirements](../../../research/inventory-repository-separation/requirements.md)
- [Research Summary](../../../research/inventory-repository-separation/research-summary.md)

---

**Last Updated:** 2025-12-16

