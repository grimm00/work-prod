# Projects Feature - MVP Roadmap

**Feature:** Project Organization and Management  
**Priority:** #1 Foundation Feature  
**Target:** MVP ready for January deadline  
**Created:** 2025-12-02  
**Approach:** Vertical Slice TDD  
**Status:** 🟡 Planned

---

## 📋 Strategic Context

- **59 existing projects** need organization and management
- **Foundation feature** for Daily Focus, Skills Matrix, Goals, and Learning features
- **Real data available** from inventory POC (classifications.json)
- **Architecture decisions complete** (ADRs 0001-0005)
- **Testing strategy TBD** (Week 2 research → ADR-0006)

## 🎯 Prerequisites

**Before Implementation:**

- Complete testing strategy research
- Create ADR-0006: Testing Framework and TDD Approach
- Decide: pytest, frontend test framework, E2E tooling
- Establish test patterns for vertical slices

**Estimated Time:** 2-3 days (Week 2 research)

**Status:** 🟡 Planned - Testing research document created, ready to begin

---

## 🚀 Implementation Phases

### Phase 0: Development Environment (Day 1)

**Goal:** Minimal skeleton with testing infrastructure

**Vertical Slice Approach:**
- This phase sets up the bare minimum to begin TDD
- Subsequent phases each deliver one complete vertical slice

**Setup Tasks:**

**Backend:**
- Initialize Flask application factory (minimal)
- Set up blueprint structure (`/api/projects`)
- Configure SQLAlchemy + Flask-Migrate
- Configure testing framework (pytest - pending ADR-0006)
- Create /api/health endpoint

**Frontend:**
- Initialize Vite + React project (minimal)
- Configure Zustand store structure
- Set up React Router
- Configure Axios with base API service
- Configure testing framework (Vitest/Jest - pending ADR-0006)

**Integration:**
- Configure Vite proxy to Flask backend
- Verify CORS configuration
- Set up test runners and CI hooks

**Testing:**
- Backend: Health endpoint test (pytest)
- Frontend: Simple component test
- Integration: Frontend calls backend health check

**Deliverables:**
- [ ] Tests can run: `pytest` and `npm test`
- [ ] Simple health check test passes (backend + frontend integration)
- [ ] Ready for vertical slice TDD
- [ ] Development environment documented

---

### Phase 1: List Projects (Days 2-3)

**Goal:** Complete vertical slice - view all projects

**TDD Flow:**

1. **Write backend model test**
   - Test Project model creation with minimal fields
   - Test model validation

2. **Implement Project model (minimal)**
   - Fields: id, name, path, created_at, updated_at
   - SQLAlchemy model in `backend/models/project.py`
   - Database migration

3. **Write API test for GET /api/projects**
   - Test empty list response
   - Test list with projects
   - Test response format

4. **Implement GET /api/projects endpoint**
   - Blueprint route in `backend/api/projects.py`
   - Query all projects
   - Return JSON response

5. **Write frontend test for ProjectList component**
   - Test empty state rendering
   - Test project list rendering
   - Test loading state

6. **Implement ProjectList component with Zustand**
   - Create Zustand store for projects
   - Fetch projects from API
   - Display project list
   - Handle loading/error states

7. **Write integration test**
   - E2E test (if framework ready from ADR-0006)
   - Verify backend → API → frontend flow

8. **Verify end-to-end**
   - Manual testing: View empty project list
   - Manual testing: See project list after seeding test data

**Deliverables:**
- [ ] Can view empty project list
- [ ] Complete test coverage for this slice
- [ ] First vertical slice complete
- [ ] Zustand store pattern established

---

### Phase 2: Create Project (Days 4-5)

**Goal:** Complete vertical slice - add new project

**TDD Flow:**

1. **Write backend validation tests**
   - Test required field validation
   - Test field length limits
   - Test duplicate detection (by path or remote_url)

2. **Extend Project model**
   - Add fields: organization, classification, status
   - Add validation rules
   - Update migration

3. **Write API test for POST /api/projects**
   - Test successful creation
   - Test validation errors
   - Test duplicate handling

4. **Implement POST endpoint with validation**
   - Create route in projects blueprint
   - Validate input data
   - Create project record
   - Return created project

5. **Write frontend test for ProjectForm component**
   - Test form rendering
   - Test form validation
   - Test submit handler

6. **Implement form with Zustand actions**
   - Create ProjectForm component
   - Form fields for name, path, organization, classification, status
   - Client-side validation
   - Zustand action for creating project
   - Success/error handling

7. **Integration test: Create project flows to list**
   - E2E test: Fill form → submit → see in list
   - Verify data persistence

8. **Verify: Can create and see project in list**
   - Manual testing: Create project via UI
   - Manual testing: Verify appears in list

**Deliverables:**
- [ ] Can create projects via UI
- [ ] Validation working (backend + frontend)
- [ ] Second vertical slice complete
- [ ] Form pattern established

---

### Phase 3: Update and Delete Projects (Days 6-7)

**Goal:** Complete CRUD operations - edit and delete

