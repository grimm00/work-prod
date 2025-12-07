#!/bin/bash
# Production startup script for Flask backend

set -e  # Exit on error

# Change to backend directory
cd "$(dirname "$0")"

# Activate virtual environment
if [ -d "../venv" ]; then
    source ../venv/bin/activate
else
    echo "Error: Virtual environment not found at ../venv"
    echo "Please create virtual environment: python3 -m venv venv"
    exit 1
fi

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    set -a  # Automatically export all variables
    source .env 2>/dev/null || true
    set +a  # Turn off automatic export
fi

# Ensure production config
export APP_CONFIG=production

# Apply database migrations (always run, not just on first deploy)
echo "Applying database migrations..."
flask db upgrade

# Check if Gunicorn is installed
if ! command -v gunicorn &> /dev/null; then
    echo "Installing Gunicorn..."
    pip install gunicorn
fi

# Start Gunicorn
echo "Starting production server..."
exec gunicorn \
    -w 4 \
    -b 0.0.0.0:5000 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --timeout 120 \
    --preload \
    "app:create_app('production')"

