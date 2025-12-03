# Project Management CLI Tool

**Purpose:** Command-line interface for managing projects via the Projects API  
**Status:** 🟡 Planned (Phase 1+)  
**Created:** 2025-12-02

---

## 📋 Overview

The `proj` CLI tool provides a user-friendly command-line interface for managing your projects. It's the primary way to interact with the Projects API during the backend MVP phase (Phases 1-7).

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Backend API running on http://localhost:5000
- Required Python packages (see Installation)

### Installation

```bash
cd scripts/project_cli
pip install -r requirements.txt
chmod +x proj
```

### First Commands

```bash
# List all projects
./proj list

# Get project details
./proj get 1

# Create a project
./proj create "My Project" --path ~/code/project --status active

# Get help
./proj --help
```

---

## 📝 Commands

### List Projects

```bash
# List all projects
./proj list

# Filter by status
./proj list --status active

# Filter by organization
./proj list --org work

# Filter by multiple criteria
./proj list --status active --org work

# Search by name/description
./proj list --search "productivity"
```

### Get Project

```bash
# Get single project by ID
./proj get 1
```

### Create Project

```bash
# Minimal create
./proj create "Project Name"

# Full create
./proj create "work-prod" \
  --path ~/Projects/work-prod \
  --org work \
  --classification primary \
  --status active \
  --description "Work productivity system"
```

### Update Project

```bash
# Update status
./proj update 1 --status completed

# Update multiple fields
./proj update 1 \
  --name "New Name" \
  --status completed \
  --classification archive
```

### Delete Project

```bash
# Delete (with confirmation)
./proj delete 1
```

### Archive Project

```bash
# Archive (soft delete)
./proj archive 1
```

### Import Projects

```bash
# Import from JSON file
./proj import projects.json
```

### Statistics (Phase 6)

```bash
# Show project statistics
./proj stats

# Show recently updated projects
./proj recent

# Show active projects (shortcut)
./proj active
```

---

## 🎨 Features

### Rich Output (Phase 6)

Beautiful terminal tables with colors:

```
Active Projects (17)
┌────┬─────────────────────┬────────────┬──────────────┐
│ ID │ Name                │ Status     │ Organization │
├────┼─────────────────────┼────────────┼──────────────┤
│  1 │ work-prod          │ active     │ work         │
│  2 │ learning-python    │ active     │ learning     │
└────┴─────────────────────┴────────────┴──────────────┘
```

### Configuration File (Phase 6)

Store preferences in `~/.projrc`:

```ini
[api]
base_url = http://localhost:5000/api

[display]
max_rows = 50
color = true
```

### Error Handling (Phase 6)

Friendly error messages with suggestions:

```
✗ Error: Could not connect to API
  → Is the backend running? Try: cd backend && python run.py
```

---

## 🔧 Development Phases

### Phase 1: Basic Commands
- `proj list` - List all projects
- `proj get <id>` - Get single project
- Basic output (plain text)

### Phase 2: Create/Update
- `proj create` - Create projects
- `proj update` - Update projects

### Phase 3: Delete/Archive
- `proj delete` - Delete projects
- `proj archive` - Archive projects

### Phase 4: Search/Filter
- Filter flags (--status, --org, --classification)
- Search flag (--search)

### Phase 5: Import
- `proj import` - Bulk import from JSON

### Phase 6: Polish
- Rich library for tables
- Configuration file
- Convenience commands (stats, recent, active)
- Better error handling

---

## 📦 Dependencies

```
requests>=2.31.0
click>=8.1.0        # Phase 6
rich>=13.7.0        # Phase 6
```

---

## 🐛 Troubleshooting

### "Connection refused"
- Backend not running
- Run: `cd backend && python run.py`

### "Command not found: proj"
- Script not executable
- Run: `chmod +x proj`
- Or run: `python proj list`

### "Module not found"
- Dependencies not installed
- Run: `pip install -r requirements.txt`

---

## 🔗 Related Documents

- [Phase 1: List & Get Projects](../../docs/maintainers/planning/features/projects/phase-1.md)
- [Backend MVP Roadmap](../../docs/maintainers/planning/mvp-roadmap.md)
- [Projects API Documentation](../../docs/backend-mvp/API.md) *(Phase 7)*

---

**Last Updated:** 2025-12-02  
**Status:** 🟡 Planned  
**Next:** Implement in Phase 1

