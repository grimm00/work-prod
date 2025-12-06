"""
Active command implementation.

Shortcut for listing active projects.
"""

import click
from rich.console import Console
from ..api_client import APIClient
from ..error_handler import handle_error
from ..progress import spinner
from .list_cmd import build_projects_table


@click.command()
@click.option('--wide', is_flag=True, help='Show all columns')
def active(wide):
    """Show active projects (shortcut for 'proj list --status active')."""
    console = Console()
    
    try:
        client = APIClient()
        with spinner(console, "Fetching active projects..."):
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
        handle_error(e, console)
        raise click.Abort() from e

