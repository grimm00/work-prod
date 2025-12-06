"""
Delete command implementation.

Deletes a project permanently with confirmation.
"""

import click
from rich.console import Console
from rich.prompt import Confirm
from ..api_client import APIClient
from ..error_handler import handle_error
from ..progress import spinner


@click.command()
@click.argument('project_id', type=int)
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation prompt')
def delete_project(project_id, yes):
    """Delete a project permanently."""
    console = Console()
    
    try:
        # Get project details first for confirmation
        client = APIClient()
        with spinner(console, f"Fetching project #{project_id}..."):
            project = client.get_project(project_id)
        
        # Confirm deletion unless --yes flag is used
        if not yes:
            console.print(f"[yellow]Warning: This will permanently delete project #{project_id}: {project['name']}[/yellow]")
            if not Confirm.ask("Are you sure you want to delete this project?", default=False):
                console.print("[yellow]Deletion cancelled.[/yellow]")
                return
        
        # Delete project
        with spinner(console, f"Deleting project #{project_id}..."):
            client.delete_project(project_id)
        
        # Display success
        console.print(f"[green]✓ Deleted project #{project_id}: {project['name']}[/green]")
        
    except Exception as e:
        handle_error(e, console)
        raise click.Abort() from e

