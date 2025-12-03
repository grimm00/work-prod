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
config_name = os.environ.get('APP_CONFIG', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    # Run development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )

