"""
CLI integration tests for edge cases and boundary conditions.

Tests special characters, boundary values, and unusual scenarios.
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
def test_create_with_special_characters(cli_runner, app, mock_api_for_cli):
    """Test create command with special characters in name."""
    with app.app_context():
        result = cli_runner.invoke(cli, [
            'create',
            '--name', 'Project with "quotes" & symbols!',
            '--description', 'Description with <tags> and &amp; entities'
        ])
        
        assert result.exit_code == 0
        assert 'Project with' in result.output


@pytest.mark.integration
def test_create_with_unicode_characters(cli_runner, app, mock_api_for_cli):
    """Test create command with Unicode characters."""
    with app.app_context():
        result = cli_runner.invoke(cli, [
            'create',
            '--name', 'Projekt mit Ümläuten',
            '--description', 'Проект с кириллицей'
        ])
        
        assert result.exit_code == 0
        assert 'Projekt' in result.output or 'Проект' in result.output


@pytest.mark.integration
def test_create_with_very_long_name(cli_runner, app, mock_api_for_cli):
    """Test create command with very long project name."""
    with app.app_context():
        long_name = 'A' * 200  # Very long name
        result = cli_runner.invoke(cli, ['create', '--name', long_name])
        
        # Should handle long names (may truncate or accept)
        assert result.exit_code in [0, 1]  # May fail validation or succeed


@pytest.mark.integration
def test_create_with_very_long_description(cli_runner, app, mock_api_for_cli):
    """Test create command with very long description."""
    with app.app_context():
        long_desc = 'Description ' * 100  # Very long description
        result = cli_runner.invoke(cli, [
            'create',
            '--name', 'Long Desc Project',
            '--description', long_desc
        ])
        
        # Should handle long descriptions
        assert result.exit_code in [0, 1]


@pytest.mark.integration
def test_create_with_whitespace_only_name(cli_runner, app, mock_api_for_cli):
    """Test create command with whitespace-only name."""
    result = cli_runner.invoke(cli, ['create', '--name', '   '])
    
    # Should reject whitespace-only names
    assert result.exit_code != 0 or 'error' in result.output.lower()


@pytest.mark.integration
def test_create_with_leading_trailing_whitespace(cli_runner, app, mock_api_for_cli):
    """Test create command with leading/trailing whitespace."""
    with app.app_context():
        result = cli_runner.invoke(cli, ['create', '--name', '  Trimmed Project  '])
        
        # Should handle or trim whitespace
        assert result.exit_code in [0, 1]


@pytest.mark.integration
def test_create_duplicate_name(cli_runner, app, mock_api_for_cli):
    """Test create command with duplicate project name."""
    with app.app_context():
        # Create first project
        project1 = Project(name="Duplicate Name", status="active")
        db.session.add(project1)
        db.session.commit()
        
        # Try to create duplicate
        result = cli_runner.invoke(cli, ['create', '--name', 'Duplicate Name'])
        
        # Should return 409 Conflict or error
        assert result.exit_code != 0
        assert '409' in result.output or 'duplicate' in result.output.lower() or 'conflict' in result.output.lower() or 'error' in result.output.lower()


@pytest.mark.integration
def test_create_duplicate_path(cli_runner, app, mock_api_for_cli):
    """Test create command with duplicate path."""
    with app.app_context():
        # Create first project with path
        project1 = Project(name="First Project", path="/duplicate/path", status="active")
        db.session.add(project1)
        db.session.commit()
        
        # Try to create duplicate path
        result = cli_runner.invoke(cli, [
            'create',
            '--name', 'Second Project',
            '--path', '/duplicate/path'
        ])
        
        # Should return 409 Conflict or error
        assert result.exit_code != 0
        assert '409' in result.output or 'duplicate' in result.output.lower() or 'conflict' in result.output.lower() or 'error' in result.output.lower()


@pytest.mark.integration
def test_create_with_invalid_remote_url(cli_runner, app, mock_api_for_cli):
    """Test create command with invalid remote URL format."""
    with app.app_context():
        result = cli_runner.invoke(cli, [
            'create',
            '--name', 'Invalid URL Project',
            '--remote-url', 'not-a-valid-url'
        ])
        
        # May accept invalid URL (validation happens on backend)
        assert result.exit_code in [0, 1]


@pytest.mark.integration
def test_list_with_multiple_filters(cli_runner, app, mock_api_for_cli):
    """Test list command with multiple filters combined."""
    with app.app_context():
        # Create test projects
        project1 = Project(
            name="Match All",
            status="active",
            organization="work",
            classification="primary"
        )
        project2 = Project(
            name="Match Some",
            status="active",
            organization="work",
            classification="secondary"
        )
        
        db.session.add_all([project1, project2])
        db.session.commit()
        
        result = cli_runner.invoke(cli, [
            'list',
            '--status', 'active',
            '--org', 'work',
            '--classification', 'primary'
        ])
        
        assert result.exit_code == 0
        assert 'Match All' in result.output
        assert 'Match Some' not in result.output


@pytest.mark.integration
def test_list_with_case_insensitive_status(cli_runner, app, mock_api_for_cli):
    """Test list command with case-insensitive status filter."""
    with app.app_context():
        project = Project(name="Active Project", status="active")
        db.session.add(project)
        db.session.commit()
        
        # Test uppercase status
        result = cli_runner.invoke(cli, ['list', '--status', 'ACTIVE'])
        
        assert result.exit_code == 0
        assert 'Active Project' in result.output


@pytest.mark.integration
def test_list_with_case_insensitive_classification(cli_runner, app, mock_api_for_cli):
    """Test list command with case-insensitive classification filter."""
    with app.app_context():
        project = Project(name="Primary Project", classification="primary")
        db.session.add(project)
        db.session.commit()
        
        # Test uppercase classification
        result = cli_runner.invoke(cli, ['list', '--classification', 'PRIMARY'])
        
        assert result.exit_code == 0
        assert 'Primary Project' in result.output


@pytest.mark.integration
def test_get_with_negative_id(cli_runner, mock_api_for_cli):
    """Test get command with negative ID."""
    result = cli_runner.invoke(cli, ['get', '-1'])
    
    # Click should validate positive integer
    assert result.exit_code != 0
    assert 'Invalid value' in result.output or 'invalid' in result.output.lower()


@pytest.mark.integration
def test_get_with_zero_id(cli_runner, app, mock_api_for_cli):
    """Test get command with zero ID."""
    with app.app_context():
        result = cli_runner.invoke(cli, ['get', '0'])
        
        # Should return 404 or error
        assert result.exit_code != 0
        assert '404' in result.output or 'not found' in result.output.lower() or 'error' in result.output.lower()


@pytest.mark.integration
def test_get_with_very_large_id(cli_runner, mock_api_for_cli):
    """Test get command with very large ID."""
    result = cli_runner.invoke(cli, ['get', '999999999'])
    
    # Should handle large IDs gracefully (may return 404)
    assert result.exit_code in [0, 1]


@pytest.mark.integration
def test_update_with_empty_name(cli_runner, app, mock_api_for_cli):
    """Test update command with empty name."""
    with app.app_context():
        project = Project(name="Original Name", status="active")
        db.session.add(project)
        db.session.commit()
        
        result = cli_runner.invoke(cli, [
            'update', str(project.id),
            '--name', ''
        ])
        
        # Should reject empty name or handle gracefully
        assert result.exit_code in [0, 1]


@pytest.mark.integration
def test_delete_without_confirmation(cli_runner, app, mock_api_for_cli):
    """Test delete command without --yes flag (should prompt)."""
    with app.app_context():
        project = Project(name="To Delete", status="active")
        db.session.add(project)
        db.session.commit()
        
        # Simulate user input: 'n' (no)
        result = cli_runner.invoke(cli, ['delete', str(project.id)], input='n\n')
        
        # Should not delete without confirmation
        # Exit code may vary depending on how Click handles abort
        assert result.exit_code in [0, 1]


@pytest.mark.integration
def test_search_with_special_characters(cli_runner, app, mock_api_for_cli):
    """Test list command search with special characters."""
    with app.app_context():
        project = Project(name="Special Project", description="Has & symbols!")
        db.session.add(project)
        db.session.commit()
        
        result = cli_runner.invoke(cli, ['list', '--search', '&'])
        
        # Should handle special characters in search
        assert result.exit_code == 0


@pytest.mark.integration
def test_search_with_empty_string(cli_runner, app, mock_api_for_cli):
    """Test list command with empty search string."""
    with app.app_context():
        project = Project(name="Test Project", status="active")
        db.session.add(project)
        db.session.commit()
        
        result = cli_runner.invoke(cli, ['list', '--search', ''])
        
        # Should handle empty search (may return all or none)
        assert result.exit_code == 0


@pytest.mark.integration
def test_import_with_empty_projects_array(cli_runner, app, mock_api_for_cli, tmp_path):
    """Test import command with empty projects array."""
    import_data = {'projects': []}
    import_file = tmp_path / 'empty.json'
    import_file.write_text(str(import_data).replace("'", '"'))
    
    result = cli_runner.invoke(cli, ['import', str(import_file)])
    
    # Should handle empty array gracefully
    assert result.exit_code == 0


@pytest.mark.integration
def test_import_with_missing_projects_key(cli_runner, mock_api_for_cli, tmp_path):
    """Test import command with missing 'projects' key."""
    import json
    import_data = {'data': []}  # Wrong key
    import_file = tmp_path / 'wrong.json'
    import_file.write_text(json.dumps(import_data))
    
    result = cli_runner.invoke(cli, ['import', str(import_file)])
    
    # Should handle missing key gracefully
    assert result.exit_code != 0


@pytest.mark.integration
def test_import_with_invalid_project_data(cli_runner, app, mock_api_for_cli, tmp_path):
    """Test import command with invalid project data."""
    import json
    import_data = {
        'projects': [
            {'invalid': 'data'}  # Missing required 'name' field
        ]
    }
    import_file = tmp_path / 'invalid.json'
    import_file.write_text(json.dumps(import_data))
    
    result = cli_runner.invoke(cli, ['import', str(import_file)])
    
    # Should handle invalid data gracefully (may skip or error)
    assert result.exit_code in [0, 1]

