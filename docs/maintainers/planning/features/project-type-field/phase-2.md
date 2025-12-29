# Project Type Field - Phase 2: Data Backfill

**Feature:** Add `project_type` field  
**Phase:** 2 of 3  
**Status:** 🟠 In Progress  
**Estimated Effort:** ~2 hours  
**Created:** 2025-12-23  
**Last Updated:** 2025-12-29  
**Dependencies:** Phase 1 complete

---

## 📋 Phase Overview

Populate `project_type` for existing projects using heuristics.

**Goal:** All existing projects have a `project_type` value based on available data.

---

## 🎯 Phase Goals

- [ ] Create backfill script with heuristics
- [ ] Run backfill in dry-run mode first
- [ ] Execute backfill on database
- [ ] Validate and document results

---

## 📋 Backfill Heuristics

From ADR-003, apply heuristics in this order:

| Priority | Condition | Result |
|----------|-----------|--------|
| 1 | `organization = 'DRW'` | `Work` |
| 2 | `path LIKE '%/Learning/%'` | `Learning` |
| 3 | `classification = 'archive'` | `Inactive` |
| 4 | Remaining (default) | `Personal` |

**Notes:**
- Heuristics are imperfect - some projects may need manual correction
- Default to `Personal` is conservative (most common non-work type)

---

## 📝 Tasks

### Task 1: Write Backfill Script Tests (TDD - RED) (~30 min)

**File:** `scripts/tests/test_backfill_project_type.py`

Write tests for the classification heuristics before implementing:

```python
"""Tests for backfill_project_type script."""

import pytest


class TestClassifyProject:
    """Test classify_project heuristics."""

    def test_drw_organization_returns_work(self):
        """Priority 1: DRW organization -> Work."""
        # Arrange
        project = MockProject(organization='DRW', path='/some/path', classification='primary')
        # Act
        result = classify_project(project)
        # Assert
        assert result == 'Work'

    def test_learning_path_returns_learning(self):
        """Priority 2: /Learning/ in path -> Learning."""
        project = MockProject(organization=None, path='/Users/me/Learning/python', classification='primary')
        result = classify_project(project)
        assert result == 'Learning'

    def test_archive_classification_returns_inactive(self):
        """Priority 3: archive classification -> Inactive."""
        project = MockProject(organization=None, path='/some/path', classification='archive')
        result = classify_project(project)
        assert result == 'Inactive'

    def test_default_returns_personal(self):
        """Priority 4: No match -> Personal (default)."""
        project = MockProject(organization=None, path='/some/path', classification='primary')
        result = classify_project(project)
        assert result == 'Personal'

    def test_drw_takes_priority_over_learning_path(self):
        """DRW organization takes priority over Learning path."""
        project = MockProject(organization='DRW', path='/Learning/project', classification='primary')
        result = classify_project(project)
        assert result == 'Work'  # DRW wins over Learning path

    def test_learning_path_takes_priority_over_archive(self):
        """Learning path takes priority over archive classification."""
        project = MockProject(organization=None, path='/Learning/old', classification='archive')
        result = classify_project(project)
        assert result == 'Learning'  # Learning wins over archive
```

**Acceptance Criteria:**
- [ ] Test file created
- [ ] Tests for each heuristic priority
- [ ] Tests for priority ordering (DRW > Learning > Archive > Default)
- [ ] Tests fail initially (RED phase)

---

### Task 2: Create Backfill Script (TDD - GREEN) (~45 min)

**File:** `scripts/backfill_project_type.py`

Implement the script to make tests pass:

```python
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
```

**Acceptance Criteria:**
- [ ] Script created
- [ ] Heuristics implemented in correct priority order
- [ ] Dry-run mode by default
- [ ] Reports results and changes
- [ ] All tests pass (GREEN phase)

---

### Task 3: Run Dry-Run and Execute Backfill (~30 min)

**Dry-Run Command:**
```bash
cd scripts
python backfill_project_type.py
```

**Review Output:**
- Verify classification counts look reasonable
- Check specific projects that may be misclassified
- Document any manual corrections needed

**Expected Distribution (approximate):**
- Work: ~10-15 projects (DRW organization)
- Learning: ~15-20 projects (/Learning/ path)
- Inactive: ~5-10 projects (archive classification)
- Personal: ~15-20 projects (remainder)

**Execute Command:**
```bash
cd scripts
python backfill_project_type.py --execute
```

**Validation Query:**
```sql
-- Check for any NULL project_type
SELECT COUNT(*) FROM project WHERE project_type IS NULL;

-- Distribution check
SELECT project_type, COUNT(*) FROM project GROUP BY project_type;
```

**Acceptance Criteria:**
- [ ] Dry-run completes successfully
- [ ] Results reviewed and reasonable
- [ ] Backfill executed successfully
- [ ] All projects have project_type
- [ ] No NULL values remain

---

### Task 4: Document Results (~15 min)

**Create:** `scripts/backfill_project_type_results.md`

Document:
- Final distribution counts
- Any manual corrections made
- Projects that may need review

**Acceptance Criteria:**
- [ ] Results documented
- [ ] Manual corrections noted

---

## ✅ Phase Completion Criteria

- [ ] Tests written for backfill heuristics
- [ ] Backfill script created and tests pass
- [ ] Dry-run reviewed and approved
- [ ] Backfill executed successfully
- [ ] All projects have `project_type`
- [ ] Results documented

---

## 📊 Progress Tracking

| Task | Status | Notes |
|------|--------|-------|
| Task 1: Write Tests (RED) | 🔴 Not Started | |
| Task 2: Create Script (GREEN) | 🔴 Not Started | |
| Task 3: Run & Execute | 🔴 Not Started | |
| Task 4: Document Results | 🔴 Not Started | |

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Transition Plan](transition-plan.md)
- [Phase 1: Schema Migration](phase-1.md)
- [Phase 3: API Updates](phase-3.md)
- [ADR-003](../../../../../dev-infra/admin/decisions/project-model-definition/adr-003-add-project-type-field.md)

---

**Last Updated:** 2025-12-29
