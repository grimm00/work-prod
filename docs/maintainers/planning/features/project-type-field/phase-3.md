# Project Type Field - Phase 3: API Updates

**Feature:** Add `project_type` field  
**Phase:** 3 of 3  
**Status:** 🔴 Not Started  
**Estimated Effort:** ~3 hours  
**Created:** 2025-12-23  
**Last Updated:** 2025-12-23  
**Dependencies:** Phase 2 complete

---

## 📋 Phase Overview

Update API to support filtering by `project_type` and update all related documentation.

**Goal:** API fully supports `project_type` field for filtering and creation.

---

## 🎯 Phase Goals

- [ ] Add `project_type` query parameter to GET `/api/projects`
- [ ] Include `project_type` in API responses
- [ ] Update OpenAPI specification
- [ ] Update mapping script to populate `project_type`
- [ ] Add/update tests

---

## 📝 Tasks

### Task 1: Update API Endpoint (~45 min)

**File:** `backend/app/api/projects.py`

**Changes:**

1. Add `project_type` to query parameters:

```python
@api_bp.route('/projects', methods=['GET'])
def get_projects():
    # ... existing code ...
    
    # Add project_type filter
    project_type = request.args.get('project_type')
    if project_type:
        valid_types = ['Work', 'Personal', 'Learning', 'Inactive']
        if project_type not in valid_types:
            return jsonify({'error': f"Invalid project_type. Must be one of: {valid_types}"}), 400
        query = query.filter(Project.project_type == project_type)
    
    # ... rest of code ...
```

2. Ensure `project_type` is included in serialization:

```python
def serialize_project(project):
    return {
        # ... existing fields ...
        'project_type': project.project_type,
    }
```

**Acceptance Criteria:**
- [ ] Query parameter added
- [ ] Invalid values return 400
- [ ] Filter works correctly
- [ ] Field included in response

---

### Task 2: Update OpenAPI Specification (~30 min)

**File:** `backend/openapi.yaml`

**Add to Project schema:**

```yaml
components:
  schemas:
    Project:
      type: object
      properties:
        # ... existing properties ...
        project_type:
          type: string
          enum: [Work, Personal, Learning, Inactive]
          nullable: true
          description: Type classification for the project
```

**Add to GET /projects parameters:**

```yaml
paths:
  /projects:
    get:
      parameters:
        # ... existing parameters ...
        - name: project_type
          in: query
          schema:
            type: string
            enum: [Work, Personal, Learning, Inactive]
          description: Filter projects by type
```

**Acceptance Criteria:**
- [ ] Schema updated with project_type field
- [ ] Query parameter documented
- [ ] Enum values documented

---

### Task 3: Update Mapping Script (~45 min)

**File:** `scripts/map_inventory_to_projects.py`

**Changes:**

1. Add `project_type` determination logic:

```python
def determine_project_type(repo_data):
    """Determine project_type from repository data."""
    # Check organization
    if repo_data.get('organization') == 'DRW':
        return 'Work'
    
    # Check path for Learning
    path = repo_data.get('path', '')
    if '/Learning/' in path:
        return 'Learning'
    
    # Check if archived
    if repo_data.get('archived', False):
        return 'Inactive'
    
    # Default to Personal
    return 'Personal'
```

2. Include `project_type` in project creation:

```python
project_data = {
    # ... existing fields ...
    'project_type': determine_project_type(repo),
}
```

**Acceptance Criteria:**
- [ ] Function added to determine project_type
- [ ] project_type included in project data
- [ ] Same heuristics as backfill script

---

### Task 4: Add/Update Tests (~60 min)

**Files:**
- `backend/tests/integration/api/test_projects.py`
- `backend/tests/unit/models/test_project.py`

**Test Cases:**

1. **API Filter Tests:**
```python
def test_filter_projects_by_type_work(client):
    """Test filtering projects by project_type=Work."""
    response = client.get('/api/projects?project_type=Work')
    assert response.status_code == 200
    data = json.loads(response.data)
    for project in data['projects']:
        assert project['project_type'] == 'Work'

def test_filter_projects_by_type_invalid(client):
    """Test invalid project_type returns 400."""
    response = client.get('/api/projects?project_type=Invalid')
    assert response.status_code == 400
```

2. **Serialization Tests:**
```python
def test_project_response_includes_project_type(client):
    """Test project response includes project_type field."""
    response = client.get('/api/projects/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'project_type' in data
```

**Acceptance Criteria:**
- [ ] Filter tests added
- [ ] Invalid value test added
- [ ] Serialization test added
- [ ] All tests pass

---

## ✅ Phase Completion Criteria

- [ ] API endpoint updated with filter
- [ ] OpenAPI spec updated
- [ ] Mapping script updated
- [ ] Tests added and passing
- [ ] All existing tests still pass
- [ ] Ready for PR

---

## 🚀 Post-Phase Actions

After Phase 3 completion:
1. Create PR for feature
2. Coordinate with proj-cli for client update
3. Update dev-infra requirements document

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Transition Plan](transition-plan.md)
- [Phase 1: Schema Migration](phase-1.md)
- [Phase 2: Data Backfill](phase-2.md)
- [ADR-003](../../../../../dev-infra/admin/decisions/project-model-definition/adr-003-add-project-type-field.md)

---

**Last Updated:** 2025-12-23

