"""
Unit tests for inventory to project mapping script.

Tests the mapping logic from classifications-merged.json format to
Project model format expected by import endpoint.
"""

import pytest
import json
from pathlib import Path
import sys
import importlib.util

# Load the mapping script as a module
# Test file is at: backend/tests/unit/test_map_inventory.py
# Script is at: scripts/map_inventory_to_projects.py
project_root = Path(__file__).parent.parent.parent.parent
script_path = project_root / 'scripts' / 'map_inventory_to_projects.py'

spec = importlib.util.spec_from_file_location("map_inventory_to_projects", script_path)
map_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(map_module)

# Import functions from the module
parse_project_key = map_module.parse_project_key
extract_organization = map_module.extract_organization
build_github_url = map_module.build_github_url
map_classification_to_project = map_module.map_classification_to_project
CLASSIFICATION_MAP = map_module.CLASSIFICATION_MAP
STATUS_MAP = map_module.STATUS_MAP


class TestParseProjectKey:
    """Test parsing of project keys."""
    
    def test_parse_merged_key(self):
        """Test parsing merged project key."""
        result = parse_project_key('merged:todolist-repo')
        assert result['name'] == 'todolist-repo'
        assert result['type'] == 'merged'
    
    def test_parse_github_key(self):
        """Test parsing GitHub-only project key."""
        result = parse_project_key('github:finance')
        assert result['name'] == 'finance'
        assert result['type'] == 'github'
    
    def test_parse_local_key(self):
        """Test parsing local project key."""
        result = parse_project_key('local:/Users/cdwilson/Projects/todolist-repo')
        assert result['name'] == 'todolist-repo'
        assert result['type'] == 'local'
        assert result['path'] == '/Users/cdwilson/Projects/todolist-repo'
    
    def test_parse_unknown_key(self):
        """Test parsing unknown key format."""
        result = parse_project_key('unknown:format')
        assert result['name'] == 'unknown:format'
        assert result['type'] == 'unknown'


class TestExtractOrganization:
    """Test organization extraction."""
    
    def test_extract_drw_organization(self):
        """Test extracting DRW organization."""
        assert extract_organization('Work (DRW)') == 'DRW'
    
    def test_extract_apprenti_organization(self):
        """Test extracting Apprenti organization."""
        assert extract_organization('Apprenti') == 'Apprenti'
    
    def test_extract_no_organization(self):
        """Test that Personal/Learning return None."""
        assert extract_organization('Personal') is None
        assert extract_organization('Learning') is None
        assert extract_organization('Inactive/Archived') is None


class TestBuildGithubUrl:
    """Test GitHub URL building."""
    
    def test_build_github_url(self):
        """Test building GitHub URL from project name."""
        assert build_github_url('todolist-repo') == 'https://github.com/grimm00/todolist-repo'
        assert build_github_url('finance') == 'https://github.com/grimm00/finance'


