"""
Configuration file management for the CLI.

Supports loading settings from ~/.projrc file.
"""

import os
import configparser
from pathlib import Path


class Config:
    """Configuration manager for CLI settings."""
    
    # Class-level instance for singleton pattern
    _instance = None
    
    DEFAULT_CONFIG = {
        'api': {
            'base_url': 'http://localhost:5000/api'
        },
        'display': {
            'max_rows': '50',
            'color': 'true'
        }
    }
    
    def __new__(cls):
        """Singleton pattern - return same instance."""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Only initialize once
        if hasattr(self, 'config'):
            return
        
        self.config_file = Path.home() / '.projrc'
        self.config = configparser.ConfigParser()
        self._load_config()
    
    @classmethod
    def get_instance(cls):
        """Get the singleton Config instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from ~/.projrc or use defaults."""
        # Set defaults
        for section, options in self.DEFAULT_CONFIG.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            for key, value in options.items():
                self.config.set(section, key, value)
        
        # Load from file if it exists
        if self.config_file.exists():
            try:
                self.config.read(self.config_file)
            except (configparser.Error, IOError) as e:
                # If config file is invalid, use defaults
                pass
    
    def get(self, section, key, fallback=None):
        """Get a configuration value."""
        try:
            return self.config.get(section, key, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    def get_api_url(self):
        """Get the API base URL (environment variable takes precedence)."""
        # Environment variable override
        env_url = os.environ.get('PROJ_API_URL')
        if env_url:
            return env_url
        return self.get('api', 'base_url', 'http://localhost:5000/api')
    
    def get_max_rows(self):
        """Get maximum rows to display."""
        default = 50
        value = self.get('display', 'max_rows', str(default))
        try:
            return int(value)
        except (TypeError, ValueError):
            return default
    
    def get_color_enabled(self):
        """Check if color output is enabled."""
        return self.get('display', 'color', 'true').lower() == 'true'
    
    def set(self, section, key, value):
        """Set a configuration value."""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
    
    def save(self):
        """Save configuration to ~/.projrc."""
        try:
            with open(self.config_file, 'w') as f:
                self.config.write(f)
        except IOError:
            # If we can't write to config file, silently fail
            pass
    
    def get_all(self):
        """Get all configuration as a dictionary, including defaults."""
        result = {}
        # Start with defaults
        for section, options in self.DEFAULT_CONFIG.items():
            result[section] = options.copy()
        
        # Override with actual config values
        for section in self.config.sections():
            if section not in result:
                result[section] = {}
            for key, value in self.config.items(section):
                result[section][key] = value
        
        return result
