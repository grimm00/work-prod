# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

[Changes not yet released]

## [0.3.0] - 2025-12-29

### Added

- **Project Type Field** - New `project_type` enum for classifying projects (PR #40, #41, #42)
  - Valid types: `Work`, `Personal`, `Learning`, `Inactive`
  - Database column with index for filtering performance
  - API query parameter: `GET /api/projects?project_type=Work`
  - Invalid values return 400 error with clear message

- **Backfill Script** - One-time script to classify existing projects (`scripts/backfill_project_type.py`)
  - Heuristic-based classification
  - Dry-run mode by default
  - Detailed results reporting

- **Manual Testing Guide** - Test scenarios for project-type-field feature
  - 5 scenarios covering API filtering
  - Located in feature documentation

### Changed

- **Project Model** - Added `project_type` field to `to_dict()` output
- **OpenAPI Specification** - Updated with `project_type` field in all relevant schemas

### Documentation

- Feature hub documentation for project-type-field feature
- Phase documents with detailed implementation plans
- Fix tracking for deferred Sourcery review items (10 issues)

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

## [0.1.0] - 2025-12-07

### Added

- **Full CRUD API** - GET, POST, PATCH, DELETE, and Archive endpoints for projects
- **Search and Filter** - Filter by status, organization, classification; text search in names/descriptions
- **Bulk Import** - Import multiple projects from JSON with duplicate detection
- **CLI Tool** - Complete command-line interface with all CRUD operations
  - `proj list` - List projects with filters
  - `proj get <id>` - Get project details
  - `proj create` - Create new project
  - `proj update <id>` - Update project
  - `proj delete <id>` - Delete project (with confirmation)
  - `proj archive <id>` - Archive project
  - `proj import <file>` - Import from JSON
  - `proj config` - Manage configuration
  - Convenience commands: `stats`, `recent`, `active`, `mine`
- **Production Configuration** - Complete production guide (PRODUCTION.md)
- **Deployment Guide** - Comprehensive deployment instructions (DEPLOYMENT.md)
- **OpenAPI Specification** - Full API documentation (openapi.yaml)

### Fixed

- **Environment Variable Loading** - Robust pattern replacing brittle `xargs` approach
- **Database Migration Logic** - Always-run pattern ensuring migrations apply on deployments

### Technical

- 97% test coverage (214 tests: 166 backend + 63 CLI)
- Query performance < 3ms for 100 projects
- Flask application factory pattern
- SQLite local-first database

---

[Unreleased]: https://github.com/grimm00/work-prod/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/grimm00/work-prod/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/grimm00/work-prod/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/grimm00/work-prod/releases/tag/v0.1.0

