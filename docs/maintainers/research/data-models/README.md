# Data Models Research (Week 2)

**Status:** 🟡 Planned  
**Timeline:** Week 2  
**Last Updated:** 2025-12-01

---

## 📋 Overview

This folder contains Week 2 research on data models for core features, specifically:
- Skills Matrix data model
- Daily Focus data model  
- Learning Journal data model

---

## 🎯 Critical Inputs for Week 2 Research

### ✅ Skills Matrix Has Real Seed Data

**Data Available:** [`/docs/maintainers/exploration/discovered-skills.md`](../../exploration/discovered-skills.md)

**What It Provides:**
- 24 real languages/technologies discovered from user's 59 projects
- Usage patterns (Python in 18 projects, JavaScript in 13, etc.)
- Project-to-skill relationships
- Suggested confidence levels based on project count

**MUST Use For:**
- Schema design: `skills` table and `skills_to_projects` relationship (many-to-many)
- Seed data strategy: How to import discovered skills into database
- Confidence calculation: Formula for project count → suggested confidence level
- UI mockups: Use real 24 languages instead of hypothetical data
- Query design: "Show skills used in X+ projects", "Which projects use skill Y?"

**Schema Implications:**
- Need `projects` table (see: [SQLite Schema Gaps](../tech-stack/sqlite-database-design.md#️-update-2025-12-01-inventory-data-reveals-schema-gaps))
- Need `projects_skills` junction table for many-to-many relationship
- Consider: Should `projects` be a core entity or supporting entity?
- See: [Requirements - Projects Feature Analysis](../../exploration/requirements.md#projects-feature-potential-8th-core-feature)

---

## 🔍 Schema Gap Analysis (From Week 1 Review)

**4 Gaps Identified in SQLite Schema:**

1. **No Projects Table** - 59 projects need tracking
2. **No Skills-to-Projects Relationship** - Can't track "used in X projects"
3. **No Classification Pattern** - Need Work/Personal/Learning/Inactive categorization
4. **Organization Field Not Ubiquitous** - Multi-context support needs expansion

**Action Items for Week 2:**
- Design Skills-to-Projects many-to-many relationship
- Decide: Projects table as core feature or supporting entity?
- Add optional `organization_id` to Skills table for multi-context support
- Design classification/categorization pattern

---

## 📊 Week 2 Research Topics

### 1. Skills Matrix Data Model

**Status:** 🔴 Not Started  
**File:** `skills-matrix-data-model.md` (create during Week 2)

**Research Questions:**
- How to model skills with project relationships?
- How to track "used in X projects"?
- How to calculate confidence levels from usage patterns?
- How to import discovered skills as seed data?
- How to handle skill progression over time?

**Inputs:**
- ✅ [Discovered Skills](../../exploration/discovered-skills.md) - 24 real languages
- ✅ [Current State Inventory](../../exploration/current-state-inventory.md) - 59 projects
- ⚠️ [SQLite Schema Gaps](../tech-stack/sqlite-database-design.md#️-update-2025-12-01-inventory-data-reveals-schema-gaps)

### 2. Daily Focus Data Model

**Status:** 🔴 Not Started  
**File:** `daily-focus-data-model.md` (create during Week 2)

**Research Questions:**
- How to model tasks with priorities and time tracking?
- Should tasks link to projects? (if Projects is core feature)
- How to handle recurring tasks?
- How to model daily/weekly review workflows?

**Considerations:**
- If Projects promoted to core: tasks may need `project_id` FK
- May need task-to-goal relationships (already in Week 1 schema)

### 3. Learning Journal Data Model

**Status:** 🔴 Not Started  
**File:** `learning-journal-data-model.md` (create during Week 2)

**Research Questions:**
- How to capture learnings with rich metadata?
- How to link learnings to projects, skills, meetings?
- How to categorize learning types?

---

## 🚀 Next Steps

**Before Starting Week 2 Research:**
1. Read [Requirements](../../exploration/requirements.md) - Updated with inventory insights
2. Review [SQLite Schema Gaps](../tech-stack/sqlite-database-design.md#️-update-2025-12-01-inventory-data-reveals-schema-gaps)
3. Examine [Discovered Skills](../../exploration/discovered-skills.md) - Real seed data
4. Consider [Projects Feature Analysis](../../exploration/requirements.md#projects-feature-potential-8th-core-feature)

**During Week 2:**
1. Create `skills-matrix-data-model.md` - Use discovered-skills.md as input
2. Design Projects table (if promoted to core) or as supporting entity
3. Design Skills-to-Projects many-to-many relationship
4. Create `daily-focus-data-model.md` - Consider project context
5. Create `learning-journal-data-model.md`
6. Update Week 1 SQLite schema if significant gaps found

**After Week 2:**
- If schema changed significantly: Create amendment to ADR-0003 or new ADR
- Update research register with completion status
- Begin Week 3 research (Microsoft integrations, Miro)

---

**Last Updated:** 2025-12-01  
**Next:** Begin Week 2 research with Skills Matrix data model






