"""
Integration tests for production configuration.

Tests environment variable handling, logging, and error handling.
"""

import pytest
import os
import logging
import importlib


@pytest.mark.integration
def test_production_config_debug_disabled():
    """Test that DEBUG is False in production config."""
    from app import create_app
    app = create_app('production')
    assert app.config['DEBUG'] is False


@pytest.mark.integration
def test_production_config_secret_key_from_env(monkeypatch):
    """Test that SECRET_KEY can be loaded from environment variable."""
    test_key = 'test-secret-key-from-env'
    monkeypatch.setenv('SECRET_KEY', test_key)
    
    # Reload config module to pick up new env var
    import config
    importlib.reload(config)
    
    from app import create_app
    app = create_app('production')
    assert app.config['SECRET_KEY'] == test_key


@pytest.mark.integration
def test_production_config_database_url_from_env(monkeypatch):
    """Test that DATABASE_URL can be loaded from environment variable."""
    test_db_url = 'sqlite:///test_production.db'
    monkeypatch.setenv('DATABASE_URL', test_db_url)
    
    # Reload config module to pick up new env var
    import config
    importlib.reload(config)
    
    from app import create_app
    app = create_app('production')
    assert app.config['SQLALCHEMY_DATABASE_URI'] == test_db_url


@pytest.mark.integration
def test_production_config_cors_origins_from_env(monkeypatch):
    """Test that CORS_ALLOWED_ORIGINS can be loaded from environment variable."""
    test_origins = 'https://example.com,https://app.example.com'
    monkeypatch.setenv('CORS_ALLOWED_ORIGINS', test_origins)
    
    # Reload config module to pick up new env var
    import config
    importlib.reload(config)
    
    from app import create_app
    app = create_app('production')
    assert 'https://example.com' in app.config['CORS_ORIGINS']
    assert 'https://app.example.com' in app.config['CORS_ORIGINS']


@pytest.mark.integration
def test_production_config_logging_setup():
    """Test that production config sets up logging correctly."""
    from app import create_app
    app = create_app('production')
    
    # Check log level is INFO
    assert app.logger.level == logging.INFO
    
    # Check handler exists
    assert len(app.logger.handlers) > 0


@pytest.mark.integration
def test_production_config_app_config_precedence(monkeypatch):
    """Test that APP_CONFIG takes precedence over FLASK_ENV."""
    monkeypatch.setenv('APP_CONFIG', 'production')
    monkeypatch.setenv('FLASK_ENV', 'development')
    
    # Reload run module to pick up new env vars
    import run
    importlib.reload(run)
    
    # Should use APP_CONFIG (production)
    from app import create_app
    app = create_app(run.config_name)
    assert app.config['DEBUG'] is False


@pytest.mark.integration
def test_production_config_fallback_to_flask_env(monkeypatch):
    """Test that FLASK_ENV is used if APP_CONFIG not set."""
    monkeypatch.delenv('APP_CONFIG', raising=False)
    monkeypatch.setenv('FLASK_ENV', 'production')
    
    # Reload run module to pick up new env vars
    import run
    importlib.reload(run)
    
    # Should use FLASK_ENV (production)
    assert run.config_name == 'production'

