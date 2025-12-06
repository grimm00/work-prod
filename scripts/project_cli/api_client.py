"""
API client for communicating with the backend.

Provides a simple interface for making API requests.
"""

import requests
from typing import List, Dict, Optional
from .config import Config
from .error_handler import BackendConnectionError, APIError, check_backend_health


def _raise_api_error(error: requests.exceptions.RequestException, response=None) -> None:
    """Convert requests exceptions to APIError or re-raise connection errors."""
    if isinstance(error, requests.exceptions.ConnectionError):
        raise BackendConnectionError(str(error)) from error
    elif isinstance(error, requests.exceptions.Timeout):
        raise error  # Let timeout errors propagate
    elif isinstance(error, requests.exceptions.HTTPError):
        error_msg = str(error)
        if response is not None:
            try:
                error_data = response.json()
                if isinstance(error_data, dict) and 'error' in error_data:
                    error_msg = error_data['error']
            except Exception:
                pass
        raise APIError(error_msg, status_code=response.status_code if response else None) from error
    else:
        raise error


class APIClient:
    """Client for interacting with the Projects API."""
    
    def __init__(self, base_url: str = None, check_health: bool = True):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for API (defaults to Config instance API URL)
            check_health: Whether to check backend health on initialization (default: True)
        """
        config = Config.get_instance()
        self.base_url = base_url or config.get_api_url()
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # Check backend health if requested
        if check_health and not check_backend_health(self.base_url):
            raise BackendConnectionError(
                f"Cannot connect to backend at {self.base_url}"
            )
    
    def list_projects(self, status: str = None, organization: str = None, 
                     classification: str = None, search: str = None) -> List[Dict]:
        """
        Get all projects with optional filtering.
        
        Args:
            status: Filter by status (active, paused, completed, cancelled)
            organization: Filter by organization name
            classification: Filter by classification (primary, secondary, archive, maintenance)
            search: Search term for name and description
        
        Returns:
            List of project dictionaries
            
        Raises:
            requests.RequestException: If API request fails
        """
        params = {}
        if status:
            params['status'] = status
        if organization:
            params['organization'] = organization
        if classification:
            params['classification'] = classification
        if search:
            params['search'] = search
        
        try:
            response = self.session.get(f'{self.base_url}/projects', params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)
    
    def get_project(self, project_id: int) -> Dict:
        """
        Get a specific project by ID.
        
        Args:
            project_id: ID of the project to retrieve
            
        Returns:
            Project dictionary
            
        Raises:
            requests.RequestException: If API request fails
        """
        try:
            response = self.session.get(f'{self.base_url}/projects/{project_id}', timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)
    
    def create_project(self, data: Dict) -> Dict:
        """
        Create a new project.
        
        Args:
            data: Project data dictionary
            
        Returns:
            Created project dictionary
            
        Raises:
            requests.RequestException: If API request fails
        """
        try:
            response = self.session.post(f'{self.base_url}/projects', json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)
    
    def update_project(self, project_id: int, data: Dict) -> Dict:
        """
        Update an existing project.
        
        Args:
            project_id: ID of the project to update
            data: Fields to update
            
        Returns:
            Updated project dictionary
            
        Raises:
            requests.RequestException: If API request fails
        """
        try:
            response = self.session.patch(f'{self.base_url}/projects/{project_id}', json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)
    
    def delete_project(self, project_id: int) -> None:
        """
        Delete a project permanently.
        
        Args:
            project_id: ID of the project to delete
            
        Raises:
            requests.RequestException: If API request fails
        """
        try:
            response = self.session.delete(f'{self.base_url}/projects/{project_id}', timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)
    
    def archive_project(self, project_id: int) -> Dict:
        """
        Archive a project by setting classification to 'archive' and status to 'completed'.
        
        Args:
            project_id: ID of the project to archive
            
        Returns:
            Archived project dictionary
            
        Raises:
            requests.RequestException: If API request fails
        """
        try:
            response = self.session.put(f'{self.base_url}/projects/{project_id}/archive', timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)
    
    def import_projects(self, projects_data: Dict) -> Dict:
        """
        Import multiple projects from JSON data.
        
        Args:
            projects_data: Dictionary with 'projects' key containing list of project data
            
        Returns:
            Dictionary with import statistics: imported, skipped, errors
            
        Raises:
            requests.RequestException: If API request fails
        """
        try:
            response = self.session.post(f'{self.base_url}/projects/import', json=projects_data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)

