# ADR-0003: SQLite Database Design

**Status:** Accepted  
**Date:** 2025-11-26  
**Supersedes:** None  
**Superseded By:** N/A

---

## Context

We needed to design a database schema and select appropriate data persistence technology for the work productivity tracking application. Requirements included:

- Support for 7 core features (daily focus, learning journal, skills matrix, meetings, goals, feedback, energy tracking)
- Local-first architecture (privacy-focused, offline-capable)
- Single-user operation
- Data relationships and integrity
- Schema evolution support (migrations)
- Backup and recovery capability
- Performance for local queries

Key considerations:
- Database technology choice (local vs. server)
- Schema design and normalization
- Migration strategy for schema changes
- Backup automation
- Data portability

## Decision

We will use **SQLite** as our database with a **comprehensive normalized schema** (12+ tables), **Flask-Migrate for migrations**, and **automated backup strategy**.

### Core Design Decisions:

1. **Database Technology: SQLite**
   - Local file-based database
   - Zero configuration required
   - Perfect for single-user applications
   - Fast for local operations
   - Built-in to Python

2. **Schema Design: Normalized 12+ Tables**
   - Organizations (DRW, Apprenti)
   - Users (future-proofing)
   - People (contacts/relationships)
   - Tasks (daily focus)
   - Learnings (journal entries)
   - Skills + SkillProgress (matrix with history)
   - Meetings + MeetingAttendees
   - Goals + GoalMilestones
   - Feedback
   - ActionItems (from meetings/feedback)
   - EnergyCheckins
   - Tags (flexible categorization)

3. **Migration Strategy: Flask-Migrate (Alembic)**
   - Version-controlled schema changes
   - Automatic migration generation
   - Rollback capability
   - Incremental feature implementation

4. **Backup Strategy: Automated Daily Backups**
   - File-copy backups before first use each day
   - Keep last 7 daily backups
   - Keep last 4 weekly backups
   - Export capabilities (JSON, CSV, SQL)

5. **Data Integrity: Foreign Key Constraints**
   - Enable FK constraints (not default in SQLite)
   - Proper relationships between entities
   - Cascading deletes where appropriate
   - Unique constraints on natural keys

### Key Schema Patterns:

- **TimestampMixin**: created_at/updated_at on all tables
- **Soft Deletes**: Can add deleted_at column if needed
- **Hierarchical Goals**: Self-referencing for parent/child goals
- **Progress Tracking**: Separate tables for historical data (SkillProgress)
- **Many-to-Many**: Separate junction tables (MeetingAttendees, Tags)
- **Strategic Indexing**: Date fields, status fields, foreign keys

## Consequences

### Positive

- **Privacy**: Data stays on user's machine; no server required
- **Performance**: Fast local queries; no network latency
- **Simplicity**: Single file database; easy to back up (copy file)
- **Offline**: Works without internet connection
- **Zero Config**: No database server to install/manage
- **Portability**: SQLite file is cross-platform
- **Comprehensive Schema**: Supports all 7 features with proper relationships
- **Scalability**: Normalized design allows adding features without major refactoring
- **Data Integrity**: Foreign keys prevent orphaned records
- **Evolution**: Flask-Migrate handles schema changes cleanly
- **Backup**: Simple file operations enable automated backups

### Negative

- **Concurrency**: Not suitable for multi-user (not an issue for us)
- **Size Limitations**: SQLite degrades after ~100GB (unlikely for personal productivity data)
- **No Built-in Replication**: Can't replicate to multiple devices easily
- **Schema Complexity**: 12+ tables may seem heavy initially
- **Migration Management**: Requires discipline to manage migrations properly

**Mitigation:**
- Concurrency not an issue (single-user app)
- Size limits irrelevant (years of data still under 1GB)
- Multi-device sync can be added later if needed
- Implement tables incrementally (start with 3-4, add as features develop)
- Strong migration testing process and documentation

## Alternatives Considered

### Alternative 1: PostgreSQL

**Description:** Full-featured relational database server

**Pros:**
- Robust feature set
- Excellent for multi-user
- Advanced query capabilities
- Better concurrency handling

**Cons:**
- Requires server installation and management
- Overkill for single-user
- More complex deployment
- Network overhead (even locally)
- Harder for users to back up

**Why Not Chosen:** Unnecessary complexity for single-user local app. Would require users to install and manage database server. SQLite's simplicity better matches use case.

### Alternative 2: JSON Files

**Description:** Store data in JSON files on filesystem

**Pros:**
- Extremely simple
- Human-readable
- Easy to version control
- No database setup

**Cons:**
- No query capabilities
- No relationships/integrity
- Poor performance at scale
- No transactions
- Manual backup logic
- Concurrent access issues

**Why Not Chosen:** Doesn't scale beyond toy apps. No relationship support means duplicated data. Performance degrades quickly. Would need to rebuild database features manually.

### Alternative 3: MongoDB / Document Database

**Description:** NoSQL document-oriented database

**Pros:**
- Flexible schema
- JSON-like documents
- Good for rapidly changing requirements

**Cons:**
- Overkill for structured data
- Requires server (like PostgreSQL)
- Relationships less natural
- More complex queries
- Larger footprint

**Why Not Chosen:** Our data is highly relational (meetings have people, tasks link to goals, etc.). SQL better fits our needs. Would trade simplicity for flexibility we don't need.

### Alternative 4: Denormalized Single-Table Design

**Description:** Store all data in minimal tables with embedded JSON

**Pros:**
- Fewer tables
- Simpler queries initially
- Faster writes

**Cons:**
- Data duplication
- Update anomalies
- Difficult to maintain integrity
- Complicated queries as features grow
- Harder to add relationships later

**Why Not Chosen:** Would cause problems as features grow. Normalized design makes relationships clear and prevents duplication. Refactoring from denormalized to normalized is painful.

## Implementation Notes

1. **Incremental Rollout:**
   - **Phase 1 (MVP):** Users, Organizations, Tasks
   - **Phase 2:** Learnings, Skills, Tags
   - **Phase 3:** People, Meetings, Goals
   - **Phase 4:** Feedback, ActionItems, EnergyCheckins

2. **SQLite Configuration:**
   ```python
   # Enable foreign key constraints
   PRAGMA foreign_keys = ON;
   
   # Use WAL mode for better concurrency
   PRAGMA journal_mode = WAL;
   
   # Optimize for local use
   PRAGMA synchronous = NORMAL;
   PRAGMA cache_size = -64000;  # 64MB cache
   ```

3. **TimestampMixin Pattern:**
   ```python
   class TimestampMixin:
       created_at = db.Column(db.DateTime, default=datetime.utcnow)
       updated_at = db.Column(db.DateTime, 
                             default=datetime.utcnow, 
                             onupdate=datetime.utcnow)
   ```

4. **Migration Workflow:**
   ```bash
   # Create migration
   flask db migrate -m "Add tasks table"
   
   # Review auto-generated migration
   # Edit if needed
   
   # Apply migration
   flask db upgrade
   
   # Rollback if needed
   flask db downgrade
   ```

5. **Backup Service:**
   ```python
   def create_backup(db_path, backup_dir):
       timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
       backup_path = f"{backup_dir}/backup_{timestamp}.db"
       shutil.copy2(db_path, backup_path)
       cleanup_old_backups(backup_dir, keep_last=7)
   ```

## References

- [SQLite Database Design Research](../research/tech-stack/sqlite-database-design.md) - Comprehensive analysis (700+ lines)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)

---

**Last Updated:** 2025-11-26  
**Status:** ✅ Accepted and Active


