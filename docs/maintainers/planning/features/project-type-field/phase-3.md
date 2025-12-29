# Project Type Field - Phase 3: API Updates

**Feature:** Add `project_type` field  
**Phase:** 3 of 3  
**Status:** 🔴 Not Started  
**Estimated Effort:** ~3 hours  
**Created:** 2025-12-23  
**Last Updated:** 2025-12-29  
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
- [ ] Tests written before implementation (TDD)

---

## 📝 Tasks

### Task 1: Write API Filter Tests (TDD - RED) (~30 min)

**File:** `backend/tests/integration/api/test_projects.py`

Write tests for filtering BEFORE implementing the filter:

```python
@pytest.mark.integration
def test_filter_projects_by_project_type_work(client, app):
    """Test filtering projects by project_type=Work."""
    # Arrange: Create projects with different types
    with app.app_context():
        work_project = Project(name="Work Project", project_type="Work")
        personal_project = Project(name="Personal Project", project_type="Personal")
        db.session.add_all([work_project, personal_project])
        db.session.commit()
    
    # Act
    response = client.get('/api/projects?project_type=Work')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['project_type'] == 'Work'


@pytest.mark.integration
def test_filter_projects_by_project_type_invalid(client):
    """Test invalid project_type returns 400."""
    response = client.get('/api/projects?project_type=InvalidType')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


@pytest.mark.integration
def test_filter_projects_by_multiple_types_combined_with_status(client, app):
    """Test filtering by project_type combined with status filter."""
    with app.app_context():
        active_work = Project(name="Active Work", project_type="Work", status="active")
        paused_work = Project(name="Paused Work", project_type="Work", status="paused")
        db.session.add_all([active_work, paused_work])
        db.session.commit()
    
    response = client.get('/api/projects?project_type=Work&status=active')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['status'] == 'active'


@pytest.mark.integration
def test_project_response_includes_project_type(client, app):
    """Test project response includes project_type field."""
    with app.app_context():
        project = Project(name="Test Project", project_type="Learning")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    response = client.get(f'/api/projects/{project_id}')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'project_type' in data
    assert data['project_type'] == 'Learning'
```

**Acceptance Criteria:**
- [ ] Filter by project_type test written
- [ ] Invalid project_type test written
- [ ] Combined filter test written
- [ ] Response includes project_type test written
- [ ] Tests fail initially (RED phase - filter not implemented yet)

---

### Task 2: Implement API Filter (TDD - GREEN) (~45 min)

**File:** `backend/app/api/projects.py`

Implement the filter to make tests pass:

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

**Acceptance Criteria:**
- [ ] Query parameter added
- [ ] Invalid values return 400
- [ ] Filter works correctly
- [ ] All tests pass (GREEN phase)

---

### Task 3: Update OpenAPI Specification (~30 min)

**File:** `backend/openapi.yaml`

**Note:** This is documentation - no TDD needed.

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

### Task 4: Write Mapping Script Tests (TDD - RED) (~30 min)

**File:** `scripts/tests/test_map_inventory.py`

Write tests for the determine_project_type function:

```python
"""Tests for map_inventory_to_projects script."""

import pytest


class TestDetermineProjectType:
    """Test determine_project_type function."""

    def test_drw_organization_returns_work(self):
        """DRW organization -> Work."""
        repo_data = {'organization': 'DRW', 'path': '/some/path', 'archived': False}
        result = determine_project_type(repo_data)
        assert result == 'Work'

    def test_learning_path_returns_learning(self):
        """/Learning/ in path -> Learning."""
        repo_data = {'organization': None, 'path': '/Users/me/Learning/python', 'archived': False}
        result = determine_project_type(repo_data)
        assert result == 'Learning'

    def test_archived_returns_inactive(self):
        """Archived repo -> Inactive."""
        repo_data = {'organization': None, 'path': '/some/path', 'archived': True}
        result = determine_project_type(repo_data)
        assert result == 'Inactive'

    def test_default_returns_personal(self):
        """No match -> Personal (default)."""
        repo_data = {'organization': None, 'path': '/some/path', 'archived': False}
        result = determine_project_type(repo_data)
        assert result == 'Personal'

    def test_drw_priority_over_learning(self):
        """DRW takes priority over Learning path."""
        repo_data = {'organization': 'DRW', 'path': '/Learning/project', 'archived': False}
        result = determine_project_type(repo_data)
        assert result == 'Work'
```

**Acceptance Criteria:**
- [ ] Tests for each heuristic
- [ ] Tests for priority ordering
- [ ] Tests fail initially (RED phase)

---

### Task 5: Update Mapping Script (TDD - GREEN) (~30 min)

**File:** `scripts/map_inventory_to_projects.py`

Implement to make tests pass:

```python
def determine_project_type(repo_data):
    """Determine project_type from repository data.
    
    Priority order:
    1. DRW organization -> Work
    2. /Learning/ in path -> Learning
    3. Archived -> Inactive
    4. Default -> Personal
    """
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

Include `project_type` in project creation:

```python
project_data = {
    # ... existing fields ...
    'project_type': determine_project_type(repo),
}
```

**Acceptance Criteria:**
- [ ] Function implemented with correct priority order
- [ ] project_type included in project data
- [ ] All tests pass (GREEN phase)

---

## ✅ Phase Completion Criteria

- [ ] API filter tests written and passing
- [ ] API endpoint updated with filter
- [ ] OpenAPI spec updated
- [ ] Mapping script tests written and passing
- [ ] Mapping script updated
- [ ] All existing tests still pass
- [ ] Ready for PR

---

## 📊 Progress Tracking

| Task | Status | Notes |
|------|--------|-------|
| Task 1: Write API Tests (RED) | 🔴 Not Started | |
| Task 2: Implement API Filter (GREEN) | 🔴 Not Started | |
| Task 3: Update OpenAPI | 🔴 Not Started | |
| Task 4: Write Mapping Tests (RED) | 🔴 Not Started | |
| Task 5: Update Mapping Script (GREEN) | 🔴 Not Started | |

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

**Last Updated:** 2025-12-29
