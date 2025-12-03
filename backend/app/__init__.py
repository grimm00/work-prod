"""
Flask application factory.

This module provides the create_app factory function for creating Flask application
instances with appropriate configuration.
"""

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='default'):
    """
    Application factory for creating Flask app instances.
    
    Args:
        config_name: Configuration to use ('development', 'testing', 'production')
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Import models to register with SQLAlchemy
    with app.app_context():
        from app import models
    
    # Register blueprints
    from app.api.health import health_bp
    from app.api.projects import projects_bp
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(projects_bp, url_prefix='/api')
    
    return app

