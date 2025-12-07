# Projects Feature - Phase 1: Projects API - List & Get

**Phase:** 1 - Projects API - List & Get (Backend + CLI)  
**Duration:** 1.5 days (Actual: 1 day)  
**Status:** ✅ Complete  
**Prerequisites:** Phase 0 complete  
**Completed:** 2025-12-03

---

## 📋 Overview

Phase 1 delivers the first backend API endpoints for viewing projects. This phase establishes the TDD pattern for backend development that will be used in all subsequent phases. By the end, you can list and retrieve projects via API endpoints and a simple CLI tool.

**Success Definition:** Can list and get projects via curl/CLI tool with backend tests passing.

---

## 🎯 Goals

1. **Project Model Created** - SQLAlchemy model with minimal fields
2. **GET /api/projects Endpoint** - Returns list of projects as JSON
3. **GET /api/projects/<id> Endpoint** - Returns single project by ID
4. **CLI List Command** - Simple `proj list` command
5. **Complete Backend Test Coverage** - TDD with pytest

---

## 📝 Tasks

### TDD Flow (Backend → CLI → Manual Testing)

#### 1. Write Backend Model Test (TDD - RED)

- [ ] Create `backend/tests/unit/models/test_project.py`
- [ ] Test Project model creation with fields: id, name, path, created_at, updated_at
- [ ] Test model validation (name required)
- [ ] Test model serialization to JSON via `to_dict()`
- [ ] Test created_at/updated_at timestamps
- [ ] Run test: **FAILS** ❌ (model doesn't exist yet)

#### 2. Implement Project Model (TDD - GREEN)

- [ ] Create `backend/app/models/__init__.py` (import Project)
- [ ] Create `backend/app/models/project.py`
- [ ] SQLAlchemy model with fields:
  - `id`: Integer, primary key, autoincrement
  - `name`: String(200), required, not null
  - `path`: String(500), unique, nullable
  - `created_at`: DateTime, default=func.now()
  - `updated_at`: DateTime, default=func.now(), onupdate=func.now()
- [ ] Add `to_dict()` method for JSON serialization
- [ ] Add `__repr__()` for debugging
- [ ] Create database migration:
  ```bash
  flask db init  # Only if first migration
  flask db migrate -m "Add projects table"
  flask db upgrade
  ```
- [ ] Run model tests: **PASSES** ✅

#### 3. Write API Endpoint Tests (TDD - RED)

- [ ] Create `backend/tests/integration/api/test_projects.py`
- [ ] Test GET /api/projects returns empty list initially
- [ ] Test GET /api/projects returns list with seeded projects
- [ ] Test GET /api/projects response format: `{"projects": [...], "total": N}`
- [ ] Test GET /api/projects/<id> returns single project
- [ ] Test GET /api/projects/<id> returns 404 for non-existent ID
- [ ] Test response status codes (200 OK, 404 Not Found)
- [ ] Run tests: **FAILS** ❌ (endpoints don't exist yet)

#### 4. Implement API Endpoints (TDD - GREEN)

- [ ] Create `backend/app/api/projects.py` blueprint
- [ ] Register projects blueprint in `app/__init__.py`
- [ ] Implement GET /api/projects route:
  ```python
  @projects_bp.route('/projects', methods=['GET'])
  def get_projects():
      projects = Project.query.all()
      return jsonify({
          'projects': [p.to_dict() for p in projects],
          'total': len(projects)
      }), 200
  ```
- [ ] Implement GET /api/projects/<id> route:
  ```python
  @projects_bp.route('/projects/<int:project_id>', methods=['GET'])
  def get_project(project_id):
      project = Project.query.get_or_404(project_id)
      return jsonify(project.to_dict()), 200
  ```
- [ ] Add error handling for 404
- [ ] Run API tests: **PASSES** ✅
- [ ] Verify test coverage: `pytest --cov=app/models --cov=app/api/projects`

#### 5. Manual API Testing with curl

- [ ] Start backend: `cd backend && python run.py`
- [ ] Test empty list:
  ```bash
  curl http://localhost:5000/api/projects
  # Expected: {"projects": [], "total": 0}
  ```
- [ ] Create test project via Python shell:
  ```bash
  flask shell
  >>> from app import db
  >>> from app.models.project import Project
  >>> p = Project(name="Test Project", path="/test/path")
  >>> db.session.add(p)
  >>> db.session.commit()
  >>> exit()
  ```
- [ ] Test list with data:
  ```bash
  curl http://localhost:5000/api/projects
  # Expected: {"projects": [{"id": 1, "name": "Test Project", ...}], "total": 1}
  ```
- [ ] Test get single project:
  ```bash
  curl http://localhost:5000/api/projects/1
  # Expected: {"id": 1, "name": "Test Project", "path": "/test/path", ...}
  ```
- [ ] Test 404:
  ```bash
  curl http://localhost:5000/api/projects/999
  # Expected: 404 error
  ```

#### 6. Create Simple CLI Tool

- [ ] Create directory: `scripts/project_cli/`
- [ ] Create `scripts/project_cli/proj` (executable bash script):
  ```bash
  #!/usr/bin/env python3
  import sys
  import requests
  import json
  
  API_BASE = "http://localhost:5000/api"
  
  def list_projects():
      resp = requests.get(f"{API_BASE}/projects")
      data = resp.json()
      print(f"\nProjects ({data['total']}):")
      for project in data['projects']:
          print(f"  [{project['id']}] {project['name']}")
          if project.get('path'):
              print(f"      Path: {project['path']}")
      print()
  
  if __name__ == "__main__":
      if len(sys.argv) < 2:
          print("Usage: proj <command>")
          print("Commands: list")
          sys.exit(1)
      
      command = sys.argv[1]
      if command == "list":
          list_projects()
      else:
          print(f"Unknown command: {command}")
          sys.exit(1)
  ```
- [ ] Make executable: `chmod +x scripts/project_cli/proj`
- [ ] Test CLI:
  ```bash
  cd scripts/project_cli
  ./proj list
  ```

#### 7. Create CLI README

- [ ] Create `scripts/project_cli/README.md`:
  - Installation instructions
  - Usage examples
  - Available commands
  - API endpoint reference

---

## ✅ Completion Criteria

- [ ] Project model exists with minimal fields (id, name, path, timestamps)
- [ ] Database migration created and applied
- [ ] GET /api/projects endpoint works (returns list)
- [ ] GET /api/projects/<id> endpoint works (returns single project)
- [ ] Backend model tests pass (100% coverage on model)
- [ ] Backend API tests pass (list and get endpoints)
- [ ] Can list projects via curl
- [ ] Can get single project via curl
- [ ] Simple CLI `proj list` command works
- [ ] No errors in backend logs
- [ ] Coverage > 80% for new code

---

## 📦 Deliverables

1. **Backend Code**
   - `backend/app/models/project.py` - SQLAlchemy model
   - `backend/app/api/projects.py` - API endpoints blueprint
   - Database migration file
   - Updated `app/__init__.py` with blueprint registration

2. **Tests**
   - `backend/tests/unit/models/test_project.py` - Model tests
   - `backend/tests/integration/api/test_projects.py` - API endpoint tests
   - Coverage report (HTML)

3. **CLI Tool**
   - `scripts/project_cli/proj` - Executable CLI script
   - `scripts/project_cli/README.md` - Usage documentation

4. **Documentation**
   - API documentation for GET /api/projects
   - API documentation for GET /api/projects/<id>
   - CLI usage examples

---

## 🔗 Dependencies

### Prerequisites

- ✅ Phase 0: Development Environment complete
- ✅ Flask-Migrate configured
- ✅ pytest configured

### External Dependencies

- None (uses existing Flask + SQLAlchemy setup)

### Blocks

- Phase 2: Create & Update Projects

---

## ⚠️ Risks

**Risk: Model Design Too Minimal**  
**Probability:** Low  
**Impact:** Low  
**Mitigation:** Start minimal, extend in Phase 2. Avoids over-engineering.  
**Contingency:** Easy to add fields via migration

**Risk: CLI Tool Too Basic**  
**Probability:** High  
**Impact:** Low  
**Mitigation:** Phase 1 is proof-of-concept, Phase 6 enhances CLI  
**Contingency:** curl always works as fallback

---

## 📊 Progress Tracking

**Phase Status:** 🔴 Not Started

**Backend (0/4 complete)**
- [ ] Project model implemented
- [ ] Database migration created
- [ ] GET /api/projects endpoint working
- [ ] GET /api/projects/<id> endpoint working

**Testing (0/3 complete)**
- [ ] Model tests passing
- [ ] API tests passing
- [ ] Coverage > 80%

**CLI (0/2 complete)**
- [ ] Basic `proj list` command working
- [ ] CLI README created

---

## 💡 Implementation Notes

### TDD Workflow

**For Model:**
1. Write test for `Project(name="Test")` → Run → FAIL
2. Create model with `name` field → Run → PASS
3. Write test for `to_dict()` → Run → FAIL
4. Implement `to_dict()` → Run → PASS
5. Refactor if needed

**For API:**
1. Write test for `GET /api/projects` returns empty list → FAIL
2. Create blueprint and route returning `[]` → PASS
3. Write test for list with projects → FAIL
4. Implement `Project.query.all()` → PASS
5. Refactor if needed

### Database Setup

**First Migration:**
```bash
cd backend
flask db init                    # Creates migrations/ directory
flask db migrate -m "Initial"    # Generates migration
flask db upgrade                 # Applies migration
```

**Subsequent Migrations:**
```bash
flask db migrate -m "Description"
flask db upgrade
```

### Testing Pattern

**Model Test Example:**
```python
def test_project_creation(app):
    project = Project(name="Test", path="/test")
    assert project.name == "Test"
    assert project.path == "/test"
    assert project.id is None  # Not committed yet
```

**API Test Example:**
```python
def test_get_projects_empty(client):
    response = client.get('/api/projects')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['projects'] == []
    assert data['total'] == 0
```

### curl Testing Commands

```bash
# List all projects
curl -s http://localhost:5000/api/projects | jq

# Get specific project
curl -s http://localhost:5000/api/projects/1 | jq

# Pretty print with python
curl -s http://localhost:5000/api/projects | python -m json.tool
```

---

## 🔗 Related Documents

- [Phase 0: Development Environment](phase-0.md)
- [Phase 2: Create & Update Projects](phase-2.md)
- [Feature Plan](feature-plan.md)
- [Projects Feature Hub](README.md)
- [ADR-0003: SQLite Database Design](../../../decisions/ADR-0003-sqlite-database-design.md)

---

**Last Updated:** 2025-12-02  
**Status:** 🔴 Not Started  
**Approach:** Backend-First API Development  
**Next:** Begin after Phase 0 complete
