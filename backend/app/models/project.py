"""
Project model.

Represents a project in the database with core tracking information.
"""

from datetime import datetime
from sqlalchemy import func, Enum
from app import db


class Project(db.Model):
    """Project model for tracking work, personal, and learning projects."""
    
    __tablename__ = 'projects'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Core fields
    name = db.Column(db.String(200), nullable=False, index=True)
    path = db.Column(db.String(500), unique=True, nullable=True)
    
    # Extended fields (Phase 2)
    organization = db.Column(db.String(100), nullable=True, index=True)
    classification = db.Column(
        Enum('primary', 'secondary', 'archive', 'maintenance', name='classification_enum'),
        nullable=True,
        index=True
    )
    status = db.Column(
        Enum('active', 'paused', 'completed', 'cancelled', name='status_enum'),
        nullable=False,
        default='active',
        index=True
    )
    description = db.Column(db.Text, nullable=True)
    remote_url = db.Column(db.String(500), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        """
        Serialize project to dictionary for JSON responses.
        
        Returns:
            dict: Project data as dictionary
            
        Raises:
            LookupError: If enum values in database are invalid (should be caught by caller)
        """
        # Safely access enum fields - if they're invalid, SQLAlchemy will raise LookupError
        # which we catch in the API layer
        try:
            classification = self.classification
        except LookupError:
            # Invalid enum value in database - re-raise to be handled by caller
            raise
        
        try:
            status = self.status
        except LookupError:
            # Invalid enum value in database - re-raise to be handled by caller
            raise
        
        return {
            'id': self.id,
            'name': self.name,
            'path': self.path,
            'organization': self.organization,
            'classification': classification,
            'status': status,
            'description': self.description,
            'remote_url': self.remote_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        """String representation of Project."""
        return f"<Project {self.id}: {self.name}>"

