"""
Active command implementation.

Shortcut for listing active projects.
"""

import click
from rich.console import Console
from ..api_client import APIClient
from .list_cmd import build_projects_table


@click.command()
@click.option('--wide', is_flag=True, help='Show all columns')
def active(wide):
    """Show active projects (shortcut for 'proj list --status active')."""
    console = Console()
    
    try:
        client = APIClient()
        projects = client.list_projects(status='active')
        
        if not projects:
            console.print("[yellow]No active projects found.[/yellow]")
            return
        
        # Display in table format
        table = build_projects_table(
            projects,
            wide=wide,
            status='active',  # This will show Status column
            organization=None,
            classification=None,
            search=None
        )
        table.title = f"Active Projects ({len(projects)})"
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort() from e

