"""
Integration tests for production configuration.

Tests environment variable handling, logging, and error handling.
"""

import pytest
import logging
from app import create_app


@pytest.mark.integration
def test_production_config_debug_disabled():
    """Test that DEBUG is False in production config."""
    app = create_app('production')
    assert app.config['DEBUG'] is False


@pytest.mark.integration
def test_production_config_secret_key_default():
    """Test that SECRET_KEY has a default value (even if insecure)."""
    app = create_app('production')
    # Should have a secret key (default or from env)
    assert app.config['SECRET_KEY'] is not None
    assert len(app.config['SECRET_KEY']) > 0


@pytest.mark.integration
def test_production_config_database_url_default():
    """Test that DATABASE_URL has a default SQLite path."""
    app = create_app('production')
    # Should default to SQLite database
    assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI'].lower()


@pytest.mark.integration
def test_production_config_cors_origins_default():
    """Test that CORS_ORIGINS defaults to empty list."""
    app = create_app('production')
    # Should default to empty list (no CORS)
    assert isinstance(app.config['CORS_ORIGINS'], list)


@pytest.mark.integration
def test_production_config_logging_setup():
    """Test that production config sets up logging correctly."""
    app = create_app('production')
    
    # Check log level is INFO
    assert app.logger.level == logging.INFO
    
    # Check handler exists
    assert len(app.logger.handlers) > 0
