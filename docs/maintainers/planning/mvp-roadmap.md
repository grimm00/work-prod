# Projects Feature - Backend MVP Roadmap

**Feature:** Project Organization and Management  
**Priority:** #1 Foundation Feature  
**Target:** Backend MVP ready for daily use (2 weeks)  
**Created:** 2025-12-02  
**Updated:** 2025-12-02 (Backend-First Pivot)  
**Approach:** Backend-First API Development with CLI  
**Status:** 🟠 In Progress (Phase 0 Complete)

---

## 📋 Strategic Context

- **59 existing projects** need organization and management
- **Foundation feature** for Daily Focus, Skills Matrix, Goals, and Learning features
- **Real data available** from inventory POC (classifications.json)
- **Architecture decisions complete** (ADRs 0001-0006)
- **Backend-first approach** reduces cognitive load, focuses on Python/Flask
- **Frontend deferred** to Phase 8 as a learning project (JavaScript/React)

---

## 🎯 Backend MVP Goals

1. **API Complete** - All CRUD operations working
2. **CLI Tools** - Daily-usable command-line interface
3. **Data Imported** - All 59 projects loaded and manageable
4. **Search/Filter** - Find projects quickly
5. **Production Ready** - Stable, tested, documented

**Timeline:** 2 weeks (10 days) vs. original 3+ weeks for full-stack

---

## 🚀 Implementation Phases

### ✅ Phase 0: Development Environment (Complete)

**Duration:** 1 day  
**Status:** ✅ Complete

**Accomplished:**
- Flask application factory with health endpoint
- React + Vite project (deferred to Phase 8)
- pytest configured (100% coverage on health endpoint)
- Vitest configured (deferred to Phase 8)
- Backend and testing infrastructure ready

**Deliverables:**
- ✅ Backend tests run: `pytest`
- ✅ Health check endpoint verified
- ✅ Ready for TDD backend development

---

### Phase 1: Projects API - List & Get (1.5 days)

**Status:** 🔴 Not Started

**Goals:**
- Project model with minimal fields (id, name, path, timestamps)
- GET /api/projects endpoint (list all)
- GET /api/projects/<id> endpoint (get single)
- Basic CLI `proj list` command
- Backend tests with >80% coverage

**TDD Flow:**
1. Write model tests → Implement model
2. Write API tests → Implement endpoints
3. Create CLI tool → Test with curl
4. Verify coverage and functionality

**Deliverables:**
- [ ] Project model and migration
- [ ] List and get endpoints working
- [ ] CLI `proj list` command
- [ ] Backend tests passing

---

### Phase 2: Projects API - Create & Update (1.5 days)

**Status:** 🔴 Not Started

**Goals:**
- Extend model with organization, classification, status
- POST /api/projects endpoint (create)
- PUT /api/projects/<id> endpoint (update)
- CLI `proj create` and `proj update` commands
- Full validation (server-side)

**TDD Flow:**
1. Extend model tests → Add fields and migration
2. Write POST/PUT tests → Implement endpoints
3. Enhance CLI → Test with curl
4. Validate all edge cases

**Deliverables:**
- [ ] Extended model with core fields
- [ ] Create and update endpoints
- [ ] CLI create/update commands
- [ ] Validation working

---

### Phase 3: Projects API - Delete & Archive (1 day)

**Status:** 🔴 Not Started

**Goals:**
- DELETE /api/projects/<id> endpoint
- PUT /api/projects/<id>/archive endpoint
- CLI `proj delete` and `proj archive` commands
- Safety checks and confirmations

**Deliverables:**
- [ ] Delete endpoint (permanent removal)
- [ ] Archive endpoint (soft delete)
- [ ] CLI delete/archive commands

---

### Phase 4: Projects API - Search & Filter (1.5 days)

**Status:** 🔴 Not Started

**Goals:**
- Query parameters (status, organization, classification)
- Text search (name, description)
- Multiple filter combinations
- CLI filter flags
- Performance optimization

**Deliverables:**
- [ ] Filtering by all criteria
- [ ] Text search working
- [ ] CLI with filter flags
- [ ] Query performance < 100ms

---

### Phase 5: Projects API - Import from JSON (1 day)

**Status:** 🔴 Not Started

**Goals:**
- POST /api/projects/import endpoint
- Data mapping from inventory POC
- Duplicate handling
- CLI `proj import` command
- All 59 projects imported

**Deliverables:**
- [ ] Bulk import endpoint
- [ ] Data mapping script
- [ ] CLI import command
- [ ] All 59 projects loaded

---

### Phase 6: CLI Enhancement & Daily Use Tools (1 day)

**Status:** 🔴 Not Started

**Goals:**
- Rich library for tables and colors
- Configuration file (~/.projrc)
- Additional commands (stats, recent, active)
- Better error handling
- Comprehensive help

**Deliverables:**
- [ ] Beautiful CLI output
- [ ] Config file support
- [ ] Convenience commands
- [ ] Production-ready CLI

---

### Phase 7: Manual Testing & Bug Fixes (2 days)

**Status:** 🔴 Not Started

**Goals:**
- Comprehensive manual testing
- Bug fixes (critical and high priority)
- Performance optimization
- API documentation (OpenAPI spec)
- User documentation complete

**Deliverables:**
- [ ] All manual tests pass
- [ ] Critical bugs fixed
- [ ] API fully documented
- [ ] Backend MVP production-ready

