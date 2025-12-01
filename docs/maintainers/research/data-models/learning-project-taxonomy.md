# Learning Project Sub-Classification Taxonomy

**Status:** 🟠 In Progress  
**Priority:** 🔴 CRITICAL (MVP Blocker)  
**Category:** Data Model Design  
**Created:** 2025-12-01  
**Last Updated:** 2025-12-01

---

## 📋 Problem Statement

**Context:** Automated project inventory discovered 17 Learning projects (29% of total 59 projects), but the current classification system treats all Learning projects as a single category.

**User Insight:** *"While there are organizational buckets, some 'Learning' projects are work-related while others are personal development. I request ideas about how this can also be separated."*

**Challenge:** Without sub-classification, the system cannot:
- Distinguish work-required learning (Python for job) from personal hobbies (game development)
- Accurately track work vs personal time allocation
- Provide meaningful metrics (e.g., "work-related learning hours" vs "personal development hours")
- Filter effectively (e.g., show only "learning projects related to my job")

**Impact:** This is **MVP CRITICAL** because the Projects feature is Priority #1, and accurate organization requires proper Learning classification.

---

## 🎯 Proposed Taxonomy

### Three-Tier Classification System

```
Learning Projects (17 total)
│
├── Work-Related Learning (estimated 8-10 projects)
│   ├── Job-Required Skills
│   │   └── Skills directly needed for current apprenticeship role
│   │   └── Examples: Python, SQL, JavaScript (for work tasks)
│   │
│   ├── Career Development
│   │   └── Skills for promotion or next role
│   │   └── Examples: System design, leadership, advanced tech stacks
│   │
│   └── Company Technologies
│       └── DRW-specific or Apprenti-specific tools/systems
│       └── Examples: Internal frameworks, trading systems, company workflows
│
├── Personal Development (estimated 5-7 projects)
│   ├── Hobby Projects
│   │   └── Side projects for fun or exploration
│   │   └── Examples: Game development, creative coding, art projects
│   │
│   ├── Non-Work Skills
│   │   └── Skills unrelated to current career path
│   │   └── Examples: Web design (if not job-related), mobile apps for fun
│   │
│   └── Academic Learning
│       └── Courses, tutorials, certifications (not required by work)
│       └── Examples: Online courses, personal research, learning new languages
│
└── Hybrid (estimated 2-3 projects)
    └── Projects that serve both work and personal goals
    └── Examples: Portfolio projects, open-source contributions beneficial to career
```

---

## 🗄️ Schema Design

### Database Fields

**Projects Table - New Fields:**

```sql
-- Learning sub-classification (NULL for non-Learning projects)
learning_type VARCHAR(20) NULL,
  -- Values: 'work_related' | 'personal_dev' | 'hybrid' | NULL
  -- NULL when classification != 'Learning'

-- Free-form learning goals/context
learning_context TEXT NULL,
  -- Examples: "Learning Python for data analysis at work"
  --            "Personal project to learn game development"
  --            "Required for Q2 apprenticeship goals"

-- Learning status (optional, for Phase 4)
learning_status VARCHAR(20) NULL,
  -- Values: 'exploring' | 'active_learning' | 'completed' | 'paused' | NULL
  -- Tracks learning progress separate from project status
```

### Enum Values Detail

**`learning_type` Options:**

1. **`work_related`** - Any learning that directly benefits work performance
   - Job-required skills (must-learn for current role)
   - Career development (preparing for next role)
   - Company technologies (DRW/Apprenti-specific)

2. **`personal_dev`** - Learning for personal growth unrelated to work
   - Hobbies and exploration
   - Non-work skills
   - Academic learning for personal interest

3. **`hybrid`** - Projects serving both purposes
   - Portfolio projects showcasing work skills
   - Open-source contributions beneficial to career
   - Learning projects that started personal but became work-relevant

4. **`NULL`** - Not a Learning project
   - Only used when `classification` is NOT 'Learning'

**`learning_status` Options (Future - Phase 4):**

1. **`exploring`** - Just discovered, preliminary investigation
2. **`active_learning`** - Currently actively learning/practicing
3. **`completed`** - Learning objectives achieved
4. **`paused`** - Temporarily on hold
5. **`NULL`** - Not applicable or not tracked yet

---

## 🤔 Design Decision Points

### 1. Should Work-Related Learning Count Toward Work Metrics?

**Options:**

**A. Yes - Work-Related Learning = Work Time** (RECOMMENDED)
- **Pros:** 
  - Accurate representation of work commitment
  - Apprenticeship includes learning as part of job
  - Aligns with reality: learning Python for work IS work
- **Cons:**
  - Might inflate "work project count" if counted as separate projects
- **Implementation:** Filter `(classification = 'Work') OR (classification = 'Learning' AND learning_type = 'work_related')`

**B. No - All Learning Separate from Work**
- **Pros:**
  - Clear separation between production work and learning
  - Easier to track "actual work" vs "learning work"
- **Cons:**
  - Misrepresents actual work time commitment
  - Doesn't reflect apprenticeship reality
