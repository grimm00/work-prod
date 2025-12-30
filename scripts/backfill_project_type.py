#!/usr/bin/env python3
"""Backfill project_type field for existing projects."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import create_app, db
from app.models.project import Project


def classify_project(project):
    """Apply heuristics to determine project_type.
    
    Priority order:
    1. DRW organization -> Work
    2. /Learning/ in path -> Learning
    3. archive classification -> Inactive
    4. Default -> Personal
    """
    # Priority 1: DRW organization = Work
    if project.organization == 'DRW':
        return 'Work'
    
    # Priority 2: Learning path = Learning
    if project.path and '/Learning/' in project.path:
        return 'Learning'
    
    # Priority 3: Archive classification = Inactive
    if project.classification == 'archive':
        return 'Inactive'
    
    # Default: Personal
    return 'Personal'


def backfill(dry_run=True):
    """Backfill project_type for all projects."""
    app = create_app()
    with app.app_context():
        projects = Project.query.filter(Project.project_type.is_(None)).all()
        
        results = {'Work': 0, 'Personal': 0, 'Learning': 0, 'Inactive': 0}
        changes = []
        
        for project in projects:
            new_type = classify_project(project)
            results[new_type] += 1
            changes.append({
                'id': project.id,
                'name': project.name,
                'old': project.project_type,
                'new': new_type,
                'reason': f"org={project.organization}, path={project.path}, class={project.classification}"
            })
            
            if not dry_run:
                project.project_type = new_type
        
        if not dry_run:
            db.session.commit()
        
        # Print report
        print(f"\n{'DRY RUN - ' if dry_run else ''}Backfill Results:")
        print(f"  Work: {results['Work']}")
        print(f"  Personal: {results['Personal']}")
        print(f"  Learning: {results['Learning']}")
        print(f"  Inactive: {results['Inactive']}")
        print(f"  Total: {sum(results.values())}")
        
        print(f"\nChanges:")
        for c in changes:
            print(f"  {c['id']}: {c['name']} -> {c['new']} ({c['reason']})")
        
        return results, changes


if __name__ == '__main__':
    dry_run = '--execute' not in sys.argv
    backfill(dry_run=dry_run)

