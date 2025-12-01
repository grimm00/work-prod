# SQLite Database Design Research

**Status:** ✅ Complete (⚠️ Refinement Needed - See Update 2025-12-01)  
**Priority:** 🔴 CRITICAL  
**Category:** Data Model  
**Timeline:** Week 1  
**Last Updated:** 2025-12-01  
**Original Completion:** 2025-11-26

---

## ⚠️ Update 2025-12-01: Inventory Data Reveals Schema Gaps

**Context:** Automated project inventory (59 projects, 24 languages) revealed data model needs not captured in original Week 1 research.

**Gaps Identified:**

1. **No Projects Table**
   - Inventory revealed: 59 projects (20 Work, 16 Personal, 17 Learning, 6 Inactive)
   - Current schema: No way to track projects, their tech stack, or status
   - Needed for: Projects feature (potential 8th core feature)

2. **Skills-to-Projects Relationship Missing**
   - Inventory shows: Languages used in varying numbers of projects (Python in 18, others in 1-2)
   - Current schema: Skills table exists, but no way to track "used in X projects"
   - Needed for: Skills Matrix showing project usage patterns

3. **Classification/Categorization Pattern**
   - Inventory uses: Classification field (Work, Personal, Learning, Inactive)
   - Current schema: No standard pattern for categorization beyond org_id
   - Needed for: Multi-context project management

4. **Organization Field Not Ubiquitous**
   - Inventory shows: Clear Work (34%) vs Personal (27%) vs Learning (29%) split
   - Current schema: Organizations table exists, but not all entities link to it
   - Needed for: Skills table, Tasks table should optionally link to org for context switching

**Impact on Week 2 Research:**

- Skills Matrix data model research must incorporate project tracking
- Daily Focus may need project context (which project am I working on today?)
- Consider if Projects should be added as supporting entity or promoted to core feature

**Action Items:**

- Week 2: Design Skills-to-Projects relationship (many-to-many)
- Week 2: Decide if Projects table needed (see requirements.md for analysis)
- Week 2: Consider adding optional org_id to more tables for multi-context support
- If schema changes significantly, amendment to ADR-0003 may be needed

