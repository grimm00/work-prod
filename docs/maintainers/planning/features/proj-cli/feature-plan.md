# proj-cli - Feature Plan

**Status:** 🟠 In Progress  
**Created:** 2025-12-16  
**Priority:** High  
**ADR:** [ADR-0007](../../../decisions/ADR-0007-inventory-system-cli-tool-architecture.md)

---

## 📋 Overview

Build a unified CLI tool (`proj`) that consolidates project management commands and inventory scanning into a single, professional Python package. This CLI will:

- **Unify** existing `proj` commands from work-prod with new inventory functionality
- **Live** in its own repository (`proj-cli`) separate from work-prod
- **Make** work-prod API-only (cleaner separation)
- **Use** modern Python tooling (Typer, Pydantic, XDG compliance)

### Key Decisions (from ADR-0007)

| Decision Point | Choice | Rationale |
|----------------|--------|-----------|
| **Command Name** | `proj` | Preserves existing muscle memory |
| **Framework** | Typer | Modern, type hints, minimal boilerplate |
| **Configuration** | YAML + Pydantic + XDG | Standard locations, type-safe |
| **Repository** | Separate (`proj-cli`) | API-only work-prod, independent CLI |

---

## 🎯 Success Criteria

- [ ] `proj` command installable via `pip install .`
- [ ] All existing `proj` commands work identically (list, get, create, update, delete, search, import)
- [ ] New `proj inv` subcommands functional (scan, analyze, dedupe, export)
- [ ] Configuration via `~/.config/proj/config.yaml`
- [ ] XDG directory compliance
- [ ] work-prod `scripts/project_cli/` removed
- [ ] work-prod README references new CLI package
- [ ] Basic tests passing

---

## 📦 Functional Requirements

### Project Commands (Migrated from work-prod)

| Requirement | Command | Priority | Status |
|-------------|---------|----------|--------|
| List projects | `proj list` | 🔴 High | 🔴 Pending |
| Get project details | `proj get <id>` | 🔴 High | 🔴 Pending |
| Create project | `proj create` | 🔴 High | 🔴 Pending |
| Update project | `proj update <id>` | 🔴 High | 🔴 Pending |
| Delete project | `proj delete <id>` | 🔴 High | 🔴 Pending |
| Search projects | `proj search` | 🔴 High | 🔴 Pending |
| Import projects | `proj import` | 🔴 High | 🔴 Pending |

### Inventory Commands (New)

| Requirement | Command | Priority | Status |
|-------------|---------|----------|--------|
| Scan GitHub repos | `proj inv scan github` | 🔴 High | 🔴 Pending |
| Scan local dirs | `proj inv scan local` | 🔴 High | 🔴 Pending |
| Analyze tech stack | `proj inv analyze` | 🔴 High | 🔴 Pending |
| Deduplicate | `proj inv dedupe` | 🟡 Medium | 🔴 Pending |
| Export to JSON | `proj inv export json` | 🔴 High | 🔴 Pending |
| Export to API | `proj inv export api` | 🔴 High | 🔴 Pending |
| Show status | `proj inv status` | 🟡 Medium | 🔴 Pending |

### Configuration

| Requirement | Description | Priority | Status |
|-------------|-------------|----------|--------|
| Config file | `~/.config/proj/config.yaml` | 🔴 High | 🔴 Pending |
| Data directory | `~/.local/share/proj/` | 🔴 High | 🔴 Pending |
| Env override | `PROJ_*` variables | 🔴 High | 🔴 Pending |
| First-run setup | Create default config | 🟡 Medium | 🔴 Pending |

---

## 🏗️ Non-Functional Requirements

| Requirement | Description | Priority | Status |
|-------------|-------------|----------|--------|
| **NFR-1** | Typer CLI framework | 🔴 High | 🔴 Pending |
| **NFR-2** | Rich terminal output | 🟡 Medium | 🔴 Pending |
| **NFR-3** | Pydantic config validation | 🔴 High | 🔴 Pending |
| **NFR-4** | XDG directory compliance | 🔴 High | 🔴 Pending |
| **NFR-5** | Pip installable | 🔴 High | 🔴 Pending |
| **NFR-6** | Error handling | 🔴 High | 🔴 Pending |
| **NFR-7** | Python 3.10+ | 🔴 High | 🔴 Pending |

---

## 📅 Implementation Phases

### Phase 1: Repository Setup (~2-3 hours)

**Goal:** Create `proj-cli` repository with package structure

- Create repository via `dev-infra/new-project.sh`
- Create `src/proj/` package structure
- Add `pyproject.toml` with `proj` entry point
- Create Pydantic config with XDG paths
- Add requirements.txt

**Deliverables:**
- Working `proj --help` command
- Basic config loading
- Repository structure ready

---

### Phase 2: Migrate Project Commands (~3-4 hours)

**Goal:** Move existing `proj` commands to new CLI

- Migrate `scripts/project_cli/` code
- Convert argparse to Typer
- Migrate API client
- Test all existing commands

**Deliverables:**
- All `proj` commands working
- Feature parity with current CLI
- API client migrated

---

### Phase 3: Add Inventory Commands (~3-4 hours)

**Goal:** Add `proj inv` subcommand group

- Create inventory command group
- Wrap existing scripts as subcommands
- Add error handling
- Test inventory workflows

**Deliverables:**
- `proj inv scan github/local` working
- `proj inv analyze/dedupe` working
- `proj inv export json/api` working

---

### Phase 4: Polish & Cleanup (~2-3 hours)

**Goal:** Testing, documentation, work-prod cleanup

- Add tests
- First-run config creation
- Progress bars and colors
- Remove `scripts/project_cli/` from work-prod
- Update work-prod README

**Deliverables:**
- Tests passing
- Polish complete
- work-prod cleaned up

---

## 🚀 Next Steps

1. Review transition plan for detailed implementation steps
2. Create `proj-cli` repository
3. Begin Phase 1 implementation

---

## 📚 References

- [ADR-0007: Unified CLI Architecture](../../../decisions/ADR-0007-inventory-system-cli-tool-architecture.md)
- [Requirements Document](../../../research/inventory-repository-separation/requirements.md)
- [Research Summary](../../../research/inventory-repository-separation/research-summary.md)
- [Transition Plan](transition-plan.md)

---

**Last Updated:** 2025-12-16

