"""
CLI integration tests for get command.

Tests the `proj get <id>` command using Click's CliRunner.
"""

import pytest
import sys
import importlib.util
from pathlib import Path

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
def test_get_command_success(cli_runner, app, mock_api_for_cli):
    """Test get command with valid project ID."""
    with app.app_context():
        # Create test project
        project = Project(name="Test Project", path="/test/path", status="active")
        db.session.add(project)
        db.session.commit()
        
        result = cli_runner.invoke(cli, ['get', str(project.id)])
        
        assert result.exit_code == 0
        assert 'Test Project' in result.output
        assert str(project.id) in result.output


@pytest.mark.integration
def test_get_command_not_found(cli_runner, app, mock_api_for_cli):
    """Test get command with non-existent project ID."""
    with app.app_context():
        result = cli_runner.invoke(cli, ['get', '999'])
        
        assert result.exit_code != 0
        # Should show error message
        assert '404' in result.output or 'not found' in result.output.lower() or 'error' in result.output.lower()


@pytest.mark.integration
def test_get_command_invalid_id(cli_runner, mock_api_for_cli):
    """Test get command with invalid ID format."""
    result = cli_runner.invoke(cli, ['get', 'invalid'])
    
    # Click should validate integer type
    assert result.exit_code != 0
    assert 'Invalid value' in result.output or 'invalid' in result.output.lower()

