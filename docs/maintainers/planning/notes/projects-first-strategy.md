# Projects-First MVP Strategy

**Status:** ✅ Approved  
**Date:** 2025-12-01  
**Impact:** Strategic pivot - Projects promoted to Priority #1 core feature  
**Decision Authority:** User insight + inventory data validation

---

## 📋 Executive Summary

**Strategic Pivot:** Projects feature promoted from "potential 8th feature" to **Priority #1 foundation feature** based on user insight and real data validation.

**User Insight:** _"Maybe right now, the project needs to start with organization of my projects in general?"_

**Data Validation:** 59 projects discovered across work, personal, and learning with no organization system

**Core Principle:** Organize what exists before adding planning systems on top of chaos

---

## 🎯 Strategic Rationale

### The Problem

User has 59 projects across multiple contexts without organization:

- **20 Work projects** (DRW + Apprenti) - 34%
- **16 Personal projects** - 27%
- **17 Learning projects** - 29%
- **6 Inactive/Archived** - 10%

**Pain Points:**

- Context switching between work/personal/learning
- No system to track "what am I working on?"
- Projects scattered across GitHub (25 remote) and local (46 local, 12 duplicates)
- Cannot answer "What project should I focus on today?"

### The Insight

Original plan: 7 core features with "potential" Projects feature as 8th

**User realization:** "I don't have a 'plan' to tackle the day. I'm hoping that this project helps to at least organize what I have so far, and maybe that's exactly what I need."

**Translation:** Before implementing sophisticated planning systems (Daily Focus with time tracking, priorities, goals, reflections), need to solve fundamental organization problem.

### Data Validates Need

Automated inventory POC delivered real evidence:

- ✅ 59 real projects cataloged
- ✅ 24 languages/tech stacks identified
- ✅ Clear organizational buckets (Work/Personal/Learning/Inactive)
- ✅ Project-to-skills relationships evident (Python in 18 projects, etc.)

**Conclusion:** Projects organization is not a "nice to have" - it's the foundation everything else builds on.

---

## 🏗️ Before vs. After Strategy

### Before Strategic Pivot

**Priority Order (Original Plan):**

1. Daily Focus System (HIGHEST) - Complex planning with time/priorities/goals/reflections
2. Engagement Opportunity Tracker (HIGH) - Meeting prep and relationship building
3. Project Organization (SECONDARY) - Mentioned as supporting feature
4. Skills Matrix, Learning, Goals, Feedback, Energy

**Problems with Original Plan:**

