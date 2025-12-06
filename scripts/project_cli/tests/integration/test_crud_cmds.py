"""
CLI integration tests for CRUD commands.

Tests the `proj create`, `proj update`, `proj delete`, and `proj archive` commands.
"""

import pytest
import sys
import importlib.util
from pathlib import Path

# Add backend to path for app imports
backend_dir = Path(__file__).parent.parent.parent.parent / 'backend'
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from click.testing import CliRunner
from app.models.project import Project
from app import db

# Import CLI from proj script file
proj_path = Path(__file__).parent.parent.parent / 'proj'
spec = importlib.util.spec_from_file_location("project_cli.proj", proj_path)
proj_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj_module)
cli = proj_module.cli


@pytest.mark.integration
def test_create_command_minimal(cli_runner, app, mock_api_for_cli):
    """Test create command with minimal data (name only)."""
    with app.app_context():
        result = cli_runner.invoke(cli, ['create', '--name', 'New Project'])
        
        assert result.exit_code == 0
        assert 'New Project' in result.output
        assert 'Created project' in result.output or 'Created' in result.output


@pytest.mark.integration
def test_create_command_full(cli_runner, app, mock_api_for_cli):
    """Test create command with all fields."""
    with app.app_context():
        result = cli_runner.invoke(cli, [
            'create',
            '--name', 'Full Project',
            '--path', '/full/path',
            '--organization', 'work',
            '--classification', 'primary',
            '--status', 'active',
            '--description', 'A full project',
            '--remote-url', 'https://github.com/user/repo.git'
        ])
        
        assert result.exit_code == 0
        assert 'Full Project' in result.output
        assert 'work' in result.output or 'primary' in result.output


@pytest.mark.integration
def test_create_command_missing_name(cli_runner, mock_api_for_cli):
    """Test create command without required name."""
    result = cli_runner.invoke(cli, ['create'])
    
    # Click should require --name
    assert result.exit_code != 0
    assert 'name' in result.output.lower() or 'required' in result.output.lower()


@pytest.mark.integration
def test_create_command_invalid_status(cli_runner, mock_api_for_cli):
    """Test create command with invalid status."""
    result = cli_runner.invoke(cli, ['create', '--name', 'Test', '--status', 'invalid'])
    
    # Click should validate status choice
    assert result.exit_code != 0
    assert 'Invalid value' in result.output or 'invalid choice' in result.output.lower()


@pytest.mark.integration
def test_update_command(cli_runner, app, mock_api_for_cli):
    """Test update command."""
    with app.app_context():
        # Create test project
        project = Project(name="Original Name", status="active")
        db.session.add(project)
        db.session.commit()
        
        result = cli_runner.invoke(cli, [
            'update', str(project.id),
            '--name', 'Updated Name',
            '--status', 'paused'
        ])
        
        assert result.exit_code == 0
        assert 'Updated Name' in result.output or 'Updated' in result.output


@pytest.mark.integration
def test_update_command_not_found(cli_runner, app, mock_api_for_cli):
    """Test update command with non-existent project ID."""
    with app.app_context():
        result = cli_runner.invoke(cli, ['update', '999', '--name', 'Test'])
        
        assert result.exit_code != 0
        assert '404' in result.output or 'not found' in result.output.lower() or 'error' in result.output.lower()


@pytest.mark.integration
def test_delete_command(cli_runner, app, mock_api_for_cli):
    """Test delete command with confirmation."""
    with app.app_context():
        # Create test project
        project = Project(name="To Delete", status="active")
        db.session.add(project)
        db.session.commit()
        project_id = project.id
        
        # Delete with --yes flag to skip confirmation
        result = cli_runner.invoke(cli, ['delete', str(project_id), '--yes'])
        
        assert result.exit_code == 0
        assert 'deleted' in result.output.lower() or 'Deleted' in result.output
        
        # Verify project is deleted
        deleted_project = Project.query.get(project_id)
        assert deleted_project is None


@pytest.mark.integration
def test_delete_command_not_found(cli_runner, app, mock_api_for_cli):
    """Test delete command with non-existent project ID."""
    with app.app_context():
        result = cli_runner.invoke(cli, ['delete', '999', '--yes'])
        
        assert result.exit_code != 0
        assert '404' in result.output or 'not found' in result.output.lower() or 'error' in result.output.lower()


@pytest.mark.integration
def test_archive_command(cli_runner, app, mock_api_for_cli):
    """Test archive command."""
    with app.app_context():
        # Create test project
        project = Project(name="To Archive", status="active", classification="primary")
        db.session.add(project)
        db.session.commit()
        
        result = cli_runner.invoke(cli, ['archive', str(project.id)])
        
        assert result.exit_code == 0
        assert 'archived' in result.output.lower() or 'Archived' in result.output
        
        # Verify project is archived
        archived_project = Project.query.get(project.id)
        assert archived_project.classification == 'archive'
        assert archived_project.status == 'paused'


@pytest.mark.integration
def test_archive_command_not_found(cli_runner, app, mock_api_for_cli):
    """Test archive command with non-existent project ID."""
    with app.app_context():
        result = cli_runner.invoke(cli, ['archive', '999'])
        
        assert result.exit_code != 0
        assert '404' in result.output or 'not found' in result.output.lower() or 'error' in result.output.lower()

