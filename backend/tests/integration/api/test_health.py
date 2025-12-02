"""
Integration tests for health check API endpoint.
"""

import pytest
import json


@pytest.mark.integration
def test_health_check_returns_200(client):
    """Test that health check endpoint returns 200 status code."""
    response = client.get('/api/health')
    assert response.status_code == 200


@pytest.mark.integration
def test_health_check_returns_json(client):
    """Test that health check endpoint returns JSON content type."""
    response = client.get('/api/health')
    assert response.content_type == 'application/json'


@pytest.mark.integration
def test_health_check_response_structure(client):
    """Test that health check response has correct structure."""
    response = client.get('/api/health')
    data = json.loads(response.data)
    
    assert 'status' in data
    assert 'message' in data


@pytest.mark.integration
def test_health_check_response_values(client):
    """Test that health check response has correct values."""
    response = client.get('/api/health')
    data = json.loads(response.data)
    
    assert data['status'] == 'ok'
    assert data['message'] == 'Flask backend is running'

