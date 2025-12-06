"""
Get command implementation.

Displays details of a specific project.
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from ..api_client import APIClient
from ..error_handler import handle_error


@click.command()
@click.argument('project_id', type=int)
def get_project(project_id):
    """Get details of a specific project by ID."""
    console = Console()
    
    try:
        # Fetch project from API
        client = APIClient()
        project = client.get_project(project_id)
        
        # Create details table
        table = Table(show_header=False, box=None)
        table.add_column("Field", style="cyan", width=15)
        table.add_column("Value", style="white")
        
        table.add_row("ID", str(project['id']))
        table.add_row("Name", project['name'])
        table.add_row("Path", project['path'] or "[dim]No path[/dim]")
        table.add_row("Created", project['created_at'])
        table.add_row("Updated", project['updated_at'])
        
        # Display in panel
        panel = Panel(
            table,
            title=f"[bold]Project: {project['name']}[/bold]",
            border_style="green"
        )
        console.print(panel)
        
    except Exception as e:
        handle_error(e, console)
        raise click.Abort() from e

