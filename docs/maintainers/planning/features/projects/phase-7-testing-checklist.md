# Phase 7: Manual Testing Execution Checklist

**Phase:** Phase 7 - Manual Testing & Bug Fixes  
**Task:** Task 1 - Manual Testing Checklist  
**Created:** 2025-12-06  
**Status:** 🔴 In Progress

---

## 📋 Overview

This checklist organizes the 58 manual testing scenarios from `manual-testing.md` into an executable testing plan. Use this to track progress through Phase 7 comprehensive testing.

**Testing Approach:**
1. Execute scenarios in order (some depend on previous scenarios)
2. Document any bugs found in `fix/bugs.md`
3. Mark scenarios as complete as you test them
4. Update this checklist with results

---

## 🚀 Pre-Testing Setup

### Backend Server Setup

- [ ] Start backend server: `cd backend && source ../venv/bin/activate && python run.py`
- [ ] Verify health endpoint: `curl http://localhost:5000/api/health`
- [ ] Backend running on http://127.0.0.1:5000

### Testing Environment

- [ ] Terminal 1: Backend server running
- [ ] Terminal 2: Ready for curl commands
- [ ] Terminal 3: Ready for CLI commands (if needed)
- [ ] Database: Fresh or known state

---

## 📊 Testing Progress Summary

**Total Scenarios:** 58  
**Completed:** 0  
**Passed:** 0  
**Failed:** 0  
**Skipped:** 0  
**Progress:** 0%

---

## 🔍 API Endpoint Testing

### Health Check
- [ ] **Scenario N/A:** GET /api/health - Basic health check
  - Expected: 200 OK, `{"message": "Flask backend is running", "status": "ok"}`
  - Status: ⬜ Not Tested

### List Projects (GET /api/projects)
- [ ] **Scenario 14:** List projects (empty database)
- [ ] **Scenario 15:** List projects (with data)
- [ ] **Scenario 16:** Filter by status
- [ ] **Scenario 17:** Filter by organization
- [ ] **Scenario 18:** Filter by classification
- [ ] **Scenario 19:** Multiple filters combined
- [ ] **Scenario 20:** Search by name
- [ ] **Scenario 21:** Search case-insensitive
- [ ] **Scenario 22:** Search partial match
- [ ] **Scenario 23:** Search in description

### Get Single Project (GET /api/projects/<id>)
- [ ] **Scenario 13:** Get project by ID
- [ ] **Scenario 12:** Get project - not found (404)

### Create Project (POST /api/projects)
- [ ] **Scenario 1:** Create with minimal data (name only)
- [ ] **Scenario 2:** Create with full data
- [ ] **Scenario 4:** Validation - invalid classification (400)
- [ ] **Scenario 5:** Validation - invalid status (400)
- [ ] **Scenario 6:** Validation - duplicate path (409)
- [ ] **Scenario 9:** Validation - missing name (400)
- [ ] **Scenario 34:** Request body validation - missing Content-Type
- [ ] **Scenario 35:** Request body validation - invalid JSON
- [ ] **Scenario 36:** Request body validation - non-object body
- [ ] **Scenario 37:** Request body validation - missing projects field (import)

### Update Project (PATCH /api/projects/<id>)
- [ ] **Scenario 3:** Update project (partial update)
- [ ] **Scenario 10:** Update - invalid classification (400)
- [ ] **Scenario 11:** Update - invalid status (400)
- [ ] **Scenario 15:** Update appears in list

### Delete Project (DELETE /api/projects/<id>)
- [ ] **Scenario 24:** Delete project
- [ ] **Scenario 25:** Delete - not found (404)

### Archive Project (PUT /api/projects/<id>/archive)
- [ ] **Scenario 26:** Archive project
- [ ] **Scenario 27:** Archive - not found (404)

### Import Projects (POST /api/projects/import)
- [ ] **Scenario 29:** Import single project
- [ ] **Scenario 30:** Import multiple projects
- [ ] **Scenario 31:** Import with duplicates (skip duplicates)
- [ ] **Scenario 32:** Import with errors (continue on error)
- [ ] **Scenario 33:** Import statistics response

