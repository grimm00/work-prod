"""
List command implementation.

Displays all projects in a formatted table.
"""

import click
from rich.console import Console
from rich.table import Table
from ..api_client import APIClient


@click.command()
@click.option(
    '--status', '-s',
    type=click.Choice(['active', 'paused', 'completed', 'cancelled'], case_sensitive=False),
    help='Filter by status (active, paused, completed, cancelled)'
)
@click.option('--org', '-o', 'organization', help='Filter by organization name')
@click.option(
    '--classification', '-c',
    type=click.Choice(['primary', 'secondary', 'archive', 'maintenance'], case_sensitive=False),
    help='Filter by classification (primary, secondary, archive, maintenance)'
)
@click.option('--search', help='Search in project names and descriptions')
@click.option('--wide', is_flag=True, help='Show all columns (status, organization, classification) and use full-width layout')
def list_projects(status, organization, classification, search, wide):
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
        
        # Create table with expand=True to use full terminal width
        table = Table(title=f"Projects ({len(projects)})", expand=True)
        table.add_column("ID", style="cyan", justify="right")
        table.add_column("Name", style="green", no_wrap=False)  # Allow wrapping
        
        # Add additional columns if --wide flag is set
        if wide:
            table.add_column("Status", style="yellow")
            table.add_column("Org", style="blue")
            table.add_column("Classification", style="magenta")
        
        table.add_column("Path", style="blue", no_wrap=False)  # Allow wrapping
        table.add_column("Created", style="magenta")
        
        # Add rows conditionally based on --wide flag
        for project in projects:
            row_data = [
                str(project['id']),
                project['name'],
            ]
            if wide:
                row_data.extend([
                    project.get('status', 'N/A'),
                    project.get('organization', 'N/A'),
                    project.get('classification', 'N/A'),
                ])
            row_data.extend([
                project['path'] or "[dim]No path[/dim]",
                project['created_at'][:10]  # Just the date
            ])
            table.add_row(*row_data)
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort() from e

