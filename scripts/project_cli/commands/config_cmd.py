"""
Configuration command implementation.

Allows users to view and edit CLI configuration settings.
"""

import click
from rich.console import Console
from rich.table import Table
from ..config import Config


@click.group()
def config_group():
    """Manage CLI configuration settings."""
    pass


@config_group.command('show')
def show_config():
    """Show current configuration settings."""
    console = Console()
    config = Config.get_instance()
    
    all_config = config.get_all()
    
    if not all_config:
        console.print("[yellow]No configuration found. Using defaults.[/yellow]")
        return
    
    table = Table(title="Configuration", show_header=True, header_style="bold cyan")
    table.add_column("Section", style="cyan")
    table.add_column("Key", style="green")
    table.add_column("Value", style="yellow")
    
    for section, options in all_config.items():
        for key, value in options.items():
            table.add_row(section, key, value)
    
    console.print(table)
    
    # Show config file location
    config_file = config.config_file
    console.print(f"\n[dim]Configuration file: {config_file}[/dim]")


@config_group.command('set')
@click.argument('section')
@click.argument('key')
@click.argument('value')
def set_config(section, key, value):
    """Set a configuration value.
    
    Examples:
        proj config set api base_url http://localhost:5000/api
        proj config set display max_rows 100
        proj config set display color false
    """
    console = Console()
    config = Config.get_instance()
    
    try:
        config.set(section, key, value)
        config.save()
        console.print(f"[green]✓ Set {section}.{key} = {value}[/green]")
    except Exception as e:
        console.print(f"[red]Error setting configuration: {e}[/red]")
        raise click.Abort() from e


@config_group.command('get')
@click.argument('section')
@click.argument('key')
def get_config(section, key):
    """Get a configuration value.
    
    Examples:
        proj config get api base_url
        proj config get display max_rows
    """
    console = Console()
    config = Config.get_instance()
    
    value = config.get(section, key)
    if value is None:
        console.print(f"[yellow]Configuration {section}.{key} not found[/yellow]")
    else:
        console.print(f"{section}.{key} = {value}")


@click.command()
@click.pass_context
def config(ctx):
    """Manage CLI configuration settings."""
    ctx.forward(config_group)

