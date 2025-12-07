# Scripts

**Purpose:** Automation and utility scripts for project management  
**Status:** ✅ Active  
**Last Updated:** 2025-12-07

---

## 📋 Quick Links

### Script Categories

- **[Project Inventory Scripts](inventory/README.md)** - Automated discovery and cataloging of repositories and projects (✅ Active)
- **[Project Management CLI](project_cli/README.md)** - Command-line interface for managing projects via the Projects API (✅ Phase 8 Complete - MVP Ready)

---

## 🎯 Overview

The scripts directory contains automation scripts for project inventory management and CLI tools for interacting with the Projects API.

### Script Types

1. **Project Inventory Scripts** - Automated discovery and cataloging of repositories and projects
2. **Project Management CLI** - Command-line interface for the Projects API
3. **Utility Scripts** - Data mapping and conversion utilities

---

## 📁 Directory Structure

```
scripts/
├── inventory/                    # Project inventory scripts
│   ├── README.md                 # Inventory scripts documentation
│   ├── fetch-github-repos.sh     # Fetch GitHub repositories
│   ├── scan-local-projects.sh    # Scan local Git repositories
│   ├── analyze-tech-stack.py     # Analyze languages and technologies
│   ├── classify-projects.py      # Interactive project classification
│   ├── deduplicate-projects.py   # Merge GitHub and local projects
│   ├── generate-report-deduplicated.py  # Generate final inventory reports
│   └── data/                     # Output data (gitignored)
├── project_cli/                  # CLI tool for Projects API
│   ├── README.md                 # CLI documentation
│   ├── proj                      # Main CLI executable
│   ├── cli.py                    # CLI entry point
│   ├── api_client.py             # API communication layer
│   ├── commands/                 # CLI command modules
│   └── tests/                    # CLI integration tests
└── map_inventory_to_projects.py  # Map inventory data to projects JSON
```

---

## 🚀 Quick Start

### Project Inventory Scripts

For automated discovery and cataloging of repositories:

```bash
cd scripts/inventory
# See inventory/README.md for complete workflow
```

### Project Management CLI

For managing projects via the CLI:

```bash
cd scripts/project_cli
pip install -r requirements.txt
chmod +x proj
./proj --help
# See project_cli/README.md for complete documentation
```

---

## 📝 Script Descriptions

### Project Inventory Scripts (`inventory/`)

Automated scripts for discovering and cataloging repositories and projects:

- **fetch-github-repos.sh** - Fetches all repositories for a GitHub user
- **scan-local-projects.sh** - Scans local directories for Git repositories
- **analyze-tech-stack.py** - Analyzes languages and technologies across repos
- **classify-projects.py** - Interactive script to classify projects by category
- **deduplicate-projects.py** - Merges GitHub and local projects when they reference the same repository
- **generate-report-deduplicated.py** - Generates final deduplicated inventory and skills documents

**See [inventory/README.md](inventory/README.md) for complete documentation.**

### Project Management CLI (`project_cli/`)

Command-line interface for managing projects via the Projects API:

- **proj** - Main CLI executable with commands for:
  - Listing projects (with filtering and search)
  - Getting project details
  - Creating, updating, deleting projects
  - Archiving projects
  - Importing projects from JSON

**See [project_cli/README.md](project_cli/README.md) for complete documentation.**

### Utility Scripts

- **map_inventory_to_projects.py** - Maps inventory data to projects JSON format for import

---

## 🔗 Integration

### Inventory → Projects Import

The inventory scripts generate data that can be imported into the Projects API:

```bash
# 1. Run inventory scripts (see inventory/README.md)
cd scripts/inventory
./fetch-github-repos.sh
./scan-local-projects.sh
python3 analyze-tech-stack.py
python3 classify-projects.py
python3 deduplicate-projects.py
python3 generate-report-deduplicated.py

# 2. Map inventory to projects JSON
cd ..
python3 map_inventory_to_projects.py

# 3. Import via CLI
cd project_cli
./proj import ../projects.json
```

---

## 📊 Status

**Project Inventory Scripts:** ✅ Active - Used for initial project discovery  
**Project Management CLI:** ✅ Phase 8 Complete - MVP Ready  
**Utility Scripts:** ✅ Active

---

**Last Updated:** 2025-12-07  
**Status:** ✅ Active  
**Next:** See individual script READMEs for usage details