**See Also:**
- [Requirements - Project Inventory Findings](../../exploration/requirements.md#project-inventory-discovered-data)
- [Current State Inventory](../../exploration/current-state-inventory.md)
- [POC Analysis](../automation/inventory-system-poc-analysis.md)

---

## 📋 Research Questions

1. What are SQLite best practices for single-user applications?
2. How to design database schema for our 7 core features?
3. How to handle migrations with Flask-Migrate/Alembic?
4. What backup and recovery strategies should we use?
5. How to optimize SQLite performance for local use?

---

## 🎯 Research Objectives

**Goal:** Design a comprehensive, normalized database schema that:
- Supports all 7 core features (daily focus, learning, skills, meetings, goals, feedback, energy)
- Uses SQLite best practices for single-user local-first apps
- Implements proper relationships and constraints
- Supports data integrity and evolution through migrations
- Enables efficient queries and backups

---

## 🔍 Research Methodology

1. **SQLite Best Practices Review**
   - Official SQLite documentation
   - Local-first software principles
   - Single-user optimization techniques

2. **Schema Design Analysis**
   - Normalization principles
   - Relationship modeling
   - User requirements mapping

3. **Migration Strategy**
   - Flask-Migrate/Alembic workflow
   - Schema evolution best practices

4. **Backup & Recovery**
   - SQLite backup methods
   - Automation strategies
   - Data portability

---

## 📚 Findings

### 1. SQLite Best Practices for Single-User Apps

**Why SQLite is Perfect for Our Use Case:**

1. **Local-First Architecture**
   - No server setup required
   - Fast access (no network latency)
   - Data stays on user's machine (privacy)
   - Works offline by default

2. **Single-User Optimization**
   - No concurrency issues
   - Simpler locking model
   - Optimized for read-heavy workloads
   - Excellent for our productivity tracking use case

3. **Simplicity**
   - Single file database
   - Zero configuration
   - Easy backups (copy file)
   - Cross-platform

4. **Performance**
   - Fast for local applications
   - Excellent for datasets under 100GB
   - Good query optimization
   - Efficient for our expected data volume

**SQLite Configuration for Flask:**

```python
# In Flask config
SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/workprod.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable to save resources
```

**Recommended Settings:**

```sql
-- Enable foreign key constraints (not on by default in SQLite!)
PRAGMA foreign_keys = ON;

-- Use Write-Ahead Logging for better concurrency
PRAGMA journal_mode = WAL;

-- Optimize for local use
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = -64000;  -- 64MB cache
```

### 2. Database Schema Design

**Core Entities (7 Features):**

1. **Users** - User profile (even for single user, good practice)
2. **Tasks** - Daily focus system
3. **Learnings** - Learning journal entries
4. **Skills** - Skills matrix
5. **People** - Contacts (managers, coaches, colleagues)
6. **Meetings** - Meeting tracking
7. **Goals** - Goals and hiring readiness
8. **Feedback** - Feedback capture
9. **Energy** - Energy/engagement tracking

**Supporting Entities:**

10. **Organizations** - DRW, Apprenti (multi-org support)
11. **Tags** - Flexible categorization
12. **ActionItems** - Follow-ups from meetings/feedback

**Entity Relationship Diagram (ERD) - Text Format:**

```
Organizations
├── id (PK)
├── name
├── type (employer/host)
└── notes

Users (even for single user - future-proofing)
├── id (PK)
├── username
├── email
└── created_at

People (Contacts)
├── id (PK)
├── name
├── role (manager/coach/colleague)
├── organization_id (FK → Organizations)
├── email
└── notes

Tasks (Daily Focus)
├── id (PK)
├── title
├── description
├── priority (high/medium/low)
├── status (todo/in_progress/done)
├── date
├── estimated_time
├── actual_time
├── goal_id (FK → Goals) [optional link]
├── created_at
└── updated_at

Learnings (Learning Journal)
├── id (PK)
├── title
├── content
├── type (aha_moment/concept/insight)
├── date
├── source (meeting/self_study/project)
├── meeting_id (FK → Meetings) [optional]
├── created_at
└── tags (many-to-many → Tags)

Skills (Skills Matrix)
├── id (PK)
├── name
├── category (technical/soft_skill)
├── confidence_level (1-5: learning/beginner/intermediate/proficient/expert)
├── last_used_date
├── notes
├── created_at
└── updated_at

SkillProgress (Track skill development over time)
├── id (PK)
├── skill_id (FK → Skills)
├── confidence_level
├── notes
└── recorded_at

TeamSkillMapping (Skills to team fit)
├── id (PK)
├── skill_id (FK → Skills)
├── team_name
└── relevance (high/medium/low)

Meetings
├── id (PK)
├── title
├── meeting_date
├── meeting_time
├── duration_minutes
├── organization_id (FK → Organizations)
├── preparation_notes
├── outcome_notes
├── questions_asked
├── created_at
└── updated_at

MeetingAttendees (Many-to-many)
├── meeting_id (FK → Meetings)
└── person_id (FK → People)

Goals
├── id (PK)
├── title
├── description
├── type (weekly/monthly/rotation)
├── category (technical/soft_skill/hiring_readiness)
├── start_date
├── target_date
├── status (not_started/in_progress/completed/cancelled)
├── progress_percentage
├── parent_goal_id (FK → Goals) [for goal hierarchy]
├── created_at
└── updated_at

GoalMilestones
├── id (PK)
├── goal_id (FK → Goals)
├── description
├── target_date
├── completed
└── completed_at

Feedback
├── id (PK)
├── from_person_id (FK → People)
├── feedback_date
├── content
├── category (technical/behavioral/general)
├── sentiment (positive/constructive/neutral)
├── created_at
└── tags (many-to-many → Tags)

ActionItems (From feedback or meetings)
├── id (PK)
├── description
├── status (todo/in_progress/done)
├── priority (high/medium/low)
├── due_date
├── source_type (feedback/meeting)
├── source_id (polymorphic: feedback_id or meeting_id)
├── completed_at
└── created_at

EnergyCheckins (Energy & Engagement)
├── id (PK)
├── checkin_datetime
├── energy_level (1-5: very_low/low/medium/high/very_high)
├── engagement_level (1-5: disengaged/low/moderate/engaged/highly_engaged)
├── mood (optional text)
├── notes
└── created_at

Tags (Flexible categorization)
├── id (PK)
├── name
├── category (learning/feedback/general)
└── created_at

LearningTags (Many-to-many)
├── learning_id (FK → Learnings)
└── tag_id (FK → Tags)

FeedbackTags (Many-to-many)
├── feedback_id (FK → Feedback)
└── tag_id (FK → Tags)
```

**Key Relationships:**

1. **Organizations → People** (one-to-many)
   - Each person belongs to an organization

2. **People → Meetings** (many-to-many via MeetingAttendees)
   - Multiple people can attend multiple meetings

3. **Meetings → Learnings** (one-to-many)
   - Learnings can be sourced from meetings

4. **Goals → Tasks** (one-to-many)
   - Tasks can link to goals

5. **Goals → Goals** (self-referencing for hierarchy)
   - Parent goals can have child goals

6. **Skills → SkillProgress** (one-to-many)
   - Track skill development over time

7. **Tags → Learnings/Feedback** (many-to-many)
   - Flexible categorization

### 3. SQLAlchemy Model Implementation

**Base Configuration:**

```python
# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps"""
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

**Example Models:**

```python
# app/models/organization.py
from app.extensions import db

class Organization(db.Model):
    __tablename__ = 'organizations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'employer' or 'host'
    notes = db.Column(db.Text)
    
    # Relationships
    people = db.relationship('Person', backref='organization', lazy=True)
    meetings = db.relationship('Meeting', backref='organization', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'notes': self.notes
        }

# app/models/person.py
from app.extensions import db

class Person(db.Model):
    __tablename__ = 'people'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50))  # manager, coach, colleague
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    email = db.Column(db.String(120))
    notes = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'organization': self.organization.name if self.organization else None,
            'email': self.email
        }

