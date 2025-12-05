"""
Integration tests for Projects API endpoints.

Tests the /api/projects endpoints including list and get operations.
"""

import pytest
import json
from app.models.project import Project
from app import db


@pytest.mark.integration
def test_list_projects_empty(client):
    """Test GET /api/projects returns empty list when no projects exist."""
    response = client.get('/api/projects')
    
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0


@pytest.mark.integration
def test_list_projects_with_data(client, app):
    """Test GET /api/projects returns all projects."""
    # Create test projects
    with app.app_context():
        project1 = Project(name="Project 1", path="/path/1")
        project2 = Project(name="Project 2", path="/path/2")
        project3 = Project(name="Project 3")  # No path
        
        db.session.add_all([project1, project2, project3])
        db.session.commit()
    
    response = client.get('/api/projects')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert isinstance(data, list)
    assert len(data) == 3
    
    # Check first project structure
    assert 'id' in data[0]
    assert 'name' in data[0]
    assert 'path' in data[0]
    assert 'created_at' in data[0]
    assert 'updated_at' in data[0]
    
    # Check project with no path is serialized with path=None (null in JSON)
    project_without_path = next((p for p in data if p.get("name") == "Project 3"), None)
    assert project_without_path is not None
    assert "path" in project_without_path
    assert project_without_path["path"] is None


@pytest.mark.integration
def test_get_project_by_id(client, app):
    """Test GET /api/projects/<id> returns specific project."""
    # Create test project
    with app.app_context():
        project = Project(name="Test Project", path="/test/path")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    response = client.get(f'/api/projects/{project_id}')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['id'] == project_id
    assert data['name'] == "Test Project"
    assert data['path'] == "/test/path"
    assert 'created_at' in data
    assert 'updated_at' in data


@pytest.mark.integration
def test_get_project_not_found(client):
    """Test GET /api/projects/<id> returns 404 for non-existent project."""
    response = client.get('/api/projects/99999')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    
    assert 'error' in data
    assert 'not found' in data['error'].lower()


@pytest.mark.integration
def test_get_project_invalid_id(client):
    """Test GET /api/projects/<id> returns 400 for invalid ID format."""
    response = client.get('/api/projects/invalid')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    
    assert 'error' in data


@pytest.mark.integration
def test_list_projects_ordering(client, app):
    """Test that projects are returned in consistent order (by ID)."""
    # Create test projects
    with app.app_context():
        project1 = Project(name="Project 1", path="/path/1")
        project2 = Project(name="Project 2", path="/path/2")
        project3 = Project(name="Project 3", path="/path/3")
        project4 = Project(name="Project 4", path="/path/4")
        project5 = Project(name="Project 5", path="/path/5")
        db.session.add_all([project1, project2, project3, project4, project5])
        db.session.commit()
        # Capture IDs before context exits
        project_ids = [project1.id, project2.id, project3.id, project4.id, project5.id]
    
    response = client.get('/api/projects')
    data = json.loads(response.data)
    
    # Check that IDs are in ascending order
    ids = [p['id'] for p in data]
    assert ids == sorted(ids)
    
    # Verify ordering matches created projects (more robust assertion)
    returned_ids = [p['id'] for p in data if p['id'] in project_ids]
    assert returned_ids == sorted(returned_ids)
    assert len(returned_ids) == 5  # All 5 projects should be returned


# POST /api/projects tests (Phase 2)


@pytest.mark.integration
def test_create_project_minimal(client):
    """Test POST /api/projects with minimal data (name only)."""
    response = client.post('/api/projects', 
                          json={'name': 'New Project'},
                          content_type='application/json')
    
    assert response.status_code == 201
    assert 'Location' in response.headers
    
    data = json.loads(response.data)
    assert data['name'] == 'New Project'
    assert data['status'] == 'active'  # Default status
    assert 'id' in data
    assert data['id'] is not None


@pytest.mark.integration
def test_create_project_full_data(client):
    """Test POST /api/projects with all fields."""
    project_data = {
        'name': 'Full Project',
        'path': '/full/path',
        'organization': 'work',
        'classification': 'primary',
        'status': 'active',
        'description': 'A complete project',
        'remote_url': 'https://github.com/user/repo'
    }
    
    response = client.post('/api/projects',
                          json=project_data,
                          content_type='application/json')
    
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert data['name'] == 'Full Project'
    assert data['path'] == '/full/path'
    assert data['organization'] == 'work'
    assert data['classification'] == 'primary'
    assert data['status'] == 'active'
    assert data['description'] == 'A complete project'
    assert data['remote_url'] == 'https://github.com/user/repo'


