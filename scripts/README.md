# Scripts

**Purpose:** Placeholder directory for future automation scripts  
**Status:** ⚠️ Migrated to [proj-cli](https://github.com/grimm00/proj-cli)  
**Last Updated:** 2025-12-18

---

## ⚠️ Migration Notice

All CLI and inventory scripts have been **migrated to the separate [proj-cli](https://github.com/grimm00/proj-cli) repository**.

### What was migrated:

| Former Location | New Location |
|-----------------|--------------|
| `scripts/project_cli/` | [proj-cli](https://github.com/grimm00/proj-cli) (`proj` command) |
| `scripts/inventory/` | [proj-cli](https://github.com/grimm00/proj-cli) (`proj inv` subcommand) |
| `scripts/map_inventory_to_projects.py` | [proj-cli](https://github.com/grimm00/proj-cli) (`proj inv export api`) |

### New unified CLI

Install and use the new `proj` command:

```bash
# Install
pip install git+https://github.com/grimm00/proj-cli.git

# Project management
proj list           # List all projects
proj get 1          # Get project details
proj create "Name"  # Create new project

# Inventory management
proj inv scan github   # Scan GitHub repos
proj inv scan local    # Scan local directories
proj inv analyze       # Analyze tech stack
proj inv export api    # Push to work-prod API
```

See [proj-cli README](https://github.com/grimm00/proj-cli#readme) for full documentation.

---

**Last Updated:** 2025-12-18
