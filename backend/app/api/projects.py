"""
Projects API endpoints.

Provides REST API for managing projects including list and get operations.
"""

from flask import Blueprint, jsonify, request
from app.models.project import Project
from app import db

projects_bp = Blueprint('projects', __name__)


@projects_bp.route('/projects', methods=['GET'])
def list_projects():
    """
    List all projects.
    
    Returns:
        JSON array of all projects ordered by ID
    """
    projects = Project.query.order_by(Project.id).all()
    return jsonify([project.to_dict() for project in projects]), 200


@projects_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """
    Get a specific project by ID.
    
    Args:
        project_id: Integer ID of the project
        
    Returns:
        JSON object of the project
        
    Raises:
        404: Project not found
    """
    project = db.session.get(Project, project_id)
    
    if project is None:
        return jsonify({'error': 'Project not found'}), 404
    
    return jsonify(project.to_dict()), 200


@projects_bp.route('/projects/<project_id>', methods=['GET'])
def get_project_invalid(project_id):
    """
    Handle invalid project ID format.
    
    This route catches non-integer IDs and returns 400 Bad Request.
    """
    return jsonify({'error': 'Invalid project ID format'}), 400


@projects_bp.errorhandler(ValueError)
def handle_value_error(error):
    """Handle ValueError exceptions (e.g., invalid ID format)."""
    return jsonify({'error': 'Invalid project ID format'}), 400

