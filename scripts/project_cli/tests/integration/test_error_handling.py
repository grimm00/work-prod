"""
CLI integration tests for error handling.

Tests error scenarios: backend down, invalid URLs, timeouts, etc.
"""

import pytest
import sys
import importlib.util
from pathlib import Path

from click.testing import CliRunner

# Import CLI from proj script file
proj_path = Path(__file__).parent.parent.parent / 'proj'
spec = importlib.util.spec_from_file_location("project_cli.proj", proj_path)
proj_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj_module)
cli = proj_module.cli


@pytest.mark.integration
def test_list_command_backend_down(cli_runner, monkeypatch):
    """Test list command when backend is down (connection error)."""
    import requests
    from project_cli import error_handler
    
    # Mock health check to return False (backend down)
    def mock_check_health(base_url):
        return False
    
    # Mock requests to raise ConnectionError
    def mock_get(url, **kwargs):
        raise requests.exceptions.ConnectionError("Connection refused")
    
    monkeypatch.setattr(error_handler, 'check_backend_health', mock_check_health)
    monkeypatch.setattr(requests, 'get', mock_get)
    monkeypatch.setattr(requests.Session, 'get', mock_get)
    
    result = cli_runner.invoke(cli, ['list'])
    
    # Should show connection error message
    assert result.exit_code != 0
    assert 'connection' in result.output.lower() or 'backend' in result.output.lower() or 'error' in result.output.lower()


@pytest.mark.integration
def test_list_command_invalid_api_url(cli_runner, monkeypatch):
    """Test list command with invalid API URL configuration."""
    from project_cli import config
    
    # Mock Config to return invalid URL
    def mock_get_api_url(self):
        return 'invalid-url'
    
    monkeypatch.setattr(config.Config, 'get_api_url', mock_get_api_url)
    
    result = cli_runner.invoke(cli, ['list'])
    
    # Should handle invalid URL gracefully
    assert result.exit_code != 0


@pytest.mark.integration
def test_get_command_invalid_id_format(cli_runner, mock_api_for_cli):
    """Test get command with invalid ID format (not an integer)."""
    result = cli_runner.invoke(cli, ['get', 'not-a-number'])
    
    # Click should validate integer type
    assert result.exit_code != 0
    assert 'Invalid value' in result.output or 'invalid' in result.output.lower()


@pytest.mark.integration
def test_create_command_missing_required_field(cli_runner, mock_api_for_cli):
    """Test create command without required name field."""
    result = cli_runner.invoke(cli, ['create'])
    
    # Click should require --name
    assert result.exit_code != 0
    assert 'name' in result.output.lower() or 'required' in result.output.lower()

