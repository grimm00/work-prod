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

**📚 Full API Documentation:** See [OpenAPI Specification](openapi.yaml) for complete API documentation with request/response schemas, examples, and error codes.

**🔍 View API Docs:**
- **Swagger UI:** Upload `openapi.yaml` to [Swagger Editor](https://editor.swagger.io/) or use [Swagger UI](https://swagger.io/tools/swagger-ui/)
- **Redoc:** Use [Redoc](https://github.com/Redocly/redoc) to generate beautiful API docs from `openapi.yaml`
- **Postman:** Import `openapi.yaml` into Postman for API testing

### Health Check
- `GET /api/health` - Server health status
  - Returns: `{"status": "ok", "message": "Flask backend is running"}`

### Projects API (Phase 1-5 Complete)

#### List Projects
- `GET /api/projects` - List all projects
- `GET /api/projects?status=active` - Filter by status (active, paused, completed, cancelled)
- `GET /api/projects?organization=work` - Filter by organization
- `GET /api/projects?classification=primary` - Filter by classification (primary, secondary, archive, maintenance)
- `GET /api/projects?search=term` - Search in name and description (case-insensitive)
- `GET /api/projects?status=active&organization=work&search=term` - Combine filters

#### Get Project
- `GET /api/projects/<id>` - Get project by ID
  - Returns: Project object or 404 if not found

#### Create Project
- `POST /api/projects` - Create new project
  - Required: `name`
  - Optional: `path`, `organization`, `classification`, `status`, `description`, `remote_url`
  - Default: `status` defaults to 'active'
  - Returns: 201 Created with Location header

#### Update Project
- `PATCH /api/projects/<id>` - Update project (partial update)
  - All fields optional - only provided fields are updated
  - Returns: 200 OK with updated project

#### Delete Project
- `DELETE /api/projects/<id>` - Delete project permanently
  - Returns: 204 No Content on success

#### Archive Project
- `PUT /api/projects/<id>/archive` - Archive project
  - Sets `classification='archive'` and `status='completed'`
  - Returns: 200 OK with archived project

#### Bulk Import
- `POST /api/projects/import` - Bulk import projects from JSON
  - Request body: `{"projects": [...]}`
  - Returns: 201 Created with statistics (`imported`, `skipped`, `errors`)

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
- `name` (required for POST /api/projects)

**Optional Fields:**
- `path` (must be unique if provided)
- `organization`
- `classification`
- `status` (defaults to 'active' if not provided)
- `description`
- `remote_url`

**Validation:**
- `name`: Required, cannot be empty
- `status`: Cannot be null (if provided), must be valid enum value
- `classification`: Must be valid enum value if provided
- `path`: Must be unique across all projects

**Error Responses:**
- `400 Bad Request`: Validation error (invalid enum, missing required field, etc.)
- `404 Not Found`: Project not found
- `409 Conflict`: Duplicate path or database integrity error
- `500 Internal Server Error`: Server error (details not exposed to client)

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

**Current Coverage:** 97% (207 tests passing: 199 backend + 8 uncovered path tests)

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

**Last Updated:** 2025-12-06  
**Status:** ✅ Phase 7 In Progress  
**Coverage:** 97% (207 tests passing)  
**API Documentation:** OpenAPI 3.0.3 specification available in `openapi.yaml`
