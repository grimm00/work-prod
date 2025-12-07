# Dev-Infra Improvements - Phase 6: CLI Enhancement & Daily Use Tools

**Source:** Phase 6 (CLI Enhancement & Daily Use Tools)  
**Target:** dev-infra template  
**Status:** 🟡 Pending  
**Why:** CLI patterns are essential for developer tools  
**How Discovered:** Phase 6 implementation  
**What Problem:** Need reusable CLI patterns for configuration, error handling, progress indicators

---

## Introduction

Phase 6 established several critical CLI patterns that should be templated:

- **Configuration Management** - Singleton Config class with environment variable override
- **Error Handling** - Centralized error handler with friendly messages
- **Progress Indicators** - Spinner and progress bar patterns
- **Help System** - Comprehensive help text with examples
- **CLI Structure** - Command organization and module structure

These patterns improve developer experience and should be available in dev-infra template.

---

## Pre-Project Setup

### CLI Module Structure Template

- [ ] **Location:** `scripts/[project]_cli/` directory structure
  - **Action:** Create CLI module structure with commands subdirectory
  - **Prevents/Enables:** Consistent CLI organization, easy to add commands
  - **Content:**
    ```
    scripts/[project]_cli/
    ├── __init__.py
    ├── [project]              # Main CLI entry point
    ├── config.py              # Configuration management
    ├── error_handler.py       # Error handling
    ├── progress.py            # Progress indicators
    ├── api_client.py          # API client
    └── commands/
        ├── __init__.py
        ├── [command]_cmd.py   # Individual commands
    ```
  - **Expected Impact:** Consistent CLI structure across projects
  - **Priority:** HIGH
  - **Effort:** LOW

---

## Configuration

### Singleton Config Class Template

- [ ] **Location:** `scripts/[project]_cli/config.py`
  - **Action:** Create Config class with singleton pattern
  - **Prevents/Enables:** Single source of truth for configuration, environment variable override
  - **Content:**
    ```python
    import os
    import configparser
    from pathlib import Path

    class Config:
        """Configuration manager for CLI settings."""
        
        _instance = None
        
        DEFAULT_CONFIG = {
            'api': {
                'base_url': 'http://localhost:5000/api'
            },
            'display': {
                'max_rows': '50',
                'color': 'true'
            }
        }
        
        def __new__(cls):
            """Singleton pattern - return same instance."""
            if cls._instance is None:
                cls._instance = super(Config, cls).__new__(cls)
            return cls._instance
        
        def __init__(self):
            if hasattr(self, 'config'):
                return
            
            self.config_file = Path.home() / f'.{project}rc'
            self.config = configparser.ConfigParser()
            self._load_config()
        
        @classmethod
        def get_instance(cls):
            """Get the singleton Config instance."""
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance
        
        def get_api_url(self):
            """Get the API base URL (environment variable takes precedence)."""
            env_url = os.environ.get(f'{PROJECT}_API_URL')
            if env_url:
                return env_url
            return self.get('api', 'base_url', 'http://localhost:5000/api')
        
        def get_max_rows(self):
            """Get maximum rows to display."""
            default = 50
            value = self.get('display', 'max_rows', str(default))
            try:
                return int(value)
            except (TypeError, ValueError):
                return default
    ```
  - **Expected Impact:** Consistent configuration management, environment variable support
  - **Priority:** HIGH
  - **Effort:** MEDIUM

### Config Command Template

- [ ] **Location:** `scripts/[project]_cli/commands/config_cmd.py`
  - **Action:** Create config command group with show/set/get subcommands
  - **Prevents/Enables:** Easy configuration management for users
  - **Content:**
    ```python
    import click
    from rich.console import Console
    from rich.table import Table
    from ..config import Config
    from ..error_handler import handle_error

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
        
        table = Table(title="Configuration", show_header=True, header_style="bold cyan")
        table.add_column("Section", style="cyan")
        table.add_column("Key", style="green")
        table.add_column("Value", style="yellow")
        
        for section, options in all_config.items():
            for key, value in options.items():
                table.add_row(section, key, value)
        
        console.print(table)
        console.print(f"\n[dim]Configuration file: {config.config_file}[/dim]")

    @config_group.command('set')
    @click.argument('section')
    @click.argument('key')
    @click.argument('value')
    def set_config(section, key, value):
        """Set a configuration value."""
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
        """Get a configuration value."""
        console = Console()
        config = Config.get_instance()
        
        value = config.get(section, key)
        if value is None:
            console.print(f"[yellow]Configuration {section}.{key} not found[/yellow]")
        else:
            console.print(f"{section}.{key} = {value}")
    ```
  - **Expected Impact:** Easy configuration management for users
  - **Priority:** HIGH
  - **Effort:** MEDIUM

