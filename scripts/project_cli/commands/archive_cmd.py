"""
Archive command implementation.

Archives a project by setting classification to 'archive' and status to 'completed'.
"""

import click
from rich.console import Console
from rich.table import Table
from ..api_client import APIClient
from ..error_handler import handle_error


@click.command()
@click.argument('project_id', type=int)
def archive_project(project_id):
    """Archive a project."""
    console = Console()
    
    try:
        # Archive project via API
        client = APIClient()
        project = client.archive_project(project_id)
        
        # Display success
        console.print(f"[green]✓ Archived project #{project['id']}: {project['name']}[/green]")
        
        # Display project details in a table
        table = Table(title="Archived Project", show_header=False)
        table.add_column("Field", style="cyan", justify="right")
        table.add_column("Value", style="green")
        
        table.add_row("ID", str(project['id']))
        table.add_row("Name", project['name'])
        if project.get('path'):
            table.add_row("Path", project['path'])
        if project.get('organization'):
            table.add_row("Organization", project['organization'])
        table.add_row("Classification", project.get('classification', 'N/A'))
        table.add_row("Status", project.get('status', 'N/A'))
        if project.get('description'):
            table.add_row("Description", project['description'])
        if project.get('remote_url'):
            table.add_row("Remote URL", project['remote_url'])
        table.add_row("Updated", project['updated_at'][:19].replace('T', ' ') if project.get('updated_at') else 'N/A')
        
        console.print(table)
        
    except Exception as e:
        handle_error(e, console)
        raise click.Abort() from e

