# Projects Feature - Phase 6: CLI Enhancement & Daily Use Tools

**Phase:** 6 - CLI Enhancement & Daily Use Tools  
**Duration:** 1 day  
**Status:** 🔴 Not Started  
**Prerequisites:** Phase 5 complete

---

## 📋 Overview

Phase 6 enhances the CLI tool for daily use. This phase adds rich formatting with tables, colors, better error handling, configuration file support, and additional convenience features. By the end, the CLI is production-ready for daily project management.

**Success Definition:** CLI tool is polished, user-friendly, and suitable for daily use.

---

## 🎯 Goals

1. **Rich Formatting** - Use `rich` library for tables, colors, progress bars
2. **Configuration File** - Store API URL and preferences in `~/.projrc`
3. **Better Error Handling** - Clear error messages and suggestions
4. **Additional Commands** - `proj stats`, `proj recent`, `proj active`
5. **Help System** - Comprehensive `--help` for all commands

---

## 📝 Tasks

#### 1. Install Rich Library
- [ ] Add to `scripts/project_cli/requirements.txt`:
  ```
  requests>=2.31.0
  click>=8.1.0
  rich>=13.7.0
  ```
- [ ] Install: `pip install -r requirements.txt`

#### 2. Refactor CLI with Click
- [ ] Convert script to use Click framework:
  ```python
  import click
  from rich.console import Console
  from rich.table import Table
  
  console = Console()
  
  @click.group()
  def cli():
      """Project management CLI tool."""
      pass
  
  @cli.command()
  @click.option('--status', help='Filter by status')
  @click.option('--org', help='Filter by organization')
  def list(status, org):
      """List all projects."""
      # Implementation
  ```

#### 3. Implement Rich Tables
- [ ] Update list command with table output:
  ```python
  table = Table(title="Projects")
  table.add_column("ID", style="cyan")
  table.add_column("Name", style="green")
  table.add_column("Status", style="yellow")
  table.add_column("Organization")
  
  for project in projects:
      table.add_row(
          str(project['id']),
          project['name'],
          project['status'],
          project.get('organization', '-')
      )
  
  console.print(table)
  ```

#### 4. Add Configuration File
- [ ] Create `~/.projrc` support:
  ```ini
  [api]
  base_url = http://localhost:5000/api
  
  [display]
  max_rows = 50
  color = true
  ```
- [ ] Load config on startup
- [ ] Add `proj config` command to edit settings

#### 5. Add Convenience Commands
- [ ] `proj stats` - Show project statistics:
  - Total projects
  - By status
  - By organization
  - By classification
- [ ] `proj recent` - Show recently updated projects
- [ ] `proj active` - Shortcut for `proj list --status active`
- [ ] `proj mine` - Show projects for current user/org

#### 6. Improve Error Handling
- [ ] Check if backend is running
- [ ] Friendly error messages
- [ ] Suggest fixes (e.g., "Is the backend running? Try: cd backend && python run.py")

#### 7. Add Progress Indicators
- [ ] Show spinner during API calls
- [ ] Progress bar for import operations

#### 8. Create Help System
- [ ] Add detailed `--help` for each command
- [ ] Add examples in help text
- [ ] Create man page or comprehensive README

---

## ✅ Completion Criteria

- [ ] CLI uses rich library for beautiful output
- [ ] Configuration file working
- [ ] All commands have proper --help
- [ ] Error messages are clear and actionable
- [ ] Stats, recent, and active commands working
- [ ] CLI is fast and responsive
- [ ] Documentation complete

---

## 📦 Deliverables

1. Refactored CLI with Click and Rich
2. Configuration file support
3. Additional convenience commands
4. Comprehensive help system
5. Updated README with examples
6. Installation script

---

## 💡 Example Output

```bash
$ proj list --status active

                    Active Projects
┌────┬───────────────────────┬────────┬──────────────┬──────────────┐
│ ID │ Name                  │ Status │ Organization │ Classification│
├────┼───────────────────────┼────────┼──────────────┼──────────────┤
│  1 │ work-prod            │ active │ work         │ primary      │
│  2 │ learning-python      │ active │ learning     │ primary      │
│  3 │ home-automation      │ active │ personal     │ secondary    │
└────┴───────────────────────┴────────┴──────────────┴──────────────┘

Total: 3 active projects

$ proj stats

Project Statistics
═══════════════════

Total Projects: 59

By Status:
  ● active: 25
  ○ paused: 10
  ✓ completed: 20
  ✗ cancelled: 4

By Organization:
  • work: 25
  • learning: 17
  • personal: 17

By Classification:
  🥇 primary: 12
  🥈 secondary: 30
  📦 archive: 15
  🔧 maintenance: 2
```

---

**Last Updated:** 2025-12-02  
**Status:** 🔴 Not Started  
**Next:** Begin after Phase 5 complete
