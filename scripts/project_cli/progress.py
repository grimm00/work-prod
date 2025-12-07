"""
Progress indicators for CLI commands.

Provides spinners and progress bars for long-running operations.
"""

from contextlib import contextmanager
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.spinner import Spinner
from typing import Optional


@contextmanager
def spinner(console: Console, message: str = "Loading..."):
    """
    Context manager for showing a spinner during an operation.
    
    Args:
        console: Rich Console instance
        message: Message to display with spinner
    
    Example:
        with spinner(console, "Fetching projects..."):
            projects = client.list_projects()
    """
    with console.status(f"[cyan]{message}[/cyan]", spinner="dots"):
        yield


@contextmanager
def progress_bar(console: Console, description: str = "Processing"):
    """
    Context manager for showing a progress bar during an operation.
    
    Args:
        console: Rich Console instance
        description: Description text for the progress bar
    
    Yields:
        Progress instance that can be used to update progress
    
    Example:
        with progress_bar(console, "Importing projects") as progress:
            task = progress.add_task(description, total=len(items))
            for item in items:
                # Process item
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


def create_progress_bar(console: Console, total: int, description: str = "Processing"):
    """
    Create a progress bar for manual control.
    
    Args:
        console: Rich Console instance
        total: Total number of items to process
        description: Description text for the progress bar
    
    Returns:
        Progress instance
    
    Example:
        progress = create_progress_bar(console, 100, "Importing")
        task = progress.add_task("Importing projects", total=100)
        progress.start()
        # ... do work ...
        progress.update(task, advance=50)
        progress.stop()
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
        transient=False
    )

