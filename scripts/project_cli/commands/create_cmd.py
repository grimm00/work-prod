"""
Create command implementation.

Creates a new project with the provided details.
"""

import click
from rich.console import Console
from rich.table import Table
from ..api_client import APIClient
from ..progress import spinner
from ..error_handler import handle_error


@click.command()
@click.option('--name', '-n', required=True, 
              help='Project name (required, must be unique)')
@click.option('--path', '-p', 
              help='Project file system path (must be unique if provided)')
@click.option('--organization', '-o', 
              help='Organization name (e.g., work, personal, learning)')
@click.option('--classification', '-c', 
              type=click.Choice(['primary', 'secondary', 'archive', 'maintenance'], case_sensitive=False),
              help='Project classification (primary, secondary, archive, maintenance)')
@click.option('--status', '-s',
              type=click.Choice(['active', 'paused', 'completed', 'cancelled'], case_sensitive=False),
              default='active',
              help='Project status (default: active)')
@click.option('--description', '-d', 
              help='Project description (supports multi-line text)')
@click.option('--remote-url', '-r', 
              help='Git repository URL (e.g., https://github.com/user/repo.git)')
def create_project(name, path, organization, classification, status, description, remote_url):
    """
    Create a new project.
    
    Create a project with the specified details. Name is required and must be unique.
    Path is optional but must be unique if provided.
    
    \b
    Examples:
        proj create --name "My Project"
        proj create -n "Work Project" --org work --classification primary
        proj create -n "Learning Python" -p /code/python-learning -d "Python tutorials"
        proj create -n "Open Source" -r https://github.com/user/repo.git
    """
    console = Console()
    
    try:
        # Build project data
        data = {'name': name}
        
        if path:
            data['path'] = path
        if organization:
            data['organization'] = organization
        if classification:
            data['classification'] = classification.lower()
        if status:
            data['status'] = status.lower()
        if description:
            data['description'] = description
        if remote_url:
            data['remote_url'] = remote_url
        
        # Create project via API
        client = APIClient()
        with spinner(console, f"Creating project '{name}'..."):
            project = client.create_project(data)
        
        # Display success
        console.print(f"[green]✓ Created project #{project['id']}: {project['name']}[/green]")
        
        # Display project details in a table
        table = Table(title="Project Details", show_header=False)
        table.add_column("Field", style="cyan", justify="right")
        table.add_column("Value", style="green")
        
        table.add_row("ID", str(project['id']))
        table.add_row("Name", project['name'])
        if project.get('path'):
            table.add_row("Path", project['path'])
        if project.get('organization'):
            table.add_row("Organization", project['organization'])
        if project.get('classification'):
            table.add_row("Classification", project['classification'])
        table.add_row("Status", project['status'])
        if project.get('description'):
            table.add_row("Description", project['description'])
        if project.get('remote_url'):
            table.add_row("Remote URL", project['remote_url'])
        table.add_row("Created", project['created_at'][:19].replace('T', ' '))
        
        console.print(table)
        
    except Exception as e:
        handle_error(e, console)
        raise click.Abort() from e

