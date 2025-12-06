"""
Tests for uncovered code paths in Projects API.

These tests target specific code paths that aren't covered by existing tests
to improve test coverage.
"""

import pytest
import json
from app.models.project import Project
from app import db
from sqlalchemy.exc import IntegrityError


@pytest.mark.integration
def test_create_project_integrity_error_handling(client, app, monkeypatch):
    """Test IntegrityError handling in create_project (lines 168-169)."""
    # Create a project with a path first
    with app.app_context():
        project = Project(name="Existing Project", path="/duplicate/path")
        db.session.add(project)
        db.session.commit()
    
    # Mock db.session.commit to raise IntegrityError on second project
    original_commit = db.session.commit
    call_count = [0]
    
    def mock_commit():
        call_count[0] += 1
        if call_count[0] == 2:  # Second commit (for duplicate path)
            raise IntegrityError("statement", "params", "orig")
        original_commit()
    
    monkeypatch.setattr(db.session, 'commit', mock_commit)
    
    # Try to create project with duplicate path
    response = client.post('/api/projects',
                          json={'name': 'New Project', 'path': '/duplicate/path'},
                          content_type='application/json')
    
    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'error' in data
    
    # Restore original commit
    monkeypatch.setattr(db.session, 'commit', original_commit)


@pytest.mark.integration
def test_delete_project_exception_handling(client, app, monkeypatch):
    """Test exception handling in delete_project (lines 302-305)."""
    # Create a project first
    with app.app_context():
        project = Project(name="Test Project")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Mock db.session.commit to raise an exception
    original_commit = db.session.commit
    
    def mock_commit():
        raise RuntimeError("Database error during delete")
    
    monkeypatch.setattr(db.session, 'commit', mock_commit)
    
    response = client.delete(f'/api/projects/{project_id}')
    
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data['error'] == 'Internal server error'
    # Verify internal details are NOT exposed
    assert 'RuntimeError' not in data['error']
    assert 'Database error' not in data['error']
    
    # Restore original commit
    monkeypatch.setattr(db.session, 'commit', original_commit)


@pytest.mark.integration
def test_import_projects_per_project_exception_handling(client, app, monkeypatch):
    """Test exception handling for individual project import errors (lines 408-416)."""
    # Mock Project creation to raise an exception for one project
    original_add = db.session.add
    
    call_count = [0]
    
    def mock_add(obj):
        call_count[0] += 1
        if call_count[0] == 1:  # First project fails
            raise ValueError("Invalid project data")
        original_add(obj)
    
    monkeypatch.setattr(db.session, 'add', mock_add)
    
    response = client.post('/api/projects/import',
                          json={
                              'projects': [
                                  {'name': 'Project 1', 'invalid_field': 'value'},  # This will fail
                                  {'name': 'Project 2'}  # This should succeed
                              ]
                          },
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['imported'] == 1  # One project imported
    assert data['skipped'] == 1  # One project skipped
    assert len(data['errors']) == 1
    assert 'error' in data['errors'][0]
    
    # Restore original add
    monkeypatch.setattr(db.session, 'add', original_add)


@pytest.mark.integration
def test_import_projects_commit_exception_handling(client, app, monkeypatch):
    """Test exception handling for commit errors in import_projects (lines 420-423)."""
    # Mock db.session.commit to raise an exception
    original_commit = db.session.commit
    
    def mock_commit():
        raise RuntimeError("Commit failed")
    
    monkeypatch.setattr(db.session, 'commit', mock_commit)
    
    response = client.post('/api/projects/import',
                          json={
                              'projects': [
                                  {'name': 'Test Project'}
                              ]
                          },
                          content_type='application/json')
    
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'error' in data
    assert 'import' in data['error'].lower() or 'failed' in data['error'].lower()
    
    # Restore original commit
    monkeypatch.setattr(db.session, 'commit', original_commit)


@pytest.mark.integration
def test_archive_project_exception_handling(client, app, monkeypatch):
    """Test exception handling in archive_project (lines 451-454)."""
    # Create a project first
    with app.app_context():
        project = Project(name="Test Project")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Mock db.session.commit to raise an exception
    original_commit = db.session.commit
    
    def mock_commit():
        raise RuntimeError("Archive commit failed")
    
    monkeypatch.setattr(db.session, 'commit', mock_commit)
    
    response = client.put(f'/api/projects/{project_id}/archive')
    
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data['error'] == 'Internal server error'
    # Verify internal details are NOT exposed
    assert 'RuntimeError' not in data['error']
    assert 'Archive commit' not in data['error']
    
    # Restore original commit
    monkeypatch.setattr(db.session, 'commit', original_commit)


@pytest.mark.integration
def test_get_project_invalid_id_format(client):
    """Test ValueError error handler for invalid project ID format (line 470)."""
    # Try to get project with non-integer ID
    response = client.get('/api/projects/invalid-id')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'invalid' in data['error'].lower() or 'format' in data['error'].lower()


@pytest.mark.integration
def test_update_project_path_unchanged_no_duplicate_check(client, app):
    """Test update_project when path is unchanged (line 250 - no duplicate check)."""
    # Create a project
    with app.app_context():
        project = Project(name="Test Project", path="/test/path")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Update project with same path (should not check for duplicates)
    response = client.patch(f'/api/projects/{project_id}',
                           json={'path': '/test/path'},  # Same path
                           content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['path'] == '/test/path'


@pytest.mark.integration
def test_update_project_path_to_none_no_duplicate_check(client, app):
    """Test update_project when path is set to None (line 260)."""
    # Create a project with a path
    with app.app_context():
        project = Project(name="Test Project", path="/test/path")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    # Update project to remove path
    response = client.patch(f'/api/projects/{project_id}',
                           json={'path': None},
                           content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['path'] is None

