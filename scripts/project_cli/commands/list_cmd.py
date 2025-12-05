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
        
        # Determine which columns to show:
        # - Show Status if --wide flag OR --status filter is used
        # - Show Org if --wide flag OR --org filter is used
        # - Show Classification if --wide flag OR --classification filter is used
        # - Show Description if --wide flag OR --search filter is used (to show where match occurred)
        show_status = wide or status is not None
        show_org = wide or organization is not None
        show_classification = wide or classification is not None
        show_description = wide or search is not None
        
        # Add columns based on filters and --wide flag
        if show_status:
            table.add_column("Status", style="yellow")
        if show_org:
            table.add_column("Org", style="blue")
        if show_classification:
            table.add_column("Classification", style="magenta")
        
        table.add_column("Path", style="blue", no_wrap=False)  # Allow wrapping
        
        # Add Description column if searching or using --wide
        if show_description:
            table.add_column("Description", style="dim", no_wrap=False)  # Allow wrapping
        
        table.add_column("Created", style="magenta")
        
        # Add rows conditionally based on visible columns
        for project in projects:
            row_data = [
                str(project['id']),
                project['name'],
            ]
            if show_status:
                row_data.append(project.get('status', 'N/A'))
            if show_org:
                row_data.append(project.get('organization', 'N/A'))
            if show_classification:
                row_data.append(project.get('classification', 'N/A'))
            
            row_data.append(project['path'] or "[dim]No path[/dim]")
            
            # Add Description column if searching or using --wide
            if show_description:
                description = project.get('description', '')
                row_data.append(description or "[dim]No description[/dim]")
            
            row_data.append(project['created_at'][:10])  # Just the date
            table.add_row(*row_data)
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort() from e