# app/models/task.py
from app.extensions import db, TimestampMixin
from datetime import date

class Task(TimestampMixin, db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')  # high, medium, low
    status = db.Column(db.String(20), default='todo')  # todo, in_progress, done
    date = db.Column(db.Date, default=date.today, nullable=False)
    estimated_time = db.Column(db.Integer)  # minutes
    actual_time = db.Column(db.Integer)  # minutes
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'date': self.date.isoformat(),
            'estimated_time': self.estimated_time,
            'actual_time': self.actual_time,
            'goal_id': self.goal_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# app/models/skill.py
from app.extensions import db, TimestampMixin

class Skill(TimestampMixin, db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50))  # technical, soft_skill
    confidence_level = db.Column(db.Integer, default=1)  # 1-5
    last_used_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    
    # Relationships
    progress = db.relationship('SkillProgress', backref='skill', lazy=True, order_by='SkillProgress.recorded_at.desc()')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'confidence_level': self.confidence_level,
            'last_used_date': self.last_used_date.isoformat() if self.last_used_date else None,
            'notes': self.notes
        }

class SkillProgress(db.Model):
    __tablename__ = 'skill_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    confidence_level = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
```

### 4. Database Migrations with Flask-Migrate

**Setup:**

```bash
# Initialize migrations
flask db init

# Create initial migration
flask db migrate -m "Initial schema"

# Apply migration
flask db upgrade
```

**Migration Workflow:**

1. **Make Model Changes**
   ```python
   # Add new field to model
   class Task(db.Model):
       # ... existing fields ...
       completed_at = db.Column(db.DateTime)  # NEW FIELD
   ```

2. **Generate Migration**
   ```bash
   flask db migrate -m "Add completed_at to tasks"
   ```

3. **Review Migration File**
   ```python
   # migrations/versions/xxx_add_completed_at.py
   def upgrade():
       op.add_column('tasks', sa.Column('completed_at', sa.DateTime(), nullable=True))
   
   def downgrade():
       op.drop_column('tasks', 'completed_at')
   ```

4. **Apply Migration**
   ```bash
   flask db upgrade
   ```

5. **Rollback if Needed**
   ```bash
   flask db downgrade  # Go back one migration
   ```

**Best Practices:**

- Always review auto-generated migrations
- Test migrations on copy of database first
- Include both upgrade and downgrade functions
- Name migrations descriptively
- Keep migrations small and focused
- Never edit applied migrations

### 5. Backup and Recovery Strategies

**Backup Methods for SQLite:**

**Method 1: File Copy (Simplest)**

```python
# app/services/backup_service.py
import shutil
from datetime import datetime
from pathlib import Path

