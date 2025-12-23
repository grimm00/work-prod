# Release Notes - v0.2.0

**Release Date:** 2025-12-23  
**Status:** ✅ Final  
**Type:** Minor Release (Architectural Change)

---

## What's New

### API-Only Architecture

work-prod is now **API-only**. All CLI functionality has been migrated to the separate **proj-cli** tool.

**Why this change:**
- Cleaner separation of concerns (API backend vs CLI frontend)
- CLI can evolve independently
- Easier to maintain and test each component
- Enables CLI to be used with other backends in the future

---

## Breaking Changes

### CLI Removed

The following have been removed from work-prod:

| Removed | Replacement |
|---------|-------------|
| `scripts/project_cli/` | Install [proj-cli](https://github.com/grimm00/proj-cli) |
| `scripts/inventory/` | Use `proj inv` subcommands |
| `scripts/map_inventory_to_projects.py` | Use `proj inv export api` |
| `scripts/projects.json` | Generate with `proj inv export json` |

### Migration Guide

**Step 1: Install proj-cli**

```bash
pip install git+https://github.com/grimm00/proj-cli.git
```

**Step 2: Configure proj-cli**

```bash
proj init
# Or set environment variable
export PROJ_API_URL=http://localhost:5000
```

**Step 3: Use new commands**

| Old (work-prod) | New (proj-cli) |
|-----------------|----------------|
| `./scripts/project_cli/proj list` | `proj list` |
| `./scripts/project_cli/proj get 1` | `proj get 1` |
| `./scripts/inventory/fetch-github-repos.sh` | `proj inv scan github` |
| `./scripts/inventory/scan-local-projects.sh` | `proj inv scan local` |

---

## Improvements

### Documentation

- **README Updated:** Clear instructions for installing proj-cli
- **Scripts README:** Now redirects to proj-cli documentation
- **Command Tracking:** Added command usage tracking documentation

---

## Technical Details

### Changes Summary

- **Files Removed:** ~50 (CLI and inventory scripts)
- **Lines Removed:** ~7,300
- **Lines Added:** ~400 (documentation updates)

### Key PRs

- **PR #38:** chore: Remove CLI and inventory scripts migrated to proj-cli

### Related Releases

- **proj-cli v0.1.0:** Full replacement CLI with all commands
  - 8 project commands (list, get, create, update, delete, search, import-json, archive)
  - 7 inventory commands (scan github/local, analyze, dedupe, export json/api, status)
  - Configuration with XDG compliance
  - Rich terminal output

---

## Known Issues

None known at this time.

---

## Upgrade Path

1. **Before upgrading:** Install proj-cli v0.1.0
2. **Upgrade:** Update work-prod to v0.2.0
3. **Verify:** Confirm `proj list` connects to API
4. **Remove:** Delete any local CLI scripts or aliases

---

**Last Updated:** 2025-12-23  
**Next Release:** TBD (v0.3.0 - project_type field)


