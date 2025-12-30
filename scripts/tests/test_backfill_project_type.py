"""Tests for backfill_project_type script."""

import pytest
import sys
import os

# Add backend and scripts to path for imports
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend')
scripts_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, backend_path)
sys.path.insert(0, scripts_path)

from app import create_app, db
from app.models.project import Project

# Import classify_project from script
from backfill_project_type import classify_project


class TestClassifyProject:
    """Test classify_project heuristics."""

    def test_drw_organization_returns_work(self, app):
        """Priority 1: DRW organization -> Work."""
        with app.app_context():
            project = Project(name="DRW Project", organization='DRW', path='/some/path', classification='primary')
            result = classify_project(project)
            assert result == 'Work'

    def test_learning_path_returns_learning(self, app):
        """Priority 2: /Learning/ in path -> Learning."""
        with app.app_context():
            project = Project(name="Learning Project", organization=None, path='/Users/me/Learning/python', classification='primary')
            result = classify_project(project)
            assert result == 'Learning'

    def test_archive_classification_returns_inactive(self, app):
        """Priority 3: archive classification -> Inactive."""
        with app.app_context():
            project = Project(name="Archived Project", organization=None, path='/some/path', classification='archive')
            result = classify_project(project)
            assert result == 'Inactive'

    def test_default_returns_personal(self, app):
        """Priority 4: No match -> Personal (default)."""
        with app.app_context():
            project = Project(name="Personal Project", organization=None, path='/some/path', classification='primary')
            result = classify_project(project)
            assert result == 'Personal'

    def test_drw_takes_priority_over_learning_path(self, app):
        """DRW organization takes priority over Learning path."""
        with app.app_context():
            project = Project(name="DRW Learning Project", organization='DRW', path='/Learning/project', classification='primary')
            result = classify_project(project)
            assert result == 'Work'  # DRW wins over Learning path

    def test_learning_path_takes_priority_over_archive(self, app):
        """Learning path takes priority over archive classification."""
        with app.app_context():
            project = Project(name="Learning Archive", organization=None, path='/Learning/old', classification='archive')
            result = classify_project(project)
            assert result == 'Learning'  # Learning wins over archive