**TDD Flow (Update):**

1. **Write backend update tests**
   - Test updating individual fields
   - Test validation on update
   - Test updating non-existent project

2. **Implement PATCH /api/projects/{id} endpoint**
   - Update project fields
   - Validate changes
   - Return updated project

3. **Write frontend test for Edit functionality**
   - Test edit form pre-population
   - Test update submission
   - Test optimistic updates in store

4. **Implement Edit UI**
   - Edit button on project detail
   - Edit mode in ProjectForm
   - Update Zustand action

**TDD Flow (Delete):**

1. **Write backend delete tests**
   - Test successful deletion
   - Test deleting non-existent project
   - Test cascade behavior (future)

2. **Implement DELETE /api/projects/{id} endpoint**
   - Delete project by ID
   - Return success response

3. **Write frontend test for Delete functionality**
   - Test delete confirmation dialog
   - Test delete action
   - Test removal from list

4. **Implement Delete UI**
   - Delete button with confirmation
   - Zustand delete action
   - Remove from store

**Deliverables:**
- [ ] Full CRUD operations working
- [ ] Can edit projects via UI
- [ ] Can delete projects with confirmation
- [ ] Project detail view complete

---

### Phase 4: Import Existing Projects (Days 8-9)

**Goal:** Import 59 projects from inventory POC

**TDD Flow:**

1. **Write import endpoint tests**
   - Test importing valid JSON
   - Test duplicate detection
   - Test validation errors
   - Test bulk insert

2. **Extend Project model for full schema**
   - Add fields: remote_url, description, tech_stack (JSON), learning_type
   - Add projects_skills junction table
   - Update migration

3. **Implement POST /api/projects/import endpoint**
   - Accept JSON array of projects
   - Validate each project
   - Detect duplicates (by remote_url or path)
   - Bulk insert with transaction
   - Return import summary

4. **Write frontend test for Import UI**
   - Test file upload
   - Test paste JSON
   - Test progress indicator
   - Test results display

5. **Implement Import UI**
   - Import button/page
   - JSON paste textarea or file upload
   - Progress indicator during import
   - Results summary (success/failures)

6. **Data mapping**
   - Map classifications.json to new schema
   - Set learning_type for Learning projects
   - Handle missing fields

**Deliverables:**
- [ ] All 59 projects imported successfully
- [ ] User can see their entire project portfolio
- [ ] Duplicate detection working
- [ ] Import results clearly displayed

---

### Phase 5: Search and Filtering (Days 10-11)

**Goal:** Find projects quickly in a 59+ project list

**TDD Flow:**

1. **Write search endpoint tests**
   - Test full-text search
   - Test filtering by organization
   - Test filtering by classification
   - Test filtering by status
   - Test filtering by learning_type
   - Test combined filters
   - Test sorting options

2. **Implement search backend**
   - SQLite FTS5 setup for full-text search
   - GET /api/projects/search endpoint
   - Query parameters: q, organization, classification, status, learning_type, sort
   - Return filtered and sorted results

3. **Write frontend search tests**
   - Test search input with debounce
   - Test filter chip components
   - Test results highlighting
   - Test no results state

4. **Implement search UI**
   - Search bar with debounced API calls
   - Filter dropdowns/chips
   - Results highlighting
   - Learning project badges
   - Sort dropdown

**Deliverables:**
- [ ] Sub-second search across all projects
- [ ] Multi-faceted filtering working
- [ ] Clear visual distinction for Learning projects
- [ ] Sort by name, date, status

---

### Phase 6: GitHub Integration (Days 12-13)

**Goal:** Sync metadata from GitHub repositories

**TDD Flow:**

1. **Write GitHub sync tests**
   - Test fetching repo metadata
   - Test updating project with GitHub data
   - Test rate limit handling
   - Test error handling (private repos, 404s)

2. **Implement GitHub integration**
   - GitHub API client
   - POST /api/projects/{id}/sync endpoint
   - Fetch: description, stars, last_updated, languages
   - Update project record
   - Store last_synced timestamp

3. **Write frontend sync tests**
   - Test sync button
   - Test sync status indicator
   - Test last synced display

4. **Implement sync UI**
   - Sync button on project detail
   - Last synced timestamp display
   - Sync status indicator (loading/success/error)
   - Batch sync for multiple projects

**Deliverables:**
- [ ] One-click sync for projects with remote_url
- [ ] GitHub data displayed in UI
- [ ] Error handling for private repos
- [ ] Rate limit awareness

---

### Phase 7: Polish and MVP Completion (Days 14-16)

**Goal:** Production-ready Projects feature

**Backend Polish:**
- Comprehensive error handling and logging
- API documentation (OpenAPI/Swagger)
- Database indexes optimization
- Backup strategy documentation

**Frontend Polish:**
- Responsive design (mobile, tablet, desktop)
- Loading states for all async operations
- Empty states with helpful messages
- Error messages with recovery suggestions
- Keyboard shortcuts (navigation, search)
- Accessibility audit (ARIA labels, focus management)