---

## Error Handling

### Centralized Error Handler Template

- [ ] **Location:** `scripts/[project]_cli/error_handler.py`
  - **Action:** Create centralized error handler with custom exceptions
  - **Prevents/Enables:** Consistent error messages, user-friendly troubleshooting
  - **Content:**
    ```python
    import requests
    from rich.console import Console
    from rich.panel import Panel

    class CLIError(Exception):
        """Base exception for CLI errors."""
        pass

    class BackendConnectionError(CLIError):
        """Raised when backend is not reachable."""
        pass

    class APIError(CLIError):
        """Raised when API returns an error response."""
        def __init__(self, message, status_code=None, response_data=None):
            super().__init__(message)
            self.status_code = status_code
            self.response_data = response_data

    def handle_error(error: Exception, console: Console = None) -> None:
        """Handle errors and display friendly messages with suggestions."""
        if console is None:
            console = Console()
        
        if isinstance(error, BackendConnectionError):
            _handle_backend_connection_error(error, console)
        elif isinstance(error, APIError):
            _handle_api_error(error, console)
        else:
            _handle_generic_error(error, console)

    def _handle_backend_connection_error(error: BackendConnectionError, console: Console) -> None:
        """Handle errors related to backend connection issues."""
        from ..config import Config
        
        config = Config.get_instance()
        api_url = config.get_api_url()
        health_url = f"{api_url.rstrip('/')}/health"
        
        message = f"[bold red]✗ Connection Error:[/bold red] Could not connect to the backend API.\n\n"
        message += "[bold]Possible reasons:[/bold]\n"
        message += "• Backend server is not running\n"
        message += "• Incorrect API URL configured\n"
        message += "• Network issues\n\n"
        message += "[bold]Try:[/bold]\n"
        message += "• Start the backend server: [cyan]cd backend && python run.py[/cyan]\n"
        message += f"• Verify server is running: [cyan]curl {health_url}[/cyan]\n"
        message += f"• Check API URL in config: [cyan]{PROJECT} config get api base_url[/cyan]\n"
        message += f"• Set API URL via env var: [cyan]export {PROJECT}_API_URL=http://your-api-url[/cyan]"
        
        console.print(Panel(message, title="Backend Connection Failed", border_style="red"))
        console.print(f"\n[dim]Technical details: {error}[/dim]")
    ```
  - **Expected Impact:** Consistent error experience, actionable troubleshooting
  - **Priority:** HIGH
  - **Effort:** MEDIUM

### Health Check Function Template

- [ ] **Location:** `scripts/[project]_cli/error_handler.py`
  - **Action:** Add health check function with robust URL construction
  - **Prevents/Enables:** Reliable backend health checks, works with various URL formats
  - **Content:**
    ```python
    import requests
    from urllib.parse import urljoin

    def check_backend_health(base_url: str) -> bool:
        """
        Check if backend is running and healthy.
        
        Args:
            base_url: Base API URL
            
        Returns:
            True if backend is healthy, False otherwise
        """
        try:
            # Construct health URL explicitly
            health_url = urljoin(base_url.rstrip('/') + '/', 'health')
            response = requests.get(health_url, timeout=2)
            return response.status_code == 200
        except Exception:
            return False
    ```
  - **Expected Impact:** Reliable health checks, works with custom URLs
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## Progress Indicators

### Progress Indicator Module Template

