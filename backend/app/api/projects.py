"""
Projects API endpoints.

Provides REST API for managing projects including list, get, and create operations.
"""

from flask import Blueprint, jsonify, request, current_app
from app.models.project import Project
from app import db
from sqlalchemy.exc import IntegrityError

projects_bp = Blueprint('projects', __name__)


# Validation constants
VALID_CLASSIFICATIONS = ['primary', 'secondary', 'archive', 'maintenance']
VALID_STATUSES = ['active', 'paused', 'completed', 'cancelled']


@projects_bp.route('/projects', methods=['GET', 'POST'])
def projects():
    """
    Handle GET and POST requests for projects collection.
    
    GET: List all projects
    POST: Create a new project
    """
    if request.method == 'GET':
        return list_projects()
    elif request.method == 'POST':
        return create_project()


def list_projects():
    """
    List all projects with optional filtering.
    
    Query parameters:
        - status: Filter by status (active, paused, completed, cancelled)
        - organization: Filter by organization name
        - classification: Filter by classification (primary, secondary, archive, maintenance)
    
    Returns:
        JSON array of projects ordered by ID, filtered by query parameters
    """
    query = Project.query
    
    # Filter by status
    if 'status' in request.args:
        status = request.args['status']
        if status in VALID_STATUSES:
            query = query.filter_by(status=status)
        # If invalid status, ignore filter (return all projects)
    
    # Filter by organization
    if 'organization' in request.args:
        organization = request.args['organization']
        if organization:  # Non-empty string
            query = query.filter_by(organization=organization)
    
    # Filter by classification
    if 'classification' in request.args:
        classification = request.args['classification']
        if classification in VALID_CLASSIFICATIONS:
            query = query.filter_by(classification=classification)
        # If invalid classification, ignore filter (return all projects)
    
    projects = query.order_by(Project.id).all()
    return jsonify([project.to_dict() for project in projects]), 200


def create_project():
    """
    Create a new project.
    
    Request body (JSON):
        - name (required): Project name
        - path (optional): File system path
        - organization (optional): Organization name
        - classification (optional): Project classification
        - status (optional): Project status (defaults to 'active')
        - description (optional): Project description
        - remote_url (optional): Git repository URL
    
    Returns:
        201: Created project with Location header
        400: Validation error
        409: Duplicate path conflict
    """
    data = request.get_json()
    
    # Validate required fields
    if not data or 'name' not in data or not data['name']:
        return jsonify({'error': 'Name is required'}), 400
    
    # Validate classification if provided
    if 'classification' in data and data['classification'] is not None:
        if data['classification'] not in VALID_CLASSIFICATIONS:
            return jsonify({
                'error': f"Invalid classification. Must be one of: {', '.join(VALID_CLASSIFICATIONS)}"
            }), 400
    
    # Validate status if provided
    if 'status' in data:
        if data['status'] is None:
            return jsonify({'error': 'Status cannot be null'}), 400
        if data['status'] not in VALID_STATUSES:
            return jsonify({
                'error': f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"
            }), 400
    
    # Check for duplicate path
    if 'path' in data and data['path']:
        existing = Project.query.filter_by(path=data['path']).first()
        if existing:
            return jsonify({'error': 'Project with this path already exists'}), 409
    
    # Create project
    try:
        project = Project(
            name=data['name'],
            path=data.get('path'),
            organization=data.get('organization'),
            classification=data.get('classification'),
            status=data.get('status', 'active'),
            description=data.get('description'),
            remote_url=data.get('remote_url')
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify(project.to_dict()), 201, {
            'Location': f'/api/projects/{project.id}'
        }
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database integrity error'}), 409
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error in create_project: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@projects_bp.route('/projects/<int:project_id>', methods=['GET', 'PATCH', 'DELETE'])
def project_detail(project_id):
    """
    Handle GET, PATCH, and DELETE requests for a specific project.
    
    GET: Retrieve project details
    PATCH: Update project fields
    DELETE: Permanently delete project
    """
    if request.method == 'GET':
        return get_project(project_id)
    elif request.method == 'PATCH':
        return update_project(project_id)
    elif request.method == 'DELETE':
        return delete_project(project_id)


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


def update_project(project_id):
    """
    Update an existing project.
    
    Request body (JSON): Fields to update (all optional)
        - name: Project name
        - path: File system path
        - organization: Organization name
        - classification: Project classification
        - status: Project status
        - description: Project description
        - remote_url: Git repository URL
    
    Returns:
        200: Updated project
        400: Validation error
        404: Project not found
        409: Duplicate path conflict
    """
    project = db.session.get(Project, project_id)
    
    if project is None:
        return jsonify({'error': 'Project not found'}), 404
    
    data = request.get_json()
    if not data:
        # No updates provided - return current project
        return jsonify(project.to_dict()), 200
    
    # Validate classification if provided
    if 'classification' in data and data['classification'] is not None:
        if data['classification'] not in VALID_CLASSIFICATIONS:
            return jsonify({
                'error': f"Invalid classification. Must be one of: {', '.join(VALID_CLASSIFICATIONS)}"
            }), 400
    
    # Validate status if provided
    if 'status' in data:
        if data['status'] is None:
            return jsonify({'error': 'Status cannot be null'}), 400
        if data['status'] not in VALID_STATUSES:
            return jsonify({
                'error': f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"
            }), 400
    
    # Check for duplicate path if updating path
    if 'path' in data and data['path'] and data['path'] != project.path:
        existing = Project.query.filter_by(path=data['path']).first()
        if existing:
            return jsonify({'error': 'Project with this path already exists'}), 409
    
    # Update fields that are provided
    try:
        if 'name' in data:
            project.name = data['name']
        if 'path' in data:
            project.path = data['path']
        if 'organization' in data:
            project.organization = data['organization']
        if 'classification' in data:
            project.classification = data['classification']
        if 'status' in data:
            project.status = data['status']
        if 'description' in data:
            project.description = data['description']
        if 'remote_url' in data:
            project.remote_url = data['remote_url']
        
        db.session.commit()
        
        return jsonify(project.to_dict()), 200
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database integrity error'}), 409
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error in update_project: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


def delete_project(project_id):
    """
    Delete a project permanently.
    
    Returns:
        204: Project deleted successfully (No Content)
        404: Project not found
    """
    project = db.session.get(Project, project_id)
    
    if project is None:
        return jsonify({'error': 'Project not found'}), 404
    
    try:
        db.session.delete(project)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error in delete_project: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@projects_bp.route('/projects/<int:project_id>/archive', methods=['PUT'])
def archive_project(project_id):
    """
    Archive a project by setting classification to 'archive' and status to 'completed'.
    
    Returns:
        200: Project archived successfully (returns updated project)
        404: Project not found
    """
    project = db.session.get(Project, project_id)
    
    if project is None:
        return jsonify({'error': 'Project not found'}), 404
    
    try:
        project.classification = 'archive'
        project.status = 'completed'
        db.session.commit()
        return jsonify(project.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error in archive_project: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


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

