# CHANGELOG Draft - v0.2.0

**Draft Created:** 2025-12-23  
**Status:** ✅ Merged into CHANGELOG.md (2025-12-23)

---

## [0.2.0] - 2025-12-23

### Changed

- **Architecture** - work-prod is now API-only; CLI functionality moved to separate proj-cli repository
- **README** - Updated with proj-cli installation and usage instructions
- **scripts/README** - Now redirects to proj-cli documentation

### Removed

- **CLI Tool** - `scripts/project_cli/` directory removed (migrated to [proj-cli](https://github.com/grimm00/proj-cli))
- **Inventory Scripts** - `scripts/inventory/` directory removed (migrated to proj-cli `inv` subcommands)
- **Mapping Script** - `scripts/map_inventory_to_projects.py` removed (use `proj inv export api`)
- **Sample Data** - `scripts/projects.json` removed (generate with `proj inv export json`)

### Added

- **Command Tracking** - Documentation for tracking CLI command usage across projects

### Migration

To continue using CLI functionality, install proj-cli:

```bash
pip install git+https://github.com/grimm00/proj-cli.git
proj init  # or set PROJ_API_URL environment variable
```

All previous CLI commands are available in proj-cli with the same syntax.

---

## Review Checklist

- [x] All PRs listed (PR #38)
- [x] Categorization correct (Changed/Removed/Added)
- [x] PR numbers accurate
- [x] Descriptions clear and user-facing
- [x] Migration instructions included
- [x] Ready to merge into CHANGELOG.md ✅

---

**Ready for merge:** [x] Yes - Merged 2025-12-23


