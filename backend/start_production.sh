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
    export $(cat .env | grep -v '^#' | xargs)
fi

# Ensure production config
export APP_CONFIG=production

# Verify database exists and is initialized
if [ ! -f instance/work_prod.db ]; then
    echo "Initializing database..."
    flask db upgrade
fi

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

