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
    from app import db
    from sqlalchemy.exc import IntegrityError
    
    with pytest.raises(IntegrityError):
        project = Project(path="/test/path")
        db.session.add(project)
        db.session.commit()
    
    # Roll back to leave session clean
    db.session.rollback()


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
    from datetime import datetime
    import time
    
    project = Project(name="Test Project")
    db.session.add(project)
    db.session.commit()
    
    # Verify initial timestamps
    assert project.created_at is not None
    assert project.updated_at is not None
    assert isinstance(project.created_at, datetime)
    assert isinstance(project.updated_at, datetime)
    
    # Store original timestamps
    original_created_at = project.created_at
    original_updated_at = project.updated_at
    
    # Wait a moment to ensure timestamp difference (SQLite may have second-level precision)
    time.sleep(1.1)
    
    # Update project
    project.name = "Updated Project"
    db.session.commit()
    
    # Verify updated_at changed but created_at didn't
    assert project.created_at == original_created_at
    assert project.updated_at > original_updated_at


def test_project_repr(app):
    """Test Project __repr__ method."""
    project = Project(name="Test Project", path="/test/path")
    
    repr_str = repr(project)
    
    assert "Test Project" in repr_str
    assert "Project" in repr_str


def test_project_path_unique(app):
    """Test that path must be unique."""
    from app import db
    from sqlalchemy.exc import IntegrityError
    
    project1 = Project(name="Project 1", path="/same/path")
    db.session.add(project1)
    db.session.commit()
    
    project2 = Project(name="Project 2", path="/same/path")
    db.session.add(project2)
    
    with pytest.raises(IntegrityError):
        db.session.commit()
    
    # Roll back to leave session clean
    db.session.rollback()


# Extended Model Fields Tests (Phase 2)


def test_project_creation_with_extended_fields(app):
    """Test creating a Project with organization, classification, status, description, remote_url."""
    project = Project(
        name="Extended Project",
        path="/extended/path",
        organization="work",
        classification="primary",
        status="active",
        description="A test project with all fields",
        remote_url="https://github.com/user/repo"
    )
    
    assert project.name == "Extended Project"
    assert project.path == "/extended/path"
    assert project.organization == "work"
    assert project.classification == "primary"
    assert project.status == "active"
    assert project.description == "A test project with all fields"
    assert project.remote_url == "https://github.com/user/repo"


def test_project_default_status(app):
    """Test that status defaults to 'active' if not provided."""
    from app import db
    
    project = Project(name="Test Project")
    db.session.add(project)
    db.session.commit()
    
    assert project.status == "active"


def test_project_extended_fields_nullable(app):
    """Test that extended fields can be null except status."""
    from app import db
    
    project = Project(name="Minimal Project")
    db.session.add(project)
    db.session.commit()
    
    assert project.organization is None
    assert project.classification is None
    assert project.status == "active"  # Has default
    assert project.description is None
    assert project.remote_url is None


def test_project_valid_classification_values(app):
    """Test that valid classification values are accepted."""
    from app import db
    
    valid_classifications = ['primary', 'secondary', 'archive', 'maintenance']
    
    for classification in valid_classifications:
        project = Project(name=f"Project {classification}", classification=classification)
        db.session.add(project)
        db.session.commit()
        
        assert project.classification == classification
        db.session.rollback()  # Clean up for next iteration


def test_project_valid_status_values(app):
    """Test that valid status values are accepted."""
    from app import db
    
    valid_statuses = ['active', 'paused', 'completed', 'cancelled']
    
    for status in valid_statuses:
        project = Project(name=f"Project {status}", status=status)
        db.session.add(project)
        db.session.commit()
        
        assert project.status == status
        db.session.rollback()  # Clean up for next iteration


def test_project_to_dict_includes_extended_fields(app):
    """Test that to_dict() includes all extended fields."""
    from app import db
    
    project = Project(
        name="Full Project",
        path="/full/path",
        organization="work",
        classification="primary",
        status="active",
        description="Full description",
        remote_url="https://github.com/user/repo"
    )
    db.session.add(project)
    db.session.commit()
    
    project_dict = project.to_dict()
    
    assert project_dict['organization'] == "work"
    assert project_dict['classification'] == "primary"
    assert project_dict['status'] == "active"
    assert project_dict['description'] == "Full description"
    assert project_dict['remote_url'] == "https://github.com/user/repo"

