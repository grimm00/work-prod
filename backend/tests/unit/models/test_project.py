"""
Unit tests for Project model.

Tests the Project SQLAlchemy model including creation, validation, 
serialization, and timestamps.
"""

import pytest
from datetime import datetime
from app.models.project import Project


def test_project_creation(app):
    """Test creating a Project instance with basic fields."""
    project = Project(name="Test Project", path="/test/path")
    
    assert project.name == "Test Project"
    assert project.path == "/test/path"
    assert project.id is None  # Not committed yet


def test_project_name_required(app):
    """Test that name field is required."""
    with pytest.raises(Exception):  # Should raise validation error
        project = Project(path="/test/path")
        # Attempting to commit without name should fail
        from app import db
        db.session.add(project)
        db.session.commit()


def test_project_path_can_be_null(app):
    """Test that path field is optional."""
    project = Project(name="Test Project")
    
    assert project.name == "Test Project"
    assert project.path is None


def test_project_to_dict(app):
    """Test Project serialization to dictionary."""
    from app import db
    
    project = Project(name="Test Project", path="/test/path")
    db.session.add(project)
    db.session.commit()
    
    project_dict = project.to_dict()
    
    assert isinstance(project_dict, dict)
    assert project_dict['id'] == project.id
    assert project_dict['name'] == "Test Project"
    assert project_dict['path'] == "/test/path"
    assert 'created_at' in project_dict
    assert 'updated_at' in project_dict


def test_project_timestamps(app):
    """Test that created_at and updated_at are set automatically."""
    from app import db
    
    project = Project(name="Test Project")
    db.session.add(project)
    db.session.commit()
    
    assert project.created_at is not None
    assert project.updated_at is not None
    assert isinstance(project.created_at, datetime)
    assert isinstance(project.updated_at, datetime)


def test_project_repr(app):
    """Test Project __repr__ method."""
    project = Project(name="Test Project", path="/test/path")
    
    repr_str = repr(project)
    
    assert "Test Project" in repr_str
    assert "Project" in repr_str


def test_project_path_unique(app):
    """Test that path must be unique."""
    from app import db
    
    project1 = Project(name="Project 1", path="/same/path")
    db.session.add(project1)
    db.session.commit()
    
    project2 = Project(name="Project 2", path="/same/path")
    db.session.add(project2)
    
    with pytest.raises(Exception):  # Should raise IntegrityError
        db.session.commit()

