"""
API client for communicating with the backend.

Provides a simple interface for making API requests.
"""

import requests
from typing import List, Dict, Optional
from .config import Config


class APIClient:
    """Client for interacting with the Projects API."""
    
    def __init__(self, base_url: str = None):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for API (defaults to Config instance API URL)
        """
        config = Config.get_instance()
        self.base_url = base_url or config.get_api_url()
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
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
        
        response = self.session.get(f'{self.base_url}/projects', params=params)
        response.raise_for_status()
        return response.json()
    
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
        response = self.session.get(f'{self.base_url}/projects/{project_id}')
        response.raise_for_status()
        return response.json()
    
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
        response = self.session.post(f'{self.base_url}/projects', json=data)
        response.raise_for_status()
        return response.json()
    
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
        response = self.session.patch(f'{self.base_url}/projects/{project_id}', json=data)
        response.raise_for_status()
        return response.json()
    
    def delete_project(self, project_id: int) -> None:
        """
        Delete a project permanently.
        
        Args:
            project_id: ID of the project to delete
            
        Raises:
            requests.RequestException: If API request fails
        """
        response = self.session.delete(f'{self.base_url}/projects/{project_id}')
        response.raise_for_status()
    
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
        response = self.session.put(f'{self.base_url}/projects/{project_id}/archive')
        response.raise_for_status()
        return response.json()
    
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
        response = self.session.post(f'{self.base_url}/projects/import', json=projects_data)
        response.raise_for_status()
        return response.json()

