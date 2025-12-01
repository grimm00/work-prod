# Requirements Gathering

**Status:** 🟠 In Progress  
**Created:** 2025-11-26  
**Last Updated:** 2025-12-01  
**Inventory Data:** ✅ Added 2025-12-01

---

## 📋 Overview

This document captures comprehensive requirements for the work productivity and engagement management system. It documents user context, current state analysis, feature priorities, and technical specifications to guide feature planning and implementation.

---

## 👤 User Context

### Role and Environment

- **Role:** DevOps Specialist Apprentice
- **Organization Structure:**
  - Employed by: Apprenti (WTIA) as contractor
  - Host Organization: Trading firm (primary management)
  - Access: macOS device (24/7 availability)

### Current Phase: "Developing Egg"

- **Learning Stage:** Exploratory phase with exposure to various technologies and workflows
- **Purpose:** Finding focus area and identifying best team fit for next rotation
- **Characteristics:**
  - General instruction without specific direction
  - Exposure to many different technologies and tools
  - Freedom to explore areas of interest

### Timeline and Critical Milestones

- **Current:** Exploratory learning phase
- **Next Rotation:** Placement on dedicated team (timing TBD)
- **Critical:** Next rotation is high-probability hiring decision point
- **Goal:** Build strong habits and workflows NOW to be excellent candidate

### Support Structure

1. **Manager**
   - Role: Main instructor
   - Focus: Teaching tech stack and job workflows
   - Interaction: Regular instruction and guidance

2. **Coaches**
   - Role: Personalized exploration support
   - Focus: Deep dives into learning topics
   - Interaction: Observational feedback and guidance
   - Goal: Maximize value from coaching time

3. **Cohort**
   - Size: 6 other apprentices
   - Relationship: Good relationships established
   - Opportunity: Could improve engagement with fellow apprentices

4. **Communities**
   - Slack channels: Multiple optional communities
   - Interest areas: Various technical and professional topics
   - Opportunity: Better engagement and participation

---

## 🔍 Current State Analysis

### Existing Tools

- **Microsoft Outlook** - Calendar and email management
- **Slack** - Team communication and community channels
- **GitHub** - Version control and code collaboration
- **Cursor IDE** - Development environment with AI assistance
- **Note:** Open to additional tool suggestions

### Current Workflows

**Planning:**
- ❌ No established daily planning workflow
- ❌ Unclear when to plan (morning, night before, etc.)
- ⚠️ Need: Structure and best practices for effective planning

**Project Management:**
- ⚠️ Managing multiple concurrent projects
- ⚠️ Mix of work and personal projects without clear separation
- ⚠️ Context switching difficulties

**Engagement:**
- ⚠️ Opportunities exist but not systematically maximized
- ⚠️ Ad-hoc meeting preparation
- ⚠️ No system for tracking interactions or relationship building

**Organization:**
- ⚠️ Calendar management needs improvement
- ⚠️ Priority identification challenges
- ⚠️ No systematic approach to organizing work

### Pain Points Identified

1. **Communication and Action**
   - Challenge: Speaking intelligently about work
   - Challenge: Acting swiftly on priorities
   - Impact: Reduced effectiveness in interactions

2. **Relationship Management**
   - Challenge: Not maximizing time with managers, coaches, teams
   - Challenge: Underutilizing Slack communities
   - Challenge: Could improve cohort engagement
   - Impact: Missing opportunities for growth and connection

3. **Focus and Prioritization**
   - Challenge: Daily focus unclear - "what should I work on today?"
   - Challenge: Multiple concurrent projects without organization
   - Challenge: Calendar and engagement management
   - Impact: Inefficient use of time and opportunities

4. **Knowledge Gaps**
   - Challenge: Large gaps in knowledge exist
   - Challenge: Don't know what questions to ask
   - Challenge: Uncertain about growth areas
   - Impact: Potential missed learning opportunities

### Project Inventory (Discovered Data)

**Status:** ✅ Completed 2025-12-01 via automated inventory system

