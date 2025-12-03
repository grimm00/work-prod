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