---

## 💻 CLI Command Testing

### List Command (`proj list`)
- [ ] **Scenario 7:** CLI list projects
- [ ] **Scenario 24:** CLI list with filters (updated)
- [ ] **Scenario 27a:** CLI list table display

### Get Command (`proj get <id>`)
- [ ] **Scenario 8:** CLI get project

### Create Command (`proj create`)
- [ ] **Scenario 7:** CLI create project (interactive)

### Update Command (`proj update`)
- [ ] **Scenario 8:** CLI update project

### Delete Command (`proj delete`)
- [ ] **Scenario 24:** CLI delete with confirmation

### Archive Command (`proj archive`)
- [ ] **Scenario 27:** CLI archive project

### Import Command (`proj import`)
- [ ] **Scenario 33:** CLI import from JSON file

### Configuration Commands (`proj config`)
- [ ] **Scenario 50:** Config show (displays defaults)
- [ ] **Scenario 51:** Config set/get API URL

### Convenience Commands
- [ ] **Scenario 38:** `proj stats` - Statistics display
- [ ] **Scenario 39:** `proj recent` - Recent projects
- [ ] **Scenario 40:** `proj active` - Active projects filter
- [ ] **Scenario 41:** `proj mine` - My projects filter

### Error Handling
- [ ] **Scenario 47:** Invalid config value handling
- [ ] **Scenario 48:** Health URL construction (with/without trailing slash)
- [ ] **Scenario 49:** Missing path handling (use .get())
- [ ] **Scenario 52:** Connection error handling
- [ ] **Scenario 53:** Timeout error handling
- [ ] **Scenario 54:** Invalid URL format handling
- [ ] **Scenario 55:** Generic error handling

---

## 🔬 Edge Case Testing

### Empty Database
- [ ] List projects with empty database
- [ ] Get project from empty database (404)
- [ ] Delete from empty database (404)

### Large Dataset
- [ ] List with 100+ projects (performance)
- [ ] Search with 100+ projects (performance)
- [ ] Filter with 100+ projects (performance)

### Invalid Input Handling
- [ ] Very long project names (>255 chars)
- [ ] Very long descriptions (>1000 chars)
- [ ] Special characters in names/paths
- [ ] SQL injection attempts (sanitized)
- [ ] XSS attempts (sanitized)

### Network Errors
- [ ] Backend down - connection error
- [ ] Backend down - timeout error
- [ ] Invalid API URL configuration
- [ ] Network timeout scenarios

### Concurrent Operations
- [ ] Create same project simultaneously (duplicate detection)
- [ ] Update same project simultaneously (last write wins)
- [ ] Delete while updating (handled gracefully)

---

## 🐛 Bug Tracking

**Bugs Found:** 0

Document all bugs in `fix/bugs.md` with:
- Priority (Critical, High, Medium, Low)
- Description
- Steps to reproduce
- Expected vs actual behavior
- Fix status

---

## ✅ Testing Completion Criteria

- [ ] All 58 scenarios executed
- [ ] All critical bugs fixed
- [ ] All high priority bugs fixed
- [ ] Medium/low bugs documented for future phases
- [ ] Performance acceptable (< 100ms for queries)
- [ ] Edge cases tested
- [ ] Error handling verified

---

## 📝 Notes

**Testing Order:**
- Execute scenarios in numerical order (some depend on previous scenarios)
- Scenario 6 requires Scenario 2 to be run first
- Scenario 8 requires Scenario 7 to be run first

**Database State:**
- Some scenarios require specific database state
- Note if database needs to be reset between test groups

**Manual Testing Guide:**
- Full scenario details: `manual-testing.md`
- Each scenario has expected results and verification checklist

---

**Last Updated:** 2025-12-06  
**Next:** Execute scenarios systematically, document bugs, fix critical issues

