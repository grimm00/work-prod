"""
Update command implementation.

Updates an existing project's details.
"""

import click
from rich.console import Console
from rich.table import Table
from ..api_client import APIClient
from ..error_handler import handle_error


@click.command()
@click.argument('project_id', type=int)
@click.option('--name', '-n', help='Project name')
@click.option('--path', '-p', help='Project file system path')
@click.option('--organization', '-o', help='Organization (e.g., work, personal)')
@click.option('--classification', '-c',
              type=click.Choice(['primary', 'secondary', 'archive', 'maintenance'], case_sensitive=False),
              help='Project classification')
@click.option('--status', '-s',
              type=click.Choice(['active', 'paused', 'completed', 'cancelled'], case_sensitive=False),
              help='Project status')
@click.option('--description', '-d', help='Project description')
@click.option('--remote-url', '-r', help='Git repository URL')
def update_project(project_id, name, path, organization, classification, status, description, remote_url):
    """Update an existing project."""
    console = Console()
    
    try:
        # Build update data (only include provided fields)
        data = {}
        
        if name is not None:
            data['name'] = name
        if path is not None:
            data['path'] = path
        if organization is not None:
            data['organization'] = organization
        if classification is not None:
            data['classification'] = classification.lower()
        if status is not None:
            data['status'] = status.lower()
        if description is not None:
            data['description'] = description
        if remote_url is not None:
            data['remote_url'] = remote_url
        
        if not data:
            console.print("[yellow]No updates provided. Use --help to see available options.[/yellow]")
            return
        
        # Get original project for comparison
        client = APIClient()
        try:
            original = client.get_project(project_id)
        except Exception as e:
            handle_error(e, console)
            raise click.Abort() from e
        
        # Update project via API
        updated = client.update_project(project_id, data)
        
        # Display success
        console.print(f"[green]✓ Updated project #{updated['id']}: {updated['name']}[/green]")
        
        # Show before/after comparison
        table = Table(title="Changes", show_header=True)
        table.add_column("Field", style="cyan", justify="right")
        table.add_column("Before", style="yellow")
        table.add_column("After", style="green")
        
        # Only show fields that were updated
        for field in data.keys():
            old_value = original.get(field, '')
            new_value = updated.get(field, '')
            
            # Format None values
            if old_value is None:
                old_value = '[dim]None[/dim]'
            if new_value is None:
                new_value = '[dim]None[/dim]'
            
            # Only show if changed
            if str(old_value) != str(new_value):
                table.add_row(field.replace('_', ' ').title(), str(old_value), str(new_value))
        
        if table.row_count > 0:
            console.print(table)
        else:
            console.print("[dim]No fields changed.[/dim]")
        
    except Exception as e:
        handle_error(e, console)
        raise click.Abort() from e

