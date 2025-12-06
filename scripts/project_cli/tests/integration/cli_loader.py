"""
Helper module for loading the CLI module.

The CLI group is now exposed from a regular Python module (cli.py),
allowing direct import instead of executing the proj script file.
This provides a more robust and debuggable loading mechanism.
"""

import sys
from pathlib import Path


def load_cli():
    """
    Load the CLI group from the cli module.
    
    Returns:
        The CLI click.Group object
    """
    # Add scripts directory to path so we can import project_cli
    scripts_dir = str(Path(__file__).parent.parent.parent.parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    
    # Import CLI group directly from module
    from project_cli.cli import cli
    
    return cli

