"""
Integration tests for Projects API import endpoint.

Tests the POST /api/projects/import endpoint for bulk importing projects.
"""

import pytest
import json
from app.models.project import Project
from app import db


@pytest.mark.integration
def test_import_single_project(client):
    """Test importing a single project from JSON."""
    import_data = {
        'projects': [
            {
                'name': 'Test Project',
                'path': '/test/path',
                'organization': 'Test Org',
                'classification': 'primary',
                'status': 'active',
                'description': 'A test project',
                'remote_url': 'https://github.com/test/test-project'
            }
        ]
    }
    
    response = client.post(
        '/api/projects/import',
        data=json.dumps(import_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    assert 'imported' in data
    assert 'skipped' in data
    assert 'errors' in data
    assert data['imported'] == 1
    assert data['skipped'] == 0
    assert len(data['errors']) == 0
    
    # Verify project was created
    project = Project.query.filter_by(name='Test Project').first()
    assert project is not None
    assert project.path == '/test/path'
    assert project.organization == 'Test Org'
    assert project.classification == 'primary'
    assert project.status == 'active'
    assert project.description == 'A test project'
    assert project.remote_url == 'https://github.com/test/test-project'


@pytest.mark.integration
def test_import_multiple_projects(client):
    """Test importing multiple projects from JSON."""
    import_data = {
        'projects': [
            {
                'name': 'Project 1',
                'path': '/path/1',
                'remote_url': 'https://github.com/test/project1'
            },
            {
                'name': 'Project 2',
                'path': '/path/2',
                'remote_url': 'https://github.com/test/project2'
            },
            {
                'name': 'Project 3',
                'organization': 'Test Org',
                'remote_url': 'https://github.com/test/project3'
            }
        ]
    }
    
    response = client.post(
        '/api/projects/import',
        data=json.dumps(import_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    assert data['imported'] == 3
    assert data['skipped'] == 0
    assert len(data['errors']) == 0
    
    # Verify all projects were created
    projects = Project.query.all()
    assert len(projects) == 3
    assert {p.name for p in projects} == {'Project 1', 'Project 2', 'Project 3'}


@pytest.mark.integration
def test_import_duplicate_handling(client, app):
    """Test that duplicate projects (by remote_url) are skipped."""
    # Create existing project
    with app.app_context():
        existing = Project(
            name='Existing Project',
            remote_url='https://github.com/test/existing'
        )
        db.session.add(existing)
        db.session.commit()
    
    import_data = {
        'projects': [
            {
                'name': 'New Project Name',
                'remote_url': 'https://github.com/test/existing'  # Same remote_url
            },
            {
                'name': 'Another Project',
                'remote_url': 'https://github.com/test/new'
            }
        ]
    }
    
    response = client.post(
        '/api/projects/import',
        data=json.dumps(import_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    assert data['imported'] == 1
    assert data['skipped'] == 1
    assert len(data['errors']) == 0
    
    # Verify only one new project was created
    projects = Project.query.all()
    assert len(projects) == 2  # Existing + 1 new
    
    # Verify existing project wasn't modified
    existing_project = Project.query.filter_by(remote_url='https://github.com/test/existing').first()
    assert existing_project.name == 'Existing Project'  # Name unchanged


@pytest.mark.integration
def test_import_invalid_json(client):
    """Test that invalid JSON returns 400 Bad Request."""
    response = client.post(
        '/api/projects/import',
        data='{invalid json}',
        content_type='application/json'
    )
    
    assert response.status_code == 400


@pytest.mark.integration
def test_import_missing_projects_key(client):
    """Test that missing 'projects' key returns 400 Bad Request."""
    import_data = {
        'wrong_key': [
            {'name': 'Test Project'}
        ]
    }
    
    response = client.post(
        '/api/projects/import',
        data=json.dumps(import_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    assert response.get_json()['error'] == "Missing 'projects' field"


@pytest.mark.integration
def test_import_non_json_content_type(client):
    """Test that non-JSON Content-Type returns 400 Bad Request."""
    response = client.post(
        '/api/projects/import',
        data='not json',
        content_type='text/plain'
    )
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Content-Type must be application/json'


@pytest.mark.integration
def test_import_non_dict_request_body(client):
    """Test that non-dict request body returns 400 Bad Request."""
    # Send a list instead of dict
    response = client.post(
        '/api/projects/import',
        data=json.dumps(['not', 'a', 'dict']),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Request body must be a JSON object'


@pytest.mark.integration
def test_import_missing_projects_field(client):
    """Test that missing 'projects' field returns 400 Bad Request."""
    response = client.post(
        '/api/projects/import',
        data=json.dumps({'not_projects': []}),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert response.get_json()['error'] == "Missing 'projects' field"


@pytest.mark.integration
def test_import_non_list_projects_field(client):
    """Test that non-list 'projects' field returns 400 Bad Request."""
    response = client.post(
        '/api/projects/import',
        data=json.dumps({'projects': 'not a list'}),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert response.get_json()['error'] == "'projects' field must be a list"


@pytest.mark.integration
def test_import_empty_projects_list(client):
    """Test importing empty projects list."""
    import_data = {
        'projects': []
    }
    
    response = client.post(
        '/api/projects/import',
        data=json.dumps(import_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    assert data['imported'] == 0
    assert data['skipped'] == 0
    assert len(data['errors']) == 0


@pytest.mark.integration
def test_import_statistics_response(client):
    """Test that import response includes accurate statistics."""
    import_data = {
        'projects': [
            {
                'name': 'Project A',
                'remote_url': 'https://github.com/test/a'
            },
            {
                'name': 'Project B',
                'remote_url': 'https://github.com/test/b'
            }
        ]
    }
    
    response = client.post(
        '/api/projects/import',
        data=json.dumps(import_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    # Verify statistics structure
    assert 'imported' in data
    assert 'skipped' in data
    assert 'errors' in data
    assert isinstance(data['imported'], int)
    assert isinstance(data['skipped'], int)
    assert isinstance(data['errors'], list)
    assert data['imported'] == 2


@pytest.mark.integration
def test_import_with_errors(client):
    """Test that projects with errors are reported but don't stop import."""
    import_data = {
        'projects': [
            {
                'name': 'Valid Project',
                'remote_url': 'https://github.com/test/valid'
            },
            {
                # Missing required 'name' field - should cause error
                'remote_url': 'https://github.com/test/invalid'
            },
            {
                'name': 'Another Valid Project',
                'remote_url': 'https://github.com/test/valid2'
            }
        ]
    }
    
    response = client.post(
        '/api/projects/import',
        data=json.dumps(import_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    # Should import valid projects and report errors
    assert data['imported'] == 2
    assert len(data['errors']) == 1
    assert 'error' in data['errors'][0]
    assert 'project' in data['errors'][0]


@pytest.mark.integration
def test_import_invalid_classification(client):
    """Test that projects with invalid classification are reported as errors."""
    import_data = {
        'projects': [
            {
                'name': 'Valid Project',
                'remote_url': 'https://github.com/test/valid',
                'classification': 'primary',
                'status': 'active'
            },
            {
                'name': 'Invalid Project',
                'classification': 'invalid_classification',
                'status': 'active'
            }
        ]
    }
    
    response = client.post(
        '/api/projects/import',
        data=json.dumps(import_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    # Should import valid project and report error for invalid one
    assert data['imported'] == 1
    assert data['skipped'] == 1
    assert len(data['errors']) == 1
    assert data['errors'][0]['project'] == 'Invalid Project'
    assert 'Invalid classification' in data['errors'][0]['error']
    
    # Verify only valid project was imported
    valid_project = Project.query.filter_by(name='Valid Project').first()
    assert valid_project is not None
    
    invalid_project = Project.query.filter_by(name='Invalid Project').first()
    assert invalid_project is None


@pytest.mark.integration
def test_import_invalid_status(client):
    """Test that projects with invalid status are reported as errors."""
    import_data = {
        'projects': [
            {
                'name': 'Valid Project',
                'remote_url': 'https://github.com/test/valid',
                'status': 'active'
            },
            {
                'name': 'Invalid Project',
                'status': 'invalid_status'
            }
        ]
    }
    
    response = client.post(
        '/api/projects/import',
        data=json.dumps(import_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    # Should import valid project and report error for invalid one
    assert data['imported'] == 1
    assert data['skipped'] == 1
    assert len(data['errors']) == 1
    assert data['errors'][0]['project'] == 'Invalid Project'
    assert 'Invalid status' in data['errors'][0]['error']
    
    # Verify only valid project was imported
    valid_project = Project.query.filter_by(name='Valid Project').first()
    assert valid_project is not None
    
    invalid_project = Project.query.filter_by(name='Invalid Project').first()
    assert invalid_project is None


@pytest.mark.integration
def test_import_default_status(client):
    """Test that projects without status default to 'active'."""
    import_data = {
        'projects': [
            {
                'name': 'Project Without Status',
                'remote_url': 'https://github.com/test/no-status'
            }
        ]
    }
    
    response = client.post(
        '/api/projects/import',
        data=json.dumps(import_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    
    # Verify project was created with default status
    project = Project.query.filter_by(name='Project Without Status').first()
    assert project is not None
    assert project.status == 'active'


@pytest.mark.integration
def test_import_duplicate_by_remote_url_only(client, app):
    """Test that duplicate detection uses remote_url, not name."""
    # Create existing project
    with app.app_context():
        existing = Project(
            name='Original Name',
            remote_url='https://github.com/test/same-url'
        )
        db.session.add(existing)
        db.session.commit()
    
    import_data = {
        'projects': [
            {
                'name': 'Different Name',  # Different name
                'remote_url': 'https://github.com/test/same-url'  # Same remote_url
            }
        ]
    }
    
    response = client.post(
        '/api/projects/import',
        data=json.dumps(import_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    # Should skip because remote_url matches
    assert data['imported'] == 0
    assert data['skipped'] == 1
    
    # Verify original project name unchanged
    project = Project.query.filter_by(remote_url='https://github.com/test/same-url').first()
    assert project.name == 'Original Name'

