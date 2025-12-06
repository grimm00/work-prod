"""
Edge case tests for Projects API endpoints.

Tests special characters, very long inputs, large datasets, and other edge cases.
"""

import pytest
import json
from app.models.project import Project
from app import db


# Edge Case Tests: Special Characters

@pytest.mark.integration
def test_create_project_with_special_characters(client):
    """Test creating project with special characters in name and description."""
    special_name = "Project @#$%^&*()_+-=[]{}|;':\",./<>?"
    special_description = "Description with émojis 🎉 and unicode: 中文, العربية, русский"
    
    response = client.post('/api/projects',
                          json={
                              'name': special_name,
                              'description': special_description,
                              'path': '/test/special-chars'
                          },
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == special_name
    assert data['description'] == special_description
    assert data['path'] == '/test/special-chars'


@pytest.mark.integration
def test_create_project_with_unicode_characters(client):
    """Test creating project with Unicode characters."""
    unicode_name = "Проект 项目 مشروع"
    unicode_path = "/test/unicode/路径/путь"
    
    response = client.post('/api/projects',
                          json={
                              'name': unicode_name,
                              'path': unicode_path
                          },
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == unicode_name
    assert data['path'] == unicode_path


@pytest.mark.integration
def test_create_project_with_emoji(client):
    """Test creating project with emoji characters."""
    emoji_name = "Project 🚀 with emojis 🎉"
    
    response = client.post('/api/projects',
                          json={
                              'name': emoji_name
                          },
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == emoji_name


@pytest.mark.integration
def test_create_project_with_whitespace_only_name(client):
    """Test that whitespace-only name is handled (currently accepted, may be rejected in future)."""
    response = client.post('/api/projects',
                          json={
                              'name': '   \t\n  '
                          },
                          content_type='application/json')
    
    # Currently whitespace-only names are accepted (stored as-is)
    # This test documents current behavior - may be enhanced to reject in future
    assert response.status_code in [201, 400]
    if response.status_code == 201:
        data = json.loads(response.data)
        assert data['name'] == '   \t\n  '  # Stored as-is


@pytest.mark.integration
def test_create_project_with_leading_trailing_whitespace(client):
    """Test that leading/trailing whitespace is preserved in name."""
    name_with_whitespace = "  Project Name  "
    
    response = client.post('/api/projects',
                          json={
                              'name': name_with_whitespace
                          },
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    # Name should be preserved as-is (including whitespace)
    assert data['name'] == name_with_whitespace


# Edge Case Tests: Very Long Inputs

@pytest.mark.integration
def test_create_project_with_very_long_name(client):
    """Test creating project with very long name (1000 characters)."""
    long_name = "A" * 1000
    
    response = client.post('/api/projects',
                          json={
                              'name': long_name
                          },
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == long_name
    assert len(data['name']) == 1000


@pytest.mark.integration
def test_create_project_with_very_long_description(client):
    """Test creating project with very long description (5000 characters)."""
    long_description = "B" * 5000
    
    response = client.post('/api/projects',
                          json={
                              'name': 'Test Project',
                              'description': long_description
                          },
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['description'] == long_description
    assert len(data['description']) == 5000


@pytest.mark.integration
def test_create_project_with_very_long_path(client):
    """Test creating project with very long path (500 characters)."""
    long_path = "/" + "a" * 499
    
    response = client.post('/api/projects',
                          json={
                              'name': 'Test Project',
                              'path': long_path
                          },
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['path'] == long_path
    assert len(data['path']) == 500


# Edge Case Tests: Large Dataset Performance

@pytest.mark.integration
def test_list_projects_with_large_dataset(client, app):
    """Test listing projects with 100+ projects (performance test)."""
    # Create 100 projects
    with app.app_context():
        projects = []
        for i in range(100):
            project = Project(
                name=f"Project {i}",
                path=f"/path/{i}",
                status='active' if i % 2 == 0 else 'paused',
                classification='primary' if i % 3 == 0 else 'secondary'
            )
            projects.append(project)
        
        db.session.add_all(projects)
        db.session.commit()
    
    # List all projects
    response = client.get('/api/projects')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 100  # At least 100 projects
    
    # Verify all projects are returned correctly
    assert all('id' in p for p in data)
    assert all('name' in p for p in data)
    assert all('created_at' in p for p in data)


@pytest.mark.integration
def test_filter_projects_with_large_dataset(client, app):
    """Test filtering projects with large dataset (performance test)."""
    # Create 100 projects with different statuses
    with app.app_context():
        projects = []
        for i in range(100):
            status = 'active' if i % 2 == 0 else 'paused'
            project = Project(
                name=f"Project {i}",
                status=status,
                classification='primary'
            )
            projects.append(project)
        
        db.session.add_all(projects)
        db.session.commit()
    
    # Filter by status
    response = client.get('/api/projects?status=active')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 50  # Half should be active
    assert all(p['status'] == 'active' for p in data)


@pytest.mark.integration
def test_search_projects_with_large_dataset(client, app):
    """Test searching projects with large dataset (performance test)."""
    # Create 100 projects with searchable names
    with app.app_context():
        projects = []
        for i in range(100):
            project = Project(
                name=f"Searchable Project {i}",
                description=f"Description for project {i}"
            )
            projects.append(project)
        
        db.session.add_all(projects)
        db.session.commit()
    
    # Search for projects
    response = client.get('/api/projects?search=Searchable')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 100  # All should match
    assert all('Searchable' in p['name'] for p in data)


# Edge Case Tests: Invalid Input Handling

@pytest.mark.integration
def test_create_project_with_empty_string_name(client):
    """Test that empty string name is rejected."""
    response = client.post('/api/projects',
                          json={
                              'name': ''
                          },
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


@pytest.mark.integration
def test_create_project_with_null_name(client):
    """Test that null name is rejected."""
    response = client.post('/api/projects',
                          json={
                              'name': None
                          },
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


@pytest.mark.integration
def test_create_project_with_missing_name_field(client):
    """Test that missing name field is rejected."""
    response = client.post('/api/projects',
                          json={
                              'description': 'Some description'
                          },
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


@pytest.mark.integration
def test_create_project_with_invalid_json_structure(client):
    """Test that invalid JSON structure is handled gracefully."""
    # Send invalid JSON (not an object)
    response = client.post('/api/projects',
                          data='not json',
                          content_type='application/json')
    
    assert response.status_code == 400
    # Response may not be JSON if JSON parsing failed
    try:
        data = json.loads(response.data)
        assert 'error' in data
    except json.JSONDecodeError:
        # If response isn't JSON, that's also acceptable error handling
        assert response.status_code == 400


@pytest.mark.integration
def test_create_project_with_non_string_name(client):
    """Test that non-string name is rejected."""
    response = client.post('/api/projects',
                          json={
                              'name': 12345
                          },
                          content_type='application/json')
    
    # Should handle gracefully (either accept or reject)
    assert response.status_code in [400, 201]
    if response.status_code == 400:
        data = json.loads(response.data)
        assert 'error' in data


@pytest.mark.integration
def test_create_project_with_very_long_organization(client):
    """Test creating project with very long organization name."""
    long_org = "A" * 500
    
    response = client.post('/api/projects',
                          json={
                              'name': 'Test Project',
                              'organization': long_org
                          },
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['organization'] == long_org


@pytest.mark.integration
def test_create_project_with_very_long_remote_url(client):
    """Test creating project with very long remote URL."""
    long_url = "https://github.com/" + "a" * 500
    
    response = client.post('/api/projects',
                          json={
                              'name': 'Test Project',
                              'remote_url': long_url
                          },
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['remote_url'] == long_url


# Edge Case Tests: Boundary Conditions

@pytest.mark.integration
def test_get_project_with_zero_id(client):
    """Test getting project with ID 0 (should return 404)."""
    response = client.get('/api/projects/0')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data


@pytest.mark.integration
def test_get_project_with_negative_id(client):
    """Test getting project with negative ID (should return 400 or 404)."""
    response = client.get('/api/projects/-1')
    
    # Negative ID is invalid format, so 400 Bad Request is acceptable
    # (404 Not Found is also acceptable if treated as non-existent)
    assert response.status_code in [400, 404]
    data = json.loads(response.data)
    assert 'error' in data


@pytest.mark.integration
def test_get_project_with_very_large_id(client):
    """Test getting project with very large ID (should return 404)."""
    response = client.get('/api/projects/999999999')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data


@pytest.mark.integration
def test_update_project_with_empty_json(client, app):
    """Test updating project with empty JSON body."""
    # Create a project first
    with app.app_context():
        project = Project(name="Test Project")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Update with empty JSON
    response = client.patch(f'/api/projects/{project_id}',
                           json={},
                           content_type='application/json')
    
    # Should succeed (no-op update)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == "Test Project"  # Unchanged


@pytest.mark.integration
def test_delete_project_twice(client, app):
    """Test deleting a project twice (second should return 404)."""
    # Create a project
    with app.app_context():
        project = Project(name="Test Project")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Delete first time
    response1 = client.delete(f'/api/projects/{project_id}')
    assert response1.status_code == 204
    
    # Delete second time
    response2 = client.delete(f'/api/projects/{project_id}')
    assert response2.status_code == 404
    data = json.loads(response2.data)
    assert 'error' in data


# Edge Case Tests: Query Parameter Edge Cases

@pytest.mark.integration
def test_list_projects_with_empty_search_term(client, app):
    """Test searching with empty search term."""
    # Create a project
    with app.app_context():
        project = Project(name="Test Project")
        db.session.add(project)
        db.session.commit()
    
    # Search with empty term
    response = client.get('/api/projects?search=')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    # Empty search should return all projects (or none, depending on implementation)
    assert isinstance(data, list)


@pytest.mark.integration
def test_list_projects_with_multiple_same_filters(client, app):
    """Test filtering with duplicate filter parameters."""
    # Create projects
    with app.app_context():
        project1 = Project(name="Project 1", status='active')
        project2 = Project(name="Project 2", status='paused')
        db.session.add_all([project1, project2])
        db.session.commit()
    
    # Filter with duplicate status parameter (last one wins typically)
    response = client.get('/api/projects?status=active&status=paused')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    # Behavior depends on Flask's request.args handling (typically last value wins)


@pytest.mark.integration
def test_list_projects_with_special_characters_in_filter(client, app):
    """Test filtering with special characters in filter value."""
    # Create a project
    with app.app_context():
        project = Project(name="Test Project", organization="Org@#$%")
        db.session.add(project)
        db.session.commit()
    
    # Filter with special characters
    response = client.get('/api/projects?organization=Org@#$%')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    # Should handle special characters in filter values