class BackupService:
    @staticmethod
    def create_backup(db_path, backup_dir):
        """Create timestamped backup of database"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = Path(backup_dir) / f'backup_{timestamp}.db'
        
        # Ensure backup directory exists
        Path(backup_dir).mkdir(parents=True, exist_ok=True)
        
        # Copy database file
        shutil.copy2(db_path, backup_path)
        
        return backup_path
    
    @staticmethod
    def cleanup_old_backups(backup_dir, keep_last=7):
        """Keep only the last N backups"""
        backups = sorted(Path(backup_dir).glob('backup_*.db'))
        
        # Delete oldest backups
        for old_backup in backups[:-keep_last]:
            old_backup.unlink()
```

**Method 2: SQLite Backup API (Safer)**

```python
import sqlite3

def backup_database(source_db, dest_db):
    """Use SQLite's backup API for consistent backup"""
    source = sqlite3.connect(source_db)
    dest = sqlite3.connect(dest_db)
    
    with dest:
        source.backup(dest)
    
    source.close()
    dest.close()
```

**Automated Backup Strategy:**

1. **Daily Backups**
   - Run backup before first use each day
   - Keep last 7 daily backups

2. **Weekly Backups**
   - Run backup every Sunday
   - Keep last 4 weekly backups

3. **Export Formats**
   - JSON export for portability
   - CSV export for spreadsheet access
   - SQL dump for migration

**Backup Schedule Implementation:**

```python
# app/services/backup_scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.backup_service import BackupService

def init_backup_scheduler(app):
    scheduler = BackgroundScheduler()
    
    # Daily backup at 6 AM
    scheduler.add_job(
        func=lambda: BackupService.create_backup(
            app.config['SQLALCHEMY_DATABASE_URI'],
            'backups/daily'
        ),
        trigger='cron',
        hour=6,
        minute=0
    )
    
    # Weekly backup on Sunday at midnight
    scheduler.add_job(
        func=lambda: BackupService.create_backup(
            app.config['SQLALCHEMY_DATABASE_URI'],
            'backups/weekly'
        ),
        trigger='cron',
        day_of_week='sun',
        hour=0,
        minute=0
    )
    
    scheduler.start()
```

### 6. Performance Optimization

**Indexing Strategy:**

```python
# Add indexes to frequently queried columns
class Task(db.Model):
    # ... fields ...
    
    __table_args__ = (
        db.Index('idx_task_date', 'date'),
        db.Index('idx_task_status', 'status'),
        db.Index('idx_task_date_status', 'date', 'status'),  # Compound index
    )

class Meeting(db.Model):
    # ... fields ...
    
    __table_args__ = (
        db.Index('idx_meeting_date', 'meeting_date'),
        db.Index('idx_meeting_org', 'organization_id'),
    )
```

**Query Optimization:**

```python
# Use eager loading to avoid N+1 queries
tasks_with_goals = Task.query.options(db.joinedload(Task.goal)).filter_by(date=today).all()

# Use select_in loading for collections
meetings = Meeting.query.options(db.selectinload(Meeting.attendees)).all()

# Pagination for large result sets
tasks = Task.query.paginate(page=1, per_page=50)
```

**Database Maintenance:**

```sql
-- Vacuum to reclaim space and defragment
VACUUM;

-- Analyze to update query planner statistics
ANALYZE;

