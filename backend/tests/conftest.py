"""
Pytest configuration and shared fixtures.

Provides common test fixtures for Flask application testing.
"""

import pytest
from app import create_app, db


@pytest.fixture
def app():
    """
    Create and configure a test Flask application instance.
    
    Yields:
        Flask application configured for testing
    """
    app = create_app('testing')
    
    # Create application context
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Create a test client for the Flask application.
    
    Args:
        app: Flask application fixture
        
    Returns:
        Flask test client
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Create a test CLI runner for the Flask application.
    
    Args:
        app: Flask application fixture
        
    Returns:
        Flask CLI test runner
    """
    return app.test_cli_runner()

