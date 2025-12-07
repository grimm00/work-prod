"""
Development server entry point.

Run this script to start the Flask development server.
"""

import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

# Create Flask app with explicit configuration
# APP_CONFIG can be: 'development', 'testing', 'production'
# Backwards compatibility: Falls back to FLASK_ENV if APP_CONFIG not set
# Priority: APP_CONFIG > FLASK_ENV > 'development'
config_name = os.environ.get('APP_CONFIG') or os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    # Run development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )

