"""
List command implementation.

Displays all projects in a formatted table.
"""

import click
from rich.console import Console
from rich.table import Table
from ..api_client import APIClient


@click.command()
@click.option('--status', '-s', help='Filter by status (active, paused, completed, cancelled)')
@click.option('--org', '-o', 'organization', help='Filter by organization name')
@click.option('--classification', '-c', help='Filter by classification (primary, secondary, archive, maintenance)')
@click.option('--search', help='Search in project names and descriptions')
def list_projects(status, organization, classification, search):
    """List all projects with optional filtering."""
    console = Console()
    
    try:
        # Fetch projects from API with filters
        client = APIClient()
        projects = client.list_projects(
            status=status,
            organization=organization,
            classification=classification,
            search=search
        )
        
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
        raise click.Abort() from e