-- Check integrity
PRAGMA integrity_check;
```

---

## 📊 Analysis

### Strengths of Design

1. **Comprehensive Coverage**
   - All 7 core features modeled
   - Proper relationships defined
   - Flexibility for future growth

2. **Data Integrity**
   - Foreign key constraints
   - Unique constraints where needed
   - Nullable/not-nullable properly defined

3. **Normalization**
   - Reduced data redundancy
   - Clear entity boundaries
   - Proper many-to-many relationships

4. **Scalability**
   - Timestamp mixins
   - Soft delete capability (can add)
   - Hierarchical goals
   - Progress tracking over time

5. **Query Efficiency**
   - Strategic indexing
   - Optimized relationships
   - Eager loading support

### Potential Challenges

1. **Complexity**
   - 12+ tables may seem overwhelming initially
   - Mitigation: Implement incrementally by feature

2. **Migration Management**
   - Schema changes need careful handling
   - Mitigation: Strong migration testing process

3. **Performance at Scale**
   - SQLite limits at very large datasets
   - Mitigation: Likely years before this is an issue

---

## 💡 Recommendations

### 1. Implement Schema Incrementally

**Recommendation:** Build database schema feature-by-feature

**Phase 1 (MVP):**
- Users, Tasks, Organizations

**Phase 2:**
- Learnings, Skills, Tags

**Phase 3:**
- People, Meetings, Goals

**Phase 4:**
- Feedback, ActionItems, EnergyCheckins

### 2. Use Foreign Key Constraints

**Recommendation:** Enable and enforce foreign key constraints

**Rationale:**
- Data integrity
- Prevents orphaned records
- Catches bugs early

### 3. Implement TimestampMixin

**Recommendation:** Use mixin for created_at/updated_at

**Rationale:**
- Audit trail
- Debugging
- Data analysis
- Consistent across all models

### 4. Strategic Indexing

**Recommendation:** Add indexes to frequently queried columns

**Focus Areas:**
- Date fields (tasks.date, meetings.meeting_date)
- Status fields (tasks.status, goals.status)
- Foreign keys (automatically indexed by some databases, but explicit is better)

### 5. Automated Backups

**Recommendation:** Implement daily automated backups

**Strategy:**
- Before-first-use daily backup
- Keep last 7 days
- Weekly backups kept for 4 weeks
- Export functionality for portability

---

## 🚀 Implementation Plan

### Phase 1: Setup (Day 1)

1. **Configure SQLAlchemy**
   - Set up database URI
   - Configure Flask-Migrate
   - Initialize migrations

2. **Create Base Models**
   - TimestampMixin
   - Base model class
   - Common utilities

### Phase 2: Core Models (Days 1-2)

1. **Implement MVP Models**
   - Organization
   - User
   - Task (Daily Focus)

2. **Create Initial Migration**
   - Generate migration
   - Review and test
   - Apply to database

### Phase 3: Expand Schema (Days 2-3)

1. **Add Feature Models**
   - Learning
   - Skill (with SkillProgress)
   - Person
   - Meeting

2. **Implement Relationships**
   - Foreign keys
   - Many-to-many tables
   - Test relationships

### Phase 4: Polish (Day 3-4)

1. **Add Remaining Models**
   - Goal (with Milestones)
   - Feedback
   - ActionItem
   - EnergyCheckin
   - Tags

2. **Implement Backup System**
   - Backup service
   - Scheduled backups
   - Export functionality

---

## 📦 Deliverables

### 1. Database Schema Design

**Status:** ✅ This document

**Content:**
- Complete ERD
- All 12+ tables defined
- Relationships documented
- Index strategy

### 2. SQLAlchemy Models

**Status:** 🔴 To Do

**Deliverable:**
- All model files created
- Relationships implemented
- Mixins and utilities
- Model tests

### 3. Migration Setup

**Status:** 🔴 To Do

**Deliverable:**
- Flask-Migrate configured
- Initial migration created
- Migration tested
- Rollback tested

### 4. Backup System

**Status:** 🔴 To Do

**Deliverable:**
- Backup service implemented
- Automated scheduling
- Retention policy
- Export functionality

---

## 🔗 References

### Official Documentation

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

### Best Practices

- Database normalization principles
- SQLite optimization techniques
- Local-first software design
- Migration best practices

### Related Research

- [Flask Backend Architecture](flask-backend-architecture.md) - Complete
- [React Frontend Architecture](react-frontend-architecture.md) - Complete
- [Flask + React Integration](flask-react-integration.md) - To Do

---

## ✅ Decision

**Decision:** Implement comprehensive normalized schema with incremental rollout and automated backups

**Schema Summary:**
- **12+ tables** covering all 7 core features
- **Proper relationships** with foreign keys
- **Strategic indexing** for performance
- **Timestamp tracking** for all entities
- **Flexible tagging** system
- **Hierarchical goals** support
- **Progress tracking** over time

**Migration Strategy:**
- Flask-Migrate with Alembic
- Incremental feature-by-feature implementation
- Test migrations before applying
- Maintain rollback capability

**Backup Strategy:**
- Daily automated backups (keep 7)
- Weekly backups (keep 4)
- Multiple export formats (JSON, CSV, SQL)
- Simple file-copy for recovery

**Next Steps:**
1. Create SQLAlchemy models
2. Set up Flask-Migrate
3. Generate and apply initial migration
4. Implement backup service
5. Test database operations

---

**Last Updated:** 2025-11-26  
**Status:** ✅ Complete  
**Next:** Begin Flask + React integration research

