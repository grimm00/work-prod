# Projects Feature - Phase 0: Development Environment

**Phase:** 0 - Development Environment Setup  
**Duration:** 1 day  
**Status:** 🔴 Not Started  
**Prerequisites:** ADR-0006 (Testing Framework Decisions)

---

## 📋 Overview

Phase 0 establishes the minimal development environment skeleton with testing infrastructure. This phase sets up the foundation for Test-Driven Development (TDD) using vertical slices. The goal is to have both backend and frontend servers running with hot reload, test frameworks configured, and a simple health check endpoint to verify end-to-end integration.

**Success Definition:** Can run `pytest`, `npm test`, and call a health check API from the React frontend.

---

## 🎯 Goals

1. **Flask Application Factory Running**
   - Minimal Flask app with application factory pattern
   - Development server running on port 5000
   - Hot reload working

2. **React + Vite Project Running**
   - Minimal React app with Vite
   - Development server running on port 5173
   - Hot reload working
   - Vite proxy to Flask backend configured

3. **Testing Infrastructure**
   - pytest configured for backend
   - Frontend test framework configured (Vitest/Jest per ADR-0006)
   - Test runners working
   - Simple tests passing

4. **Integration Verified**
   - Flask serves /api/health endpoint
   - React calls /api/health successfully
   - CORS working via Vite proxy
   - End-to-end data flow confirmed

---

## 📝 Tasks

### Backend Setup

- [ ] **Create Flask application structure**
  ```
  backend/
  ├── app/
  │   ├── __init__.py          # Application factory
  │   ├── api/
  │   │   ├── __init__.py
  │   │   └── projects.py      # Projects blueprint (stub)
  │   └── models/
  │       └── __init__.py
  ├── tests/
  │   ├── __init__.py
  │   └── test_health.py       # Health check test
  ├── config.py                 # Configuration
  ├── requirements.txt          # Dependencies
  └── run.py                    # Development server entry
  ```

- [ ] **Install Flask dependencies**
  - Flask
  - Flask-CORS
  - Flask-SQLAlchemy
  - Flask-Migrate
  - python-dotenv

- [ ] **Configure pytest**
  - Create pytest.ini
  - Set up test fixtures
  - Configure Flask test client

- [ ] **Create health check endpoint**
  - Route: GET /api/health
  - Response: `{"status": "ok", "message": "Flask backend is running"}`

- [ ] **Write health check test**
  - Test GET /api/health returns 200
  - Test response JSON structure

- [ ] **Run Flask development server**
  - Verify server starts on port 5000
  - Verify hot reload working
  - Test health endpoint with curl/Postman

### Frontend Setup

- [ ] **Initialize Vite + React project**
  ```
  frontend/
  ├── src/
  │   ├── main.jsx
  │   ├── App.jsx
  │   ├── services/
  │   │   └── api.js           # Axios base configuration
  │   ├── stores/
  │   │   └── projectsStore.js # Zustand store (stub)
  │   └── components/
  │       └── HealthCheck.jsx  # Test component
  ├── tests/
  │   └── App.test.jsx
  ├── vite.config.js           # Vite proxy configuration
  ├── package.json
  └── index.html
  ```

- [ ] **Install frontend dependencies**
  - React 18
  - React Router v6
  - Zustand
  - Axios
  - Frontend testing framework (per ADR-0006)

- [ ] **Configure Vite proxy**
  - Proxy `/api/*` to `http://localhost:5000`
  - Enable CORS handling

- [ ] **Create Axios service**
  - Base URL configuration
  - Request/response interceptors
  - Error handling

- [ ] **Configure frontend tests**
  - Set up test framework
  - Configure test environment
  - Mock API responses

- [ ] **Create HealthCheck component**
  - Call GET /api/health on mount
  - Display response message
  - Show loading and error states

- [ ] **Write component test**
  - Test HealthCheck renders
  - Test loading state
  - Test successful API call
  - Test error handling

- [ ] **Run Vite development server**
  - Verify server starts on port 5173
  - Verify hot reload working
  - Test API call to backend

### Integration Testing

- [ ] **Run both servers concurrently**
  - Backend: Flask on port 5000
  - Frontend: Vite on port 5173

- [ ] **Verify end-to-end flow**
  - Frontend calls /api/health
  - Backend responds with JSON
  - Frontend displays response
  - No CORS errors

