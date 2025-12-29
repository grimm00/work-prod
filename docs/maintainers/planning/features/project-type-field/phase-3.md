# Project Type Field - Phase 3: API Updates

**Feature:** Add `project_type` field  
**Phase:** 3 of 3  
**Status:** 🟠 In Progress  
**Estimated Effort:** ~1.5 hours  
**Created:** 2025-12-23  
**Last Updated:** 2025-12-29  
**Dependencies:** Phase 2 complete  
**Review:** [Phase 3 Review](phase-3-review.md) - ✅ Addressed

---

## 📋 Phase Overview

Update API to support filtering by `project_type` and update all related documentation.

**Goal:** API fully supports `project_type` field for filtering and creation.

---

## 🎯 Phase Goals

- [ ] Add `project_type` query parameter to GET `/api/projects`
- [ ] Include `project_type` in API responses (already done in Phase 1 via `to_dict()`)
- [ ] Update OpenAPI specification
- [ ] Tests written before implementation (TDD)
- [ ] Maintain 97% test coverage

**Note:** Mapping script (`project_type` support) is handled separately in proj-cli's `project-type-support` feature.

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

## ✅ Phase Completion Criteria

- [ ] API filter tests written and passing
- [ ] API endpoint updated with filter
- [ ] OpenAPI spec updated
- [ ] All existing tests still pass
- [ ] Test coverage maintained at 97%
- [ ] Ready for PR

---

## 📊 Progress Tracking

| Task                                 | Status         | Notes   |
| ------------------------------------ | -------------- | ------- |
| Task 1: Write API Tests (RED)        | 🔴 Not Started | ~30 min |
| Task 2: Implement API Filter (GREEN) | 🔴 Not Started | ~45 min |
| Task 3: Update OpenAPI               | 🔴 Not Started | ~30 min |

**Total:** ~1.5 hours (3 tasks)

---

## 🚀 Post-Phase Actions

After Phase 3 completion:

1. Create PR for phase
2. **proj-cli:** Coordinate `project-type-support` feature for client update
   - Feature plan: `proj-cli/docs/maintainers/planning/features/project-type-support/`
   - Update `inventory.py` to include `project_type` in export
3. Update dev-infra requirements document (FR-2 complete)

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Transition Plan](transition-plan.md)
- [Phase 1: Schema Migration](phase-1.md)
- [Phase 2: Data Backfill](phase-2.md)
- [ADR-003](../../../../../dev-infra/admin/decisions/project-model-definition/adr-003-add-project-type-field.md)

---

**Last Updated:** 2025-12-29
