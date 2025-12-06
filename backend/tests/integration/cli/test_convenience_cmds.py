"""
CLI integration tests for convenience commands.

Tests the `proj stats`, `proj recent`, `proj active`, and `proj mine` commands.
"""

import pytest
import sys
import importlib.util
from pathlib import Path
from datetime import datetime, timedelta

# Add scripts directory to path
scripts_dir = str(Path(__file__).parent.parent.parent.parent / 'scripts')
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from click.testing import CliRunner
from app.models.project import Project
from app import db

# Import CLI from proj script file
proj_path = Path(__file__).parent.parent.parent.parent / 'scripts' / 'project_cli' / 'proj'
spec = importlib.util.spec_from_file_location("project_cli.proj", proj_path)
proj_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj_module)
cli = proj_module.cli


@pytest.mark.integration
def test_stats_command_empty(cli_runner, app, mock_api_for_cli):
    """Test stats command with empty database."""
    with app.app_context():
        result = cli_runner.invoke(cli, ['stats'])
        
        assert result.exit_code == 0
        assert 'No projects found' in result.output or 'Total Projects: 0' in result.output


@pytest.mark.integration
def test_stats_command_with_projects(cli_runner, app, mock_api_for_cli):
    """Test stats command with projects."""
    with app.app_context():
        # Create test projects with different statuses
        project1 = Project(name="Active 1", status="active")
        project2 = Project(name="Active 2", status="active")
        project3 = Project(name="Paused 1", status="paused")
        project4 = Project(name="Completed 1", status="completed")
        
        db.session.add_all([project1, project2, project3, project4])
        db.session.commit()
        
        result = cli_runner.invoke(cli, ['stats'])
        
        assert result.exit_code == 0
        assert 'Total Projects: 4' in result.output or '4' in result.output
        assert 'active' in result.output.lower()
        assert 'paused' in result.output.lower()
        assert 'completed' in result.output.lower()


@pytest.mark.integration
def test_recent_command(cli_runner, app, mock_api_for_cli):
    """Test recent command."""
    with app.app_context():
        # Create test projects
        project1 = Project(name="Recent Project 1", status="active")
        project2 = Project(name="Recent Project 2", status="active")
        
        db.session.add_all([project1, project2])
        db.session.commit()
        
        result = cli_runner.invoke(cli, ['recent'])
        
        assert result.exit_code == 0
        assert 'Recent Project' in result.output or 'Recent' in result.output


@pytest.mark.integration
def test_recent_command_with_limit(cli_runner, app, mock_api_for_cli):
    """Test recent command with limit."""
    with app.app_context():
        # Create test projects
        for i in range(5):
            project = Project(name=f"Project {i}", status="active")
            db.session.add(project)
        db.session.commit()
        
        result = cli_runner.invoke(cli, ['recent', '--limit', '3'])
        
        assert result.exit_code == 0
        # Should show recent projects (may be limited to 3)


@pytest.mark.integration
def test_active_command(cli_runner, app, mock_api_for_cli):
    """Test active command."""
    with app.app_context():
        # Create test projects
        project1 = Project(name="Active Project", status="active")
        project2 = Project(name="Paused Project", status="paused")
        
        db.session.add_all([project1, project2])
        db.session.commit()
        
        result = cli_runner.invoke(cli, ['active'])
        
        assert result.exit_code == 0
        assert 'Active Project' in result.output
        assert 'Paused Project' not in result.output


@pytest.mark.integration
def test_active_command_with_wide(cli_runner, app, mock_api_for_cli):
    """Test active command with --wide flag."""
    with app.app_context():
        project = Project(
            name="Active Wide",
            status="active",
            organization="work",
            classification="primary"
        )
        db.session.add(project)
        db.session.commit()
        
        result = cli_runner.invoke(cli, ['active', '--wide'])
        
        assert result.exit_code == 0
        assert 'Active Wide' in result.output


@pytest.mark.integration
def test_mine_command_default(cli_runner, app, mock_api_for_cli):
    """Test mine command with default organization."""
    with app.app_context():
        # Create test projects
        project1 = Project(name="Work Project", organization="work")
        project2 = Project(name="Personal Project", organization="personal")
        
        db.session.add_all([project1, project2])
        db.session.commit()
        
        result = cli_runner.invoke(cli, ['mine'])
        
        assert result.exit_code == 0
        # Defaults to "work" organization
        assert 'Work Project' in result.output
        assert 'Personal Project' not in result.output


@pytest.mark.integration
def test_mine_command_with_org(cli_runner, app, mock_api_for_cli):
    """Test mine command with specified organization."""
    with app.app_context():
        # Create test projects
        project1 = Project(name="Work Project", organization="work")
        project2 = Project(name="Personal Project", organization="personal")
        
        db.session.add_all([project1, project2])
        db.session.commit()
        
        result = cli_runner.invoke(cli, ['mine', '--org', 'personal'])
        
        assert result.exit_code == 0
        assert 'Personal Project' in result.output
        assert 'Work Project' not in result.output