- [ ] **Run all tests**
  - Backend: `pytest`
  - Frontend: `npm test`
  - All tests pass

---

## ✅ Completion Criteria

- [ ] Flask development server runs and serves /api/health
- [ ] React development server runs and makes API calls
- [ ] Vite proxy correctly routes /api/* to Flask backend
- [ ] CORS configured and working (no errors in browser console)
- [ ] pytest runs and health check test passes
- [ ] Frontend tests run and HealthCheck component test passes
- [ ] Hot reload works for both backend and frontend
- [ ] Can see "Flask backend is running" message in React UI
- [ ] No errors in terminal or browser console
- [ ] Documentation: README with setup instructions

---

## 📦 Deliverables

1. **Backend Code**
   - Flask application factory
   - Health check endpoint
   - pytest configuration
   - requirements.txt

2. **Frontend Code**
   - Vite + React project
   - Axios service configuration
   - HealthCheck component
   - Test configuration

3. **Configuration Files**
   - vite.config.js with proxy
   - pytest.ini
   - config.py for Flask
   - .env.example

4. **Documentation**
   - README.md with setup instructions
   - How to run development servers
   - How to run tests
   - Troubleshooting guide

5. **Tests**
   - Backend health check test
   - Frontend HealthCheck component test
   - All tests passing

---

## 🔗 Dependencies

### Prerequisites

- ✅ ADR-0001: Flask Backend Architecture
- ✅ ADR-0002: React Frontend Architecture
- ✅ ADR-0004: Flask-React Integration Strategy
- 🟡 ADR-0006: Testing Framework and TDD Approach (BLOCKER)

### External Dependencies

- Python 3.11+
- Node.js 18+
- npm or yarn

### Blocks

- Phase 1: List Projects (needs working environment)
- All subsequent phases

---

## ⚠️ Risks

### Risk 1: Flask + React Integration Issues

**Probability:** Low (already researched)  
**Impact:** High (blocks all development)  
**Mitigation:** Follow ADR-0004 integration strategy exactly  
**Contingency:** Refer to ADR-0004 troubleshooting section

### Risk 2: Testing Framework Configuration

**Probability:** Medium  
**Impact:** Medium (delays Phase 0)  
**Mitigation:** ADR-0006 provides clear decisions and examples  
**Contingency:** Start with minimal test setup, enhance later

### Risk 3: CORS Issues

**Probability:** Low  
**Impact:** Medium (API calls fail)  
**Mitigation:** Vite proxy handles CORS in development  
**Contingency:** Add Flask-CORS if proxy insufficient

---

## 📊 Progress Tracking

**Phase Status:** 🔴 Not Started

### Task Checklist

**Backend (0/6 complete)**
- [ ] Flask structure created
- [ ] Dependencies installed
- [ ] pytest configured
- [ ] Health endpoint created
- [ ] Health test passing
- [ ] Server running

**Frontend (0/7 complete)**
- [ ] Vite project initialized
- [ ] Dependencies installed
- [ ] Proxy configured
- [ ] Axios service created
- [ ] Test framework configured
- [ ] HealthCheck component working
- [ ] Server running

**Integration (0/3 complete)**
- [ ] Both servers running
- [ ] End-to-end flow verified
- [ ] All tests passing

---

## 💡 Notes

### Development Workflow

1. Start backend: `cd backend && python run.py`
2. Start frontend: `cd frontend && npm run dev`
3. Open browser: http://localhost:5173
4. See "Flask backend is running" message

### Testing Workflow

1. Backend tests: `cd backend && pytest`
2. Frontend tests: `cd frontend && npm test`
3. Watch mode: Add `-- --watch` flag

### Hot Reload

- **Backend:** Flask auto-reloads on .py file changes
- **Frontend:** Vite HMR updates on .jsx/.js file changes

---

## 🔗 Related Documents

- [Projects Feature Hub](README.md)
- [Feature Plan](feature-plan.md)
- [Status and Next Steps](status-and-next-steps.md)
- [Phase 1: List Projects](phase-1.md)
- [ADR-0004: Flask-React Integration Strategy](../../../decisions/ADR-0004-flask-react-integration-strategy.md)

---

**Last Updated:** 2025-12-02  
**Status:** 🔴 Not Started  
**Blocker:** ADR-0006 (Testing Framework Decisions)  
**Next:** Begin setup after testing strategy complete


