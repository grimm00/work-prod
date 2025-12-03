"""
List command implementation.

Displays all projects in a formatted table.
"""

import click
from rich.console import Console
from rich.table import Table
from project_cli.api_client import APIClient


@click.command()
def list_projects():
    """List all projects."""
    console = Console()
    
    try:
        # Fetch projects from API
        client = APIClient()
        projects = client.list_projects()
        
        if not projects:
            console.print("[yellow]No projects found.[/yellow]")
            return
        
        # Create table
        table = Table(title=f"Projects ({len(projects)})")
        table.add_column("ID", style="cyan", justify="right")
        table.add_column("Name", style="green")
        table.add_column("Path", style="blue")
        table.add_column("Created", style="magenta")
        
        # Add rows
        for project in projects:
            table.add_row(
                str(project['id']),
                project['name'],
                project['path'] or "[dim]No path[/dim]",
                project['created_at'][:10]  # Just the date
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()

