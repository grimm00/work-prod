# Projects Feature - Phase 2: Projects API - Create & Update

**Phase:** 2 - Projects API - Create & Update (Backend + CLI)  
**Duration:** 1 day  
**Status:** ✅ Complete  
**Completed:** 2025-12-03  
**Prerequisites:** Phase 1 complete

---

## 📋 Overview

Phase 2 extends the Projects API with create and update operations. This phase adds more fields to the Project model (organization, classification, status) and implements POST and PUT endpoints with validation. By the end, you can create and update projects via API and CLI.

**Success Definition:** Can create and update projects via curl/CLI with full validation working.

---

## 🎯 Goals

1. **Extended Project Model** - Add organization, classification, status, and other core fields
2. **POST /api/projects Endpoint** - Create new projects with validation
3. **PUT /api/projects/<id> Endpoint** - Update existing projects
4. **CLI Create/Update Commands** - `proj create` and `proj update`
5. **Complete Validation** - Server-side validation for all fields

---

## 📝 Tasks

### TDD Flow (Backend → CLI → Manual Testing)

#### 1. Write Model Extension Tests (TDD - RED)

- [ ] Test Project creation with extended fields:
  - `organization` (String - work/personal/learning)
  - `classification` (Enum - Primary/Secondary/Archive/Maintenance)
  - `status` (Enum - active/paused/completed/cancelled)
  - `description` (Text, nullable)
  - `remote_url` (String, nullable, for GitHub repos)
- [ ] Test enum validation (invalid classification rejects)
- [ ] Test field constraints (name max 200 chars)
- [ ] Test `to_dict()` includes new fields
- [ ] Run tests: **FAILS** ❌

#### 2. Extend Project Model (TDD - GREEN)

- [ ] Update `backend/app/models/project.py`:
  - Add `organization` String(100), nullable
  - Add `classification` Enum (primary/secondary/archive/maintenance)
  - Add `status` Enum (active/paused/completed/cancelled)
  - Add `description` Text, nullable
  - Add `remote_url` String(500), nullable
- [ ] Create migration: `flask db migrate -m "Extend project model with core fields"`
- [ ] Apply migration: `flask db upgrade`
- [ ] Update `to_dict()` to include new fields
- [ ] Run model tests: **PASSES** ✅

#### 3. Write POST Endpoint Tests (TDD - RED)

- [ ] Test POST /api/projects creates project (201 Created)
- [ ] Test response includes created project with ID
- [ ] Test Location header points to new resource
- [ ] Test validation errors return 400:
  - Missing required field (name)
  - Invalid classification value
  - Invalid status value
  - Name too long (> 200 chars)
- [ ] Test duplicate path returns 409 Conflict
- [ ] Run tests: **FAILS** ❌

#### 4. Implement POST Endpoint (TDD - GREEN)

- [ ] Add POST route to `backend/app/api/projects.py`:
  ```python
  @projects_bp.route('/projects', methods=['POST'])
  def create_project():
      data = request.get_json()
      
      # Validate required fields
      if not data.get('name'):
          return jsonify({'error': 'Name is required'}), 400
      
      # Check for duplicates
      if data.get('path'):
          existing = Project.query.filter_by(path=data['path']).first()
          if existing:
              return jsonify({'error': 'Project with this path already exists'}), 409
      
      # Create project
      project = Project(
          name=data['name'],
          path=data.get('path'),
          organization=data.get('organization'),
          classification=data.get('classification'),
          status=data.get('status', 'active'),
          description=data.get('description'),
          remote_url=data.get('remote_url')
      )
      
      db.session.add(project)
      db.session.commit()
      
      return jsonify(project.to_dict()), 201, {
          'Location': f'/api/projects/{project.id}'
      }
  ```
- [ ] Add request validation helper function
- [ ] Run POST tests: **PASSES** ✅

#### 5. Write PUT Endpoint Tests (TDD - RED)

- [ ] Test PUT /api/projects/<id> updates project (200 OK)
- [ ] Test response includes updated project
- [ ] Test partial updates (only provided fields change)
- [ ] Test validation on update
- [ ] Test 404 for non-existent project
- [ ] Test cannot update to duplicate path
- [ ] Run tests: **FAILS** ❌

#### 6. Implement PUT Endpoint (TDD - GREEN)

- [ ] Add PUT route to `backend/app/api/projects.py`:
  ```python
  @projects_bp.route('/projects/<int:project_id>', methods=['PUT'])
  def update_project(project_id):
      project = Project.query.get_or_404(project_id)
      data = request.get_json()
      
      # Update fields if provided
      if 'name' in data:
          project.name = data['name']
      if 'path' in data:
          project.path = data['path']
      if 'organization' in data:
          project.organization = data['organization']
      if 'classification' in data:
          project.classification = data['classification']
      if 'status' in data:
          project.status = data['status']
      if 'description' in data:
          project.description = data['description']
      if 'remote_url' in data:
          project.remote_url = data['remote_url']
      
      db.session.commit()
      return jsonify(project.to_dict()), 200
  ```
- [ ] Add validation for updates
- [ ] Run PUT tests: **PASSES** ✅

#### 7. Manual API Testing

- [ ] Test POST with curl:
  ```bash
  curl -X POST http://localhost:5000/api/projects \
    -H "Content-Type: application/json" \
    -d '{
      "name": "work-prod",
      "path": "/Users/cdwilson/Projects/work-prod",
      "organization": "work",
      "classification": "primary",
      "status": "active",
      "description": "Work productivity system"
    }'
  ```