- Daily Focus assumes user has planning workflow (doesn't exist)
- No clear project context for "What am I working on today?"
- Projects buried as Priority #3 despite 59 projects needing organization
- Trying to build advanced planning before basic organization

### After Strategic Pivot

**Priority Order (New Plan - Projects-First):**

1. **Projects Feature** (HIGHEST - FOUNDATION) - Organize 59 projects
2. **Daily Focus** (HIGH - PROJECT-CENTRIC) - Simplified to "What project today?" + tasks
3. **Skills Matrix** (HIGH - CONNECTED) - Shows "used in X projects"
4. **Engagement Tracker** (HIGH) - Meeting prep unchanged
   5-8. Learning, Goals, Feedback, Energy

**Advantages of New Plan:**

- ✅ Solves actual pain point first (project organization)
- ✅ Provides foundation for other features
- ✅ Simplifies Daily Focus (project-centric vs. complex planning)
- ✅ Real data available day 1 (59 projects to import)
- ✅ Clear success criteria (all projects organized)
- ✅ Enables "What project am I working on today?" question

---

## 📊 How Inventory POC Informs This Decision

### Real Data Available

**POC Deliverables:**

- [`current-state-inventory.md`](../../exploration/current-state-inventory.md) - All 59 projects cataloged
- [`discovered-skills.md`](../../exploration/discovered-skills.md) - 24 languages with usage patterns
- `classifications.json` - User-categorized projects (Work/Personal/Learning/Inactive)
- `github-repos.json`, `local-projects.json` - Project metadata
- Deduplication logic (merged 12 GitHub+Local duplicates)

### Data Model Insights

**From POC scripts:**

- Projects need: name, path, remote_url, organization, classification, status, tech_stack
- Many-to-many: Projects ↔ Skills (Python used in 18 projects)
- GitHub integration: Can sync repo metadata automatically
- Local detection: Can discover projects in ~/Projects and ~/Learning

**Schema Needs** (See [SQLite Schema Gaps](../../research/tech-stack/sqlite-database-design.md)):

- Projects table (currently missing)
- projects_skills junction table
- Classification field pattern
- Organization context (optional org_id on tables)

### Implementation Insights from POC

**What worked:**

- GitHub API (`gh repo list`) - Fast, reliable
- Local scanning - File extension analysis effective
- Classification - User provided clear Work/Personal/Learning/Inactive
- Deduplication - Remote URL matching identified duplicates

**What needs improvement (Week 4 research):**

- Configuration management (hardcoded paths)
- Pipeline orchestration (5 separate scripts)
- Data model (classification separate from project data)
- See: [POC Analysis](../../research/automation/inventory-system-poc-analysis.md)

---

## 🔗 Connection Points: Projects → Other Features

### Projects → Skills Matrix

**Connection:** Many-to-many relationship

**Value:**

- Skills show "used in X projects"
- Real usage patterns visible (Python: 18 projects, JavaScript: 13, etc.)
- Confidence levels informed by project count
- Skill gaps identified (technologies not yet used)

**Implementation:**

- `projects_skills` junction table
- Import discovered-skills.md data
- UI: Click skill → see projects using it

### Projects → Daily Focus

**Connection:** Project context for tasks

**Value:**

- Answer "What project am I working on today?"
- Tasks belong to project context
- Simpler than original complex Daily Focus plan
- Reduces "what should I work on?" decision fatigue

**Implementation (Phased):**

- Phase 2: Project selector + simple task list per project
- Phase 4: Add time tracking, priorities, goals per project

### Projects → Goals

**Connection:** Goals linked to projects

**Value:**

- "Complete project X" as goal
- "Learn skill Y via project Z"
- Track goal progress via project milestones

**Implementation:**

- `project_id` FK on goals table (optional)
- Goal progress = project progress

### Projects → Learning Journal

**Connection:** Learnings associated with project work

**Value:**

- "Learned X while working on project Y"
- Context for aha moments
- Track learning per project

**Implementation:**

- `project_id` FK on learnings table (optional)
- Filter learnings by project

---

## 📈 Implementation Phases (Hybrid Complexity Model)

### Phase 1: MVP Foundation - Projects Organization

**Goal:** Organize all 59 projects in system

**Capabilities:**

- ✅ Project CRUD (create, read, update, delete)
- ✅ Classification (Work / Personal / Learning / Inactive)
- ✅ Basic metadata (name, description, tech stack, status, path, remote URL)
- ✅ Simple filtering and search
- ✅ Organization tagging (DRW, Apprenti, Personal)

**Data Import:**

- Import 59 projects from inventory POC
- Import 24 skills from discovered-skills.md
- Pre-populate project-to-skill relationships

**Success Criteria:**

- All 59 projects visible in UI
- Filterable by organization, classification, tech stack
- Searchable by name
- Clear separation (Work vs Personal vs Learning)

**Timeline:** MVP Priority (implement first)

---

### Phase 2: Simple Planning - Project-Centric Daily Focus

**Goal:** Answer "What project am I working on today?"

**Capabilities:**

- ✅ Project selection for the day
- ✅ Simple task list per project
- ✅ Basic status tracking (Todo / In Progress / Done)
- ✅ Quick task capture

**Simplified from Original Plan:**

- ❌ No time tracking (Phase 4)
- ❌ No priority levels (Phase 4)
- ❌ No goal connections (Phase 4)
- ❌ No daily/weekly reflections (Phase 4)

**Advantages:**

- Faster to implement
- Easier to use (no overwhelming features)
- Validates project-centric approach
- Can add advanced features later

**Success Criteria:**

- Can select "today's project"
- Can add/complete tasks for that project
- Reduces "what to work on?" decision fatigue

**Timeline:** MVP Priority (implement after Phase 1)

---

### Phase 3: Connections - Skills Integration

**Goal:** Link skills to projects with usage patterns

**Capabilities:**

- ✅ Skills table populated from discovered-skills.md
- ✅ Skills-to-Projects many-to-many relationship
- ✅ "Used in X projects" display
- ✅ Skill usage patterns visible
- ✅ Confidence levels (derived from project count)

**Data Available:**

- 24 languages ready to import
- Project counts per skill already calculated
- Suggested confidence levels based on usage

**Success Criteria:**

- All 24 skills visible
- Each skill shows project count
- Click skill → see projects using it
- Click project → see skills used

**Timeline:** MVP or early post-MVP

---

### Phase 4: Advanced Planning - Full Planning Features

**Goal:** Add sophisticated planning capabilities

**Capabilities:**

- Time tracking per task/project
- Priority levels (high/medium/low)
- Goals linked to projects
- Daily/weekly reflections
- Advanced reporting

**When to Implement:**

- After Phases 1-3 validated
- After user establishes planning habits
- When simple project-centric approach needs enhancement

**Success Criteria:**

- Advanced users have power features
- Simple users not overwhelmed
- Planning habits established

**Timeline:** Post-MVP (Week 4+ or later)

---

## ✅ Success Criteria

### Organizational Success

- ✅ All 59 projects organized and tracked in system
- ✅ Clear Work / Personal / Learning / Inactive separation
- ✅ Easy project lookup and filtering
- ✅ Tech stack visible for each project
- ✅ GitHub integration working for remote projects
- ✅ Local projects detected and linked

### User Experience Success

- ✅ Can answer "What project am I working on today?"
- ✅ Reduced context-switching chaos
- ✅ Reduced "what should I work on?" decision fatigue
- ✅ Simple enough to actually use daily
- ✅ Foundation for future planning features

### Technical Success

- ✅ Projects table designed and implemented
- ✅ Projects-to-Skills many-to-many relationship working
- ✅ Data import from POC successful
- ✅ Schema supports future enhancements
- ✅ Organization context available (multi-org ready)

### Strategic Success

- ✅ Foundation feature implemented first
- ✅ Other features can build on Projects base
- ✅ MVP scope simplified (easier to deliver by January)
- ✅ Real data validates approach
- ✅ User pain point addressed

---

## 🚀 Next Steps

### Immediate (Week 2)

1. **Data Model Research:**

   - Create Projects Data Model research document
   - Design Projects table schema
   - Design projects_skills junction table
   - Update Week 1 SQLite schema if needed

2. **Update Research Register:**

   - Add "Projects Data Model" as HIGH priority (Week 2)
   - Reframe Skills Matrix research to emphasize project connection
   - Note Daily Focus will be simplified (project-centric)

3. **Create ADR-0005:**
   - Document "Projects as Foundation Architecture" decision
   - Context: 59 projects, user insight, organization need
   - Decision: Projects promoted to core feature #1
   - Consequences: Simpler MVP, clear starting point

### Planning (Week 2-3)

4. **Create Projects Feature Plan:**

   - In `docs/maintainers/planning/features/projects/`
   - Follow hub-and-spoke pattern
   - Document 4 implementation phases
   - Link to inventory POC data

5. **Update Cursor Rules:**
   - Add projects-first strategy to rules
   - Document new priority order
   - Note simplified Daily Focus approach

### Implementation (Post Week 3 Research)

6. **Phase 1 Implementation:**
   - Backend: Projects table, CRUD API
   - Frontend: Projects dashboard, CRUD UI
   - Data import: 59 projects from POC
   - Skills import: 24 languages from discovered-skills.md

---

## 📚 Related Documentation

### Exploration & Requirements

- [Requirements - Updated Feature Priorities](../../exploration/requirements.md#feature-priorities)
- [Current State Inventory](../../exploration/current-state-inventory.md) - 59 projects catalog
- [Discovered Skills](../../exploration/discovered-skills.md) - 24 languages for Skills Matrix

### Research & Decisions

- [SQLite Schema Gaps](../../research/tech-stack/sqlite-database-design.md#update-2025-12-01-inventory-data-reveals-schema-gaps)
- [Skills Matrix Research Prep](../../research/data-models/README.md) - Week 2 inputs
- [Research Register - Projects Data Model](../../research/research-register.md) - Week 2 HIGH priority
- **Future:** ADR-0005 will document this strategic decision

### Inventory POC

- [POC Analysis](../../research/automation/inventory-system-poc-analysis.md) - What worked, technical debt
- [Research Register - Inventory System](../../research/research-register.md) - Week 4 refactoring

---

## 💡 Key Takeaways

1. **Organization Before Planning:** Can't plan effectively without organized foundation
2. **Data-Driven Decisions:** 59 real projects validates need better than hypotheticals
3. **User Insight Valuable:** "Organize first" aligns with actual need
4. **Simplicity Wins:** Project-centric Daily Focus simpler than complex planning system
5. **Foundation Enables Growth:** Projects feature supports Skills, Goals, Learning, Daily Focus
6. **Real Data Day 1:** POC means 59 projects + 24 skills ready to import
7. **Phased Approach:** MVP organization → Simple planning → Connections → Advanced features

---

**Last Updated:** 2025-12-01  
**Status:** ✅ Approved - Ready for Week 2 research  
**Next:** Create Projects Data Model research document (Week 2 HIGH priority)