- **Implementation:** Keep strict `classification = 'Work'` filters

**C. Configurable Per-Project**
- **Pros:**
  - Maximum flexibility
  - User decides per learning project
- **Cons:**
  - Adds complexity to UI
  - Inconsistent metrics
- **Implementation:** Add `count_as_work BOOLEAN` field

**RECOMMENDATION:** **Option A** - Work-Related Learning counts toward work metrics. This accurately represents the apprenticeship reality where learning IS part of the job.

### 2. Should Hybrid Projects Appear in Both Work AND Personal Views?

**Options:**

**A. Yes - Show in Both, Marked as Hybrid** (RECOMMENDED)
- **Pros:**
  - Maximum visibility
  - User doesn't miss hybrid projects when filtering
  - Clear "hybrid" badge shows dual nature
- **Cons:**
  - Could inflate counts if not careful
- **Implementation:** 
  - Filter: `learning_type IN ('work_related', 'hybrid')` for work view
  - Filter: `learning_type IN ('personal_dev', 'hybrid')` for personal view
  - Badge: "🔀 Hybrid" indicator in UI

**B. No - User Chooses Primary Category**
- **Pros:**
  - Simpler counting
  - No duplication in views
- **Cons:**
  - Reduces visibility
  - Doesn't reflect reality of dual-purpose projects
- **Implementation:** Force single `learning_type` value, no hybrid option

**RECOMMENDATION:** **Option A** - Show in both views with clear hybrid indicator. Most accurate to project reality.

### 3. How to Handle Projects That Transition?

**Scenario:** Personal learning project (e.g., learning React for fun) becomes work-relevant (e.g., assigned React task at work).

**Options:**

**A. Manual Re-classification** (RECOMMENDED for MVP)
- **Pros:**
  - Simple to implement
  - User maintains control
  - Clear audit trail if needed
- **Cons:**
  - Requires user action
  - Might forget to update
- **Implementation:** 
  - Update `learning_type` field
  - Update `learning_context` to reflect change
  - (Optional Phase 4) Track classification history

**B. Auto-suggest Re-classification**
- **Pros:**
  - Proactive assistance
  - Catches transitions automatically
- **Cons:**
  - Complex logic needed
  - Might suggest incorrectly
- **Implementation:** 
  - AI/heuristics detect potential transitions
  - Show notification: "Is this project now work-related?"

**C. Allow Multiple Simultaneous Classifications**
- **Pros:**
  - No need to choose
  - Captures full context
- **Cons:**
  - Database complexity (many-to-many relationship)
  - UI complexity
- **Implementation:** `project_learning_types` junction table

**RECOMMENDATION:** **Option A** for MVP. Manual re-classification is simple, transparent, and sufficient. Phase 4 can add auto-suggestions.

---

## 📊 Data Migration Strategy

### Importing Existing 17 Learning Projects

**Step 1: Initial Import**
- Import all 17 Learning projects with `learning_type = NULL`
- Keep `classification = 'Learning'`
- This maintains existing data structure

**Step 2: Interactive Classification**
- Extend `classify-projects.py` script with sub-classification prompt
- For each Learning project, ask:
  ```
  Project: [project_name]
  Current Classification: Learning
  
  Is this learning project:
  1) Work-Related (job skills, career development, company tech)
  2) Personal Development (hobbies, personal interests)
  3) Hybrid (serves both purposes)
  
  Choice (1/2/3): _
  
  (Optional) Learning context: _
  ```

**Step 3: Seed Common Patterns**
- Pre-populate likely classifications based on project names/paths
- User confirms or corrects
- Examples:
  - Project in `~/Learning/python-for-work` → Suggest `work_related`
  - Project in `~/Learning/game-dev-tutorial` → Suggest `personal_dev`
  - Project with "portfolio" in name → Suggest `hybrid`

**Step 4: Bulk Update**
- Apply user classifications to database
- Validate: all Learning projects should have `learning_type != NULL`

---

## 🎨 UI/UX Implications

### Filtering Interface

**Basic Filters:**
```
[All Projects ▼]
  ├── All Projects (59)
  ├── Work (20)
  ├── Personal (16)
  ├── Learning (17)
  │   ├── Work-Related Learning (10)
  │   ├── Personal Development (5)
  │   └── Hybrid (2)
  └── Inactive (6)
```

**Advanced Filters:**
```
Organization: [All ▼]
Classification: [All ▼]
Learning Type: [All ▼] (only shown if classification = Learning)
Tech Stack: [All ▼]
Status: [All ▼]
```

### Project Card Display

**Learning Project Card:**
```
┌─────────────────────────────────────┐
│ 🎓 Python Data Analysis            │
│ Learning • Work-Related             │
│                                     │
│ Learning Python for data analysis   │
│ tasks at DRW                        │
│                                     │
│ 🏷️ Python, Pandas, SQL             │
│ 📊 Status: Active Learning          │
└─────────────────────────────────────┘
```