---

### Phase 8: Frontend Learning Project (Deferred)

**Status:** 🟡 Deferred (No Deadline)

**Goals:**
- Learn React with working backend
- Build UI on top of stable API
- No deadline pressure
- Track as separate learning project

**Why Deferred:**
- Reduces cognitive load during MVP
- Allows focus on Python/Flask (strength area)
- Backend is usable via CLI in the meantime
- JavaScript/React learning is tracked as its own project
- Can learn React at own pace without deadline

**Future Phases (When Ready):**
- Phase 8a: Basic React components
- Phase 8b: Project list/detail views
- Phase 8c: Create/edit forms
- Phase 8d: Search and filters
- Phase 8e: UI polish

---

## 📊 Timeline Comparison

### Original Full-Stack Approach
- Phase 0: 1 day
- Phases 1-6: 2 days each = 12 days
- Phase 7: 3 days
- **Total: ~16 days (3+ weeks)**

### Backend-First Approach
- Phase 0: ✅ 1 day (complete)
- Phase 1: 1.5 days
- Phase 2: 1.5 days
- Phase 3: 1 day
- Phase 4: 1.5 days
- Phase 5: 1 day
- Phase 6: 1 day
- Phase 7: 2 days
- **Total: ~10 days (2 weeks)**

**Time Saved:** 6 days (38% faster)

---

## ✅ Success Criteria

### Backend MVP Complete When:
- [ ] All CRUD operations working via API
- [ ] CLI enables daily project management
- [ ] All 59 projects imported and manageable
- [ ] Search and filter working efficiently
- [ ] Backend test coverage > 80%
- [ ] API documented (OpenAPI spec)
- [ ] No critical bugs
- [ ] Production-ready for daily use

### Phase 8 (Frontend) Complete When:
- [ ] React UI fully functional
- [ ] All API endpoints have UI
- [ ] UX is polished and intuitive
- [ ] Frontend tests pass
- [ ] JavaScript learning project goals met

---

## 🛠️ Technology Stack

### Backend (Current Focus)
- Python 3.11+
- Flask 3.0 (application factory)
- SQLAlchemy + Flask-Migrate
- SQLite (local-first)
- pytest (testing)

### CLI Tools
- Python requests library
- Click (CLI framework)
- Rich (beautiful terminal output)
- Configuration file support

### Frontend (Phase 8 - Deferred)
- React 18
- Vite (build tool)
- Zustand (state management)
- React Router v6
- Vitest (testing)

---

## 📝 CLI Tool Design

### Commands

```bash
# List projects
proj list [--status STATUS] [--org ORG] [--search TERM]

# Get single project
proj get <id>

# Create project
proj create NAME [--path PATH] [--org ORG] [--status STATUS]

# Update project
proj update <id> [--name NAME] [--status STATUS] [...]

# Delete project
proj delete <id>

# Archive project
proj archive <id>

# Import projects
proj import <file.json>

# Statistics
proj stats

# Recent projects
proj recent

# Active projects
proj active
```

### Example Usage

```bash
# List all active work projects
proj list --status active --org work

# Create a new project
proj create "work-prod" --path ~/Projects/work-prod --org work --status active

# Update project status
proj update 1 --status completed

# Show project statistics
proj stats

# Import all projects
proj import projects.json
```

---

## 🔍 Risk Mitigation

### Risk: Backend-Only Seems Limited
**Mitigation:** CLI provides full functionality, sufficient for daily use  
**Evidence:** Many developers prefer CLI tools (git, gh, docker, kubectl)

### Risk: Learning Two Things Separately
**Mitigation:** Deep understanding of backend before frontend actually helps learning  
**Evidence:** TDD and API design patterns apply to both

### Risk: Frontend Takes Longer Later
**Mitigation:** No deadline on Phase 8, it's a learning project  
**Evidence:** Working API makes frontend straightforward

---

## 📚 Documentation

### Backend MVP Documentation
- API Reference (OpenAPI spec)
- CLI Usage Guide
- Development Setup
- Testing Guide
- Troubleshooting

### Phase 8 Documentation (Future)
- Frontend Architecture
- Component Guide
- State Management Patterns
- Testing Patterns

---

## 🎯 Next Steps

**Immediate (This Week):**
1. ✅ Update all planning documents (this session)
2. Begin Phase 1: List & Get Projects
3. Establish backend TDD workflow

**Next Week:**
1. Complete Phases 2-3 (Create, Update, Delete)
2. Begin Phases 4-5 (Search, Import)

**Week 3:**
1. Complete Phase 6 (CLI Polish)
2. Begin Phase 7 (Testing & Documentation)

**MVP Complete:** ~2 weeks from Phase 1 start

---

## 📞 Decision Points

### When to Start Phase 8?
- Backend MVP complete and stable
- Using CLI daily without issues
- Ready to dedicate time to JavaScript/React learning
- No other pressing projects

### Criteria for Phase 8 Readiness:
- Backend has been stable for 1+ week
- Comfortable with backend codebase
- JavaScript learning project prioritized
- Time available for learning (not rushed)

---

**Last Updated:** 2025-12-02  
**Status:** 🟠 In Progress (Phase 0 Complete)  
**Next:** Begin Phase 1 - List & Get Projects  
**Timeline:** 2 weeks to Backend MVP