- [ ] **Location:** `scripts/[project]_cli/progress.py`
  - **Action:** Create progress indicator module with spinner and progress bar
  - **Prevents/Enables:** Visual feedback during operations, better UX
  - **Content:**
    ```python
    from contextlib import contextmanager
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

    @contextmanager
    def spinner(console: Console, message: str = "Loading..."):
        """
        Context manager for showing a spinner during an operation.
        
        Example:
            with spinner(console, "Fetching projects..."):
                projects = client.list_projects()
        """
        with console.status(f"[cyan]{message}[/cyan]", spinner="dots"):
            yield

    @contextmanager
    def progress_bar(console: Console, total: int, description: str = "Processing"):
        """
        Context manager for showing a progress bar during an operation.
        
        Example:
            with progress_bar(console, len(items), "Importing projects") as progress:
                task = progress.add_task(description, total=len(items))
                for item in items:
                    process_item(item)
                    progress.update(task, advance=1)
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
            transient=False
        ) as progress:
            yield progress
    ```
  - **Expected Impact:** Better UX with visual feedback
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## CLI Structure

### Command Module Pattern Template

- [ ] **Location:** `scripts/[project]_cli/commands/[command]_cmd.py`
  - **Action:** Create command module template with error handling and progress indicators
  - **Prevents/Enables:** Consistent command structure, easy to add new commands
  - **Content:**
    ```python
    import click
    from rich.console import Console
    from ..api_client import APIClient
    from ..error_handler import handle_error
    from ..progress import spinner

    @click.command()
    @click.option('--option', help='Option description')
    def command_name(option):
        """
        Command description.
        
        Examples:
            {project} command-name
            {project} command-name --option value
        """
        console = Console()
        
        try:
            client = APIClient()
            with spinner(console, "Processing..."):
                result = client.api_call(option)
            
            # Display results
            console.print(result)
            
        except Exception as e:
            handle_error(e, console)
            raise click.Abort() from e
    ```
  - **Expected Impact:** Consistent command structure, easy to add commands
  - **Priority:** HIGH
  - **Effort:** LOW

### Main CLI Entry Point Template

- [ ] **Location:** `scripts/[project]_cli/[project]`
  - **Action:** Create main CLI entry point with command registration
  - **Prevents/Enables:** Easy command registration, comprehensive help
  - **Content:**
    ```python
    #!/usr/bin/env python3
    """
    {Project} CLI Tool
    
    A command-line interface for managing {project}.
    """
    
    import click
    from rich.console import Console
    
    console = Console()
    
    @click.group()
    @click.version_option(version='0.1.0')
    def cli():
        """
        {Project} CLI Tool
        
        Quick Start:
            {project} list                    # List all items
            {project} config show             # Show configuration
            {project} --help                  # Show help
        
        Configuration:
            Configuration is stored in ~/.{project}rc
            Use '{project} config' commands to manage settings
        
        Examples:
            {project} list --status active
            {project} config set display max_rows 100
        """
        pass
    
    # Import and register commands
    from .commands import (
        list_cmd, get_cmd, create_cmd, update_cmd,
        delete_cmd, config_cmd, stats_cmd
    )
    
    cli.add_command(list_cmd.list, name='list')
    cli.add_command(get_cmd.get, name='get')
    cli.add_command(create_cmd.create, name='create')
    cli.add_command(update_cmd.update, name='update')
    cli.add_command(delete_cmd.delete, name='delete')
    cli.add_command(config_cmd.config_group, name='config')
    cli.add_command(stats_cmd.stats, name='stats')
    
    if __name__ == '__main__':
        cli()
    ```
  - **Expected Impact:** Easy command registration, comprehensive help
  - **Priority:** HIGH
  - **Effort:** LOW

---

## Documentation

### CLI Help Text Template

- [ ] **Location:** Command docstrings and help text
  - **Action:** Create help text template with examples and valid values
  - **Prevents/Enables:** Better user experience, easier command discovery
  - **Content:**
    ```python
    @click.command()
    @click.option('--status', type=click.Choice(['active', 'paused', 'completed', 'cancelled']),
                  help='Filter by status (choices: active, paused, completed, cancelled)')
    @click.option('--wide', is_flag=True,
                  help='Show all columns (status, organization, classification, and full-width layout)')
    def list(status, wide):
        """
        List all items.
        
        Examples:
            {project} list
            {project} list --status active
            {project} list --status active --wide
            {project} list --org work
            {project} list --search productivity
        """
    ```
  - **Expected Impact:** Better user experience, easier command discovery
  - **Priority:** MEDIUM
  - **Effort:** LOW

