"""
Performance tests for project queries.

Tests query performance with 100+ projects to ensure all queries < 100ms.
"""

import pytest
import time
from app.models.project import Project
from app import db


@pytest.mark.performance
def test_list_projects_performance(app):
    """Test list projects query performance with 100 projects."""
    with app.app_context():
        # Create 100 test projects
        projects = []
        for i in range(100):
            project = Project(
                name=f"Project {i}",
                path=f"/test/path/{i}",
                status="active" if i % 2 == 0 else "paused",
                organization="work" if i % 3 == 0 else "personal",
                classification="primary" if i % 4 == 0 else "secondary"
            )
            projects.append(project)
        
        db.session.add_all(projects)
        db.session.commit()
        
        # Measure query time
        start = time.time()
        result = Project.query.order_by(Project.id).all()
        elapsed = time.time() - start
        
        assert len(result) >= 100
        assert elapsed < 0.1  # Should be < 100ms
        print(f"\nList projects query: {elapsed*1000:.2f}ms for {len(result)} projects")


@pytest.mark.performance
def test_filter_by_status_performance(app):
    """Test filter by status query performance."""
    with app.app_context():
        # Create 100 test projects (50 active, 50 paused)
        projects = []
        for i in range(100):
            project = Project(
                name=f"Project {i}",
                path=f"/test/path/{i}",
                status="active" if i % 2 == 0 else "paused"
            )
            projects.append(project)
        
        db.session.add_all(projects)
        db.session.commit()
        
        # Measure query time
        start = time.time()
        result = Project.query.filter_by(status="active").all()
        elapsed = time.time() - start
        
        assert len(result) == 50
        assert elapsed < 0.1  # Should be < 100ms
        print(f"\nFilter by status query: {elapsed*1000:.2f}ms for {len(result)} projects")


@pytest.mark.performance
def test_filter_by_organization_performance(app):
    """Test filter by organization query performance."""
    with app.app_context():
        # Create 100 test projects
        projects = []
        for i in range(100):
            project = Project(
                name=f"Project {i}",
                path=f"/test/path/{i}",
                organization="work" if i % 3 == 0 else "personal"
            )
            projects.append(project)
        
        db.session.add_all(projects)
        db.session.commit()
        
        # Measure query time
        start = time.time()
        result = Project.query.filter_by(organization="work").all()
        elapsed = time.time() - start
        
        assert elapsed < 0.1  # Should be < 100ms
        print(f"\nFilter by organization query: {elapsed*1000:.2f}ms for {len(result)} projects")


@pytest.mark.performance
def test_filter_by_classification_performance(app):
    """Test filter by classification query performance."""
    with app.app_context():
        # Create 100 test projects
        projects = []
        for i in range(100):
            project = Project(
                name=f"Project {i}",
                path=f"/test/path/{i}",
                classification="primary" if i % 4 == 0 else "secondary"
            )
            projects.append(project)
        
        db.session.add_all(projects)
        db.session.commit()
        
        # Measure query time
        start = time.time()
        result = Project.query.filter_by(classification="primary").all()
        elapsed = time.time() - start
        
        assert elapsed < 0.1  # Should be < 100ms
        print(f"\nFilter by classification query: {elapsed*1000:.2f}ms for {len(result)} projects")


@pytest.mark.performance
def test_text_search_performance(app):
    """Test text search query performance."""
    with app.app_context():
        # Create 100 test projects with varied names
        projects = []
        for i in range(100):
            project = Project(
                name=f"Project {i}",
                path=f"/test/path/{i}",
                description=f"Description for project {i}" if i % 2 == 0 else None
            )
            projects.append(project)
        
        db.session.add_all(projects)
        db.session.commit()
        
        # Measure query time for text search
        from sqlalchemy import or_
        start = time.time()
        search_pattern = "%Project 5%"
        result = Project.query.filter(
            or_(
                Project.name.ilike(search_pattern),
                Project.description.ilike(search_pattern)
            )
        ).all()
        elapsed = time.time() - start
        
        assert elapsed < 0.1  # Should be < 100ms
        print(f"\nText search query: {elapsed*1000:.2f}ms for {len(result)} projects")


@pytest.mark.performance
def test_get_project_by_id_performance(app):
    """Test get project by ID query performance."""
    with app.app_context():
        # Create 100 test projects
        projects = []
        for i in range(100):
            project = Project(
                name=f"Project {i}",
                path=f"/test/path/{i}"
            )
            projects.append(project)
        
        db.session.add_all(projects)
        db.session.commit()
        
        # Measure query time for get by ID (should use primary key)
        project_id = projects[50].id
        start = time.time()
        result = db.session.get(Project, project_id)
        elapsed = time.time() - start
        
        assert result is not None
        assert elapsed < 0.01  # Should be very fast (< 10ms) with primary key
        print(f"\nGet by ID query: {elapsed*1000:.2f}ms")


@pytest.mark.performance
def test_combined_filters_performance(app):
    """Test combined filter query performance."""
    with app.app_context():
        # Create 100 test projects
        projects = []
        for i in range(100):
            project = Project(
                name=f"Project {i}",
                path=f"/test/path/{i}",
                status="active" if i % 2 == 0 else "paused",
                organization="work" if i % 3 == 0 else "personal",
                classification="primary" if i % 4 == 0 else "secondary"
            )
            projects.append(project)
        
        db.session.add_all(projects)
        db.session.commit()
        
        # Measure query time with multiple filters
        start = time.time()
        result = Project.query.filter_by(
            status="active",
            organization="work",
            classification="primary"
        ).all()
        elapsed = time.time() - start
        
        assert elapsed < 0.1  # Should be < 100ms
        print(f"\nCombined filters query: {elapsed*1000:.2f}ms for {len(result)} projects")

