"""
Delete command implementation.

Deletes a project permanently with confirmation.
"""

import click
from rich.console import Console
from rich.prompt import Confirm
from project_cli.api_client import APIClient


@click.command()
@click.argument('project_id', type=int)
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation prompt')
def delete_project(project_id, yes):
    """Delete a project permanently."""
    console = Console()
    
    try:
        # Get project details first for confirmation
        client = APIClient()
        project = client.get_project(project_id)
        
        # Confirm deletion unless --yes flag is used
        if not yes:
            console.print(f"[yellow]Warning: This will permanently delete project #{project_id}: {project['name']}[/yellow]")
            if not Confirm.ask("Are you sure you want to delete this project?", default=False):
                console.print("[yellow]Deletion cancelled.[/yellow]")
                return
        
        # Delete project
        client.delete_project(project_id)
        
        # Display success
        console.print(f"[green]✓ Deleted project #{project_id}: {project['name']}[/green]")
        
    except Exception as e:
        error_msg = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                if 'error' in error_data:
                    error_msg = error_data['error']
            except:
                pass
        console.print(f"[red]✗ Error: {error_msg}[/red]")
        raise click.Abort()

