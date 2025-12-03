"""
Flask application configuration.

Provides environment-specific configuration classes for development, testing, and production.
"""

import os
from pathlib import Path


class Config:
    """Base configuration with common settings."""
    
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Get the base directory (backend directory)
    BASE_DIR = Path(__file__).parent
    
    # CORS settings (override in subclasses)
    CORS_ORIGINS = []
    
    @staticmethod
    def init_app(app):
        """Initialize application with config-specific settings."""
        pass


class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{Config.BASE_DIR / 'instance' / 'work_prod_dev.db'}"
    
    # Enable Flask debug toolbar if available
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    
    # CORS: Allow localhost development servers
    CORS_ORIGINS = [
        'http://localhost:5173',  # Vite dev server
        'http://localhost:3000',  # Alternative frontend port
    ]


class TestingConfig(Config):
    """Testing configuration."""
    
    TESTING = True
    DEBUG = True
    
    # Use in-memory SQLite database for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # CORS: Allow test client
    CORS_ORIGINS = ['http://localhost:5173']


class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{Config.BASE_DIR / 'instance' / 'work_prod.db'}"
    
    # CORS: Load from environment variable (comma-separated origins)
    CORS_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',') if os.environ.get('CORS_ALLOWED_ORIGINS') else []
    
    @classmethod
    def init_app(cls, app):
        """Initialize production-specific settings."""
        Config.init_app(app)
        
        # Only add handler if not already present (prevent duplicates)
        if not app.logger.handlers:
            import logging
            from logging import StreamHandler
            
            handler = StreamHandler()
            handler.setLevel(logging.INFO)
            
            # Add formatter with timestamp, level, and module
            formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
            )
            handler.setFormatter(formatter)
            
            app.logger.addHandler(handler)
            app.logger.setLevel(logging.INFO)


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

