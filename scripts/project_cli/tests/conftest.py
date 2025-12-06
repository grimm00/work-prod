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
    
    This fixture patches the requests library and health check to use
    the Flask test client, allowing CLI commands to be tested without
    a running backend server.
    
    Args:
        client: Flask test client fixture (from backend)
        monkeypatch: pytest monkeypatch fixture
        
    Returns:
        Flask test client (for convenience)
    """
    import requests
    from project_cli import error_handler
    from .integration.test_helpers import FlaskTestClientAdapter
    
    adapter = FlaskTestClientAdapter(client)
    
    # Mock requests.Session methods
    def mock_session_init(self, *args, **kwargs):
        """Initialize session with mocked methods."""
        # Call original init but don't set up real session
        self.headers = {}
        # Replace methods with adapter methods
        self.get = adapter.get
        self.post = adapter.post
        self.patch = adapter.patch
        self.put = adapter.put
        self.delete = adapter.delete
    
    monkeypatch.setattr(requests.Session, '__init__', mock_session_init)
    
    # Mock direct requests functions
    monkeypatch.setattr(requests, 'get', adapter.get)
    monkeypatch.setattr(requests, 'post', adapter.post)
    monkeypatch.setattr(requests, 'patch', adapter.patch)
    monkeypatch.setattr(requests, 'put', adapter.put)
    monkeypatch.setattr(requests, 'delete', adapter.delete)
    
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

