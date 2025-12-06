"""
Configuration command implementation.

Allows users to view and edit CLI configuration settings.
"""

import click
from rich.console import Console
from rich.table import Table
from ..config import Config
from ..error_handler import handle_error


@click.group()
def config_group():
    """
    Manage CLI configuration settings.
    
    View and modify CLI configuration stored in ~/.projrc file.
    Configuration includes API URL, display preferences, and other settings.
    
    \b
    Examples:
        proj config show
        proj config get api base_url
        proj config set api base_url http://localhost:5000/api
        proj config set display max_rows 100
    """
    pass


@config_group.command('show')
def show_config():
    """
    Show current configuration settings.
    
    Display all configuration values from ~/.projrc file in a formatted table.
    Shows both API and display settings.
    
    \b
    Examples:
        proj config show
    """
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
    """
    Set a configuration value.
    
    Update a configuration setting in ~/.projrc file. Changes take effect
    immediately for subsequent commands.
    
    \b
    SECTION: Configuration section (api, display)
    KEY: Configuration key (base_url, max_rows, color)
    VALUE: New value to set
    
    \b
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
        handle_error(e, console)
        raise click.Abort() from e


@config_group.command('get')
@click.argument('section')
@click.argument('key')
def get_config(section, key):
    """
    Get a configuration value.
    
    Display the current value of a specific configuration setting.
    
    \b
    SECTION: Configuration section (api, display)
    KEY: Configuration key (base_url, max_rows, color)
    
    \b
    Examples:
        proj config get api base_url
        proj config get display max_rows
        proj config get display color
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

