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
        for i in range(5):
            project = Project(name=f"Project {i}", path=f"/path/{i}")
            db.session.add(project)
        db.session.commit()
    
    response = client.get('/api/projects')
    data = json.loads(response.data)
    
    # Check that IDs are in ascending order
    ids = [p['id'] for p in data]
    assert ids == sorted(ids)


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
    assert 'name' in data['error'].lower()


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

