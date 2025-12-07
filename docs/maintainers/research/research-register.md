◊# Research Register

**Purpose:** Catalog of research topics to investigate before implementation  
**Status:** 🟠 In Progress  
**Created:** 2025-11-26
**Last Updated:** 2025-12-02  
**Week 1:** ✅ Complete (4/4 topics)  
**Week 2:** ✅ Complete (1/1 critical prerequisite - Testing Strategy)  
**Inventory Refined:** 2025-12-01

---

## ⚠️ Update 2025-12-01: Inventory Findings Refined Research Plan

**Context:** Automated project inventory system discovered 59 unique projects and 24 languages, revealing data-driven insights that refine research priorities.

**Key Findings That Impact Research:**

1. **Projects Feature Under Evaluation**

   - 59 projects (20 Work, 16 Personal, 17 Learning, 6 Inactive) validates need
   - Decision: Being evaluated for promotion to 8th core feature during Week 2
   - See: [Requirements - Projects Feature Analysis](../exploration/requirements.md#projects-feature-potential-8th-core-feature)

2. **Multi-Org Priority Elevated**

   - Real data shows 34% Work, 27% Personal, 29% Learning split
   - Priority: 🔵 LOW → ⚠️ Under Review for 🟡 MEDIUM (Week 4)
   - See: Section 8.1 below

3. **Skills Matrix Has Real Seed Data**

   - 24 languages with usage patterns now available
   - Week 2 research can use [discovered-skills.md](../exploration/discovered-skills.md)
   - Schema must support "used in X projects" tracking

4. **SQLite Schema Gaps Identified**
   - Missing: Projects table, Skills-to-Projects relationship, classification patterns
   - See: [SQLite Schema Update](tech-stack/sqlite-database-design.md#️-update-2025-12-01-inventory-data-reveals-schema-gaps)

**Impact on Week 2 Research:**

- Skills Matrix research: Use real 24-language dataset
- Data models: Design Projects table and relationships
- Daily Focus: Consider project context for tasks

---

## 📋 Overview

This register catalogs all research topics identified for the work productivity and engagement management system. Topics are organized by category and prioritized based on impact on MVP delivery (January deadline) and user needs from the scope clarification questionnaire.

**Inventory-Driven Refinement:** After Week 1 completion, automated inventory system provided real user data (59 projects, 24 languages) that refined requirements and research priorities.

### Priority Levels

- 🔴 **CRITICAL** - Blocks MVP development, must research first
- 🟠 **HIGH** - Needed for core features, research early
- 🟡 **MEDIUM** - Important but can be researched during development
- 🔵 **LOW** - Nice to have, can be deferred

---

## 🎯 Research Topic Categories

### 1. Technology Stack & Architecture

### 2. Microsoft Ecosystem & Integration

### 3. Miro Integration & Capabilities

### 4. Data Model & Storage

### 5. User Interface & Experience

### 6. Security & Privacy

### 7. Feature-Specific Research

### 8. Productivity Best Practices

---

## 🔴 CRITICAL PRIORITY - Blocks MVP

### 1.1 Python Flask Backend Architecture

**Priority:** 🔴 CRITICAL  
**Category:** Technology Stack  
**Timeline:** Week 1

**Research Questions:**

- What is the best project structure for Flask applications in 2024?
- How to implement RESTful API design with Flask?
- Best practices for Flask configuration management (dev vs. production)?
- How to structure Flask apps for scalability?
- Flask extensions needed (Flask-CORS, Flask-SQLAlchemy, etc.)?

**Why Critical:**
Foundation for entire backend implementation.

**Resources:**

- Flask official documentation
- Flask mega-tutorial (Miguel Grinberg)
- Modern Flask project structures
- Flask best practices 2024

**Deliverables:**

- Backend architecture decision document
- Recommended Flask project structure
- List of required Flask extensions

**Status:** ✅ Complete - See [tech-stack/flask-backend-architecture.md](tech-stack/flask-backend-architecture.md)

---

### 1.2 React Frontend Architecture

**Priority:** 🔴 CRITICAL  
**Category:** Technology Stack  
**Timeline:** Week 1

**Research Questions:**

- React 18+ best practices for 2024?
- State management: Context API vs. Redux vs. Zustand?
- Component structure and organization patterns?
- React Router v6 for navigation?
- Build tools: Vite vs. Create React App vs. Next.js?

**Why Critical:**
Foundation for entire frontend implementation.

**Resources:**

- React official documentation
- React 2024 ecosystem overview
- State management comparison
- Modern React patterns

**Deliverables:**

- Frontend architecture decision document
- Recommended React project structure
- State management strategy
- Component design patterns

**Status:** ✅ Complete - See [tech-stack/react-frontend-architecture.md](tech-stack/react-frontend-architecture.md)

---

### 1.3 SQLite Database Design

**Priority:** 🔴 CRITICAL  
**Category:** Data Model  
**Timeline:** Week 1

**Research Questions:**

- SQLite best practices for single-user applications?
- Database schema design for productivity tracking?
- How to handle migrations with SQLAlchemy?
- Backup and recovery strategies for SQLite?
- Performance optimization for local database?

**Why Critical:**
Data persistence strategy must be decided before feature implementation.

**Resources:**

- SQLite documentation
- SQLAlchemy ORM patterns
- Database design best practices
- Local-first software principles

**Deliverables:**

- Initial database schema design
- Migration strategy
- Backup/recovery approach
- Entity Relationship Diagram (ERD)

**Status:** ✅ Complete - See [tech-stack/sqlite-database-design.md](tech-stack/sqlite-database-design.md)

---

### 1.4 Flask + React Integration

**Priority:** 🔴 CRITICAL  
**Category:** Technology Stack  
**Timeline:** Week 1

**Research Questions:**

- How to serve React app from Flask in development?
- Production deployment strategy (single server vs. separate)?
- CORS configuration for local development?
- API authentication/authorization patterns?
- Hot reload setup for development?

**Why Critical:**
Must work seamlessly for development workflow.

**Resources:**

- Flask + React integration tutorials
- CORS best practices
- Development environment setup guides

**Deliverables:**

- Development environment setup guide
- API integration patterns
- Authentication strategy

**Status:** ✅ Complete - See [tech-stack/flask-react-integration.md](tech-stack/flask-react-integration.md)

---

### 1.5 Testing Strategy and Framework Selection

**Priority:** 🔴 CRITICAL  
**Category:** Technology Stack  
**Timeline:** Week 2  
**Created:** 2025-12-02

**Research Questions:**

- Backend testing: pytest vs unittest vs nose2 for Flask applications?
- Frontend testing: Vitest vs Jest vs React Testing Library for React + Vite?
- E2E testing: Playwright vs Cypress vs Selenium for full-stack integration?
- How to structure tests for vertical slice TDD approach?
- Test organization: by feature vs by layer?
- Fixtures and test data management patterns?
- How to test Flask application factory and blueprints?
- How to test SQLAlchemy models and database interactions?
- How to test Zustand stores and React components?
- Coverage requirements and CI integration strategy?
- Pre-commit hooks for testing?

**Why Critical:**

Test-driven development approach requires testing infrastructure before implementation begins. Vertical slice architecture needs clear testing patterns for backend → API → frontend flow.

**Resources:**

- pytest documentation and Flask testing guides
- Vitest documentation and Vite integration
- Playwright/Cypress comparison studies
- TDD best practices for full-stack applications
- Testing patterns for vertical slice architecture

**Deliverables:**

- ADR-0006: Testing Framework and TDD Approach
- Backend testing framework decision (pytest recommended)
- Frontend testing framework decision (Vitest vs Jest)
- E2E testing framework decision
- Test organization patterns
- TDD workflow documentation
- CI integration strategy

**Status:** ✅ Complete - See [tech-stack/testing-strategy.md](tech-stack/testing-strategy.md) and [ADR-0006](../decisions/ADR-0006-testing-framework-and-tdd-approach.md)

---

## 🟠 HIGH PRIORITY - Core Features

### 2.0 Projects Data Model (NEW - ADDED 2025-12-01)

**Priority:** 🟠 HIGH - **STRATEGIC PIVOT**  
**Category:** Data Model  
**Timeline:** Week 2

**⚠️ Strategic Change:** Projects promoted from "potential 8th feature" to **Priority #1 core feature** based on user insight and inventory data (59 projects discovered).

**Research Questions:**

- How to model Projects table? (name, path, remote_url, organization, classification, status, tech_stack)
- **Learning sub-classification (MVP CRITICAL):** How to model Work-related vs Personal development learning?
  - Schema: learning_type (work_related | personal_dev | hybrid | null), learning_context, learning_status?
  - UI implications: filter by learning type, show learning progress?
  - Metrics: should work-related learning count toward work metrics?
  - Transitions: how to handle learning projects that change classification?
- Projects-to-Skills many-to-many relationship design?
- GitHub integration: how to sync repo metadata automatically?
- Local project detection: how to discover ~/Projects and ~/Learning projects?
- Classification system: Work / Personal / Learning / Inactive?
- Organization context: optional org_id for multi-context support?
- Project status lifecycle: active / learning / archived / inactive?
- Import strategy: how to import 59 projects from inventory POC?

**Why High Priority:**

- User insight: "Maybe right now, the project needs to start with organization of my projects in general?"
- 59 real projects discovered via inventory POC - no organization system exists
- Foundation for other features (Daily Focus, Skills Matrix, Goals, Learning)
- Real data available day 1 (can import immediately after schema design)

**Data Available:**

- [Current State Inventory](../exploration/current-state-inventory.md) - All 59 projects cataloged
- [Discovered Skills](../exploration/discovered-skills.md) - 24 languages for Skills-to-Projects relationship
- [Learning Project Taxonomy](data-models/learning-project-taxonomy.md) - Work vs Personal classification design (17 Learning projects)
- `classifications.json` - User-categorized projects
- Inventory POC scripts - Import logic reference

**Integration Points:**

- **Skills Matrix:** Projects-to-Skills many-to-many (show "used in X projects")
- **Daily Focus:** Project context for tasks (simplified: "What project today?")
- **Goals:** Goals can link to projects (optional project_id FK)
- **Learning Journal:** Learnings can associate with projects (optional project_id FK)

**Schema Gaps Identified:**

See [SQLite Schema Update](tech-stack/sqlite-database-design.md#️-update-2025-12-01-inventory-data-reveals-schema-gaps):

1. No Projects table (59 projects need tracking)
2. No Skills-to-Projects relationship
3. No classification/categorization pattern
4. Organization field not ubiquitous

**Deliverables:**

- Projects Data Model research document
- Projects table schema design (with learning_type, learning_context, learning_status fields)
- projects_skills junction table design
- Learning project classification schema (Work-related vs Personal development)
- Import strategy for 59 projects (including Learning sub-classification)
- UI mockups for Learning project filters and badges
- GitHub sync strategy
- Local project detection approach

**Resources:**

- [Projects-First Strategy](../planning/notes/projects-first-strategy.md) - Strategic rationale
- [Requirements - Projects Priority #1](../exploration/requirements.md#feature-priorities)
- [POC Analysis](automation/inventory-system-poc-analysis.md) - Implementation insights
- Week 1 SQLite research (needs Projects table addition)

**Status:** ✅ Complete - See [data-models/projects-data-model.md](data-models/projects-data-model.md)

**See Also:** [ADR-0005: Projects as Foundation Architecture](../decisions/ADR-0005-projects-as-foundation-architecture.md)

---

### 2.1 Microsoft Graph API - Outlook Integration

**Priority:** 🟠 HIGH  
**Category:** Microsoft Ecosystem  
**Timeline:** Week 2

**Research Questions:**

- How to authenticate with Microsoft Graph API?
- What are the rate limits and quotas?
- How to access Outlook calendar events via Graph API?
- Can we get meeting attendees, notes, and details?
- Real-time notifications via webhooks possible?
- Python SDK vs. direct REST API calls?

**Why High Priority:**
User has Outlook and wants automatic meeting population (Q10.1: pull from Outlook automatically).

**Resources:**

- Microsoft Graph API documentation
- Microsoft Graph Python SDK
- OAuth 2.0 authentication flows
- Calendar API endpoints

**Deliverables:**

- Outlook integration architecture
- Authentication flow documentation
- API endpoint mapping
- Proof of concept code

**Status:** 🔴 Not Started

---

### 2.2 Microsoft 365 Ecosystem Discovery

**Priority:** 🟠 HIGH  
**Category:** Microsoft Ecosystem  
**Timeline:** Week 2

**Research Questions:**

- What Microsoft 365 tools does the user have access to?
- Can we integrate with Teams (chat, status, presence)?
- OneNote API for capturing notes/learnings?
- Planner/To Do integration possibilities?
- Power Automate for workflow automation?
- What data can we access from these tools?

**Why High Priority:**
User works at trading firm, likely has full Microsoft 365 suite. Could unlock significant value.

**Resources:**

- Microsoft 365 admin center documentation
- Microsoft Graph API capabilities
- Teams API documentation
- OneNote API documentation

**Deliverables:**

- Available Microsoft 365 tools inventory
- Integration opportunities map
- Recommended integrations priority list

**Status:** 🔴 Not Started

---

### 2.3 Project Search and Filtering Architecture

**Priority:** 🟠 HIGH  
**Category:** Technology Stack  
**Timeline:** Week 2

**Context:** 59 projects across multiple classifications need robust search and filtering capabilities. Learning sub-classification adds additional filtering complexity.

**Research Questions:**

- What Python libraries for full-text search? (Whoosh, elasticsearch-py, PostgreSQL FTS?)
- SQLite FTS5 full-text search capabilities and performance?
- Tagging system architecture (free-form tags vs predefined categories)?
- Multi-faceted filtering: organization + classification + tech_stack + learning_type?
- Search performance with 59+ projects (scalability)?
- React UI components for search/filter (search bars, tag clouds, faceted filters)?
- Auto-complete and suggestion strategies?

**Why High Priority:**

- 59 projects is too many to browse without search
- Learning sub-classification (work_related vs personal_dev vs hybrid) adds filtering complexity
- User needs quick discovery: "all Python work projects" or "personal learning projects"
- Projects feature is Priority #1 - search is essential for usability

**Technology Options:**

**1. SQLite FTS5 (Full-Text Search extension)** ⭐ RECOMMENDED

- **Pros:** Built-in, no additional dependencies, fast for <1000 records, simple integration
- **Cons:** Limited to text search, no semantic search, requires separate FTS table
- **Use Case:** Search project names, descriptions, tech stack

**2. Flask-Elasticsearch**

- **Pros:** Powerful search, typo tolerance, semantic capabilities, aggregations
- **Cons:** Heavy infrastructure requirement, overkill for 59 projects, adds complexity
- **Use Case:** If project count grows to thousands

**3. Simple SQL LIKE with indexes**

- **Pros:** No new dependencies, works immediately
- **Cons:** Slow with growth, no relevance ranking, poor UX for multi-word queries
- **Use Case:** Temporary solution only

**React Search/Filter Libraries:**

- `react-select` - Multi-select dropdowns for tags/classifications (robust, accessible)
- `react-search-autocomplete` - Autocomplete search bars with suggestions
- `use-debounce` - Debounce search input for performance (reduce DB queries)
- `@tanstack/react-table` - Advanced table with built-in filtering (if using table view)

**Filtering Requirements:**

**Required Filters:**

1. **Organization:** DRW / Apprenti / Personal / null
2. **Classification:** Work / Personal / Learning / Inactive
3. **Learning Type:** work_related / personal_dev / hybrid / null (only for Learning projects)
4. **Tech Stack:** Multi-select from 24 discovered languages
5. **Status:** active / archived / paused / etc.

**Advanced Features:**

- **Search:** Free-text search across project name, description, path
- **Combined Filters:** AND logic (Organization=DRW AND Classification=Learning AND learning_type=work_related)
- **Saved Searches:** Store common filter combinations (e.g., "My Active Work Projects")

**Deliverables:**

- Search architecture decision (recommend: SQLite FTS5 + react-select)
- Tagging system design (if implemented)
- Filter UX mockups (wireframes for search bar + filter panel)
- Performance benchmarks (search latency with 59 projects)
- Schema design for FTS5 table (if using)

**Resources:**

- [SQLite FTS5 Documentation](https://www.sqlite.org/fts5.html)
- [react-select Documentation](https://react-select.com/)
- [Learning Project Taxonomy](data-models/learning-project-taxonomy.md) - Filtering requirements

**Status:** 🔴 Not Started - **Week 2 Priority #2** (after Projects Data Model)

---

### 3.1 Miro Platform Capabilities

**Priority:** 🔵 LOW → Deferred (2025-12-01)  
**Category:** Miro Integration  
**Timeline:** Post-MVP / Reconsider Later

**⚠️ Update 2025-12-01: Moved to Deferred**

**Reason for Deferral:**

- User insight: "I'm only adding Miro because it seems like 'the thing' to have"
- No clear use case identified during exploration phase
- Projects-first strategy pivot makes Miro less critical
- May revisit if visual board/goal tracking needs emerge

**Research Questions** (if reconsidered):

- What can Miro be used for in productivity tracking context?
- Does Miro have an API for programmatic access?
- Can we embed Miro boards in our web app?
- Can we create/update Miro boards automatically?
- Webhooks for real-time updates from Miro?
- Use cases: visual goal tracking, skill matrix, team exploration?

**Why Originally High Priority:**
User just discovered Miro access - could be valuable for visual tracking (skills matrix, goal boards, team exploration).

**Why Deferred:**
Without clear use case, implementing Miro integration would be premature optimization. Focus on Projects organization and Daily Focus first.

**Reconsider If:**

- User identifies specific visual board need
- Project planning requires visual Kanban/boards
- Team exploration needs visual mapping

**Resources** (if reconsidered):

- Miro API documentation
- Miro REST API reference
- Miro Web SDK
- Miro use cases for productivity

**Status:** 🔴 Deferred - No Clear Use Case

---

### 4.1 Daily Focus System Data Model

**Priority:** 🟠 HIGH  
**Category:** Data Model  
**Timeline:** Week 2

**Research Questions:**

- How to model daily priorities and tasks?
- How to capture "what should I focus on today?"
- Quick-capture mechanism design?
- Connection between tasks and goals/skills/meetings?
- Daily review and weekly reflection data structure?
- Time-based vs. outcome-based task tracking?

**Why High Priority:**
Highest priority feature (Priority 1 from original requirements).

**Resources:**

- Task management database schemas
- GTD (Getting Things Done) methodology
- Bullet journal digital implementations
- Personal productivity systems

**Deliverables:**

- Daily focus data model
- Task-goal-skill relationship map
- Quick capture interface design
- Review workflow design

**Status:** 🔴 Not Started

---

### 4.2 Learning Journal Data Model

**Priority:** 🟠 HIGH  
**Category:** Data Model  
**Timeline:** Week 2

**Research Questions:**

- How to capture daily/weekly learnings?
- Structure for "aha moments" and key concepts?
- Pattern identification: what relationships to track?
- Tagging/categorization strategy?
- Connection to skills development?
- Search and retrieval optimization?

**Why High Priority:**
User marked as HIGH priority (Q1), wants both daily and weekly capture with theme identification.

**Resources:**

- Knowledge management systems
- Note-taking app architectures (Obsidian, Roam)
- Zettelkasten method
- Learning analytics research

**Deliverables:**

- Learning journal data model
- Tagging/categorization strategy
- Pattern identification approach
- Weekly review workflow

**Status:** 🔴 Not Started

---

### 4.3 Skills Matrix Data Model

**Priority:** 🟠 HIGH  
**Category:** Data Model  
**Timeline:** Week 2

**Research Questions:**

- How to structure skill tracking (comprehensive)?
- Confidence levels: scale design (beginner → proficient)?
- Skill-to-team mapping data structure?
- Skill-to-opportunity connections?
- How to track skill progression over time?
- Skill categories and taxonomies?

**Why High Priority:**
User marked as HIGH priority (Q2), wants comprehensive tracking with team placement mapping.

**Resources:**

- Skills matrix examples
- Competency frameworks
- Career development tracking systems
- Skill assessment methodologies

**Deliverables:**

- Skills data model
- Confidence rating scale
- Skill taxonomy/categories
- Team-skill mapping approach
- Visual representation designs (Miro candidate?)

**Status:** 🔴 Not Started

---

### 4.4 Engagement & Meeting Data Model

**Priority:** 🟠 HIGH  
**Category:** Data Model  
**Timeline:** Week 2-3

**Research Questions:**

- How to model people/contacts (managers, coaches, colleagues)?
- Meeting preparation data structure?
- Meeting outcomes and follow-ups tracking?
- Questions asked vs. learnings captured?
- Action items and reminders?
- Search and linking across people/topics/meetings?
- Relationship to organizations (DRW vs. Apprenti)?

**Why High Priority:**
User marked as HIGH priority (Q4), critical for next rotation success.

**Resources:**

- CRM database schemas
- Meeting management systems
- Contact relationship management
- Interaction tracking patterns

**Deliverables:**

- People/contacts data model
- Meeting data model
- Engagement tracking schema
- Follow-up reminder system design
- Search architecture

**Status:** 🔴 Not Started

---

### 4.5 Goals & Hiring Readiness Data Model

**Priority:** 🟠 HIGH  
**Category:** Data Model  
**Timeline:** Week 2-3

**Research Questions:**

- How to structure weekly/monthly/rotation goals?
- Hierarchy: rotation goals → monthly → weekly → daily?
- Hiring readiness criteria: what to track?
- Technical vs. soft skills goal tracking?
- Progress measurement: metrics vs. checkpoints vs. reflection?
- Connection to daily focus and skills tracking?

**Why High Priority:**
User marked as HIGH priority (Q3), next rotation (January) is hiring decision point.

**Resources:**

- OKR (Objectives and Key Results) frameworks
- Goal tracking systems
- Career development frameworks
- Progress tracking methodologies

**Deliverables:**

- Goals hierarchy data model
- Hiring readiness framework
- Progress measurement approach
- Goal-to-daily-focus connection design

**Status:** 🔴 Not Started

---

### 4.6 Feedback Tracking Data Model

**Priority:** 🟠 HIGH  
**Category:** Data Model  
**Timeline:** Week 3

**Research Questions:**

- How to capture feedback from managers/coaches?
- Feedback categorization/tagging?
- Manual action item creation workflow?
- Simple theme aggregation approach?
- Connection to goals and daily focus?
- Historical tracking and review?

**Why High Priority:**
User marked as HIGH priority (Q5), coaches give regular feedback that needs systematic handling.

**Resources:**

- Performance review systems
- Feedback management tools
- 360-degree feedback models
- Action planning frameworks

**Deliverables:**

- Feedback data model
- Categorization strategy
- Action item workflow
- Theme aggregation approach

**Status:** 🔴 Not Started

---

### 4.7 Energy & Engagement Monitoring Data Model

**Priority:** 🟠 HIGH  
**Category:** Data Model  
**Timeline:** Week 3

**Research Questions:**

- How to capture energy levels (multiple times per day)?
- Engagement quality vs. quantity metrics?
- Productivity pattern identification algorithms?
- How to suggest best times for tasks based on patterns?
- Simple check-in interface design?
- Data visualization for insights?

**Why High Priority:**
User marked as HIGH priority (Q7), wants to identify productivity patterns and optimize scheduling.

**Resources:**

- Mood tracking apps
- Energy management research
- Circadian rhythm research
- Well-being monitoring systems

**Deliverables:**

- Energy tracking data model
- Check-in interface design
- Pattern analysis approach
- Scheduling recommendation algorithm

**Status:** 🔴 Not Started

---

## 🟡 MEDIUM PRIORITY - Important Features

### 5.1 User Interface Design Patterns

**Priority:** 🟡 MEDIUM  
**Category:** UI/UX  
**Timeline:** Week 3-4

**Research Questions:**

- Modern web app UI frameworks (Material-UI, Ant Design, Tailwind)?
- Dashboard design best practices?
- Mobile-responsive design requirements?
- Dark mode implementation?
- Accessibility (WCAG) compliance?
- Navigation patterns for productivity apps?

**Why Medium Priority:**
Important for user adoption but can evolve during development.

**Resources:**

- Material Design guidelines
- React component libraries comparison
- Productivity app UI analysis
- Accessibility guidelines

**Deliverables:**

- UI framework selection
- Design system basics
- Component library choices
- Wireframes for key views

**Status:** 🔴 Not Started

---

### 5.2 Daily Planning Workflow Research

**Priority:** 🟡 MEDIUM  
**Category:** Productivity Best Practices  
**Timeline:** Week 3

**Research Questions:**

- When is the best time to plan (morning vs. evening)?
- How long should daily planning take?
- What triggers should prompt re-planning during the day?
- Best practices for weekly reviews?
- Integration with existing time management methodologies?

**Why Medium Priority:**
User doesn't currently plan (Q3.2 response), needs guidance. Can refine based on user feedback.

**Resources:**

- Time management research
- GTD methodology
- Pomodoro technique
- Morning/evening routine research
- Weekly review best practices

**Deliverables:**

- Recommended planning workflow
- Default planning times
- Quick re-planning triggers
- Weekly review structure

**Status:** 🔴 Not Started

---

### 5.3 Notification & Reminder System

**Priority:** 🟡 MEDIUM  
**Category:** Feature-Specific  
**Timeline:** Week 4

**Research Questions:**

- Browser notification API capabilities?
- How to implement meeting preparation reminders?
- Follow-up reminder timing strategies?
- User notification preferences (frequency, timing)?
- Desktop vs. web vs. email notifications?

**Why Medium Priority:**
User wants automatic reminders (Q4.2, Q10.2) but can be added after core capture features.

**Resources:**

- Web Push API documentation
- Notification best practices
- Email notification services
- Reminder timing research

**Deliverables:**

- Notification architecture
- Reminder timing strategy
- User preference configuration
- Implementation approach

**Status:** 🔴 Not Started

---

### 6.1 Data Privacy & Security

**Priority:** 🟡 MEDIUM  
**Category:** Security & Privacy  
**Timeline:** Week 3-4

**Research Questions:**

- How to secure locally-stored sensitive data?
- SQLite encryption options?
- API authentication best practices?
- HTTPS setup for local development?
- Data export and backup security?
- Compliance considerations (even for personal use)?

**Why Medium Priority:**
User has privacy concerns (start.txt mentions keeping work data private/gitignored).

**Resources:**

- SQLite encryption extensions
- Flask security best practices
- OAuth 2.0 flows
- Local data security patterns

**Deliverables:**

- Security architecture
- Data encryption strategy
- Authentication implementation plan
- Privacy compliance checklist

**Status:** 🔴 Not Started

---

### 6.2 Data Export & Portability

**Priority:** 🟡 MEDIUM  
**Category:** Data Model  
**Timeline:** Week 4

**Research Questions:**

- What export formats to support (JSON, CSV, Markdown)?
- How to structure exports for portability?
- Import from other systems?
- Backup automation strategies?
- Data migration between versions?

**Why Medium Priority:**
User wants system to be replicable, suggests data should be portable.

**Resources:**

- Data portability standards
- Export format best practices
- Backup strategies
- Data migration patterns

**Deliverables:**

- Export format specifications
- Backup automation approach
- Import capabilities design

**Status:** 🔴 Not Started

---

### 7.1 Search & Filtering Architecture

**Priority:** 🟡 MEDIUM  
**Category:** Feature-Specific  
**Timeline:** Week 4

**Research Questions:**

- Full-text search implementation in SQLite?
- How to make meeting notes searchable/linkable?
- Filtering across multiple dimensions (people, topics, dates)?
- Search result ranking?
- Real-time search vs. indexed search?

**Why Medium Priority:**
User wants full search capability (Q4.4) but can be added after core data capture.

**Resources:**

- SQLite FTS (Full-Text Search)
- Search UX patterns
- Filtering best practices
- Search result ranking algorithms

**Deliverables:**

- Search architecture
- Filtering implementation plan
- Search result ranking strategy

**Status:** 🔴 Not Started

---

### 8.6 Project Inventory & Automation System

**Priority:** 🟡 MEDIUM  
**Category:** Automation / Tooling  
**Timeline:** Week 4

**Research Questions:**

- Data model for project tracking (classification embedded vs separate)?
- Pipeline architecture (stages, deduplication timing)?
- Configuration management approach (config file vs environment variables)?
- Integration with Skills Matrix and potential Projects feature?
- Script organization patterns (flat vs subdirectories)?
- Master orchestration vs individual scripts?

**Why Medium Priority:**
POC already works and generated valuable data (59 unique projects cataloged, 24 languages identified for Skills Matrix seed data). Refactoring improves maintainability but not blocking MVP development. Week 2-4 focused on HIGH priority user-facing features.

**Resources:**

- Automation best practices
- Pipeline architecture patterns
- Configuration management approaches
- Data model design patterns

**Deliverables:**

- POC analysis document (what works, technical debt)
- Full research document (data model, pipeline, config options)
- ADR-0005 for inventory system architecture
- Refactored implementation (scripts reorganization)
- Updated documentation

**Status:** 🟡 POC Complete - Research Scheduled Week 4

---

## 🔵 LOW PRIORITY - Future Enhancements

### 8.1 Multi-Organization Support Architecture

**Priority:** 🔵 LOW → ⚠️ Under Review (2025-12-01)  
**Category:** Feature-Specific  
**Timeline:** Post-MVP (possibly Week 4)

**⚠️ Update 2025-12-01: Inventory Data Suggests Priority Increase**

**Inventory Findings:**

- 20 Work/Apprenti projects (34%)
- 16 Personal projects (27%)
- 17 Learning projects (29%)
- 6 Inactive projects (10%)

**Current Assessment:**

- Clear organizational separation exists in user's actual project data
- Context switching is a documented pain point (questionnaire)
- Real data validates need (not hypothetical)
- Could affect data model design across multiple features

**Recommendation:** Consider elevating to 🟡 MEDIUM priority (Week 4) alongside other polish/architecture topics.

**Decision Point:** Week 2 data model research (when designing Skills, Tasks, Projects tables)

**Research Questions:**

- How to model multiple organizations (DRW, Apprenti)?
- Unified vs. separate views?
- Organization-specific configurations?
- Data isolation between organizations?
- Should `organization_id` be added to Skills, Tasks, Projects tables?

**Why Originally Low Priority:**
User marked as HIGH priority (Q8) but noted "DRW is primary focus" - can implement basic support initially, enhance later.

**Why Reconsidering:**

- 59 projects show clear org separation (34% Work, 27% Personal, 29% Learning)
- Context switching documented as pain point
- May be simpler to design org support into schema from start vs. retrofit later

**Resources:**

- Multi-tenancy patterns
- Organization hierarchy modeling
- Context switching UX
- [Requirements - Multi-Org Priority Re-evaluation](../../exploration/requirements.md#multi-organization-support-priority-re-evaluation)

**Deliverables:**

- Multi-org data model
- View switching approach
- Basic implementation plan

**Status:** 🔴 Not Started

---

### 8.2 Team Exploration Feature

**Priority:** 🔵 LOW  
**Category:** Feature-Specific  
**Timeline:** Post-MVP

**Research Questions:**

- How to track team interactions?
- Team profile/wiki structure?
- Interest tracking and rating?
- Question suggestion based on team?

**Why Low Priority:**
User marked as LOW priority (Q9), doesn't know teams yet - can add later when needed.

**Resources:**

- Team discovery frameworks
- Career exploration tools
- Team fit assessment methods

**Deliverables:**

- Team tracking data model (basic)
- Interest tracking approach

**Status:** 🔴 Not Started

---

### 8.3 Advanced Analytics & Insights

**Priority:** 🔵 LOW  
**Category:** Feature-Specific  
**Timeline:** Post-MVP

**Research Questions:**

- What analytics provide value vs. overhead?
- Predictive insights based on patterns?
- Goal progress visualization?
- Skill development trajectory?
- Engagement trend analysis?

**Why Low Priority:**
Focus on capture first, insights later per user's philosophy (Q5 note).

**Resources:**

- Personal analytics research
- Data visualization libraries (Chart.js, D3.js)
- Pattern detection algorithms
- Insight generation frameworks

**Deliverables:**

- Analytics requirements
- Visualization approach
- Insight generation strategy

**Status:** 🔴 Not Started

---

### 8.4 Mobile Access

**Priority:** 🔵 LOW  
**Category:** Feature-Specific  
**Timeline:** Post-MVP

**Research Questions:**

- Progressive Web App (PWA) vs. native app?
- Mobile-responsive web app sufficient?
- Offline capabilities needed?
- Quick-capture via mobile?

**Why Low Priority:**
Not mentioned in user requirements, desktop/browser focus implied.

**Resources:**

- PWA documentation
- Mobile-first design patterns
- Offline-first architecture
- Mobile quick-capture UX

**Deliverables:**

- Mobile strategy
- Responsive design approach
- Quick-capture mobile interface

**Status:** 🔴 Not Started

---

### 8.5 AI-Assisted Features

**Priority:** 🔵 LOW  
**Category:** Feature-Specific  
**Timeline:** Post-MVP

**Research Questions:**

- AI agent for meeting prep assistance (user's Q10 note)?
- Pattern recognition in learnings/feedback?
- Goal recommendation based on trajectory?
- Smart scheduling suggestions?
- Integration with ChatGPT/Claude/other LLMs?

**Why Low Priority:**
User mentioned AI agent could help with prep "once I have all information logged" - capture first, intelligence later.

**Resources:**

- LLM API documentation (OpenAI, Anthropic)
- Prompt engineering best practices
- AI assistant patterns
- RAG (Retrieval Augmented Generation)

**Deliverables:**

- AI feature opportunities
- LLM integration architecture
- Prompt templates

**Status:** 🔴 Not Started

---

## 🔵 DEFERRED - Post-MVP Considerations

### 9.1 ITIL 4 Framework Integration

**Priority:** 🔵 DEFERRED  
**Category:** Process Framework  
**Timeline:** Post-MVP

**Context:** User is ITIL 4 Certified and interested in applying ITIL service management concepts to project organization.

**User Question (2025-12-01):** _"I believe that there needs to be some kind of framework surrounding how we go about organizing our projects. I am ITIL 4 Certified, and honestly this is the only thing that I can think about adding to the 'brain' of this project. I'm open to other ways to inject organizational thought processes into our project."_

**Potential Applications:**

- Service lifecycle stages for projects (design → transition → operation → continual improvement)
- Change management for project status transitions
- Service catalog metaphor for project organization
- Value streams for learning and skill development
- Service desk concepts for task/issue management
- Continual improvement mindset for productivity optimization

**Why Deferred:**

- MVP focuses on basic project organization first (Projects Priority #1)
- ITIL concepts valuable but not blocking functionality
- User prefers: "Focus on basic organization first, discuss ITIL integration after MVP"
- Need working system before adding process framework layer
- Can retrospectively map ITIL concepts to MVP structure

**Decision Point:** After Phase 1 (Projects CRUD) operational, evaluate if ITIL 4 concepts would enhance UX or organizational clarity.

**Resources:**

- ITIL 4 Foundation documentation
- Service management best practices
- User's ITIL expertise (primary resource)

**Deliverables (Post-MVP):**

- ITIL 4 mapping to project lifecycle
- Service catalog design for project types
- Change management workflow for project status
- Value stream mapping for learning paths

**Status:** 🔵 DEFERRED - Evaluate after Phase 1

---

### 9.2 Project Hash/Deduplication Strategy

**Priority:** 🔵 NOT NEEDED  
**Category:** Data Integrity  
**Timeline:** N/A

**User Question (2025-12-01):** _"Projects may need a hash (based on name and author maybe? Some conventional means?) to make sure project duplication doesn't happen, which will be key if I ever use another machine with similar projects."_

**Decision:** NOT NEEDED

**Rationale:**

- **Current Deduplication Works:** Inventory POC uses `remote_url` for deduplication (proven effective)
- **Deduplication Script Success:** `deduplicate-projects.py` successfully merged GitHub + local projects by remote URL
- **Data Validates Approach:** 59 projects deduplicated to 59 unique entries (from 70 with duplicates) - 100% success rate
- **Local Projects:** Projects without remotes use local path as primary key (unique per machine, no cross-machine concern)
- **Edge Cases Minimal:** Projects without remotes are typically machine-specific anyway (POC, experiments)

**Alternative Considered:**

- Hash based on name + author
- **Problem:** Doesn't handle renames, author changes, or projects without clear "author"
- **Problem:** More complex than needed for the use case
- **Problem:** Still requires unique identifier (hash collision risk, however small)

**Multi-Machine Scenario:**

- **Different machines:** Local paths are inherently different, no collision
- **Same project on different machines:** Should have same `remote_url`, deduplicated correctly
- **Project without remote:** Typically machine-specific (tutorials, experiments), duplication acceptable

**Conclusion:** `remote_url` + `local_path` is sufficient identifier strategy. No hash needed.

**Status:** ✅ Decided - No Action Required

---

## 📊 Research Execution Plan

### Week 1: Foundation (CRITICAL)

- [ ] Python Flask backend architecture
- [ ] React frontend architecture
- [ ] SQLite database design
- [ ] Flask + React integration

### Week 2: Core Data Models & Microsoft Integration (HIGH)

- [ ] Microsoft Graph API - Outlook integration
- [ ] Microsoft 365 ecosystem discovery
- [ ] Daily focus system data model
- [ ] Learning journal data model
- [ ] Skills matrix data model

### Week 3: Additional Data Models & Miro (HIGH)

- [ ] Engagement & meeting data model
- [ ] Goals & hiring readiness data model
- [ ] Feedback tracking data model
- [ ] Energy & engagement monitoring data model
- [ ] Miro platform capabilities

### Week 4: Polish & Medium Priority (MEDIUM)

- [ ] User interface design patterns
- [ ] Daily planning workflow research
- [ ] Notification & reminder system
- [ ] Data privacy & security
- [ ] Data export & portability
- [ ] Search & filtering architecture
- [ ] Project inventory & automation system

### Post-MVP: Enhancements (LOW)

- Future phases after January MVP delivery

---

## 📋 Research Methods

### For Each Topic:

1. **Literature Review**

   - Official documentation
   - Best practices articles
   - Academic research (where relevant)
   - Case studies

2. **Proof of Concept**

   - Quick prototype/spike for technical topics
   - Test feasibility
   - Validate assumptions

3. **Document Findings**

   - Create research document in `exploration/` directory
   - Document decisions in ADRs if architectural
   - Update this register with status

4. **Create Deliverables**
   - Templates, guides, or plans as specified
   - Store in appropriate feature `deliverables/` folder when features are created

---

## 📝 Notes

### Research Philosophy

**"Capture First, Automate Later"** (from user Q5 note)

- Focus research on data capture and manual workflows initially
- Defer automation and intelligence features
- Build foundation that can support future enhancements

### Critical Timeline

**Next rotation: Beginning of January 2025**

- Must have MVP operational before rotation
- ~5-6 weeks for research + development
- Prioritize ruthlessly

### Key User Insights

- User doesn't currently plan daily - needs workflow guidance
- Energy tracking multiple times per day - keep interface simple
- Comprehensive skill tracking - consider Miro for visualization
- Meeting prep is crucial - Outlook integration high value
- DRW primary, Apprenti secondary (admin/reporting)
- Manual conversion preferred over automatic (feedback → tasks)

---

## 🔗 Related Documents

- [Requirements](requirements.md) - Comprehensive requirements gathering
- [Scope Clarification Questionnaire](scope-clarification-questionnaire.md) - User responses
- [Exploration Hub](README.md) - Exploration directory overview

---

**Last Updated:** 2025-12-01  
**Status:** 🟠 In Progress  
**Next:** Begin Week 2 research (Projects Data Model, Learning Sub-Classification, Search Architecture)