- [ ] Test PUT with curl:
  ```bash
  curl -X PUT http://localhost:5000/api/projects/1 \
    -H "Content-Type: application/json" \
    -d '{"status": "completed"}'
  ```
- [ ] Test validation errors
- [ ] Test duplicate detection

#### 8. Enhance CLI Tool

- [ ] Update `scripts/project_cli/proj` with create command:
  ```python
  def create_project(name, **kwargs):
      data = {'name': name}
      data.update(kwargs)
      
      resp = requests.post(f"{API_BASE}/projects", json=data)
      if resp.status_code == 201:
          project = resp.json()
          print(f"✓ Created project #{project['id']}: {project['name']}")
      else:
          print(f"✗ Error: {resp.json().get('error', 'Unknown error')}")
  ```
- [ ] Add update command:
  ```python
  def update_project(project_id, **kwargs):
      resp = requests.put(f"{API_BASE}/projects/{project_id}", json=kwargs)
      if resp.status_code == 200:
          project = resp.json()
          print(f"✓ Updated project #{project_id}")
      else:
          print(f"✗ Error: {resp.json().get('error', 'Unknown error')}")
  ```
- [ ] Test CLI commands:
  ```bash
  ./proj create "My Project" --org work --status active
  ./proj update 1 --status completed
  ```

---

## ✅ Completion Criteria

- [ ] Project model extended with organization, classification, status fields
- [ ] Database migration applied
- [ ] POST /api/projects endpoint works with validation
- [ ] PUT /api/projects/<id> endpoint works
- [ ] Validation errors return appropriate status codes
- [ ] Duplicate detection works
- [ ] Backend tests pass (model + API POST/PUT)
- [ ] Can create projects via curl
- [ ] Can update projects via curl
- [ ] CLI `proj create` command works
- [ ] CLI `proj update` command works
- [ ] Coverage > 80% for new code

---

## 📦 Deliverables

1. **Backend Code**
   - Extended `backend/app/models/project.py` with new fields
   - POST /api/projects endpoint in `backend/app/api/projects.py`
   - PUT /api/projects/<id> endpoint
   - Database migration for new fields
   - Validation helpers

2. **Tests**
   - Extended model tests
   - POST endpoint tests
   - PUT endpoint tests
   - Validation tests

3. **CLI Tool**
   - Enhanced `scripts/project_cli/proj` with create/update
   - Updated README with new commands

4. **Documentation**
   - API documentation for POST /api/projects
   - API documentation for PUT /api/projects/<id>
   - Field validation rules documented

---

## 🔗 Dependencies

### Prerequisites

- ✅ Phase 1: List & Get Projects complete

### External Dependencies

- None

### Blocks

- Phase 3: Delete & Archive Projects

---

## ⚠️ Risks

**Risk: Validation Logic Complex**  
**Probability:** Medium  
**Impact:** Medium  
**Mitigation:** Start with simple validation, enhance iteratively  
**Contingency:** Can refactor validation to separate module

---

## 📊 Progress Tracking

**Phase Status:** 🔴 Not Started

**Backend (0/4 complete)**
- [ ] Model extended with new fields
- [ ] POST endpoint implemented
- [ ] PUT endpoint implemented
- [ ] Validation working

**Testing (0/2 complete)**
- [ ] All new tests passing
- [ ] Coverage > 80%

**CLI (0/2 complete)**
- [ ] create command working
- [ ] update command working

---

## 💡 Implementation Notes

### Field Descriptions

**organization:** work/personal/learning - helps filter projects by context

**classification:** 
- `primary`: Main active projects
- `secondary`: Supporting projects
- `archive`: Completed/historical
- `maintenance`: Ongoing maintenance

**status:**
- `active`: Currently working on
- `paused`: Temporarily on hold
- `completed`: Finished
- `cancelled`: Abandoned

### Validation Rules

- `name`: Required, 1-200 characters
- `path`: Optional, unique if provided
- `organization`: Optional, free text
- `classification`: Optional, one of valid enum values
- `status`: Optional, defaults to 'active', one of valid enum values
- `description`: Optional, free text
- `remote_url`: Optional, should be valid URL format

### curl Examples

```bash
# Create minimal project
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Project"}'

# Create full project
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "work-prod",
    "path": "/Users/cdwilson/Projects/work-prod",
    "organization": "work",
    "classification": "primary",
    "status": "active",
    "description": "Work productivity management system",
    "remote_url": "https://github.com/grimm00/work-prod"
  }' | jq

# Update project status
curl -X PUT http://localhost:5000/api/projects/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}' | jq

# Update multiple fields
curl -X PUT http://localhost:5000/api/projects/1 \
  -H "Content-Type: application/json" \
  -d '{
    "classification": "archive",
    "status": "completed",
    "description": "Project completed and archived"
  }' | jq
```

---

## 🔗 Related Documents

- [Phase 1: List & Get Projects](phase-1.md)
- [Phase 3: Delete & Archive Projects](phase-3.md)
- [Projects Data Model Research](../../../research/data-models/projects-data-model.md)
- [Feature Plan](feature-plan.md)
- [Manual Testing Guide](manual-testing.md) - Comprehensive testing scenarios for Phase 2

---

**Last Updated:** 2025-12-07  
**Status:** ✅ Complete  
**Completed:** 2025-12-03  
**Merged:** PR #8 (2025-12-04)  
**Approach:** Backend-First API Development
