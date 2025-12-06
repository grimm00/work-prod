"""
Import command implementation.

Imports multiple projects from a JSON file.
"""

import json
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from ..api_client import APIClient
from ..error_handler import handle_error
from ..progress import progress_bar


@click.command()
@click.argument('file', type=click.Path(exists=True, readable=True, path_type=Path))
def import_projects(file):
    """
    Import projects from a JSON file.
    
    Bulk import multiple projects from a JSON file. Shows progress bar during import
    and displays statistics (imported, skipped, errors) after completion.
    Projects with duplicate paths or names are automatically skipped.
    
    \b
    FILE: Path to JSON file containing projects data.
    
    Expected JSON format:
    {
        "projects": [
            {
                "name": "Project Name",
                "path": "/optional/path",
                "organization": "work",
                "classification": "primary",
                "status": "active",
                "description": "Project description",
                "remote_url": "https://github.com/user/repo.git"
            },
            ...
        ]
    }
    
    \b
    Examples:
        proj import projects.json
        proj import ../data/projects.json
        proj import ~/backup/projects-2025.json
    """
    console = Console()
    client = APIClient()
    
    # Read JSON file
    try:
        with open(file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        console.print(f"[red]Error: Invalid JSON in file: {e}[/red]")
        raise click.Abort() from e
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        raise click.Abort() from e
    
    # Validate data structure
    if 'projects' not in data:
        console.print("[red]Error: JSON file must contain 'projects' key[/red]")
        raise click.Abort()
    
    if not isinstance(data['projects'], list):
        console.print("[red]Error: 'projects' must be an array[/red]")
        raise click.Abort()
    
    projects_count = len(data['projects'])
    
    # Import projects with progress bar
    try:
        with progress_bar(console, projects_count, f"Importing {projects_count} project(s)") as progress:
            task = progress.add_task(f"Importing from {file.name}", total=projects_count)
            result = client.import_projects(data)
            progress.update(task, completed=projects_count)
        
        # Display results
        imported = result.get('imported', 0)
        skipped = result.get('skipped', 0)
        errors = result.get('errors', [])
        
        # Create results table
        table = Table(title="Import Results", show_header=True, header_style="bold cyan")
        table.add_column("Metric", style="cyan", width=20)
        table.add_column("Count", style="white", justify="right")
        
        table.add_row("Total Projects", str(projects_count))
        table.add_row("Imported", f"[green]{imported}[/green]")
        table.add_row("Skipped", f"[yellow]{skipped}[/yellow]")
        table.add_row("Errors", f"[red]{len(errors)}[/red]" if errors else "[green]0[/green]")
        
        # Display table in panel
        panel = Panel(
            table,
            title="[bold]Import Complete[/bold]",
            border_style="yellow" if errors else "green"
        )
        console.print(panel)
        
        # Display errors if any
        if errors:
            console.print("\n[red]Errors encountered:[/red]")
            error_table = Table(show_header=True, header_style="bold red")
            error_table.add_column("Project", style="cyan")
            error_table.add_column("Error", style="red")
            
            for error in errors:
                project_name = error.get('project', 'Unknown')
                error_msg = error.get('error', 'Unknown error')
                error_table.add_row(project_name, error_msg)
            
            console.print(error_table)
        
        # Success message
        if imported > 0:
            console.print(f"\n[green]✓ Successfully imported {imported} project(s)[/green]")
        if skipped > 0:
            console.print(f"[yellow]⊘ Skipped {skipped} project(s) (already exist)[/yellow]")
        
    except Exception as e:
        handle_error(e, console)
        raise click.Abort() from e

