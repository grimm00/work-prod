"""
CLI test configuration and fixtures.

Provides fixtures for testing CLI commands with mocked API calls.
"""

import pytest
import sys
from pathlib import Path

# Add scripts directory to path so we can import project_cli
scripts_dir = str(Path(__file__).parent.parent.parent.parent / 'scripts')
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)


@pytest.fixture
def mock_api_for_cli(client, monkeypatch):
    """
    Mock API calls to use Flask test client instead of real HTTP requests.
    
    This fixture patches the requests library and health check to use
    the Flask test client, allowing CLI commands to be tested without
    a running backend server.
    
    Args:
        client: Flask test client fixture
        monkeypatch: pytest monkeypatch fixture
        
    Returns:
        Flask test client (for convenience)
    """
    from .test_helpers import FlaskTestClientAdapter
    import requests
    from scripts.project_cli import error_handler
    
    adapter = FlaskTestClientAdapter(client)
    
    # Mock requests.Session methods
    original_session_init = requests.Session.__init__
    
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
    from scripts.project_cli import config
    original_get_api_url = config.Config.get_api_url
    
    def mock_get_api_url(self):
        """Return test API URL."""
        return 'http://localhost:5000/api'
    
    monkeypatch.setattr(config.Config, 'get_api_url', mock_get_api_url)
    
    return client