**Hybrid Project Card:**
```
┌─────────────────────────────────────┐
│ 🔀 Portfolio Website                │
│ Learning • Hybrid                   │
│                                     │
│ Building portfolio to showcase work │
│ and learn modern web tech           │
│                                     │
│ 🏷️ React, TypeScript, Tailwind     │
│ 📊 Status: Active Learning          │
└─────────────────────────────────────┘
```

### Work View Behavior

**When "Work" filter selected:**
- Show: `classification = 'Work'`
- Show: `classification = 'Learning' AND learning_type = 'work_related'`
- Show: `classification = 'Learning' AND learning_type = 'hybrid'`
- Total: 20 Work + ~10 Work-Related Learning + ~2 Hybrid = ~32 projects

**Label:** "Work & Work-Related Learning (32)"

### Personal View Behavior

**When "Personal" filter selected:**
- Show: `classification = 'Personal'`
- Show: `classification = 'Learning' AND learning_type = 'personal_dev'`
- Show: `classification = 'Learning' AND learning_type = 'hybrid'`
- Total: 16 Personal + ~5 Personal Dev + ~2 Hybrid = ~23 projects

**Label:** "Personal & Personal Learning (23)"

---

## 📈 Metrics & Reporting Impact

### Time Tracking (Phase 4)

**Work Hours Calculation:**
```sql
SELECT SUM(time_spent) 
FROM time_entries te
JOIN projects p ON te.project_id = p.id
WHERE p.classification = 'Work'
   OR (p.classification = 'Learning' AND p.learning_type IN ('work_related', 'hybrid'))
```

### Project Count Metrics

**Dashboard Display:**
```
Total Projects: 59

Work Projects: 20
└─ Work-Related Learning: 10
└─ Total Work Context: 30

Personal Projects: 16
└─ Personal Development: 5
└─ Total Personal Context: 21

Hybrid Learning: 2 (counted in both above)

Pure Learning (Unclassified): 0
Inactive: 6
```

### Skills Matrix Integration

**Skill Usage Display:**
```
Python
├─ Used in 18 projects
├─ Work projects: 8
├─ Learning projects: 7 (5 work-related, 2 personal)
└─ Personal projects: 3
```

---

## ✅ Implementation Checklist

### Week 2 Research Deliverables

- [ ] **Schema Design Complete**
  - [ ] Add `learning_type` field to Projects table
  - [ ] Add `learning_context` field to Projects table
  - [ ] Add `learning_status` field (optional, Phase 4)
  - [ ] Update database migration scripts

- [ ] **Classification Logic**
  - [ ] Extend `classify-projects.py` with Learning sub-classification
  - [ ] Add validation: Learning projects MUST have `learning_type`
  - [ ] Add data consistency checks

- [ ] **UI Mockups**
  - [ ] Filtering interface design
  - [ ] Project card display (with learning badges)
  - [ ] Work/Personal view behavior specification

- [ ] **Metrics Design**
  - [ ] Work hours calculation (including work-related learning)
  - [ ] Project count logic (handling hybrid projects)
  - [ ] Skills matrix integration

- [ ] **Decision Documentation**
  - [ ] Document chosen options for 3 decision points
  - [ ] Rationale for recommendations
  - [ ] Future enhancement notes

---

## 🔮 Future Enhancements (Post-MVP)

### Phase 4 Additions

1. **Learning Progress Tracking**
   - Track `learning_status` transitions
   - Learning milestones and goals per project
   - Completion percentage

2. **Auto-suggest Re-classification**
   - Detect when personal learning becomes work-relevant
   - Suggest hybrid status when project used in both contexts
   - Classification history/audit trail

3. **Learning Path Visualization**
   - Show learning journey across projects
   - Prerequisite relationships (learned X to enable Y)
   - Skill progression timeline

4. **Learning Analytics**
   - Time spent on work vs personal learning
   - Most active learning areas
   - Learning velocity metrics

---

## 📚 Related Documentation

- **[Projects-First Strategy](../../planning/notes/projects-first-strategy.md)** - Strategic rationale for Projects as Priority #1
- **[Current State Inventory](../../exploration/current-state-inventory.md)** - 17 Learning projects identified
- **[SQLite Database Design](../tech-stack/sqlite-database-design.md)** - Schema gaps identified
- **[Projects Data Model Research](../../research/research-register.md#20-projects-data-model)** - Parent research topic

---

## 🎯 Success Criteria

- [ ] All 17 Learning projects can be sub-classified as work_related, personal_dev, or hybrid
- [ ] Work view correctly includes work-related learning projects
- [ ] Personal view correctly includes personal development learning projects
- [ ] Hybrid projects visible in both work and personal views with clear indicators
- [ ] Metrics accurately represent work vs personal time (including learning)
- [ ] UI clearly communicates learning project type to user
- [ ] Data migration completed for all existing Learning projects

---

**Next Steps:**
1. Review this taxonomy with user for approval
2. Incorporate into Projects Data Model research (section 2.0)
3. Design database schema with new fields
4. Update inventory scripts to handle sub-classification
5. Create UI mockups showing Learning filters and badges

**Status:** 🟠 In Progress - Awaiting user approval and Week 2 research integration