class TestMapClassificationToProject:
    """Test mapping inventory data to project format."""
    
    def test_map_single_merged_project(self):
        """Test mapping single merged project."""
        inventory_data = {
            'merged:todolist-repo': 'Personal',
            'github:todolist-repo': 'Personal',
            'local:/Users/cdwilson/Projects/todolist-repo': 'Personal'
        }
        
        projects = map_classification_to_project(inventory_data)
        
        assert len(projects) == 1
        project = projects[0]
        assert project['name'] == 'todolist-repo'
        assert project['classification'] == 'primary'
        assert project['status'] == 'active'
        assert project['remote_url'] == 'https://github.com/grimm00/todolist-repo'
        assert project['path'] == '/Users/cdwilson/Projects/todolist-repo'
    
    def test_map_github_only_project(self):
        """Test mapping GitHub-only project."""
        inventory_data = {
            'github:finance': 'Personal'
        }
        
        projects = map_classification_to_project(inventory_data)
        
        assert len(projects) == 1
        project = projects[0]
        assert project['name'] == 'finance'
        assert project['classification'] == 'primary'
        assert project['status'] == 'active'
        assert project['remote_url'] == 'https://github.com/grimm00/finance'
        assert 'path' not in project
    
    def test_map_local_only_project(self):
        """Test mapping local-only project."""
        inventory_data = {
            'local:/Users/cdwilson/Projects/pokedex': 'Personal'
        }
        
        projects = map_classification_to_project(inventory_data)
        
        assert len(projects) == 1
        project = projects[0]
        assert project['name'] == 'pokedex'
        assert project['classification'] == 'primary'
        assert project['status'] == 'active'
        assert project['path'] == '/Users/cdwilson/Projects/pokedex'
        assert 'remote_url' not in project
    
    def test_map_work_project_with_organization(self):
        """Test mapping work project with organization."""
        inventory_data = {
            'merged:music-app': 'Work (DRW)',
            'github:music-app': 'Work (DRW)',
            'local:/Users/cdwilson/Projects/music-app-drw': 'Work (DRW)'
        }
        
        projects = map_classification_to_project(inventory_data)
        
        assert len(projects) == 1
        project = projects[0]
        assert project['name'] == 'music-app'
        assert project['organization'] == 'DRW'
        assert project['classification'] == 'primary'
        assert project['status'] == 'active'
    
    def test_map_learning_project(self):
        """Test mapping learning project."""
        inventory_data = {
            'merged:containers-learning-path': 'Learning',
            'github:containers-learning-path': 'Learning',
            'local:/Users/cdwilson/Learning/containers': 'Learning'
        }
        
        projects = map_classification_to_project(inventory_data)
        
        assert len(projects) == 1
        project = projects[0]
        assert project['name'] == 'containers-learning-path'
        assert project['classification'] == 'secondary'
        assert project['status'] == 'active'
    
    def test_map_inactive_project(self):
        """Test mapping inactive/archived project."""
        inventory_data = {
            'github:B-IT': 'Inactive/Archived'
        }
        
        projects = map_classification_to_project(inventory_data)
        
        assert len(projects) == 1
        project = projects[0]
        assert project['name'] == 'B-IT'
        assert project['classification'] == 'archive'
        assert project['status'] == 'cancelled'
    
    def test_skip_skip_classification(self):
        """Test that Skip classification is excluded."""
        inventory_data = {
            'github:testrepo': 'Skip',
            'github:valid-repo': 'Personal'
        }
        
        projects = map_classification_to_project(inventory_data)
        
        assert len(projects) == 1
        assert projects[0]['name'] == 'valid-repo'
    
    def test_deduplicate_same_project(self):
        """Test that same project name is deduplicated."""
        inventory_data = {
            'merged:todolist-repo': 'Personal',
            'github:todolist-repo': 'Personal',
            'local:/Users/cdwilson/Projects/todolist-repo': 'Personal'
        }
        
        projects = map_classification_to_project(inventory_data)
        
        # Should only have one project despite multiple entries
        assert len(projects) == 1
        assert projects[0]['name'] == 'todolist-repo'
    
    def test_map_multiple_projects(self):
        """Test mapping multiple projects."""
        inventory_data = {
            'merged:project1': 'Personal',
            'github:project1': 'Personal',
            'local:/Users/cdwilson/Projects/project1': 'Personal',
            'github:project2': 'Work (DRW)',
            'local:/Users/cdwilson/Projects/project3': 'Learning'
        }
        
        projects = map_classification_to_project(inventory_data)
        
        assert len(projects) == 3
        
        # Check project1 (merged)
        project1 = next(p for p in projects if p['name'] == 'project1')
        assert project1['classification'] == 'primary'
        assert 'remote_url' in project1
        assert 'path' in project1
        
        # Check project2 (github only)
        project2 = next(p for p in projects if p['name'] == 'project2')
        assert project2['classification'] == 'primary'
        assert project2['organization'] == 'DRW'
        assert 'remote_url' in project2
        
        # Check project3 (local only)
        project3 = next(p for p in projects if p['name'] == 'project3')
        assert project3['classification'] == 'secondary'
        assert 'path' in project3
        assert 'remote_url' not in project3
    
    def test_prefer_merged_over_local(self):
        """Test that merged entry is preferred over local-only."""
        inventory_data = {
            'merged:project1': 'Personal',
            'local:/Users/cdwilson/Projects/project1': 'Personal'
        }
        
        projects = map_classification_to_project(inventory_data)
        
        assert len(projects) == 1
        project = projects[0]
        # Should have both remote_url (from merged) and path (from local)
        assert 'remote_url' in project
        assert 'path' in project


class TestClassificationMaps:
    """Test classification and status mapping constants."""
    
    @pytest.mark.parametrize("classification", [
        'Personal', 'Work (DRW)', 'Apprenti', 'Learning', 'Inactive/Archived', 'Skip'
    ])
    def test_classification_map_completeness(self, classification):
        """Test that all expected classifications are mapped."""
        assert classification in CLASSIFICATION_MAP
    
    @pytest.mark.parametrize("classification", [
        'Personal', 'Work (DRW)', 'Apprenti', 'Learning', 'Inactive/Archived', 'Skip'
    ])
    def test_status_map_completeness(self, classification):
        """Test that all expected classifications have status mappings."""
        assert classification in STATUS_MAP
    
    @pytest.mark.parametrize("classification,mapped_value", [
        ('Personal', 'primary'),
        ('Work (DRW)', 'primary'),
        ('Apprenti', 'primary'),
        ('Learning', 'secondary'),
        ('Inactive/Archived', 'archive'),
        ('Skip', None),
    ])
    def test_classification_map_values(self, classification, mapped_value):
        """Test that classification map values are valid Project enum values."""
        assert CLASSIFICATION_MAP[classification] == mapped_value
        assert mapped_value in {'primary', 'secondary', 'archive', 'maintenance', None}
    
    @pytest.mark.parametrize("classification,status_value", [
        ('Personal', 'active'),
        ('Work (DRW)', 'active'),
        ('Apprenti', 'active'),
        ('Learning', 'active'),
        ('Inactive/Archived', 'cancelled'),
        ('Skip', None),
    ])
    def test_status_map_values(self, classification, status_value):
        """Test that status map values are valid Project enum values."""
        assert STATUS_MAP[classification] == status_value
        assert status_value in {'active', 'paused', 'completed', 'cancelled', None}
    
    def test_classification_map_all_entries_valid(self):
        """Test that all CLASSIFICATION_MAP entries have valid values."""
        valid_classifications = {'primary', 'secondary', 'archive', 'maintenance', None}
        for cls, mapped in CLASSIFICATION_MAP.items():
            assert mapped in valid_classifications, f"Invalid classification mapping: {cls} -> {mapped}"
    
    def test_status_map_all_entries_valid(self):
        """Test that all STATUS_MAP entries have valid values."""
        valid_statuses = {'active', 'paused', 'completed', 'cancelled', None}
        for cls, mapped in STATUS_MAP.items():
            assert mapped in valid_statuses, f"Invalid status mapping: {cls} -> {mapped}"

