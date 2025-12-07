# Projects Data Model Research

**Status:** 🟠 In Progress  
**Priority:** 🔴 CRITICAL (Week 2 Priority #1)  
**Category:** Data Model  
**Created:** 2025-12-01  
**Last Updated:** 2025-12-01

---

## 📋 Executive Summary

This research designs the **Projects table schema** and associated relationships to support the Projects-First MVP strategy. Based on automated inventory findings (59 projects, 24 technologies), we need a comprehensive data model that:

1. **Tracks project metadata** (name, path, remote URL, organization)
2. **Classifies projects** (Work, Personal, Learning, Inactive)
3. **Sub-classifies Learning projects** (work-related vs personal development)
4. **Associates projects with skills** (many-to-many relationship)
5. **Supports search and filtering** (SQLite FTS5)
6. **Enables GitHub sync** (remote metadata updates)
7. **Provides import path** (59 projects from inventory POC)

**Key Findings:**
- Projects table requires 15+ fields for comprehensive tracking
- Learning sub-classification is MVP-critical (17 of 59 projects are Learning)
- SQLite FTS5 provides adequate full-text search for <1000 projects
- Remote URL serves as natural deduplication key
- Import strategy requires user input for Learning classification

---

## 🎯 Research Questions

### 1. Core Schema Design

**Q: How to model the Projects table?**

**Required Fields:**
- `id` (INTEGER PRIMARY KEY) - Auto-incrementing identifier
- `name` (TEXT NOT NULL) - Display name for project
- `path` (TEXT) - Local filesystem path (~/Projects/work-prod)
- `remote_url` (TEXT UNIQUE) - GitHub/GitLab URL (deduplication key)
- `organization_id` (INTEGER FK) - DRW, Apprenti, Personal, or NULL
- `classification` (TEXT NOT NULL) - Work, Personal, Learning, Inactive
- `status` (TEXT NOT NULL) - active, learning, archived, inactive
- `description` (TEXT) - Optional project description
- `created_at` (DATETIME) - Record creation timestamp
- `updated_at` (DATETIME) - Last modification timestamp

**Optional/Computed Fields:**
- `last_worked_on` (DATE) - Last git commit or file modification
- `is_active` (BOOLEAN) - Computed from status
- `project_size` (INTEGER) - Lines of code or file count

**Decision:** Use comprehensive schema with all fields. Storage is cheap, flexibility is valuable.

### 2. Learning Sub-Classification (MVP CRITICAL)

**Q: How to model Work-related vs Personal development learning?**

**Challenge:** 17 Learning projects (29% of portfolio) need distinction between:
- Learning Python for work tasks (work-related)
- Learning game development for fun (personal)
- Learning React for both work and side projects (hybrid)

**Schema Design:**

```sql
-- Learning-specific fields (only populated when classification='Learning')
learning_type TEXT CHECK (learning_type IN ('work_related', 'personal_dev', 'hybrid') OR learning_type IS NULL)
learning_context TEXT  -- Free-form description of learning goals
learning_status TEXT CHECK (learning_status IN ('exploring', 'active_learning', 'completed', 'paused') OR learning_status IS NULL)
```

**Rules:**
- `learning_type` required when `classification='Learning'`, NULL otherwise
- `learning_context` provides free-form description (e.g., "Learning Python for data analysis at work")
- `learning_status` tracks learning progress separately from project status

**UI Implications:**
- Filter projects by learning_type: "Show all work-related learning"
- Badge display: 🏢 Work Learning, 🏠 Personal Learning, 🔄 Hybrid
- Metrics separation: Work learning may count toward work hours

**Metrics Impact:**
```
Work Projects: 20
Work-Related Learning: 8 (estimated, needs classification)
Total Work Context: 28

Personal Projects: 16
Personal Development Learning: 7 (estimated)
Total Personal Context: 23
```

**Decision:** Include learning_type, learning_context, learning_status as dedicated fields. This is MVP-critical for accurate project organization.

### 3. Tech Stack Tracking

**Q: How to store discovered technologies (24 languages)?**

**Options Evaluated:**

**Option A: JSON Field (RECOMMENDED)**
```sql
tech_stack JSON DEFAULT '[]'
-- Example: ["Python", "JavaScript", "SQL", "Docker"]
```

**Pros:**
- Simple to store and retrieve
- No additional tables needed
- Easy to query with JSON functions
- Matches inventory POC data structure

**Cons:**
- Harder to enforce referential integrity
- Can't easily query "all projects using Python"
- Duplication of skill names

**Option B: Many-to-Many with Skills Table**
```sql
CREATE TABLE projects_skills (
    project_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    proficiency_used TEXT,  -- beginner, intermediate, advanced, expert
    PRIMARY KEY (project_id, skill_id),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);
```

**Pros:**
- Referential integrity enforced
- Can query "all projects using Python" easily
- Proficiency tracking per project
- No duplication of skill names
- Better for Skills Matrix feature

**Cons:**
- Requires Skills table to exist first
- More complex queries
- Requires junction table management

**Option C: Hybrid Approach (RECOMMENDED)**
```sql
-- Projects table includes JSON field for quick access
tech_stack JSON DEFAULT '[]'

-- projects_skills junction table for proper relationships
-- (populated after Skills table is seeded)
```

**Pros:**
- JSON field works immediately for import
- Can migrate to junction table when Skills Matrix implemented
- Best of both worlds

**Cons:**
- Data duplication (tech_stack JSON and projects_skills records)
- Need to keep in sync

**Decision:** Use Hybrid Approach. Start with JSON field for Phase 1 import, add projects_skills junction table in Phase 2 when Skills Matrix is built.

### 4. Projects-to-Skills Relationship

**Q: How to design the many-to-many relationship?**

**Schema:**

```sql
CREATE TABLE projects_skills (
    project_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    proficiency_used TEXT CHECK (proficiency_used IN ('beginner', 'intermediate', 'advanced', 'expert') OR proficiency_used IS NULL),
    hours_spent INTEGER DEFAULT 0,  -- Optional: track time investment
    is_primary_skill BOOLEAN DEFAULT 0,  -- Flag main skill for project
    notes TEXT,  -- Optional: how skill was used
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (project_id, skill_id),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);

-- Indexes for common queries
CREATE INDEX idx_projects_skills_project ON projects_skills(project_id);
CREATE INDEX idx_projects_skills_skill ON projects_skills(skill_id);
CREATE INDEX idx_projects_skills_primary ON projects_skills(is_primary_skill) WHERE is_primary_skill = 1;
```

**Key Features:**
- `proficiency_used`: Track skill level for this specific project
- `hours_spent`: Optional time investment tracking
- `is_primary_skill`: Flag main technology (e.g., Python for ML project)
- `notes`: Context for how skill was used
- Cascading deletes: Remove associations when project deleted

**Query Examples:**

```sql
-- Find all projects using Python
SELECT p.* FROM projects p
JOIN projects_skills ps ON p.id = ps.project_id
JOIN skills s ON ps.skill_id = s.id
WHERE s.name = 'Python';

-- Find primary skills for a project
SELECT s.name, ps.proficiency_used
FROM skills s
JOIN projects_skills ps ON s.id = ps.skill_id
WHERE ps.project_id = 42 AND ps.is_primary_skill = 1;

-- Count projects per skill
SELECT s.name, COUNT(ps.project_id) as project_count
FROM skills s
LEFT JOIN projects_skills ps ON s.id = ps.skill_id
GROUP BY s.id
ORDER BY project_count DESC;
```

**Decision:** Use junction table with proficiency and primary skill tracking. This supports rich Skills Matrix features.

### 5. Project Classification System

**Q: What classifications are needed?**

**Categories:**
- **Work:** Projects for DRW or work-related activities
- **Personal:** Side projects, hobby projects
- **Learning:** Educational projects (requires sub-classification)
- **Inactive:** Archived, abandoned, or completed projects

**Inventory Distribution:**
- Work: 20 projects (34%)
- Personal: 16 projects (27%)
- Learning: 17 projects (29%)
- Inactive: 6 projects (10%)

**Classification Rules:**

1. **Work Projects:**
   - Organization = DRW or Apprenti
   - Work-related deliverables
   - May include work-related learning

2. **Personal Projects:**
   - Organization = Personal or NULL
   - Side projects, experiments
   - May include personal learning

3. **Learning Projects:**
   - Primary purpose is learning/education
   - Requires learning_type classification
   - May transition to Work or Personal later

4. **Inactive Projects:**
   - Archived or abandoned
   - No recent activity (>6 months)
   - Completed and no longer maintained

**Transitions:**
```
Learning (exploring) → Learning (active_learning) → Learning (completed)
                     ↓
                   Work or Personal (project graduates from learning)
```

**Schema Enforcement:**

```sql
classification TEXT NOT NULL 
    CHECK (classification IN ('Work', 'Personal', 'Learning', 'Inactive'))
```

**Decision:** Use 4-category classification with check constraints. Support transitions via status updates.

### 6. Organization Context

**Q: How to model multi-organizational context (DRW, Apprenti, Personal)?**

**Inventory Distribution:**
- DRW: ~18 projects
- Apprenti: ~2 projects  
- Personal: ~33 projects
- Unclassified: ~6 projects

**Schema Options:**

**Option A: Simple String Field**
```sql
organization TEXT  -- 'DRW', 'Apprenti', 'Personal', NULL
```

**Pros:**
- Simple, no joins needed
- Fast queries
- Easy to understand

**Cons:**
- Typo risk ('DRw', 'drw')
- No metadata about organization
- Can't enforce referential integrity

**Option B: Foreign Key to Organizations Table (RECOMMENDED)**
```sql
organization_id INTEGER,
FOREIGN KEY (organization_id) REFERENCES organizations(id)
```

**Pros:**
- Referential integrity enforced
- Can store organization metadata (logo, color, description)
- Prevents typos
- Supports future expansion (new organizations)

**Cons:**
- Requires Organizations table
- Slightly more complex queries (JOIN)

**Decision:** Use Foreign Key to Organizations table (already exists in Phase 1 schema from ADR-0003). This provides data integrity and future flexibility.

**Organizations Table (Reference):**
```sql
CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,  -- 'DRW', 'Apprenti', 'Personal'
    display_name TEXT,  -- 'DRW Trading', 'Apprenti/WTIA', 'Personal Projects'
    type TEXT,  -- 'employer_host', 'employer', 'personal'
    color TEXT,  -- UI color code
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Seed data
INSERT INTO organizations (name, display_name, type) VALUES
    ('DRW', 'DRW Trading', 'employer_host'),
    ('Apprenti', 'Apprenti/WTIA', 'employer'),
    ('Personal', 'Personal Projects', 'personal');
```

### 7. Project Status Lifecycle

**Q: What status values are needed?**

**Status Values:**
- **active:** Currently working on this project
- **learning:** In learning phase (may transition to active)
- **archived:** Completed and preserved, not actively developed
- **inactive:** Abandoned or paused indefinitely

**Lifecycle:**

```
[New Project]
   ↓
active ← → learning
   ↓
archived or inactive
```

**Schema:**

```sql
status TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'learning', 'archived', 'inactive'))
```

**Decision:** Use 4-status lifecycle with check constraints. `learning` status is distinct from `classification='Learning'` (a project can be Learning classification but active status).

---

## 📊 Complete Projects Table Schema

```sql
CREATE TABLE projects (
    -- Primary Key
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Core Fields
    name TEXT NOT NULL,
    path TEXT,  -- ~/Projects/work-prod, ~/Learning/python-ml
    remote_url TEXT UNIQUE,  -- https://github.com/grimm00/work-prod
    description TEXT,
    
    -- Classification
    classification TEXT NOT NULL 
        CHECK (classification IN ('Work', 'Personal', 'Learning', 'Inactive')),
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'learning', 'archived', 'inactive')),
    organization_id INTEGER,
    
    -- Learning Sub-Classification (MVP CRITICAL)
    learning_type TEXT 
        CHECK (learning_type IN ('work_related', 'personal_dev', 'hybrid') OR learning_type IS NULL),
    learning_context TEXT,  -- Free-form: "Learning Python for data analysis"
    learning_status TEXT 
        CHECK (learning_status IN ('exploring', 'active_learning', 'completed', 'paused') OR learning_status IS NULL),
    
    -- Tech Stack (Phase 1: JSON, Phase 2: projects_skills junction)
    tech_stack JSON DEFAULT '[]',  -- ["Python", "Flask", "React", "SQLite"]
    
    -- Metadata
    last_worked_on DATE,  -- Last git commit or file modification
    project_size INTEGER,  -- Lines of code (optional)
    is_favorite BOOLEAN DEFAULT 0,  -- User can star projects
    notes TEXT,  -- Free-form notes
    
    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (organization_id) REFERENCES organizations(id),
    
    -- Constraints
    CHECK (
        (classification = 'Learning' AND learning_type IS NOT NULL) OR
        (classification != 'Learning' AND learning_type IS NULL)
    ),
    CHECK (
        (learning_type IS NOT NULL AND learning_status IS NOT NULL) OR
        (learning_type IS NULL AND learning_status IS NULL)
    )
);

-- Indexes
CREATE INDEX idx_projects_classification ON projects(classification);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_organization ON projects(organization_id);
CREATE INDEX idx_projects_learning_type ON projects(learning_type) WHERE learning_type IS NOT NULL;
CREATE INDEX idx_projects_last_worked ON projects(last_worked_on DESC);
CREATE INDEX idx_projects_remote_url ON projects(remote_url) WHERE remote_url IS NOT NULL;

-- Full-Text Search (SQLite FTS5)
CREATE VIRTUAL TABLE projects_fts USING fts5(
    name,
    description,
    notes,
    tech_stack,  -- Stored as JSON string, searchable
    content=projects,
    content_rowid=id
);

-- Triggers to keep FTS in sync
CREATE TRIGGER projects_fts_insert AFTER INSERT ON projects BEGIN
    INSERT INTO projects_fts(rowid, name, description, notes, tech_stack)
    VALUES (new.id, new.name, new.description, new.notes, new.tech_stack);
END;

CREATE TRIGGER projects_fts_update AFTER UPDATE ON projects BEGIN
    UPDATE projects_fts 
    SET name = new.name,
        description = new.description,
        notes = new.notes,
        tech_stack = new.tech_stack
    WHERE rowid = new.id;
END;

CREATE TRIGGER projects_fts_delete AFTER DELETE ON projects BEGIN
    DELETE FROM projects_fts WHERE rowid = old.id;
END;
```

---

## 🔗 Projects-Skills Junction Table

```sql
CREATE TABLE projects_skills (
    -- Composite Primary Key
    project_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    
    -- Relationship Metadata
    proficiency_used TEXT 
        CHECK (proficiency_used IN ('beginner', 'intermediate', 'advanced', 'expert') OR proficiency_used IS NULL),
    is_primary_skill BOOLEAN DEFAULT 0,  -- Main technology for this project
    hours_spent INTEGER DEFAULT 0,  -- Optional time tracking
    notes TEXT,  -- How skill was used in this project
    
    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    PRIMARY KEY (project_id, skill_id),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_projects_skills_project ON projects_skills(project_id);
CREATE INDEX idx_projects_skills_skill ON projects_skills(skill_id);
CREATE INDEX idx_projects_skills_primary ON projects_skills(is_primary_skill) 
    WHERE is_primary_skill = 1;
CREATE INDEX idx_projects_skills_proficiency ON projects_skills(proficiency_used);
```

---

## 📥 Import Strategy (59 Projects)

### Data Source

**Inventory POC Files:**
- `scripts/inventory/data/github-repos.json` - Remote projects from GitHub
- `scripts/inventory/data/local-projects.json` - Local filesystem projects
- `scripts/inventory/data/classifications-merged.json` - User classifications (deduplicated)
- `scripts/inventory/data/tech-stack.json` - Discovered technologies

### Import Process

**Phase 1: Organizations (Seed Data)**
```sql
INSERT INTO organizations (name, display_name, type) VALUES
    ('DRW', 'DRW Trading', 'employer_host'),
    ('Apprenti', 'Apprenti/WTIA', 'employer'),
    ('Personal', 'Personal Projects', 'personal');
```

**Phase 2: Skills (Bootstrap from 24 Discovered Technologies)**
```python
# From discovered-skills.md
skills = [
    "Python", "JavaScript", "TypeScript", "HTML", "CSS",
    "Jupyter Notebook", "Shell", "Ruby", "Go", "Java",
    "Dockerfile", "Makefile", "C", "C++", "PHP",
    "Rust", "Swift", "Kotlin", "Dart", "YAML",
    "JSON", "Markdown", "SQL", "Vim Script"
]

for skill_name in skills:
    cursor.execute("""
        INSERT OR IGNORE INTO skills (name, category, created_at)
        VALUES (?, 'programming_language', CURRENT_TIMESTAMP)
    """, (skill_name,))
```

**Phase 3: Projects (Import from Inventory)**
```python
import json
from datetime import datetime

# Load classifications
with open('scripts/inventory/data/classifications-merged.json', 'r') as f:
    projects_data = json.load(f)

for project in projects_data:
    # Map inventory fields to schema
    name = project.get('name')
    path = project.get('path')
    remote_url = project.get('remote_url')
    classification = project.get('classification', 'Personal')
    
    # Determine organization
    if 'drw' in name.lower() or 'drw' in path.lower():
        org_name = 'DRW'
    elif 'apprenti' in name.lower():
        org_name = 'Apprenti'
    else:
        org_name = 'Personal'
    
    org_id = get_organization_id(org_name)
    
    # Extract tech stack
    tech_stack = json.dumps(project.get('languages', []))
    
    # Handle Learning projects (REQUIRES USER INPUT)
    learning_type = None
    learning_context = None
    learning_status = None
    
    if classification == 'Learning':
        # Interactive prompt for Learning classification
        learning_type = prompt_learning_type(name)
        learning_context = prompt_learning_context(name)
        learning_status = 'active_learning'  # Default
    
    # Insert project
    cursor.execute("""
        INSERT INTO projects (
            name, path, remote_url, classification, status,
            organization_id, learning_type, learning_context, learning_status,
            tech_stack, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name, path, remote_url, classification, 'active',
        org_id, learning_type, learning_context, learning_status,
        tech_stack, datetime.utcnow(), datetime.utcnow()
    ))
```

**Phase 4: Projects-Skills Relationships (Populate Junction Table)**
```python
# After Skills and Projects are imported
for project in projects_data:
    project_id = get_project_id(project['name'])
    languages = project.get('languages', [])
    
    for lang in languages:
        skill_id = get_skill_id(lang)
        
        if skill_id:
            # Default proficiency: intermediate
            # User can update later
            cursor.execute("""
                INSERT OR IGNORE INTO projects_skills (
                    project_id, skill_id, proficiency_used, is_primary_skill
                ) VALUES (?, ?, ?, ?)
            """, (project_id, skill_id, 'intermediate', 0))
```

### Import Script Structure

```
scripts/import/
├── import_projects.py          # Main import orchestration
├── seed_organizations.py       # Phase 1: Organizations
├── seed_skills.py              # Phase 2: Skills (24 technologies)
├── import_projects_data.py     # Phase 3: Projects (59 projects)
├── link_projects_skills.py     # Phase 4: Junction table
└── classify_learning.py        # Interactive Learning classification
```

### Learning Classification UI

**Interactive Prompt:**
```
Project: python-ml-tutorial
Current Classification: Learning

How is this learning project related to your work?
1. Work-related (learning for job/career)
2. Personal development (hobby/interest)
3. Hybrid (both work and personal)

Choice [1/2/3]: 1

Learning Context (optional):
> Learning Python ML libraries for data analysis at work

Learning Status:
1. Exploring (just starting)
2. Active learning (in progress)
3. Completed (finished)
4. Paused (on hold)

Choice [1/2/3/4]: 2

✅ Classified as Work-Related Learning (Active)
```

---

## 🔍 Search and Filtering Architecture

### SQLite FTS5 Full-Text Search

**Capabilities:**
- Search across name, description, notes, tech_stack
- Boolean operators (AND, OR, NOT)
- Phrase search ("machine learning")
- Prefix matching (pyth* matches Python, python-ml)

**Query Examples:**

```sql
-- Simple search
SELECT p.* FROM projects p
JOIN projects_fts fts ON p.id = fts.rowid
WHERE projects_fts MATCH 'python';

-- Multi-term search
SELECT p.* FROM projects p
JOIN projects_fts fts ON p.id = fts.rowid
WHERE projects_fts MATCH 'python AND machine learning';

-- Phrase search
SELECT p.* FROM projects p
JOIN projects_fts fts ON p.id = fts.rowid
WHERE projects_fts MATCH '"react frontend"';

-- Search with ranking
SELECT p.*, rank FROM projects p
JOIN projects_fts fts ON p.id = fts.rowid
WHERE projects_fts MATCH 'flask react'
ORDER BY rank;
```

### Multi-Faceted Filtering

**Supported Filters:**

1. **Organization** (DRW / Apprenti / Personal)
2. **Classification** (Work / Personal / Learning / Inactive)
3. **Learning Type** (work_related / personal_dev / hybrid)
4. **Status** (active / learning / archived / inactive)
5. **Tech Stack** (Python, JavaScript, etc.)
6. **Date Range** (last_worked_on)
7. **Favorites** (is_favorite = 1)

**Combined Filter Query:**

```sql
SELECT p.*, o.name as org_name
FROM projects p
LEFT JOIN organizations o ON p.organization_id = o.id
WHERE 1=1
    AND (p.organization_id = ? OR ? IS NULL)  -- Organization filter
    AND (p.classification = ? OR ? IS NULL)   -- Classification filter
    AND (p.learning_type = ? OR ? IS NULL)    -- Learning type filter
    AND (p.status = ? OR ? IS NULL)           -- Status filter
    AND (p.tech_stack LIKE ? OR ? IS NULL)    -- Tech stack contains
    AND (p.last_worked_on >= ? OR ? IS NULL)  -- Date range
    AND (p.is_favorite = ? OR ? IS NULL)      -- Favorites only
ORDER BY p.last_worked_on DESC NULLS LAST;
```

### React Search/Filter Components

**Recommended Libraries:**
- `react-select` - Multi-select dropdowns for filters
- `react-search-autocomplete` - Search bar with autocomplete
- `use-debounce` - Debounce search input (300ms)

**UI Mockup:**

```
┌────────────────────────────────────────────────────┐
│  🔍 Search projects...                         ⚙️  │
├────────────────────────────────────────────────────┤
│  Organization: [All ▼] Classification: [All ▼]    │
│  Learning Type: [All ▼]  Status: [All ▼]          │
│  Tech Stack: [Python ×] [React ×] [+ Add]         │
│  ⭐ Favorites only  📅 Last 30 days               │
└────────────────────────────────────────────────────┘

Results: 12 projects
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 work-prod (DRW • Work • Active) ⭐
   ~/Projects/work-prod
   🏷️ Python, Flask, React, SQLite
   Last worked: 2025-12-01

📚 python-ml-tutorial (Personal • Learning 🏢 Work-Related • Active Learning)
   ~/Learning/python-ml-tutorial
   🏷️ Python, Jupyter Notebook
   Last worked: 2025-11-28
   💡 Learning Python ML libraries for work

🎨 react-portfolio (Personal • Personal • Active)
   ~/Projects/react-portfolio
   🏷️ React, TypeScript, CSS
   Last worked: 2025-11-25
```

---

## 🔄 GitHub Sync Strategy

### Manual Sync (MVP)

**User-triggered refresh:**
```python
def sync_github_project(project_id):
    project = Project.query.get(project_id)
    
    if not project.remote_url:
        return None
    
    # Extract owner/repo from URL
    # https://github.com/grimm00/work-prod
    owner, repo = parse_github_url(project.remote_url)
    
    # Fetch metadata via GitHub API
    repo_data = github_api.get_repo(owner, repo)
    
    # Update project
    project.description = repo_data.get('description')
    project.last_worked_on = repo_data.get('updated_at')
    project.tech_stack = json.dumps(repo_data.get('languages', []))
    project.updated_at = datetime.utcnow()
    
    db.session.commit()
```

### Automatic Sync (Future)

**GitHub Webhooks:**
- Subscribe to push events
- Update `last_worked_on` on new commits
- Refresh tech stack on language changes

**Scheduled Sync:**
- Daily/weekly cron job
- Refresh all projects with remote_url
- Check for new repos in GitHub account

---

## 📂 Local Project Detection

### Filesystem Scanning

**Directories to scan:**
- `~/Projects/` - Work and personal projects
- `~/Learning/` - Learning projects
- `~/Developer/` - Alternative location

**Detection Logic:**

```python
import os
from pathlib import Path

def scan_local_projects(base_dirs):
    projects = []
    
    for base_dir in base_dirs:
        base_path = Path(base_dir).expanduser()
        
        if not base_path.exists():
            continue
        
        for entry in base_path.iterdir():
            if not entry.is_dir():
                continue
            
            # Check if it's a git repository
            is_git_repo = (entry / '.git').exists()
            
            # Check for project indicators
            has_package_json = (entry / 'package.json').exists()
            has_requirements = (entry / 'requirements.txt').exists()
            has_gemfile = (entry / 'Gemfile').exists()
            has_cargo = (entry / 'Cargo.toml').exists()
            
            is_project = is_git_repo or has_package_json or has_requirements or has_gemfile or has_cargo
            
            if is_project:
                # Extract remote URL if git repo
                remote_url = None
                if is_git_repo:
                    remote_url = get_git_remote_url(entry)
                
                projects.append({
                    'name': entry.name,
                    'path': str(entry),
                    'remote_url': remote_url,
                    'base_dir': str(base_path)
                })
    
    return projects
```

### Incremental Detection

**Don't re-import existing projects:**
```python
def find_new_projects(scanned_projects):
    existing_urls = {p.remote_url for p in Project.query.all() if p.remote_url}
    existing_paths = {p.path for p in Project.query.all() if p.path}
    
    new_projects = []
    for project in scanned_projects:
        # Skip if remote_url already exists
        if project['remote_url'] and project['remote_url'] in existing_urls:
            continue
        
        # Skip if path already exists
        if project['path'] in existing_paths:
            continue
        
        new_projects.append(project)
    
    return new_projects
```

---

## 📊 Data Validation Rules

### Required Field Validation

```python
class Project(db.Model):
    __tablename__ = 'projects'
    
    # ... fields ...
    
    @validates('classification')
    def validate_classification(self, key, value):
        allowed = ['Work', 'Personal', 'Learning', 'Inactive']
        if value not in allowed:
            raise ValueError(f"Classification must be one of: {allowed}")
        return value
    
    @validates('learning_type')
    def validate_learning_type(self, key, value):
        # If classification is Learning, learning_type is required
        if self.classification == 'Learning' and not value:
            raise ValueError("learning_type required for Learning projects")
        
        # If not Learning, learning_type must be NULL
        if self.classification != 'Learning' and value:
            raise ValueError("learning_type only allowed for Learning projects")
        
        if value:
            allowed = ['work_related', 'personal_dev', 'hybrid']
            if value not in allowed:
                raise ValueError(f"learning_type must be one of: {allowed}")
        
        return value
    
    @validates('remote_url')
    def validate_remote_url(self, key, value):
        if value:
            # Basic URL validation
            if not value.startswith('http'):
                raise ValueError("remote_url must be a valid URL")
        return value
```

### Business Logic Validation

```python
def can_transition_status(current_status, new_status):
    """
    Validate status transitions
    
    Allowed:
    - active → learning, archived, inactive
    - learning → active, archived, inactive
    - archived → active (reopen)
    - inactive → active (reactivate)
    
    Not allowed:
    - archived → learning
    - inactive → learning
    """
    if current_status == new_status:
        return True
    
    invalid_transitions = [
        ('archived', 'learning'),
        ('inactive', 'learning')
    ]
    
    if (current_status, new_status) in invalid_transitions:
        return False
    
    return True
```

---

## 🎨 UI/UX Considerations

### Project List View

**Display Priority:**
1. Name (bold, clickable)
2. Organization badge (DRW, Apprenti, Personal)
3. Classification badge (Work, Learning, Personal, Inactive)
4. Learning badge (if applicable): 🏢 Work / 🏠 Personal / 🔄 Hybrid
5. Tech stack tags (first 3, then +N more)
6. Last worked date (relative: "2 days ago")
7. Favorite star (if applicable)

**Sort Options:**
- Last worked (default)
- Name (A-Z)
- Classification
- Organization
- Creation date

**Bulk Actions:**
- Mark as archived
- Change organization
- Add/remove tags
- Export selection

### Project Detail View

**Sections:**
1. **Header:** Name, status, favorite toggle
2. **Meta:** Organization, classification, learning details
3. **Description:** Editable text area
4. **Tech Stack:** Tag editor (add/remove skills)
5. **Files:** Path, remote URL (with sync button)
6. **Activity:** Last worked, created date
7. **Skills:** Linked skills with proficiency
8. **Notes:** Free-form notes area
9. **Actions:** Edit, archive, delete

### Learning Project Badges

```
🏢 Work Learning - learning_type: work_related
🏠 Personal Learning - learning_type: personal_dev
🔄 Hybrid Learning - learning_type: hybrid
```

**Status Indicators:**
```
🔍 Exploring - learning_status: exploring
📚 Learning - learning_status: active_learning
✅ Completed - learning_status: completed
⏸️ Paused - learning_status: paused
```

---

## 🚀 Implementation Phases

### Phase 1: Foundation (Week 2-3)

**Database:**
- ✅ Organizations table (seed data: DRW, Apprenti, Personal)
- ✅ Projects table (complete schema with Learning fields)
- ✅ Skills table (bootstrap 24 technologies)
- ✅ projects_skills junction table
- ✅ SQLite FTS5 setup with triggers

**Backend API:**
- `GET /api/projects` - List projects (with filters)
- `GET /api/projects/:id` - Get project details
- `POST /api/projects` - Create project
- `PUT /api/projects/:id` - Update project
- `DELETE /api/projects/:id` - Delete project
- `GET /api/projects/search?q=python` - Full-text search
- `POST /api/projects/:id/sync` - Sync with GitHub

**Import Scripts:**
- Seed organizations (3 records)
- Seed skills (24 records)
- Import projects (59 records, with Learning classification)
- Link projects to skills (auto from tech_stack JSON)

### Phase 2: UI & Filtering (Week 4)

**Frontend Components:**
- ProjectList component (list view with filters)
- ProjectCard component (item display)
- ProjectFilters component (multi-faceted filtering)
- ProjectSearch component (search bar with autocomplete)
- ProjectDetail component (detail view)
- LearningBadge component (work/personal/hybrid indicator)

**Features:**
- Multi-select filters (organization, classification, learning type, status)
- Tech stack filter (tag-based)
- Search with debounce (300ms)
- Sort options
- Favorite toggle

### Phase 3: Advanced Features (Week 5-6)

**Enhancements:**
- GitHub auto-sync (webhooks or scheduled)
- Local project scanner (auto-detect new projects)
- Bulk actions (archive, tag, export)
- Project analytics (skills distribution, activity heatmap)
- Export to CSV/JSON

---

## ✅ Success Criteria

### Functional Requirements

1. ✅ **Import 59 Projects:** All inventory projects successfully imported
2. ✅ **Learning Classification:** All 17 Learning projects sub-classified (work/personal/hybrid)
3. ✅ **Skills Linked:** 24 skills associated with projects via projects_skills
4. ✅ **Search Works:** Full-text search returns relevant results
5. ✅ **Filters Work:** Can filter by organization, classification, learning type, status, tech stack
6. ✅ **CRUD Operations:** Can create, read, update, delete projects
7. ✅ **GitHub Sync:** Can manually sync project metadata from GitHub
8. ✅ **Local Detection:** Can scan filesystem for new projects

### Data Quality

1. **No Duplicates:** remote_url ensures uniqueness
2. **Learning Integrity:** All Learning projects have learning_type
3. **Organization Consistency:** All projects link to valid organization
4. **Tech Stack Accuracy:** Skills match inventory data

### Performance

1. **Search Speed:** < 200ms for full-text search on 59 projects
2. **Filter Speed:** < 100ms for multi-faceted filtering
3. **List Load:** < 500ms to load project list with 59 items

### User Experience

1. **Intuitive Filters:** Can find projects in ≤ 3 clicks
2. **Learning Clarity:** Work vs personal learning clearly indicated
3. **Tech Stack Visible:** Skills displayed prominently
4. **Quick Search:** Can search and find project in < 5 seconds

---

## 📚 References

### Internal Documentation

- [ADR-0005: Projects as Foundation Architecture](../../decisions/ADR-0005-projects-as-foundation-architecture.md) - Strategic decision
- [ADR-0003: SQLite Database Design](../../decisions/ADR-0003-sqlite-database-design.md) - Database foundation
- [Learning Project Taxonomy](learning-project-taxonomy.md) - Classification design
- [Projects-First Strategy](../../planning/notes/projects-first-strategy.md) - Strategic rationale
- [Current State Inventory](../../exploration/current-state-inventory.md) - 59 projects data
- [Discovered Skills](../../exploration/discovered-skills.md) - 24 technologies
- [Additional Libraries](../tech-stack/additional-libraries.md) - Search/filter tools

### External Resources

- [SQLite FTS5 Documentation](https://www.sqlite.org/fts5.html)
- [SQLAlchemy Relationship Patterns](https://docs.sqlalchemy.org/en/14/orm/relationship_api.html)
- [React Select Documentation](https://react-select.com/)
- [GitHub REST API](https://docs.github.com/en/rest)

---

## 🎯 Next Steps

1. **Review & Validate:** Get user feedback on schema design
2. **Create Migrations:** Write Alembic migrations for Projects and projects_skills tables
3. **Build Import Scripts:** Implement 4-phase import process
4. **API Development:** Build Flask API endpoints for Projects
5. **Frontend Components:** Create React components for project management
6. **Testing:** Import 59 real projects, verify data integrity
7. **Documentation:** Update user guides with project management features

---

**Last Updated:** 2025-12-01  
**Status:** 🟠 In Progress (Draft Complete - Awaiting Review)  
**Next:** Review with user, finalize schema, create ADR if needed