**Findings:**
- **59 unique projects** identified across GitHub and local directories
- **Distribution:**
  - Work (DRW + Apprenti): 20 projects (34%)
  - Personal: 16 projects (27%)
  - Learning: 17 projects (29%)
  - Inactive/Archived: 6 projects (10%)
- **24 languages/technologies** discovered across all projects
- **Project patterns:**
  - Clear organizational separation needed (Work vs Personal vs Learning)
  - Mix of active development and archived projects
  - Strong GitHub integration (25 remote repos, 12 have local clones)
  - Project lifecycle stages visible (active, learning, inactive)

**Top Technologies by Usage:**
- Python: 18 projects (31%)
- Markdown: 17 projects (29%)
- JavaScript: 13 projects (22%)
- Shell: 12 projects (20%)
- HTML, CSS, YAML, JSON: 8-10 projects each
- 16 additional languages: 1-5 projects each

**Impact on Requirements:**
- **Skills Matrix:** Has real seed data (24 languages with usage patterns)
- **Projects Feature:** 59 projects validates need for project organization feature
- **Multi-Org Support:** Clear split (20 Work vs 16 Personal) shows context-switching need
- **Daily Focus:** Could benefit from project context (which project am I working on today?)

**See Also:**
- [Current State Inventory](current-state-inventory.md) - Full project catalog
- [Discovered Skills](discovered-skills.md) - Languages identified for Skills Matrix
- [POC Analysis](../research/automation/inventory-system-poc-analysis.md) - How data was gathered

---

## 🎯 Feature Priorities

### Priority 1: Daily Focus System (HIGHEST)

**Goal:** Answer "What should I focus on today?" effectively

**Key Capabilities:**
- Daily priority identification and tracking
- Quick-capture for tasks and opportunities
- Review system (daily and weekly reflections)
- Connect tasks to larger goals (hiring readiness, skill development, relationships)
- Planning workflow guidance (when and how to plan)

**Success Criteria:**
- Clear daily priorities established each day
- Improved task completion rates
- Better time allocation awareness
- Regular reflection habit established

### Priority 2: Engagement Opportunity Tracker (HIGH)

**Goal:** Maximize interactions with managers, coaches, teams, and communities

