"""
Helper module for loading the CLI module from the proj script file.

Since the proj file doesn't have a .py extension, we need to load it
manually by reading and executing its content.
"""

import sys
import importlib.util
from pathlib import Path


def load_cli():
    """
    Load the CLI module from the proj script file.
    
    Returns:
        The CLI click.Group object
    """
    # Add scripts directory to path so we can import project_cli
    scripts_dir = str(Path(__file__).parent.parent.parent.parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    
    proj_path = Path(__file__).parent.parent.parent / 'proj'
    if not proj_path.exists():
        raise FileNotFoundError(f"CLI script not found at {proj_path}")
    
    # Load the proj script file (it doesn't have .py extension, so we need to exec it)
    proj_module = importlib.util.module_from_spec(
        importlib.util.spec_from_loader("proj", loader=None)
    )
    # Create a custom loader that reads and execs the file
    proj_module.__file__ = str(proj_path.resolve())
    with open(proj_path.resolve(), 'r', encoding='utf-8') as f:
        code = compile(f.read(), str(proj_path.resolve()), 'exec')
        exec(code, proj_module.__dict__)
    
    return proj_module.cli

