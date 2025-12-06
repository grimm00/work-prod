"""
Error handling utilities for CLI commands.

Provides friendly error messages and suggestions for common issues.
"""

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
    """
    Handle errors and display friendly messages with suggestions.
    
    Args:
        error: The exception that occurred
        console: Rich Console instance (creates new one if not provided)
    """
    if console is None:
        console = Console()
    
    # Check for connection errors
    if isinstance(error, requests.exceptions.ConnectionError):
        _handle_connection_error(error, console)
    elif isinstance(error, requests.exceptions.Timeout):
        _handle_timeout_error(error, console)
    elif isinstance(error, requests.exceptions.HTTPError):
        _handle_http_error(error, console)
    elif isinstance(error, BackendConnectionError):
        _handle_backend_connection_error(error, console)
    elif isinstance(error, APIError):
        _handle_api_error(error, console)
    else:
        _handle_generic_error(error, console)


def _handle_connection_error(error: requests.exceptions.ConnectionError, console: Console) -> None:
    """Handle connection refused/network errors."""
    config_url = "http://localhost:5000/api"
    
    message = "[bold red]Cannot connect to backend API[/bold red]\n\n"
    message += "The backend server appears to be offline or unreachable.\n\n"
    message += "[bold]To fix this:[/bold]\n"
    message += "1. Start the backend server:\n"
    message += "   [cyan]cd backend && python run.py[/cyan]\n\n"
    message += "2. Verify the server is running:\n"
    message += f"   [cyan]curl {config_url.replace('/api', '/api/health')}[/cyan]\n\n"
    message += "3. Check your API URL configuration:\n"
    message += "   [cyan]proj config get api base_url[/cyan]\n"
    message += "   Or set it: [cyan]proj config set api base_url <your-url>[/cyan]"
    
    console.print(Panel(message, title="Connection Error", border_style="red"))
    console.print(f"\n[dim]Technical details: {error}[/dim]")


def _handle_timeout_error(error: requests.exceptions.Timeout, console: Console) -> None:
    """Handle timeout errors."""
    message = "[bold red]Request timed out[/bold red]\n\n"
    message += "The backend server took too long to respond.\n\n"
    message += "[bold]Possible causes:[/bold]\n"
    message += "• Backend server is overloaded\n"
    message += "• Network connectivity issues\n"
    message += "• Backend server may be unresponsive\n\n"
    message += "[bold]Try:[/bold]\n"
    message += "• Check if backend is running: [cyan]curl http://localhost:5000/api/health[/cyan]\n"
    message += "• Restart the backend server"
    
    console.print(Panel(message, title="Timeout Error", border_style="yellow"))
    console.print(f"\n[dim]Technical details: {error}[/dim]")


def _handle_http_error(error: requests.exceptions.HTTPError, console: Console) -> None:
    """Handle HTTP error responses."""
    response = error.response
    
    # Try to extract error message from response
    error_msg = None
    if response is not None:
        try:
            error_data = response.json()
            if isinstance(error_data, dict) and 'error' in error_data:
                error_msg = error_data['error']
        except:
            pass
    
    status_code = response.status_code if response else None
    
    # Customize message based on status code
    if status_code == 404:
        title = "Not Found"
        border = "yellow"
        message = f"[bold yellow]Resource not found[/bold yellow]\n\n"
        if error_msg:
            message += f"{error_msg}\n\n"
        message += "The requested resource does not exist."
    elif status_code == 400:
        title = "Bad Request"
        border = "yellow"
        message = f"[bold yellow]Invalid request[/bold yellow]\n\n"
        if error_msg:
            message += f"{error_msg}\n\n"
        message += "Please check your input and try again."
    elif status_code == 409:
        title = "Conflict"
        border = "yellow"
        message = f"[bold yellow]Conflict detected[/bold yellow]\n\n"
        if error_msg:
            message += f"{error_msg}\n\n"
        message += "The operation conflicts with existing data."
    elif status_code == 500:
        title = "Server Error"
        border = "red"
        message = f"[bold red]Backend server error[/bold red]\n\n"
        message += "The backend encountered an internal error.\n\n"
        message += "[bold]Try:[/bold]\n"
        message += "• Check backend server logs\n"
        message += "• Restart the backend server\n"
        message += "• Report this issue if it persists"
    else:
        title = "HTTP Error"
        border = "red"
        message = f"[bold red]HTTP {status_code} Error[/bold red]\n\n"
        if error_msg:
            message += f"{error_msg}\n"
    
    console.print(Panel(message, title=title, border_style=border))
    if status_code:
        console.print(f"\n[dim]HTTP Status: {status_code}[/dim]")


def _handle_backend_connection_error(error: BackendConnectionError, console: Console) -> None:
    """Handle backend connection errors."""
    _handle_connection_error(error, console)


def _handle_api_error(error: APIError, console: Console) -> None:
    """Handle API-specific errors."""
    message = f"[bold red]API Error[/bold red]\n\n"
    message += f"{error}\n"
    
    if error.status_code:
        message += f"\n[dim]HTTP Status: {error.status_code}[/dim]"
    
    console.print(Panel(message, title="API Error", border_style="red"))


def _handle_generic_error(error: Exception, console: Console) -> None:
    """Handle generic/unexpected errors."""
    message = "[bold red]An unexpected error occurred[/bold red]\n\n"
    message += f"{error}\n\n"
    message += "[bold]Try:[/bold]\n"
    message += "• Check if backend is running: [cyan]curl http://localhost:5000/api/health[/cyan]\n"
    message += "• Verify your configuration: [cyan]proj config show[/cyan]\n"
    message += "• Check the error message above for details"
    
    console.print(Panel(message, title="Error", border_style="red"))
    console.print(f"\n[dim]Technical details: {type(error).__name__}: {error}[/dim]")


def check_backend_health(base_url: str) -> bool:
    """
    Check if backend is running and healthy.
    
    Args:
        base_url: Base API URL
        
    Returns:
        True if backend is healthy, False otherwise
    """
    try:
        health_url = base_url.replace('/api', '/api/health')
        response = requests.get(health_url, timeout=2)
        return response.status_code == 200
    except:
        return False