### CLI README Template

- [ ] **Location:** `scripts/[project]_cli/README.md`
  - **Action:** Create CLI README with installation, configuration, and usage examples
  - **Prevents/Enables:** Easy onboarding, clear usage documentation
  - **Content:**
    ```markdown
    # {Project} CLI Tool
    
    Command-line interface for managing {project}.
    
    ## Installation
    
    ```bash
    cd scripts/{project}_cli
    pip install -r requirements.txt
    ```
    
    ## Configuration
    
    Configuration is stored in `~/.{project}rc`:
    
    ```ini
    [api]
    base_url = http://localhost:5000/api
    
    [display]
    max_rows = 50
    color = true
    ```
    
    Manage configuration:
    
    ```bash
    {project} config show              # Show all settings
    {project} config set api base_url http://localhost:5000/api
    {project} config get display max_rows
    ```
    
    Environment variables override config file:
    
    ```bash
    export {PROJECT}_API_URL=http://localhost:5000/api
    ```
    
    ## Usage Examples
    
    ```bash
    # List all items
    {project} list
    
    # Filter by status
    {project} list --status active
    
    # Show statistics
    {project} stats
    
    # Get help
    {project} --help
    {project} list --help
    ```
    ```
  - **Expected Impact:** Easy onboarding, clear usage documentation
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## Testing Infrastructure

### CLI Testing Patterns

- [ ] **Location:** `tests/integration/cli/` directory
  - **Action:** Create CLI testing patterns and fixtures
  - **Prevents/Enables:** Automated CLI testing, catch regressions
  - **Content:**
    ```python
    import pytest
    from click.testing import CliRunner
    from scripts.{project}_cli.{project} import cli

    @pytest.fixture
    def runner():
        """CLI test runner fixture."""
        return CliRunner()

    def test_list_command(runner):
        """Test list command."""
        result = runner.invoke(cli, ['list'])
        assert result.exit_code == 0
        assert 'Projects' in result.output

    def test_config_show(runner):
        """Test config show command."""
        result = runner.invoke(cli, ['config', 'show'])
        assert result.exit_code == 0
        assert 'Configuration' in result.output
    ```
  - **Expected Impact:** Automated CLI testing, catch regressions
  - **Priority:** MEDIUM
  - **Effort:** MEDIUM

---

## Development Workflow

### CLI Development Checklist

- [ ] **Location:** Development workflow documentation
  - **Action:** Add CLI development checklist to workflow docs
  - **Prevents/Enables:** Consistent CLI development, catch common issues
  - **Content:**
    ```markdown
    ## CLI Development Checklist
    
    - [ ] Command has comprehensive help text with examples
    - [ ] Command uses centralized error handling
    - [ ] Command uses progress indicators for long operations
    - [ ] Command validates inputs (click.Choice for enums)
    - [ ] Command uses Rich formatting for output
    - [ ] Command handles missing backend gracefully
    - [ ] Command respects configuration settings
    - [ ] Manual testing scenarios added to testing guide
    ```
  - **Expected Impact:** Consistent CLI development, catch common issues
  - **Priority:** MEDIUM
  - **Effort:** LOW

---

## Summary

**Total Improvements:** 10  
**Priority Breakdown:**
- HIGH: 5 improvements (Config class, error handler, command structure, CLI entry point, config commands)
- MEDIUM: 5 improvements (Health check, progress indicators, help text, README, testing patterns)

**Key Patterns to Template:**
1. Singleton Config class with environment variable override
2. Centralized error handler with custom exceptions
3. Progress indicator context managers
4. Command module structure
5. Comprehensive help system

**Expected Impact:**
- Consistent CLI patterns across projects
- Better developer experience
- Easier to add new CLI commands
- Professional error handling and progress feedback

---

**Last Updated:** 2025-12-06

