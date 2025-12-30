"""
Pytest configuration for script tests.

Provides common test fixtures for script testing.
"""

import pytest
import sys
import os

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

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

