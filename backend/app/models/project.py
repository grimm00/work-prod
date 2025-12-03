"""
Project model.

Represents a project in the database with core tracking information.
"""

from datetime import datetime
from sqlalchemy import func
from app import db


class Project(db.Model):
    """Project model for tracking work, personal, and learning projects."""
    
    __tablename__ = 'projects'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Core fields
    name = db.Column(db.String(200), nullable=False, index=True)
    path = db.Column(db.String(500), unique=True, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        """
        Serialize project to dictionary for JSON responses.
        
        Returns:
            dict: Project data as dictionary
        """
        return {
            'id': self.id,
            'name': self.name,
            'path': self.path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        """String representation of Project."""
        return f"<Project {self.id}: {self.name}>"