**Testing:**
- Manual testing checklist
- Edge cases (empty projects, long names, special characters, unicode)
- Performance testing (100+ projects)
- Browser compatibility testing

**Documentation:**
- User guide for Projects feature
- API documentation
- Developer setup guide
- Deployment instructions

**Deliverables:**
- [ ] Stable, polished Projects MVP
- [ ] Ready for daily use
- [ ] Foundation ready for other features
- [ ] All tests passing
- [ ] Documentation complete

---

## 📅 Timeline Summary

**Total Estimated Time:** 16 days (3 weeks)

- **Prerequisites:** 2-3 days (Testing research + ADR-0006)
- **Phase 0:** 1 day (Development environment)
- **Phase 1:** 2 days (List projects)
- **Phase 2:** 2 days (Create project)
- **Phase 3:** 2 days (Update/Delete)
- **Phase 4:** 2 days (Import 59 projects)
- **Phase 5:** 2 days (Search and filtering)
- **Phase 6:** 2 days (GitHub integration)
- **Phase 7:** 3 days (Polish and completion)

**Target Completion:** Mid-December (allows 2-3 weeks for other features before January deadline)

---

## ✅ Success Criteria

- [ ] All 59 projects imported and visible
- [ ] CRUD operations work flawlessly
- [ ] Search finds projects in < 1 second
- [ ] Filters work correctly (org, classification, learning_type)
- [ ] GitHub sync working for public repos
- [ ] UI is responsive and polished
- [ ] No critical bugs
- [ ] Test coverage > 80%
- [ ] Ready to use as daily project reference

---

## 🎯 Key Milestones

1. **Testing Strategy Complete** (ADR-0006 published)
2. **Environment Working** (End of Phase 0)
3. **First Project Created via UI** (Phase 2, Day 5)
4. **All 59 Projects Imported** (Phase 4, Day 9)
5. **Search and Filters Working** (Phase 5, Day 11)
6. **GitHub Sync Functional** (Phase 6, Day 13)
7. **MVP Complete** (Phase 7, Day 16)

---

## 📦 Dependencies

**Completed:**
- ✅ ADR-0001: Flask Backend Architecture
- ✅ ADR-0002: React Frontend Architecture
- ✅ ADR-0003: SQLite Database Design
- ✅ ADR-0004: Flask-React Integration Strategy
- ✅ ADR-0005: Projects as Foundation Architecture
- ✅ Projects Data Model Research (1,200+ lines)

**In Progress:**
- 🟠 Testing Strategy Research → ADR-0006

**Required for Start:**
- ADR-0006: Testing Framework and TDD Approach (Week 2)

**External Dependencies:**
- GitHub API (for sync feature - Phase 6)
- Python 3.11+
- Node.js 18+

---

## ⚠️ Risks and Mitigations

**Risk 1: Integration Issues Between Flask and React**
- **Mitigation:** Phase 0 validates Flask + React + SQLite integration early with health check test
- **Fallback:** Detailed troubleshooting in ADR-0004

**Risk 2: FTS5 Performance with Large Project Lists**
- **Mitigation:** Test with 100+ projects before committing to FTS5 approach
- **Fallback:** Use standard SQLite LIKE queries if FTS5 proves problematic

**Risk 3: GitHub Rate Limits**
- **Mitigation:** Implement caching, respect rate limits, graceful degradation
- **Fallback:** Manual metadata entry if sync fails

**Risk 4: Time Overrun**
- **Mitigation:** Phases 6-7 are optional for MVP. Core value is Phases 0-5 (CRUD + Import + Search)
- **Priority:** Phases 0-4 are essential, 5-7 are enhancements

**Risk 5: Testing Framework Learning Curve**
- **Mitigation:** Comprehensive research and ADR before implementation
- **Fallback:** Start with simple unit tests, add integration tests incrementally

---

## 🔮 Next Steps After MVP

Once Projects MVP is complete, these features can leverage the foundation:

1. **Daily Focus Integration**
   - Add project_id foreign key to tasks table
   - Associate daily tasks with projects
   - View tasks by project

2. **Skills Matrix Integration**
   - Leverage projects_skills junction table
   - Skill proficiency tracking per project
   - Skills discovered from project work

3. **Learning Journal**
   - Associate learnings with projects
   - Track learning progress per project
   - Link to Learning-type projects

4. **Goals**
   - Link goals to projects
   - Track project contribution to goals
   - Project-based milestone tracking

---

## 📚 References

- [ADR-0005: Projects as Foundation Architecture](../decisions/ADR-0005-projects-as-foundation-architecture.md)
- [Projects Data Model Research](../research/data-models/projects-data-model.md)
- [Testing Strategy Research](../research/tech-stack/testing-strategy.md)
- [Projects-First Strategy](notes/projects-first-strategy.md)
- [Current State Inventory](../exploration/current-state-inventory.md) - 59 projects

---

**Last Updated:** 2025-12-02  
**Status:** 🟡 Planned  
**Next:** Complete testing strategy research → ADR-0006 → Begin Phase 0