**Key Capabilities:**
- Track interactions and meetings with key people
- **Prepare questions and topics BEFORE meetings** (highest sub-priority)
- Define desired outcomes for interactions
- Log insights and feedback received
- Identify engagement gaps (who haven't connected with lately?)
- Slack channel and community tracking
- Relationship building support

**Success Criteria:**
- Prepared for every important meeting
- Increased meaningful interactions
- Better utilization of manager and coach time
- Improved cohort relationships
- Active in relevant Slack communities

### Priority 3: Project Organization System (SECONDARY)

**Goal:** Separate and manage multiple concurrent projects effectively

**Key Capabilities:**
- Work vs. personal project separation
- Project status tracking
- Context switching support (what was I working on?)
- Project documentation and notes
- Connection to daily focus system

**Success Criteria:**
- Clear project boundaries
- Easier context switching
- Better project tracking
- Reduced mental overhead

---

## 📝 Specific Requirements

### Daily Planning Workflow

**Current State:** No established planning workflow

**Requirements:**
- System should guide when to plan (suggest best timing)
- Support both morning and evening planning options
- Quick daily review process
- Weekly reflection capability
- Connect daily tasks to weekly and rotation goals

**Open Questions:**
- What time of day is most effective for planning?
- Morning (start of day) vs. Evening (prepare for next day)?
- How long should daily planning take?
- What triggers should prompt re-planning during the day?

### Engagement Tracking Details

**Meeting Preparation:**
- Pre-meeting question/topic preparation
- Desired outcome definition
- Context from previous interactions
- Post-meeting notes and follow-ups

**Relationship Management:**
- Track frequency of interactions with key people
- Identify gaps (people not connected with recently)
- Community participation tracking
- Relationship building reminders

**Learning and Feedback:**
- Log insights gained from interactions
- Track feedback received
- Identify patterns and themes
- Connect learnings to skill development

### Privacy and Security Considerations

**Work Data Protection:**
- Organization names (DRW, Apprenti) should be gitignored or configurable
- Actual work project details should stay private
- Meeting notes with sensitive content need protection
- Personal data stays local on macOS device

**Generalization for Replication:**
- Use generic terms: "Organization", "Manager", "Coach", "Colleague"
- Configurable via gitignored config files
- Template files provided for others to use
- System should work for any apprenticeship or work environment

**Implementation Strategy:**
```
backend/
├── config/
│   ├── workplaces.json         # Gitignored - user's orgs
│   └── workplaces.example.json # Template for others
├── data/                        # Gitignored - all personal data
└── models/                      # Generic data models
```

### Multi-Organization Support

**Context:**
- Primary: Trading firm (DRW) - day-to-day management
- Secondary: Apprenti (WTIA) - employer and program provider
- Both organizations have opportunities for engagement and productivity

**Requirements:**
- Support tracking across multiple organizations
- Different engagement opportunities per organization
- Separate project contexts
- Unified daily view across organizations

---

## 🛠️ Technical Preferences

### Architecture

**Approach:** Web-based productivity application

**Rationale:**
- Accessible from macOS browser
- Modern, interactive interface
- Easier to build rich UI for planning and tracking
- Can integrate with existing web-based tools

### Backend Stack

**Recommendation:** Python + Flask

**Rationale:**
- Python: Great for data tracking and analysis
- Flask: Simple, flexible, quick to get started
- Extensive library ecosystem
- Good for prototyping and iteration

**Alternatives Considered:**
- Node.js + Express (also viable, but Python preferred for data work)

### Database

**Recommendation:** SQLite

**Rationale:**
- Local database (no server needed)
- Privacy-first approach (data stays on device)
- Simple setup and management
- Sufficient for single-user productivity app
- Easy backups (single file)

**Alternatives Considered:**
- PostgreSQL (overkill for single-user local app)
- JSON files (less structured, harder to query)

### Frontend Stack

**Recommendation:** React

**Rationale:**
- Modern, component-based architecture
- Rich ecosystem and tooling
- Good for interactive, dynamic interfaces
- Strong community support

**Alternatives Considered:**
- Vue.js (also excellent choice, React slightly more familiar)
- Simple HTML/CSS/JS (too limited for rich features needed)

### Integration Opportunities

**Microsoft Outlook:**
- Calendar data integration for daily planning
- Meeting tracking and preparation
- Automatic engagement logging
- API available for calendar access

**Slack:**
- Community engagement tracking (manual initially)
- Potential for future integration
- Message/participation tracking

**GitHub:**
- Project activity tracking
- Work vs. personal repository separation
- Contribution patterns

---

## 🔮 Potential Feature Expansions

Based on inventory findings and user context, these features warrant consideration:

### Projects Feature (Potential 8th Core Feature)

**Status:** Under evaluation (Week 2 research)

**Motivation:** Inventory revealed 59 projects across work, personal, and learning categories, showing significant need for project organization beyond just Skills Matrix.

**Scope Questions:**
- Should Projects be promoted from "potential" to core feature?
- Is this MVP or post-MVP priority?
- What unique value does project tracking provide beyond Skills Matrix?

**Potential Capabilities:**
- Track project metadata (name, description, tech stack, status)
- Associate projects with organization (DRW/Apprenti/Personal)
- Link projects to skills (which skills used in which projects)
- Track project status/lifecycle (active, learning, archived)
- Connect to Daily Focus (what project am I working on today?)
- GitHub integration (sync repo info)
- Local project detection

**Integration Points:**
- **Skills Matrix:** "Used in X projects" for each skill
- **Daily Focus:** Project context for tasks
- **Goals:** Link goals to specific projects
- **Learning Journal:** Associate learnings with project work

**Data Model Needs:**
- Projects table with: name, path, remote URL, org, classification, status
- Project-to-Skills relationship (many-to-many)
- Project-to-Tasks relationship (for Daily Focus)
- Project-to-Goals relationship

**Decision Timing:** Week 2 data model research

**See Also:**
- [Current State Inventory](current-state-inventory.md) - Full 59-project catalog
- [POC Analysis](../research/automation/inventory-system-poc-analysis.md) - Technical debt and data model insights

### Multi-Organization Support Priority Re-evaluation

**Current Priority:** 🔵 LOW (Post-MVP)

**Inventory Shows:**
- 20 Work/Apprenti projects (34%)
- 16 Personal projects (27%)
- Clear separation needed for context switching

**Question:** Should Multi-Org research move from LOW (Post-MVP) to MEDIUM (Week 4)?

**Rationale:**
- User manages projects across multiple contexts (DRW, Apprenti, Personal, Learning)
- Context switching is a pain point identified in questionnaire
- Real data validates need (not hypothetical)

**Implications:**
- May affect data model design (organization field in multiple tables)
- May affect UI design (org switcher, filtering)
- May affect Skills Matrix (skills used at Work vs Personal)

**Decision Timing:** During Week 2-3 data model research

---

## ❓ Open Questions

### Daily Planning Workflow

1. What is the optimal time for daily planning?
   - Morning (start of workday)?
   - Evening (prepare for tomorrow)?
   - Both (review + plan)?

2. How long should daily planning take?
   - 5 minutes quick check-in?
   - 15 minutes structured planning?
   - 30 minutes comprehensive review?

3. What format works best?
   - Checklist style?
   - Time-blocked schedule?
   - Priority-based (P0, P1, P2)?
   - Goal-oriented (what outcomes to achieve)?

### Engagement Tracking

1. What level of detail is helpful for meeting prep?
   - Quick bullet points?
   - Structured questions?
   - Outcome definitions?
   - All of the above?

2. How to measure engagement quality vs. quantity?
   - Track frequency of interactions?
   - Track depth/value of interactions?
   - Both?

3. What makes an interaction "successful"?
   - Specific questions answered?
   - Feedback received?
   - Action items generated?
   - Relationship strengthened?

### Technical Implementation

1. Development timeline expectations?
   - MVP in weeks or months?
   - Phased rollout preferred?

2. Deployment approach?
   - Local development server?
   - Production-ready deployment?
   - Docker containerization?

3. Testing strategy?
   - Manual testing initially?
   - Automated tests from start?
   - User acceptance testing process?

---

## 🎯 Success Metrics

### User Success Metrics

**Productivity:**
- Improved task completion rates
- Better time allocation awareness
- Reduced context switching overhead
- Clear daily priorities established

**Engagement:**
- Increased meaningful interactions
- Better preparation for meetings
- Improved relationship building
- Active community participation

**Learning:**
- Knowledge gaps identified and addressed
- Regular reflection habit
- Feedback incorporation
- Skill development tracking

**Outcome:**
- Strong candidate for hiring after next rotation
- Demonstrated productivity improvement
- Clear growth trajectory
- Effective habit formation

### System Success Metrics

**Adoption:**
- Daily active usage
- Planning workflow adherence
- Engagement tracking consistency
- Feature utilization rates

**Effectiveness:**
- Time saved in planning
- Better meeting outcomes
- Reduced missed opportunities
- Improved organization

---

## 🚀 Next Steps

1. **Review and Validate**
   - User reviews this requirements document
   - Clarify open questions
   - Prioritize features if needed
   - Identify any missing requirements

2. **Technology Research**
   - Create technology-research.md
   - Evaluate Flask + React stack in detail
   - Document setup and integration approach
   - Create proof of concept if needed

3. **Workflow Analysis**
   - Create workflow-analysis.md
   - Document current daily workflow in detail
   - Design ideal workflow
   - Identify transition steps

4. **Feature Planning**
   - Create first feature plan (Daily Focus System)
   - Break into implementation phases
   - Define Phase 1 scope and tasks
   - Set up development environment

---

## 📚 Related Documents

- [Exploration Hub](README.md) - Main exploration directory
- [Technology Research](technology-research.md) - Tech stack evaluation (planned)
- [Workflow Analysis](workflow-analysis.md) - Current vs. ideal workflows (planned)

---

**Last Updated:** 2025-11-26  
**Status:** 🟠 In Progress  
**Next:** Review with user, clarify open questions, begin technology research



