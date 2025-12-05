# Backend

**Purpose:** Flask API backend for project management  
**Status:** ✅ Phase 5 Complete - Import Projects API + CLI  
**Last Updated:** 2025-12-05

---

## 🚀 Quick Start

```bash
# Setup
cd backend
source ../venv/bin/activate
pip install -r requirements.txt

# Initialize database
flask db upgrade

# Run development server
python run.py
# Server runs on http://localhost:5000
```

---

## 📡 API Endpoints

### Health Check
- `GET /api/health` - Server health status

### Projects API (Phase 1-5 Complete)
- `GET /api/projects` - List all projects (with filtering and search)
- `GET /api/projects?status=active&organization=work&search=term` - Filter and search projects
- `GET /api/projects/<id>` - Get project by ID
- `POST /api/projects` - Create new project
- `PATCH /api/projects/<id>` - Update project
- `DELETE /api/projects/<id>` - Delete project permanently
- `PUT /api/projects/<id>/archive` - Archive project
- `POST /api/projects/import` - Bulk import projects from JSON

### Request/Response Examples

**Create Project:**
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

**Update Project:**
```bash
curl -X PATCH http://localhost:5000/api/projects/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

**Archive Project:**
```bash
curl -X PUT http://localhost:5000/api/projects/1/archive
# Sets classification='archive' and status='completed'
```

**Delete Project:**
```bash
curl -X DELETE http://localhost:5000/api/projects/1
# Returns 204 No Content on success
```

**Import Projects:**
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
      }
    ]
  }'
# Returns 201 with statistics: {"imported": 1, "skipped": 0, "errors": []}
```

### Validation Rules

**Classification:** `primary`, `secondary`, `archive`, `maintenance`  
**Status:** `active`, `paused`, `completed`, `cancelled`

**Required Fields:**
- `name` (for POST)

**Optional Fields:**
- `path`, `organization`, `classification`, `status`, `description`, `remote_url`

---

## 🗄️ Database

**Engine:** SQLite  
**ORM:** SQLAlchemy  
**Migrations:** Flask-Migrate

**Models:**
- `Project` - Core project tracking with organization, classification, status

**Migrations:**
```bash
# Create migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Rollback
flask db downgrade
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/integration/api/test_projects.py

# Run specific test
pytest tests/unit/models/test_project.py::test_project_creation
```

**Current Coverage:** 88% (21 integration tests, 13 unit tests)

---

## 📁 Directory Structure

```
backend/
├── app/
│   ├── __init__.py          # Application factory
│   ├── api/                 # API endpoints
│   │   ├── health.py        # Health check
│   │   └── projects.py      # Projects CRUD
│   └── models/              # Database models
│       └── project.py       # Project model
├── migrations/              # Database migrations
├── tests/
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── config.py               # Configuration classes
├── run.py                  # Development server
└── requirements.txt        # Python dependencies
```

---

## ⚙️ Configuration

Environment variables:
- `APP_CONFIG` - Configuration to use (development, production, testing)
- `DATABASE_URL` - Database connection string (production)
- `CORS_ALLOWED_ORIGINS` - Comma-separated allowed origins (production)

Configurations:
- `DevelopmentConfig` - Local development (DEBUG=True)
- `TestingConfig` - Testing environment (in-memory DB)
- `ProductionConfig` - Production deployment

---

**Last Updated:** 2025-12-03  
**Status:** ✅ Phase 2 Complete  
**Coverage:** 88% (34 tests passing)  
**Next:** Phase 3 - Delete & Archive Projects
