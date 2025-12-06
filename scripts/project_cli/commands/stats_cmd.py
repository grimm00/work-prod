"""
Stats command implementation.

Displays project statistics.
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from ..api_client import APIClient
from ..error_handler import handle_error


@click.command()
def stats():
    """Show project statistics."""
    console = Console()
    
    try:
        client = APIClient()
        projects = client.list_projects()
        
        if not projects:
            console.print("[yellow]No projects found.[/yellow]")
            return
        
        # Calculate statistics
        total = len(projects)
        
        # By status
        status_counts = {}
        for project in projects:
            status = project.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # By organization
        org_counts = {}
        for project in projects:
            org = project.get('organization') or 'none'
            org_counts[org] = org_counts.get(org, 0) + 1
        
        # By classification
        classification_counts = {}
        for project in projects:
            classification = project.get('classification') or 'none'
            classification_counts[classification] = classification_counts.get(classification, 0) + 1
        
        # Display statistics
        console.print("\n[bold cyan]Project Statistics[/bold cyan]")
        console.print("=" * 50)
        
        # Total projects
        console.print(f"\n[bold]Total Projects:[/bold] {total}\n")
        
        # By status
        console.print("[bold]By Status:[/bold]")
        status_symbols = {
            'active': '●',
            'paused': '○',
            'completed': '✓',
            'cancelled': '✗'
        }
        for status in ['active', 'paused', 'completed', 'cancelled']:
            count = status_counts.get(status, 0)
            symbol = status_symbols.get(status, '•')
            console.print(f"  {symbol} {status}: {count}")
        
        # By organization
        console.print("\n[bold]By Organization:[/bold]")
        for org, count in sorted(org_counts.items(), key=lambda x: x[1], reverse=True):
            console.print(f"  • {org}: {count}")
        
        # By classification
        console.print("\n[bold]By Classification:[/bold]")
        classification_symbols = {
            'primary': '🥇',
            'secondary': '🥈',
            'archive': '📦',
            'maintenance': '🔧'
        }
        for classification in ['primary', 'secondary', 'archive', 'maintenance']:
            count = classification_counts.get(classification, 0)
            symbol = classification_symbols.get(classification, '•')
            console.print(f"  {symbol} {classification}: {count}")
        
        console.print()
        
    except Exception as e:
        handle_error(e, console)
        raise click.Abort() from e

