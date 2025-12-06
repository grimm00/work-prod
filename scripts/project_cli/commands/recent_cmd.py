"""
Recent command implementation.

Shows recently updated projects.
"""

import click
from rich.console import Console
from ..api_client import APIClient
from ..error_handler import handle_error
from .list_cmd import build_projects_table


@click.command()
@click.option('--limit', '-n', default=10, help='Number of recent projects to show (default: 10)')
def recent(limit):
    """Show recently updated projects."""
    console = Console()
    
    try:
        client = APIClient()
        projects = client.list_projects()
        
        if not projects:
            console.print("[yellow]No projects found.[/yellow]")
            return
        
        # Sort by updated_at (most recent first)
        # Note: API doesn't currently return updated_at, so we'll sort by created_at for now
        # This will be improved when API adds updated_at field
        projects_sorted = sorted(
            projects,
            key=lambda p: p.get('created_at', ''),
            reverse=True
        )
        
        # Limit results
        recent_projects = projects_sorted[:limit]
        
        # Display in table format
        table = build_projects_table(
            recent_projects,
            wide=True,  # Show all columns for recent projects
            status=None,
            organization=None,
            classification=None,
            search=None
        )
        table.title = f"Recently Updated Projects (showing {len(recent_projects)} of {len(projects)})"
        
        console.print(table)
        
    except Exception as e:
        handle_error(e, console)
        raise click.Abort() from e