@pytest.mark.integration
def test_create_project_location_header(client):
    """Test that POST returns correct Location header."""
    response = client.post('/api/projects',
                          json={'name': 'Test Project'},
                          content_type='application/json')
    
    assert response.status_code == 201
    assert 'Location' in response.headers
    
    data = json.loads(response.data)
    project_id = data['id']
    
    # Location header should point to the new resource
    assert f'/api/projects/{project_id}' in response.headers['Location']


@pytest.mark.integration
def test_create_project_missing_name(client):
    """Test POST /api/projects without name returns 400."""
    response = client.post('/api/projects',
                          json={'path': '/some/path'},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Name is required'


@pytest.mark.integration
def test_create_project_invalid_classification(client):
    """Test POST /api/projects with invalid classification returns 400."""
    response = client.post('/api/projects',
                          json={
                              'name': 'Test Project',
                              'classification': 'invalid_type'
                          },
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


@pytest.mark.integration
def test_create_project_invalid_status(client):
    """Test POST /api/projects with invalid status returns 400."""
    response = client.post('/api/projects',
                          json={
                              'name': 'Test Project',
                              'status': 'invalid_status'
                          },
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


@pytest.mark.integration
def test_create_project_duplicate_path(client, app):
    """Test POST /api/projects with duplicate path returns 409."""
    # Create first project
    with app.app_context():
        project = Project(name="Existing Project", path="/duplicate/path")
        db.session.add(project)
        db.session.commit()
    
    # Try to create second project with same path
    response = client.post('/api/projects',
                          json={
                              'name': 'New Project',
                              'path': '/duplicate/path'
                          },
                          content_type='application/json')
    
    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'error' in data


@pytest.mark.integration
def test_create_project_appears_in_list(client):
    """Test that created project appears in GET /api/projects."""
    # Create project via POST
    response = client.post('/api/projects',
                          json={'name': 'Listed Project'},
                          content_type='application/json')
    
    assert response.status_code == 201
    created_data = json.loads(response.data)
    project_id = created_data['id']
    
    # Verify it appears in list
    response = client.get('/api/projects')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    project_ids = [p['id'] for p in data]
    assert project_id in project_ids


# PATCH /api/projects/<id> tests (Phase 2)


@pytest.mark.integration
def test_update_project_single_field(client, app):
    """Test PATCH /api/projects/<id> updates single field."""
    # Create project
    with app.app_context():
        project = Project(name="Original Name", status="active")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Update only status
    response = client.patch(f'/api/projects/{project_id}',
                           json={'status': 'completed'},
                           content_type='application/json')
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'completed'
    assert data['name'] == 'Original Name'  # Unchanged


@pytest.mark.integration
def test_update_project_multiple_fields(client, app):
    """Test PATCH /api/projects/<id> updates multiple fields."""
    # Create project
    with app.app_context():
        project = Project(name="Test Project")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Update multiple fields
    updates = {
        'name': 'Updated Name',
        'organization': 'work',
        'classification': 'primary',
        'status': 'active',
        'description': 'Updated description'
    }
    
    response = client.patch(f'/api/projects/{project_id}',
                           json=updates,
                           content_type='application/json')
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['name'] == 'Updated Name'
    assert data['organization'] == 'work'
    assert data['classification'] == 'primary'
    assert data['status'] == 'active'
    assert data['description'] == 'Updated description'


@pytest.mark.integration
def test_update_project_idempotent(client, app):
    """Test PATCH /api/projects/<id> with no changes succeeds."""
    # Create project
    with app.app_context():
        project = Project(name="Test Project", status="active")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Update with same values
    response = client.patch(f'/api/projects/{project_id}',
                           json={},
                           content_type='application/json')
    
    assert response.status_code == 200


@pytest.mark.integration
def test_update_project_invalid_classification(client, app):
    """Test PATCH /api/projects/<id> with invalid classification returns 400."""
    # Create project
    with app.app_context():
        project = Project(name="Test Project")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Try invalid classification
    response = client.patch(f'/api/projects/{project_id}',
                           json={'classification': 'invalid_type'},
                           content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


@pytest.mark.integration
def test_update_project_invalid_status(client, app):
    """Test PATCH /api/projects/<id> with invalid status returns 400."""
    # Create project
    with app.app_context():
        project = Project(name="Test Project")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Try invalid status
    response = client.patch(f'/api/projects/{project_id}',
                           json={'status': 'invalid_status'},
                           content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


@pytest.mark.integration
def test_update_project_not_found(client):
    """Test PATCH /api/projects/<id> returns 404 for non-existent project."""
    response = client.patch('/api/projects/99999',
                           json={'status': 'active'},
                           content_type='application/json')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data


@pytest.mark.integration
def test_update_project_duplicate_path(client, app):
    """Test PATCH /api/projects/<id> prevents duplicate path."""
    # Create two projects
    with app.app_context():
        project1 = Project(name="Project 1", path="/path/1")
        project2 = Project(name="Project 2", path="/path/2")
        db.session.add_all([project1, project2])
        db.session.commit()
        project2_id = project2.id
    
    # Try to update project2's path to project1's path
    response = client.patch(f'/api/projects/{project2_id}',
                           json={'path': '/path/1'},
                           content_type='application/json')
    
    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'error' in data


# Security and Validation Fix Tests (PR08-#1, PR08-#2)

@pytest.mark.integration
def test_create_project_null_status_rejected(client):
    """Test that POST with null status returns 400 (PR08-#2)."""
    response = client.post('/api/projects',
                          json={'name': 'Test Project', 'status': None},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Status cannot be null'


@pytest.mark.integration
def test_update_project_null_status_rejected(client, app):
    """Test that PATCH with null status returns 400 (PR08-#2)."""
    # Create a project first
    with app.app_context():
        project = Project(name="Test Project", status="active")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Try to update with null status
    response = client.patch(f'/api/projects/{project_id}',
                           json={'status': None},
                           content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Status cannot be null'


@pytest.mark.integration
def test_create_project_exception_not_leaked(client, app, monkeypatch):
    """Test that unexpected exceptions return generic 500 message (PR08-#1)."""
    # Mock db.session.commit to raise an unexpected exception
    original_commit = db.session.commit
    
    def mock_commit():
        # Simulate an unexpected error that's not IntegrityError
        raise RuntimeError("Database connection lost - internal error details")
    
    monkeypatch.setattr(db.session, 'commit', mock_commit)
    
    response = client.post('/api/projects',
                          json={'name': 'Test Project'},
                          content_type='application/json')
    
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data['error'] == 'Internal server error'
    # Verify internal details are NOT exposed
    assert 'RuntimeError' not in data['error']
    assert 'Database connection' not in data['error']
    assert 'internal error details' not in data['error']
    
    # Restore original commit
    monkeypatch.setattr(db.session, 'commit', original_commit)


@pytest.mark.integration
def test_update_project_exception_not_leaked(client, app, monkeypatch):
    """Test that unexpected exceptions return generic 500 message in PATCH (PR08-#1)."""
    # Create a project first
    with app.app_context():
        project = Project(name="Test Project")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Mock db.session.commit to raise an unexpected exception
    original_commit = db.session.commit
    
    def mock_commit():
        raise RuntimeError("SQL injection detected - internal security error")
    
    monkeypatch.setattr(db.session, 'commit', mock_commit)
    
    response = client.patch(f'/api/projects/{project_id}',
                           json={'name': 'Updated Name'},
                           content_type='application/json')
    
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data['error'] == 'Internal server error'
    # Verify internal details are NOT exposed
    assert 'RuntimeError' not in data['error']
    assert 'SQL injection' not in data['error']
    assert 'security error' not in data['error']
    
    # Restore original commit
    monkeypatch.setattr(db.session, 'commit', original_commit)


# Phase 3: Delete & Archive Tests

@pytest.mark.integration
def test_delete_project_returns_204(client, app):
    """Test DELETE /api/projects/<id> returns 204 No Content."""
    # Create a project first
    with app.app_context():
        project = Project(name="Test Project", path="/test/delete")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Delete the project
    response = client.delete(f'/api/projects/{project_id}')
    
    assert response.status_code == 204
    assert len(response.data) == 0  # No content body


@pytest.mark.integration
def test_delete_project_removes_from_database(client, app):
    """Test DELETE removes project from database."""
    # Create a project first
    with app.app_context():
        project = Project(name="Test Project", path="/test/delete")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
        
        # Verify project exists
        assert Project.query.get(project_id) is not None
    
    # Delete the project
    response = client.delete(f'/api/projects/{project_id}')
    assert response.status_code == 204
    
    # Verify project no longer exists
    with app.app_context():
        assert Project.query.get(project_id) is None


@pytest.mark.integration
def test_delete_nonexistent_project_returns_404(client):
    """Test DELETE on non-existent project returns 404."""
    response = client.delete('/api/projects/9999')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data


@pytest.mark.integration
def test_project_cannot_be_retrieved_after_deletion(client, app):
    """Test project cannot be retrieved after deletion."""
    # Create a project first
    with app.app_context():
        project = Project(name="Test Project", path="/test/delete")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Verify project can be retrieved before deletion
    response = client.get(f'/api/projects/{project_id}')
    assert response.status_code == 200
    
    # Delete the project
    response = client.delete(f'/api/projects/{project_id}')
    assert response.status_code == 204
    
    # Verify project cannot be retrieved after deletion
    response = client.get(f'/api/projects/{project_id}')
    assert response.status_code == 404


@pytest.mark.integration
def test_archive_project_sets_classification_and_status(client, app):
    """Test archiving sets classification to 'archive' and status to 'completed'."""
    # Create a project first
    with app.app_context():
        project = Project(name="Test Project", classification="primary", status="active")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Archive the project
    response = client.put(f'/api/projects/{project_id}/archive',
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Verify classification and status updated
    assert data['classification'] == 'archive'
    assert data['status'] == 'completed'
    
    # Verify project still exists in database
    with app.app_context():
        archived_project = Project.query.get(project_id)
        assert archived_project is not None
        # Handle both Enum objects and string values from SQLAlchemy
        classification_value = archived_project.classification.value if hasattr(archived_project.classification, 'value') else archived_project.classification
        status_value = archived_project.status.value if hasattr(archived_project.status, 'value') else archived_project.status
        assert classification_value == 'archive'
        assert status_value == 'completed'


@pytest.mark.integration
def test_archive_project_still_appears_in_list(client, app):
    """Test archived projects still appear in list."""
    # Create a project first
    with app.app_context():
        project = Project(name="Test Project", classification="primary", status="active")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Archive the project
    response = client.put(f'/api/projects/{project_id}/archive',
                         content_type='application/json')
    assert response.status_code == 200
    
    # Get list of projects
    response = client.get('/api/projects')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    project_ids = [p['id'] for p in data]
    
    # Verify archived project appears in list
    assert project_id in project_ids


@pytest.mark.integration
def test_archive_nonexistent_project_returns_404(client):
    """Test archiving non-existent project returns 404."""
    response = client.put('/api/projects/9999/archive',
                         content_type='application/json')
    
    assert response.status_code == 404
    # Route doesn't exist yet, so response may not be JSON in RED phase
    # Once implemented, this will return JSON with error message


# Phase 4: Search & Filter Tests

@pytest.mark.integration
def test_filter_projects_by_status(client, app):
    """Test GET /api/projects?status=active filters by status."""
    # Create projects with different statuses
    with app.app_context():
        active_project = Project(name="Active Project", status="active")
        paused_project = Project(name="Paused Project", status="paused")
        completed_project = Project(name="Completed Project", status="completed")
        
        db.session.add_all([active_project, paused_project, completed_project])
        db.session.commit()
    
    # Filter by active status
    response = client.get('/api/projects?status=active')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['name'] == "Active Project"
    assert data[0]['status'] == 'active'


@pytest.mark.integration
def test_filter_projects_by_organization(client, app):
    """Test GET /api/projects?organization=work filters by organization."""
    # Create projects with different organizations
    with app.app_context():
        work_project = Project(name="Work Project", organization="work")
        personal_project = Project(name="Personal Project", organization="personal")
        work_project2 = Project(name="Another Work Project", organization="work")
        
        db.session.add_all([work_project, personal_project, work_project2])
        db.session.commit()
    
    # Filter by work organization
    response = client.get('/api/projects?organization=work')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert isinstance(data, list)
    assert len(data) == 2
    assert all(p['organization'] == 'work' for p in data)


@pytest.mark.integration
def test_filter_projects_by_classification(client, app):
    """Test GET /api/projects?classification=primary filters by classification."""
    # Create projects with different classifications
    with app.app_context():
        primary_project = Project(name="Primary Project", classification="primary")
        secondary_project = Project(name="Secondary Project", classification="secondary")
        archive_project = Project(name="Archive Project", classification="archive")
        
        db.session.add_all([primary_project, secondary_project, archive_project])
        db.session.commit()
    
    # Filter by primary classification
    response = client.get('/api/projects?classification=primary')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['name'] == "Primary Project"
    assert data[0]['classification'] == 'primary'


@pytest.mark.integration
def test_filter_projects_multiple_filters(client, app):
    """Test GET /api/projects?status=active&organization=work combines filters."""
    # Create projects with various combinations
    with app.app_context():
        # Matches both filters
        match1 = Project(name="Match 1", status="active", organization="work")
        match2 = Project(name="Match 2", status="active", organization="work")
        # Matches status only
        status_only = Project(name="Status Only", status="active", organization="personal")
        # Matches organization only
        org_only = Project(name="Org Only", status="paused", organization="work")
        # Matches neither
        neither = Project(name="Neither", status="paused", organization="personal")
        
        db.session.add_all([match1, match2, status_only, org_only, neither])
        db.session.commit()
    
    # Filter by both status and organization
    response = client.get('/api/projects?status=active&organization=work')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert isinstance(data, list)
    assert len(data) == 2
    assert all(p['status'] == 'active' and p['organization'] == 'work' for p in data)
    assert all(p['name'] in ['Match 1', 'Match 2'] for p in data)


@pytest.mark.integration
def test_filter_projects_invalid_status_value_ignored(client, app):
    """Test GET /api/projects?status=invalid ignores invalid filter and returns all projects."""
    # Create some projects
    with app.app_context():
        project1 = Project(name="Project 1", status="active")
        project2 = Project(name="Project 2", status="paused")
        db.session.add_all([project1, project2])
        db.session.commit()
        project1_id = project1.id
        project2_id = project2.id
    
    # Try to filter by invalid status
    response = client.get('/api/projects?status=invalid')
    
    # Invalid status values are ignored, so all projects should be returned
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    
    # Verify that the returned projects are exactly the ones created in this test
    returned_ids = {project["id"] for project in data}
    assert returned_ids == {project1_id, project2_id}


@pytest.mark.integration
def test_filter_projects_invalid_classification_value_ignored(client, app):
    """Test GET /api/projects?classification=invalid ignores invalid filter and returns all projects."""
    # Create some projects
    with app.app_context():
        project1 = Project(name="Project 1", classification="primary")
        project2 = Project(name="Project 2", classification="secondary")
        db.session.add_all([project1, project2])
        db.session.commit()
        project1_id = project1.id
        project2_id = project2.id
    
    # Try to filter by invalid classification
    response = client.get('/api/projects?classification=invalid')
    
    # Invalid classification values are ignored, so all projects should be returned
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    
    # Verify that the returned projects are exactly the ones created in this test
    returned_ids = {project["id"] for project in data}
    assert returned_ids == {project1_id, project2_id}


# Phase 4: Search Tests

@pytest.mark.integration
def test_search_projects_by_name(client, app):
    """Test GET /api/projects?search=term searches project names."""
    # Create projects with different names
    with app.app_context():
        work_project = Project(name="Work Productivity Tool", description="A tool for work")
        personal_project = Project(name="Personal Blog", description="My personal blog")
        work_project2 = Project(name="Work Tracker", description="Track work hours")
        
        db.session.add_all([work_project, personal_project, work_project2])
        db.session.commit()
    
    # Search for "work" in names
    response = client.get('/api/projects?search=work')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert isinstance(data, list)
    assert len(data) == 2
    assert all('work' in p['name'].lower() for p in data)


@pytest.mark.integration
def test_search_projects_case_insensitive(client, app):
    """Test search is case-insensitive."""
    # Create projects
    with app.app_context():
        project1 = Project(name="Productivity Tool", description="A tool")
        project2 = Project(name="PRODUCTIVITY APP", description="An app")
        project3 = Project(name="Productivity System", description="A system")
        
        db.session.add_all([project1, project2, project3])
        db.session.commit()
    
    # Search with different cases
    response = client.get('/api/projects?search=PRODUCTIVITY')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert isinstance(data, list)
    assert len(data) == 3
    assert all('productivity' in p['name'].lower() for p in data)


@pytest.mark.integration
def test_search_projects_partial_match(client, app):
    """Test search matches partial names."""
    # Create projects
    with app.app_context():
        project1 = Project(name="Productivity Tool", description="A tool")
        project2 = Project(name="Product Manager", description="Manager role")
        project3 = Project(name="Production System", description="A system")
        
        db.session.add_all([project1, project2, project3])
        db.session.commit()
    
    # Search for partial match "product"
    response = client.get('/api/projects?search=product')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert isinstance(data, list)
    assert len(data) == 3
    assert all('product' in p['name'].lower() for p in data)


@pytest.mark.integration
def test_search_projects_in_description(client, app):
    """Test search matches description field."""
    # Create projects
    with app.app_context():
        project1 = Project(name="Project A", description="A productivity tool for work")
        project2 = Project(name="Project B", description="A personal blog")
        project3 = Project(name="Project C", description="Work tracking system")
        
        db.session.add_all([project1, project2, project3])
        db.session.commit()
    
    # Search for "work" in descriptions
    response = client.get('/api/projects?search=work')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert isinstance(data, list)
    assert len(data) == 2
    # Should match projects with "work" in name or description
    assert any('work' in p.get('description', '').lower() or 'work' in p['name'].lower() for p in data)

