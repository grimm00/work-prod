# Project Management CLI Tool

**Purpose:** Command-line interface for managing projects via the Projects API  
**Status:** ✅ Active (Phase 1 Complete)  
**Created:** 2025-12-02  
**Updated:** 2025-12-03

---

## 📋 Overview

The `proj` CLI tool provides a user-friendly command-line interface for managing your projects. It's the primary way to interact with the Projects API during the backend MVP phase (Phases 1-7).

**Phase 1 Status:** ✅ Complete
- ✅ List all projects
- ✅ Get project by ID
- ✅ Beautiful Rich formatting
- ✅ Error handling

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

# Get help
./proj --help
```

---

## 📝 Commands

### Phase 1 Commands (✅ Implemented)

#### `list` - List All Projects

```bash
./proj list
```

**Output Example:**
```
                                  Projects (3)                                  
┏━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ ID ┃ Name            ┃ Path                                     ┃ Created    ┃
┡━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│  1 │ work-prod       │ /Users/cdwilson/Projects/work-prod       │ 2025-12-03 │
│  2 │ learning-python │ /Users/cdwilson/Projects/learning-python │ 2025-12-03 │
│  3 │ home-automation │ No path                                  │ 2025-12-03 │
└────┴─────────────────┴──────────────────────────────────────────┴────────────┘
```

#### `get` - Get Project Details

```bash
./proj get <project_id>
```

**Example:**
```bash
./proj get 1
```

**Output:**
```
╭───────────────────────────── Project: work-prod ─────────────────────────────╮
│  ID               1                                                          │
│  Name             work-prod                                                  │
│  Path             /Users/cdwilson/Projects/work-prod                         │
│  Created          2025-12-03T15:59:48                                        │
│  Updated          2025-12-03T15:59:48                                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### Future Commands (Phase 2+)

#### `create` - Create New Project (Phase 2)

```bash
./proj create "Project Name" --path /path/to/project
```

#### `update` - Update Project (Phase 2)

```bash
./proj update <project_id> --name "New Name" --path /new/path
```

#### `delete` - Delete Project (Phase 3)

```bash
./proj delete <project_id>
```

#### `search` - Search Projects (Phase 4)

```bash
./proj search "keyword"
```

#### `import` - Import Projects (Phase 5)

```bash
./proj import ../inventory/data/classifications.json
```

---

## ⚙️ Configuration

### Environment Variables

- `PROJ_API_URL` - API base URL (default: `http://localhost:5000/api`)

**Example:**
```bash
export PROJ_API_URL=http://localhost:5000/api
./proj list
```

### Config File (Future)

Configuration will be stored in `~/.proj/config.json` for persistent settings.

---

## 🏗️ Architecture

### Directory Structure

```
project_cli/
├── README.md           # This file
├── proj                # Main CLI executable
├── requirements.txt    # Python dependencies
├── config.py           # Configuration management
├── api_client.py       # API communication layer
└── commands/
    ├── __init__.py
    ├── list_cmd.py     # ✅ List projects
    ├── get_cmd.py      # ✅ Get project
    ├── create.py       # 🟡 Create project (Phase 2)
    ├── update.py       # 🟡 Update project (Phase 2)
    ├── delete.py       # 🟡 Delete project (Phase 3)
    └── search.py       # 🟡 Search projects (Phase 4)
```

### Technology Stack

- **Click** (8.1.7+) - CLI framework
- **Rich** (13.7.0+) - Beautiful terminal formatting
- **Requests** (2.31.0+) - HTTP client for API calls

### Design Patterns

1. **Command Pattern** - Each CLI command is a separate module
2. **Client Pattern** - APIClient abstracts HTTP communication
3. **Configuration Pattern** - Centralized config management

---

## 🧪 Testing

### Manual Testing

```bash
# Terminal 1: Start backend
cd backend
python run.py

# Terminal 2: Test CLI
cd scripts/project_cli
./proj list
./proj get 1
```

### Test Results (Phase 1)

✅ All tests passing:
- List command displays projects correctly
- Get command shows project details
- Error handling for invalid IDs
- Connection error handling
- Beautiful Rich formatting

---

## 🐛 Troubleshooting

### Connection Refused

**Problem:** `Connection refused` error when running commands.

**Solution:**
1. Start backend server: `cd backend && python run.py`
2. Verify server is running: `curl http://localhost:5000/api/health`
3. Check `PROJ_API_URL` environment variable

### Module Not Found

**Problem:** `ModuleNotFoundError` when running `./proj`

**Solution:**
```bash
cd scripts/project_cli
pip install -r requirements.txt
```

### Permission Denied

**Problem:** `Permission denied` when running `./proj`

**Solution:**
```bash
chmod +x proj
```

### Invalid Project ID

**Problem:** `Invalid project ID format` error

**Solution:**
- Ensure you're using a numeric ID: `./proj get 1`
- Check project exists: `./proj list`

---

## 📚 Usage Examples

### Daily Workflow

```bash
# Morning: Check all projects
./proj list

# View details of current project
./proj get 1

# (Phase 2+) Update project status
./proj update 1 --status active

# (Phase 4+) Search for learning projects
./proj search "learning"
```

### Batch Operations (Future)

```bash
# Import all projects from inventory
./proj import ../inventory/data/classifications.json

# Export projects to JSON
./proj list --format json > projects.json
```

---

## 🔮 Roadmap

### Phase 1: List & Get (✅ Complete)
- ✅ List all projects
- ✅ Get project by ID
- ✅ Rich table formatting
- ✅ Error handling

### Phase 2: Create & Update (🟡 Planned)
- Create new projects
- Update existing projects
- Validation and error handling

### Phase 3: Delete & Archive (🟡 Planned)
- Delete projects
- Archive projects
- Confirmation prompts

### Phase 4: Search & Filter (🟡 Planned)
- Search by name/path
- Filter by status/organization
- Advanced queries

### Phase 5: Import (🟡 Planned)
- Import from JSON
- Bulk project creation
- Duplicate detection

### Phase 6: CLI Enhancement (🟡 Planned)
- Interactive mode
- Output formats (JSON, CSV, table)
- Batch operations
- Configuration file support

---

## 📝 Development

### Adding New Commands

1. Create `commands/new_cmd.py`:
```python
import click
from rich.console import Console
from api_client import APIClient

@click.command()
def new_command():
    """Command description."""
    console = Console()
    client = APIClient()
    # Implementation
```

2. Register in `proj`:
```python
from commands.new_cmd import new_command
cli.add_command(new_command, name='new')
```

3. Update this README

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Keep commands focused

---

**Last Updated:** 2025-12-03  
**Status:** ✅ Phase 1 Complete  
**Next:** Phase 2 - Create & Update commands
