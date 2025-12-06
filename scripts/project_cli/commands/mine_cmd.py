"""
Mine command implementation.

Shows projects for current user/organization.
"""

import click
import os
from rich.console import Console
from ..api_client import APIClient
from ..error_handler import handle_error
from ..progress import spinner
from .list_cmd import build_projects_table


@click.command()
@click.option('--org', '-o', 
              help='Organization name (defaults to PROJ_ORG env var or "work")')
@click.option('--wide', is_flag=True, 
              help='Show all columns (status, organization, classification)')
def mine(org, wide):
    """
    Show projects for current user/organization.
    
    Display projects filtered by organization. Defaults to "work" organization
    or the value of PROJ_ORG environment variable if set.
    
    \b
    Examples:
        proj mine
        proj mine --org personal
        proj mine -o learning --wide
    """
    console = Console()
    
    try:
        # Determine organization
        if not org:
            org = os.environ.get('PROJ_ORG', 'work')
        
        client = APIClient()
        with spinner(console, f"Fetching projects for {org}..."):
            projects = client.list_projects(organization=org)
        
        if not projects:
            console.print(f"[yellow]No projects found for organization: {org}[/yellow]")
            return
        
        # Display in table format
        table = build_projects_table(
            projects,
            wide=wide,
            status=None,
            organization=org,  # This will show Org column
            classification=None,
            search=None
        )
        table.title = f"My Projects ({org}) - {len(projects)} projects"
        
        console.print(table)
        
    except Exception as e:
        handle_error(e, console)
        raise click.Abort() from e

