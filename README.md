# work-prod

**Purpose:** Manage Productivity and Engagement for Work  
**Version:** v0.1.0-dev (Phase 7 In Progress)  
**Last Updated:** 2025-12-06  
**Status:** ✅ Backend MVP Complete (Phases 1-6), Phase 7 In Progress  
**Approach:** Backend-First API Development with CLI Tools

---

## 🎯 Quick Start

### Prerequisites

- Python 3.11+
- Git

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd work-prod

# Backend Setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
cd backend
pip install -r requirements.txt

# Initialize database
flask db upgrade
```

### Running the Backend

```bash
cd backend
source ../venv/bin/activate
python run.py
# Backend runs on http://localhost:5000
```

### Using the CLI Tool

```bash
# Install CLI dependencies
cd scripts/project_cli
pip install -r requirements.txt
chmod +x proj

# List all projects
./proj list

# Get project details
./proj get 1

# Create a project
./proj create --name "My Project" --org work --classification primary

# Show statistics
./proj stats

# For help
./proj --help
```

**See [CLI Usage Guide](#cli-usage-guide) below for complete documentation.**

### First Steps

1. **Start the backend server:**
   ```bash
   cd backend
   source ../venv/bin/activate
   python run.py
   ```

2. **Verify health:**
   ```bash
   curl http://localhost:5000/api/health
   ```

3. **Use CLI to interact:**
   ```bash
   cd scripts/project_cli
   ./proj list
   ```

4. **Run tests:**
   ```bash
   cd backend
   pytest
   ```

---

## 📁 Project Structure

This project follows a **hub-and-spoke documentation pattern**:

- **Hub Files** (README.md) serve as entry points and navigation guides
- **Spoke Directories** contain detailed implementation and specialized documentation
- **Maintainers Directory** manages project planning, feedback, and decision tracking

### Key Directories

- **`docs/maintainers/`** - Project management hub ([Maintainers Guide](docs/maintainers/README.md))
  - `planning/` - Feature plans, roadmap, notes
  - `research/` - Technical research documents
  - `decisions/` - Architecture Decision Records (ADRs)
  - `feedback/` - External code reviews (Sourcery)
- **`backend/`** - Flask API application ([Backend Guide](backend/README.md))
- **`scripts/project_cli/`** - Command-line interface tools ([CLI Guide](scripts/project_cli/README.md))
- **`scripts/inventory/`** - Project inventory automation
- **`tests/`** - End-to-end testing (E2E only)
- **`frontend/`** - React application (deferred to Phase 8)
- **`docs/`** - User documentation

---

## 🚀 Development Workflow

### Git Flow

- **`main`** - Production releases only
- **`develop`** - Ongoing development
- **`feat/*`** - Feature branches (require PRs)
- **`fix/*`** - Bug fixes (require PRs)
- **`docs/*`** - Documentation (can push directly)
- **`chore/*`** - Maintenance (can push directly)

### Branch Requirements

- Feature branches: Full testing, linting, external reviews
- Documentation branches: Minimal validation
- Release branches: Full validation + external reviews

---

## 🛠️ Technology Stack

### Backend

- **Python 3.11+** - Programming language
- **Flask 3.0** - Web framework with application factory pattern
- **SQLAlchemy** - ORM for database operations
- **Flask-Migrate** - Database migrations
- **SQLite** - Local-first database
- **pytest** - Testing framework with pytest-flask and pytest-cov

### Frontend

- **React 18** - UI framework
- **Vite** - Build tool and development server
- **Zustand** - State management
- **React Router v6** - Client-side routing
- **Axios** - HTTP client for API calls
- **Vitest** - Testing framework with React Testing Library

### Integration

- **Vite Proxy** - Development proxy from frontend to backend
- **Flask-CORS** - Cross-origin resource sharing support

---

## 📊 Project Status

### ✅ Completed (Phases 0-6)

**Phase 0: Development Environment**
- Flask backend with application factory pattern
- Health check API endpoint (`/api/health`)
- Backend testing infrastructure (pytest, 100% coverage on Phase 0)
- Database migrations with Flask-Migrate

**Phase 1: List & Get Projects**
- Project model (id, name, path, timestamps)
- GET `/api/projects` - List all projects with filtering
- GET `/api/projects/<id>` - Get single project
- CLI commands: `proj list` and `proj get`

**Phase 2: Create & Update Projects**
- POST `/api/projects` - Create new projects
- PATCH `/api/projects/<id>` - Update projects
- CLI commands: `proj create` and `proj update`
- Validation and error handling

**Phase 3: Delete & Archive Projects**
- DELETE `/api/projects/<id>` - Delete projects
- PUT `/api/projects/<id>/archive` - Archive projects
- CLI commands: `proj delete` and `proj archive`

**Phase 4: Search & Filter**
- Enhanced filtering (status, organization, classification)
- Text search in names and descriptions
- CLI filtering options

**Phase 5: Bulk Import**
- POST `/api/projects/import` - Bulk import from JSON
- CLI command: `proj import`
- Duplicate detection and error handling

**Phase 6: CLI Enhancement**
- Configuration management (`proj config`)
- Convenience commands (`stats`, `recent`, `active`, `mine`)
- Enhanced error handling and progress indicators

### 🟠 Current (Phase 7 - Testing & Documentation)

- Automated CLI testing (infrastructure complete, 7 tests deferred)
- Bug fixes from PR validation (complete - no critical bugs)
- Test coverage improvements (97% coverage achieved)
- API documentation (OpenAPI spec complete)
- User documentation (in progress)

### 🟡 Planned (Phase 8 - Frontend Learning Project)

- React UI for project management
- Build on working backend API
- Learn JavaScript/React without deadline pressure
- Frontend is a separate learning project

---

## 🎯 Backend MVP Features

The backend MVP provides a complete REST API for managing projects with a command-line interface.

### Core Features

- ✅ **Project Management** - Create, read, update, delete, and archive projects
- ✅ **Filtering & Search** - Filter by status, organization, classification; search in names and descriptions
- ✅ **Bulk Import** - Import multiple projects from JSON files
- ✅ **CLI Tool** - User-friendly command-line interface with Rich formatting
- ✅ **Configuration** - Persistent configuration management
- ✅ **Error Handling** - Comprehensive error handling with user-friendly messages
- ✅ **API Documentation** - Complete OpenAPI 3.0.3 specification

### Project Fields

- **id** (auto-generated) - Unique project identifier
- **name** (required) - Project name
- **path** (optional, unique) - File system path
- **organization** (optional) - Organization name
- **classification** (optional) - primary, secondary, archive, maintenance
- **status** (optional, default: active) - active, paused, completed, cancelled
- **description** (optional) - Project description
- **remote_url** (optional) - Git repository URL
- **created_at** (auto-generated) - Creation timestamp
- **updated_at** (auto-generated) - Last update timestamp

---

## 📡 API Endpoints

**📚 Complete API Documentation:**
- **OpenAPI Specification:** [`backend/openapi.yaml`](backend/openapi.yaml) - Full API spec with schemas and examples
- **Backend README:** [`backend/README.md`](backend/README.md) - API endpoint reference

**🔍 View API Docs:**
- Upload `backend/openapi.yaml` to [Swagger Editor](https://editor.swagger.io/)
- Use [Redoc](https://github.com/Redocly/redoc) to generate docs
- Import into Postman for API testing

### Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/projects` | List projects (with filters) |
| GET | `/api/projects/<id>` | Get project by ID |
| POST | `/api/projects` | Create new project |
| PATCH | `/api/projects/<id>` | Update project |
| DELETE | `/api/projects/<id>` | Delete project |
| PUT | `/api/projects/<id>/archive` | Archive project |
| POST | `/api/projects/import` | Bulk import projects |

**See [`backend/README.md`](backend/README.md) for detailed endpoint documentation.**

---

## 💻 CLI Usage Guide

The `proj` CLI tool provides a user-friendly interface for managing projects.

### Installation

```bash
# Install CLI dependencies
cd scripts/project_cli
pip install -r requirements.txt
chmod +x proj

# Verify installation
./proj --help
```

### Configuration

Configuration is stored in `~/.projrc`. Use `proj config` to manage settings:

```bash
# Show current configuration
./proj config show

# Set API URL
./proj config set api.url http://localhost:5000/api

# Get specific setting
./proj config get api.url
```

**Environment Variable:**
```bash
export PROJ_API_URL=http://localhost:5000/api
```

### Basic Commands

#### List Projects
```bash
# List all projects
./proj list

# Filter by status
./proj list --status active

# Filter by organization
./proj list --org work

# Filter by classification
./proj list --classification primary

# Search projects
./proj list --search "productivity"

# Combine filters
./proj list --status active --org work --search "project"

# Wide format (show all columns)
./proj list --wide
```

#### Get Project
```bash
# Get project by ID
./proj get 1
```

#### Create Project
```bash
# Minimal (name only)
./proj create --name "My Project"

# Full project
./proj create \
  --name "My Project" \
  --path "/path/to/project" \
  --org work \
  --classification primary \
  --status active \
  --description "Project description" \
  --remote-url "https://github.com/user/repo"
```

#### Update Project
```bash
# Update single field
./proj update 1 --status paused

# Update multiple fields
./proj update 1 --status completed --description "Updated description"
```

#### Delete Project
```bash
# Delete with confirmation prompt
./proj delete 1
```

#### Archive Project
```bash
# Archive project (sets classification=archive, status=completed)
./proj archive 1
```

#### Import Projects
```bash
# Import from JSON file
./proj import projects.json

# JSON format:
# {
#   "projects": [
#     {"name": "Project 1", "path": "/path/1", ...},
#     {"name": "Project 2", ...}
#   ]
# }
```

### Convenience Commands

```bash
# Show statistics
./proj stats

# Show recent projects
./proj recent

# Show active projects
./proj active

# Show your projects (filtered by organization)
./proj mine --org work
```

### Getting Help

```bash
# General help
./proj --help

# Command-specific help
./proj list --help
./proj create --help
```

**📚 Complete CLI Documentation:** See [`scripts/project_cli/README.md`](scripts/project_cli/README.md) for detailed CLI documentation.

---

## 📖 API Usage Examples

### Using curl

#### Create Project
```bash
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Project",
    "organization": "work",
    "classification": "primary",
    "status": "active",
    "description": "Project description"
  }'
```

#### List Projects with Filters
```bash
# Filter by status
curl "http://localhost:5000/api/projects?status=active"

# Filter by organization
curl "http://localhost:5000/api/projects?organization=work"

# Search projects
curl "http://localhost:5000/api/projects?search=productivity"

# Combine filters
curl "http://localhost:5000/api/projects?status=active&organization=work&search=project"
```

#### Update Project
```bash
curl -X PATCH http://localhost:5000/api/projects/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

#### Archive Project
```bash
curl -X PUT http://localhost:5000/api/projects/1/archive
```

#### Delete Project
```bash
curl -X DELETE http://localhost:5000/api/projects/1
```

#### Bulk Import
```bash
curl -X POST http://localhost:5000/api/projects/import \
  -H "Content-Type: application/json" \
  -d '{
    "projects": [
      {
        "name": "Project 1",
        "path": "/path/1",
        "remote_url": "https://github.com/user/project1",
        "classification": "primary",
        "status": "active"
      },
      {
        "name": "Project 2",
        "organization": "work",
        "classification": "secondary",
        "status": "paused"
      }
    ]
  }'
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:5000/api"

# Create project
response = requests.post(f"{BASE_URL}/projects", json={
    "name": "My Project",
    "organization": "work",
    "classification": "primary",
    "status": "active"
})
project = response.json()

# List projects
response = requests.get(f"{BASE_URL}/projects?status=active")
projects = response.json()

# Update project
response = requests.patch(f"{BASE_URL}/projects/1", json={
    "status": "completed"
})
updated = response.json()

# Delete project
response = requests.delete(f"{BASE_URL}/projects/1")
# Returns 204 No Content on success
```

---

## 🛠️ Development Setup

### Prerequisites

- **Python 3.11+** - Backend and CLI require Python 3.11 or higher
- **Git** - Version control
- **Virtual Environment** - Recommended for Python dependencies

### Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd work-prod

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Initialize database
flask db upgrade

# Install CLI dependencies
cd ../scripts/project_cli
pip install -r requirements.txt
chmod +x proj
```

### Running the Backend

```bash
# From project root
cd backend
source ../venv/bin/activate
python run.py

# Backend runs on http://localhost:5000
# Health check: curl http://localhost:5000/api/health
```

### Running Tests

```bash
# Run all tests
cd backend
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/integration/api/test_projects.py

# Run CLI tests
pytest scripts/project_cli/tests/
```

### Database Migrations

```bash
cd backend

# Create new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback last migration
flask db downgrade
```

### Development Workflow

1. **Start Backend:**
   ```bash
   cd backend
   source ../venv/bin/activate
   python run.py
   ```

2. **Test with CLI:**
   ```bash
   cd scripts/project_cli
   ./proj list
   ```

3. **Run Tests:**
   ```bash
   cd backend
   pytest
   ```

---

## 🔧 Troubleshooting

### Backend Issues

#### Port Already in Use
**Problem:** `Address already in use` when starting backend

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or use a different port
export FLASK_RUN_PORT=5001
python run.py
```

#### Database Migration Errors
**Problem:** Migration fails or database is out of sync

**Solution:**
```bash
cd backend

# Reset database (development only!)
rm instance/*.db

# Recreate database
flask db upgrade
```

#### Module Import Errors
**Problem:** `ModuleNotFoundError` when running backend

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### CLI Issues

#### Connection Refused
**Problem:** `Connection refused` when running CLI commands

**Solution:**
1. **Start backend server:**
   ```bash
   cd backend
   source ../venv/bin/activate
   python run.py
   ```

2. **Verify backend is running:**
   ```bash
   curl http://localhost:5000/api/health
   ```

3. **Check API URL configuration:**
   ```bash
   ./proj config show
   # Or set via environment variable:
   export PROJ_API_URL=http://localhost:5000/api
   ```

#### Permission Denied
**Problem:** `Permission denied` when running `./proj`

**Solution:**
```bash
chmod +x scripts/project_cli/proj
```

#### Module Not Found (CLI)
**Problem:** `ModuleNotFoundError` when running CLI

**Solution:**
```bash
cd scripts/project_cli
pip install -r requirements.txt
```

#### Invalid Project ID
**Problem:** `Invalid project ID format` or `Project not found`

**Solution:**
- Use numeric ID: `./proj get 1` (not `./proj get "1"`)
- Check project exists: `./proj list`
- Verify ID is correct: `./proj get <id>`

### Configuration Issues

#### Config File Not Found
**Problem:** Configuration file doesn't exist

**Solution:**
- Config file is created automatically on first use
- Use `./proj config set` to create and configure
- Default location: `~/.projrc`

#### Invalid API URL
**Problem:** CLI can't connect to backend

**Solution:**
```bash
# Check current API URL
./proj config get api.url

# Set correct API URL
./proj config set api.url http://localhost:5000/api

# Or use environment variable
export PROJ_API_URL=http://localhost:5000/api
```

### Testing Issues

#### Tests Fail with Database Errors
**Problem:** Tests fail due to database state

**Solution:**
```bash
cd backend

# Tests use in-memory database by default
# If issues persist, check test configuration in pytest.ini
pytest --tb=short -v
```

#### Coverage Report Not Generated
**Problem:** Coverage HTML report not created

**Solution:**
```bash
cd backend
pytest --cov=app --cov-report=html
# Report available at backend/htmlcov/index.html
```

---

## 📚 Documentation

### Quick References

- **[Backend README](backend/README.md)** - Backend API documentation
- **[CLI README](scripts/project_cli/README.md)** - Complete CLI usage guide
- **[OpenAPI Spec](backend/openapi.yaml)** - Full API specification

### Planning Documents

- [Project Roadmap](docs/maintainers/planning/roadmap.md)
- [Feature Plans](docs/maintainers/planning/features/)
- [Release History](docs/maintainers/planning/releases/)

---

## 🔧 Development Commands

### Backend

```bash
# Run development server
cd backend
source ../venv/bin/activate
python run.py

# Run tests
cd backend
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/integration/api/test_health.py
```

### Frontend

```bash
# Run development server
cd frontend
npm run dev

# Run tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage

# Build for production
npm run build
```

---

## 📈 Metrics

**Backend MVP (Phases 1-6):**
- **207 tests** (199 backend + 8 uncovered path tests) with **97% coverage**
- **28 PRs merged** (features, bug fixes, quality improvements)
- **2,000+ lines** of backend code
- **Complete REST API** with 8 endpoints
- **Full CLI tool** with 13 commands
- **OpenAPI 3.0.3 specification** (691 lines)

**Test Coverage:**
- **Models:** 100% coverage
- **API Endpoints:** 97% coverage
- **CLI Commands:** Infrastructure complete (7 tests deferred)

**Documentation:**
- **OpenAPI Specification** - Complete API documentation
- **CLI Usage Guide** - Comprehensive command reference
- **User Documentation** - Installation, setup, troubleshooting

---

## 🎊 Key Achievements

**Week 1 (Nov 26 - Dec 1):**
1. ✅ Tech stack research complete (4 ADRs, 2,500+ lines analysis)
2. ✅ Testing strategy finalized (ADR-0006)
3. ✅ Projects-first architecture decided (ADR-0005)
4. ✅ Backend-first MVP pivot completed

**Week 2 (Dec 2-6):**
1. ✅ Phase 0: Development environment setup (1 day)
2. ✅ Phase 1: List & Get Projects API + CLI (1 day)
3. ✅ Code quality fixes (CORS, logging, FLASK_ENV)
4. ✅ Opportunities documentation structure created
5. ✅ Phase 1 learnings captured for dev-infra template

**Quality & Process:**
- TDD vertical slice approach working excellently
- Hub-and-spoke documentation pattern scaling well
- PR review workflow preventing issues before merge
- CLI-first approach accelerating backend development

---

## 📞 Support

- [Documentation](docs/)
- [Issues]([issues-url])
- [Discussions]([discussions-url])

---

**Last Updated:** 2025-12-06  
**Status:** ✅ Backend MVP Complete (Phases 1-6), Phase 7 In Progress  
**Next:** Complete Phase 7 (Testing & Documentation), then Phase 8 (Frontend)
