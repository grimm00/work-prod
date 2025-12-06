"""
Test helpers for CLI integration tests.

Provides utilities for mocking API calls to use Flask test client.
"""

import json
from typing import Optional
from unittest.mock import Mock, MagicMock


class FlaskTestClientAdapter:
    """
    Adapter to make Flask test client work like requests library.
    
    This allows CLI commands to use the Flask test client instead of
    making real HTTP requests.
    """
    
    def __init__(self, test_client):
        """
        Initialize adapter with Flask test client.
        
        Args:
            test_client: Flask test client instance
        """
        self.test_client = test_client
    
    def _make_request(self, method, url, **kwargs):
        """
        Make a request using Flask test client.
        
        Args:
            method: HTTP method (get, post, patch, put, delete)
            url: Full URL or path
            **kwargs: Request arguments (params, json, data, headers, etc.)
        """
        from urllib.parse import urlparse, parse_qs
        
        # Parse URL to extract path and query string
        parsed = urlparse(url)
        path = parsed.path
        
        # Handle query parameters
        query_string = None
        if parsed.query:
            query_string = parsed.query
        elif 'params' in kwargs:
            # Build query string from params dict
            params = kwargs['params']
            if params:
                query_string = '&'.join(f"{k}={v}" for k, v in params.items())
        
        # Prepare request data
        data = kwargs.get('data') or kwargs.get('json')
        if data and isinstance(data, dict):
            data = json.dumps(data)
        
        headers = kwargs.get('headers', {})
        content_type = headers.get('Content-Type', 'application/json')
        
        # Make request using test client
        method_func = getattr(self.test_client, method.lower())
        response = method_func(
            path,
            data=data,
            content_type=content_type,
            headers=headers,
            query_string=query_string
        )
        
        # Create mock response that looks like requests.Response
        mock_response = Mock()
        mock_response.status_code = response.status_code
        mock_response.text = response.data.decode('utf-8')
        mock_response.content = response.data
        mock_response.headers = dict(response.headers)
        
        # Add json() method
        def json_method():
            try:
                return json.loads(mock_response.text)
            except json.JSONDecodeError:
                return {}
        mock_response.json = json_method
        
        # Add raise_for_status() method
        def raise_for_status():
            if response.status_code >= 400:
                from requests.exceptions import HTTPError
                http_error = HTTPError(f"{response.status_code} Client Error")
                http_error.response = mock_response
                raise http_error
        mock_response.raise_for_status = raise_for_status
        
        return mock_response
    
    def get(self, url, **kwargs):
        """GET request."""
        return self._make_request('get', url, **kwargs)
    
    def post(self, url, **kwargs):
        """POST request."""
        return self._make_request('post', url, **kwargs)
    
    def patch(self, url, **kwargs):
        """PATCH request."""
        return self._make_request('patch', url, **kwargs)
    
    def put(self, url, **kwargs):
        """PUT request."""
        return self._make_request('put', url, **kwargs)
    
    def delete(self, url, **kwargs):
        """DELETE request."""
        return self._make_request('delete', url, **kwargs)


def mock_api_client(test_client, monkeypatch):
    """
    Mock the requests library to use Flask test client.
    
    Args:
        test_client: Flask test client instance
        monkeypatch: pytest monkeypatch fixture
    """
    adapter = FlaskTestClientAdapter(test_client)
    
    # Mock requests.Session to use our adapter
    def mock_session_init(self, *args, **kwargs):
        self.get = adapter.get
        self.post = adapter.post
        self.patch = adapter.patch
        self.put = adapter.put
        self.delete = adapter.delete
    
    # Patch requests.Session.__init__ to use our adapter
    import requests
    monkeypatch.setattr(requests.Session, '__init__', mock_session_init)
    
    # Also patch requests.get/post/etc for direct usage
    monkeypatch.setattr(requests, 'get', adapter.get)
    monkeypatch.setattr(requests, 'post', adapter.post)
    monkeypatch.setattr(requests, 'patch', adapter.patch)
    monkeypatch.setattr(requests, 'put', adapter.put)
    monkeypatch.setattr(requests, 'delete', adapter.delete)

