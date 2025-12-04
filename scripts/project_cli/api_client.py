"""
API client for communicating with the backend.

Provides a simple interface for making API requests.
"""

import requests
from typing import List, Dict, Optional
from project_cli.config import Config


class APIClient:
    """Client for interacting with the Projects API."""
    
    def __init__(self, base_url: str = None):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for API (defaults to Config.API_BASE_URL)
        """
        self.base_url = base_url or Config.API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def list_projects(self) -> List[Dict]:
        """
        Get all projects.
        
        Returns:
            List of project dictionaries
            
        Raises:
            requests.RequestException: If API request fails
        """
        response = self.session.get(f'{self.base_url}/projects')
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

