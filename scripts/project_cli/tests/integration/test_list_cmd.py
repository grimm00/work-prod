"""
CLI integration tests for list command.

Tests the `proj list` command using Click's CliRunner.
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
def test_list_command_empty(cli_runner, app, mock_api_for_cli):
    """Test list command with empty database."""
    with app.app_context():
        result = cli_runner.invoke(cli, ['list'])
        
        assert result.exit_code == 0
        assert 'No projects found' in result.output or 'Projects (0)' in result.output


@pytest.mark.integration
def test_list_command_with_projects(cli_runner, app, mock_api_for_cli):
    """Test list command with projects in database."""
    with app.app_context():
        # Create test projects
        project1 = Project(name="Test Project 1", path="/test/1", status="active")
        project2 = Project(name="Test Project 2", path="/test/2", status="paused")
        project3 = Project(name="Test Project 3", status="active")
        
        db.session.add_all([project1, project2, project3])
        db.session.commit()
        
        result = cli_runner.invoke(cli, ['list'])
        
        assert result.exit_code == 0
        assert 'Test Project 1' in result.output
        assert 'Test Project 2' in result.output
        assert 'Test Project 3' in result.output
        assert 'Projects (3)' in result.output


@pytest.mark.integration
def test_list_command_with_status_filter(cli_runner, app, mock_api_for_cli):
    """Test list command with status filter."""
    with app.app_context():
        # Create test projects
        project1 = Project(name="Active Project", status="active")
        project2 = Project(name="Paused Project", status="paused")
        
        db.session.add_all([project1, project2])
        db.session.commit()
        
        result = cli_runner.invoke(cli, ['list', '--status', 'active'])
        
        assert result.exit_code == 0
        assert 'Active Project' in result.output
        assert 'Paused Project' not in result.output


@pytest.mark.integration
def test_list_command_with_organization_filter(cli_runner, app, mock_api_for_cli):
    """Test list command with organization filter."""
    with app.app_context():
        # Create test projects
        project1 = Project(name="Work Project", organization="work")
        project2 = Project(name="Personal Project", organization="personal")
        
        db.session.add_all([project1, project2])
        db.session.commit()
        
        result = cli_runner.invoke(cli, ['list', '--org', 'work'])
        
        assert result.exit_code == 0
        assert 'Work Project' in result.output
        assert 'Personal Project' not in result.output


@pytest.mark.integration
def test_list_command_with_search(cli_runner, app, mock_api_for_cli):
    """Test list command with search filter."""
    with app.app_context():
        # Create test projects
        project1 = Project(name="Productivity Tool", description="Helps with work")
        project2 = Project(name="Learning Project", description="Educational")
        
        db.session.add_all([project1, project2])
        db.session.commit()
        
        result = cli_runner.invoke(cli, ['list', '--search', 'productivity'])
        
        assert result.exit_code == 0
        assert 'Productivity Tool' in result.output
        assert 'Learning Project' not in result.output


@pytest.mark.integration
def test_list_command_with_wide_flag(cli_runner, app, mock_api_for_cli):
    """Test list command with --wide flag."""
    with app.app_context():
        # Create test project with all fields
        project = Project(
            name="Full Project",
            path="/full/path",
            organization="work",
            classification="primary",
            status="active",
            description="A full project"
        )
        
        db.session.add(project)
        db.session.commit()
        
        result = cli_runner.invoke(cli, ['list', '--wide'])
        
        assert result.exit_code == 0
        assert 'Full Project' in result.output
        # Wide mode should show all columns
        assert 'Status' in result.output or 'active' in result.output
        assert 'Org' in result.output or 'work' in result.output


@pytest.mark.integration
def test_list_command_invalid_status(cli_runner, mock_api_for_cli):
    """Test list command with invalid status value."""
    result = cli_runner.invoke(cli, ['list', '--status', 'invalid'])
    
    # Click should validate and show error
    assert result.exit_code != 0
    assert 'Invalid value' in result.output or 'invalid choice' in result.output.lower()

