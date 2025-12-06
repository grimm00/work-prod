"""
Health check API endpoint.

Provides a simple health check endpoint to verify the backend is running.
"""

from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.

    Returns:
        JSON response with status and message
    """
    return jsonify({
        'status': 'ok',
        'message': 'Flask backend is running'
    }), 200
