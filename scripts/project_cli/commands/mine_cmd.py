"""
Mine command implementation.

Shows projects for current user/organization.
"""

import click
import os
from rich.console import Console
from ..api_client import APIClient
from .list_cmd import build_projects_table


@click.command()
@click.option('--org', '-o', help='Organization name (defaults to PROJ_ORG env var or "work")')
@click.option('--wide', is_flag=True, help='Show all columns')
def mine(org, wide):
    """Show projects for current user/organization."""
    console = Console()
    
    try:
        # Determine organization
        if not org:
            org = os.environ.get('PROJ_ORG', 'work')
        
        client = APIClient()
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
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort() from e

