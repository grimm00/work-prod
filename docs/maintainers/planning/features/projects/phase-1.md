# Projects Feature - Phase 1: List Projects

**Phase:** 1 - List Projects (First Vertical Slice)  
**Duration:** 2 days  
**Status:** 🔴 Not Started  
**Prerequisites:** Phase 0 complete

---

## 📋 Overview

Phase 1 delivers the first complete vertical slice: viewing all projects. This phase establishes the TDD pattern for backend → API → frontend flow that will be used in all subsequent phases. By the end, users can see an empty project list with proper loading and empty states.

**Success Definition:** Can view project list in UI (empty state renders correctly).

---

## 🎯 Goals

1. **Project Model Created** - SQLAlchemy model with minimal fields
2. **GET /api/projects Endpoint** - Returns list of projects as JSON
3. **ProjectList Component** - Displays projects in React UI
4. **Zustand Store** - Manages projects state globally
5. **Complete Test Coverage** - Unit and integration tests passing

---

## 📝 Tasks

### TDD Flow (Backend → Frontend → Integration)

#### 1. Write Backend Model Test

- [ ] Create `tests/models/test_project.py`
- [ ] Test Project model creation with fields: id, name, path, created_at, updated_at
- [ ] Test model validation (name required, path unique)
- [ ] Test model serialization to JSON

#### 2. Implement Project Model

- [ ] Create `app/models/project.py`
- [ ] SQLAlchemy model with fields:
  - `id`: Integer, primary key
  - `name`: String(200), required
  - `path`: String(500), unique, nullable
  - `created_at`: DateTime, default now
  - `updated_at`: DateTime, onupdate now
- [ ] Add `to_dict()` method for JSON serialization
- [ ] Create database migration: `flask db init && flask db migrate -m "Add projects table"`

#### 3. Write API Endpoint Test

- [ ] Create `tests/api/test_projects.py`
- [ ] Test GET /api/projects returns empty list
- [ ] Test GET /api/projects returns list with projects (seed test data)
- [ ] Test response format: `{"projects": [...], "total": N}`
- [ ] Test response status codes (200 OK)

#### 4. Implement GET /api/projects Endpoint

- [ ] Create `app/api/projects.py` blueprint
- [ ] Register blueprint in application factory
- [ ] Implement GET /api/projects route:
  ```python
  @projects_bp.route('/projects', methods=['GET'])
  def get_projects():
      projects = Project.query.all()
      return jsonify({
          'projects': [p.to_dict() for p in projects],
          'total': len(projects)
      })
  ```
- [ ] Run backend tests: `pytest`

#### 5. Write Frontend Component Test

- [ ] Create `frontend/tests/components/ProjectList.test.jsx`
- [ ] Test ProjectList renders loading state
- [ ] Test ProjectList renders empty state
- [ ] Test ProjectList renders project list
- [ ] Test error state rendering

#### 6. Implement ProjectList Component with Zustand

- [ ] Create `frontend/src/stores/projectsStore.js`:
  ```javascript
  import create from 'zustand'
  
  export const useProjectsStore = create((set) => ({
    projects: [],
    loading: false,
    error: null,
    fetchProjects: async () => {
      set({ loading: true, error: null })
      try {
        const response = await api.get('/api/projects')
        set({ projects: response.data.projects, loading: false })
      } catch (error) {
        set({ error: error.message, loading: false })
      }
    }
  }))
  ```

- [ ] Create `frontend/src/components/ProjectList.jsx`:
  - Display loading spinner when loading
  - Display empty state message when no projects
  - Display project list with name and path
  - Handle errors gracefully

- [ ] Add ProjectList to App.jsx

#### 7. Write Integration Test

- [ ] Create E2E test (if framework ready):
  - Navigate to projects page
  - Verify page loads
  - Verify empty state message displays
  - Seed test project
  - Verify project appears in list

#### 8. Manual Testing

- [ ] Run backend: `python run.py`
- [ ] Run frontend: `npm run dev`
- [ ] Open http://localhost:5173
- [ ] Verify empty state renders
- [ ] Add test project via API: `curl -X POST http://localhost:5000/api/projects -d '{"name": "Test", "path": "/test"}'`
- [ ] Verify project appears in UI

---

## ✅ Completion Criteria

- [ ] Project model exists with minimal fields
- [ ] Database migration created and applied
- [ ] GET /api/projects endpoint works
- [ ] Backend tests pass (model + API)
- [ ] Zustand projects store implemented
- [ ] ProjectList component renders correctly
- [ ] Frontend tests pass
- [ ] Can view empty project list in browser
- [ ] Can view seeded projects in browser
- [ ] No errors in console (backend or frontend)

---

## 📦 Deliverables

1. **Backend Code**
   - Project SQLAlchemy model
   - GET /api/projects endpoint
   - Database migration
   - Model and API tests

2. **Frontend Code**
   - ProjectList component
   - Zustand projects store
   - Component tests

3. **Tests**
   - Backend: test_project.py, test_projects.py
   - Frontend: ProjectList.test.jsx
   - Integration test (if E2E framework ready)

4. **Documentation**
   - Update README with ProjectList usage
   - API documentation for GET /api/projects

---

## 🔗 Dependencies

### Prerequisites

- ✅ Phase 0: Development Environment complete

### External Dependencies

- None (uses existing Flask + React setup)

### Blocks

- Phase 2: Create Project

---

## ⚠️ Risks

**Risk: Model Design Too Minimal**  
**Mitigation:** Start minimal, extend in Phase 2. Avoids over-engineering.

**Risk: Empty State Not Clear**  
**Mitigation:** Use friendly message like "No projects yet. Create your first project!"

---

## 📊 Progress Tracking

**Phase Status:** 🔴 Not Started

- [ ] Backend model tests written
- [ ] Project model implemented
- [ ] API tests written
- [ ] GET endpoint implemented
- [ ] Frontend tests written
- [ ] ProjectList component implemented
- [ ] Zustand store implemented
- [ ] Integration test written
- [ ] Manual testing complete

---

## 🔗 Related Documents

- [Phase 0: Development Environment](phase-0.md)
- [Phase 2: Create Project](phase-2.md)
- [Feature Plan](feature-plan.md)
- [Projects Feature Hub](README.md)

---

**Last Updated:** 2025-12-02  
**Status:** 🔴 Not Started  
**Next:** Begin after Phase 0 complete


