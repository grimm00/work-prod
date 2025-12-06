"""
CLI integration tests for import command.

Tests the `proj import` command using Click's CliRunner.
"""

import pytest
import sys
import importlib.util
import json
import tempfile
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
def test_import_command_single_project(cli_runner, app, mock_api_for_cli, tmp_path):
    """Test import command with single project."""
    with app.app_context():
        # Create import JSON file
        import_data = {
            'projects': [
                {
                    'name': 'Imported Project',
                    'path': '/imported/path',
                    'organization': 'work',
                    'classification': 'primary',
                    'status': 'active'
                }
            ]
        }
        
        import_file = tmp_path / 'import.json'
        import_file.write_text(json.dumps(import_data))
        
        result = cli_runner.invoke(cli, ['import', str(import_file)])
        
        assert result.exit_code == 0
        assert 'Imported' in result.output or 'imported' in result.output.lower()
        
        # Verify project was created
        project = Project.query.filter_by(name='Imported Project').first()
        assert project is not None
        assert project.path == '/imported/path'


@pytest.mark.integration
def test_import_command_multiple_projects(cli_runner, app, mock_api_for_cli, tmp_path):
    """Test import command with multiple projects."""
    with app.app_context():
        # Create import JSON file
        import_data = {
            'projects': [
                {'name': f'Project {i}', 'status': 'active'}
                for i in range(3)
            ]
        }
        
        import_file = tmp_path / 'import.json'
        import_file.write_text(json.dumps(import_data))
        
        result = cli_runner.invoke(cli, ['import', str(import_file)])
        
        assert result.exit_code == 0
        assert 'imported' in result.output.lower() or '3' in result.output
        
        # Verify projects were created
        projects = Project.query.filter(Project.name.like('Project %')).all()
        assert len(projects) == 3


@pytest.mark.integration
def test_import_command_duplicate_handling(cli_runner, app, mock_api_for_cli, tmp_path):
    """Test import command handles duplicates."""
    with app.app_context():
        # Create existing project
        existing = Project(
            name='Existing Project',
            remote_url='https://github.com/user/existing.git'
        )
        db.session.add(existing)
        db.session.commit()
        
        # Create import JSON with duplicate remote_url
        import_data = {
            'projects': [
                {
                    'name': 'Duplicate Project',
                    'remote_url': 'https://github.com/user/existing.git'
                }
            ]
        }
        
        import_file = tmp_path / 'import.json'
        import_file.write_text(json.dumps(import_data))
        
        result = cli_runner.invoke(cli, ['import', str(import_file)])
        
        assert result.exit_code == 0
        # Should show skipped or duplicate message
        assert 'skipped' in result.output.lower() or 'duplicate' in result.output.lower() or 'imported' in result.output.lower()


@pytest.mark.integration
def test_import_command_invalid_file(cli_runner, mock_api_for_cli, tmp_path):
    """Test import command with invalid JSON file."""
    # Create invalid JSON file
    invalid_file = tmp_path / 'invalid.json'
    invalid_file.write_text('{ invalid json }')
    
    result = cli_runner.invoke(cli, ['import', str(invalid_file)])
    
    # Should handle invalid JSON gracefully
    assert result.exit_code != 0
    assert 'error' in result.output.lower() or 'invalid' in result.output.lower()


@pytest.mark.integration
def test_import_command_missing_file(cli_runner, mock_api_for_cli):
    """Test import command with non-existent file."""
    result = cli_runner.invoke(cli, ['import', '/nonexistent/file.json'])
    
    # Should show file not found error
    assert result.exit_code != 0
    assert 'not found' in result.output.lower() or 'error' in result.output.lower() or 'file' in result.output.lower()

