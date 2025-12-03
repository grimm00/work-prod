"""
CLI configuration.

Manages API endpoint configuration for the CLI tool.
"""

import os
from pathlib import Path


class Config:
    """CLI configuration settings."""
    
    # API endpoint (default to localhost development server)
    API_BASE_URL = os.environ.get('PROJ_API_URL', 'http://localhost:5000/api')
    
    # Config directory
    CONFIG_DIR = Path.home() / '.proj'
    CONFIG_FILE = CONFIG_DIR / 'config.json'
    
    @classmethod
    def ensure_config_dir(cls):
        """Ensure config directory exists."""
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

