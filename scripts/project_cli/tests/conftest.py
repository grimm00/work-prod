"""
CLI test configuration and fixtures.

Provides fixtures for testing CLI commands with mocked API calls.
Imports backend fixtures for integration testing.
"""

import pytest
import sys
from pathlib import Path

# Add backend directory to path to import backend fixtures
backend_dir = Path(__file__).parent.parent.parent.parent / 'backend'
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Import backend fixtures
from tests.conftest import app, client, db, cli_runner

# Import CLI-specific fixtures from integration test helpers
# Note: Import happens inside fixture to avoid circular imports


@pytest.fixture
def mock_api_for_cli(client, monkeypatch):
    """
    Mock API calls to use Flask test client instead of real HTTP requests.
    
    This fixture delegates to the shared mock_api_client helper for FlaskTestClientAdapter
    setup, keeping only CLI-specific overrides (health check and config).
    
    The mocking is scoped to the test lifecycle via pytest's monkeypatch fixture,
    which automatically restores original methods after each test, reducing
    global side effects.
    
    Args:
        client: Flask test client fixture (from backend)
        monkeypatch: pytest monkeypatch fixture (provides test-scoped cleanup)
        
    Returns:
        Flask test client (for convenience)
    """
    from project_cli import error_handler
    from .integration.test_helpers import mock_api_client
    
    # Delegate to shared helper for FlaskTestClientAdapter setup
    # monkeypatch fixture ensures cleanup after test
    mock_api_client(client, monkeypatch)
    
    # CLI-specific overrides: health check and config
    # Mock health check to always return True (since we're using test client)
    def mock_check_health(base_url):
        """Mock health check - always return True for test client."""
        return True
    
    monkeypatch.setattr(error_handler, 'check_backend_health', mock_check_health)
    
    # Mock Config to return test URL
    from project_cli import config
    
    def mock_get_api_url(self):
        """Return test API URL."""
        return 'http://localhost:5000/api'
    
    monkeypatch.setattr(config.Config, 'get_api_url', mock_get_api_url)
    
    return client

