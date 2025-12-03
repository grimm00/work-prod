"""
API client for communicating with the backend.

Provides a simple interface for making API requests.
"""

import requests
from typing import List, Dict, Optional
from config import Config


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

