# Phase 2 Manual Testing Guide

**Phase:** Phase 2 - Create & Update Projects  
**Testing Date:** 2025-12-03  
**Tester:** User verification before PR merge

---

## 🚀 Pre-Testing Setup

### 1. Start the Backend Server

```bash
# Terminal 1: Start backend
cd /Users/cdwilson/Projects/work-prod/backend
source ../venv/bin/activate
python run.py

# You should see:
# * Running on http://127.0.0.1:5000
```

### 2. Verify Server is Running

```bash
# Terminal 2: Test health endpoint
curl http://localhost:5000/api/health
# Expected: {"message": "Flask backend is running", "status": "ok"}
```

---

## 📋 Test Scenarios

### Scenario 1: Create Project with curl (Minimal Data)

**Test:** Create a project with only required field (name)

```bash
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Minimal Test Project"}' | python -m json.tool
```

**Expected Result:**
- Status: 201 Created
- Response includes:
  - `id` (auto-generated)
  - `name`: "Minimal Test Project"
  - `status`: "active" (default)
  - `created_at` and `updated_at` timestamps
  - All other fields null

**Verify:**
- [ ] Status code is 201
- [ ] Project has an ID
- [ ] Default status is "active"

---

### Scenario 2: Create Project with curl (Full Data)

**Test:** Create a project with all fields populated

```bash
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Full Test Project",
    "path": "/test/full",
    "organization": "work",
    "classification": "primary",
    "status": "active",
    "description": "A complete test project",
    "remote_url": "https://github.com/user/test-repo"
  }' | python -m json.tool
```

**Expected Result:**
- Status: 201 Created
- All fields populated as provided

**Verify:**
- [ ] All fields match input
- [ ] Timestamps are present
- [ ] ID is auto-generated

---

### Scenario 3: Update Project with curl (Partial Update)

**Test:** Update only status and description of project #1

```bash
curl -X PATCH http://localhost:5000/api/projects/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed", "description": "Testing PATCH"}' | python -m json.tool
```

**Expected Result:**
- Status: 200 OK
- Only `status` and `description` changed
- Other fields unchanged
- `updated_at` timestamp updated

**Verify:**
- [ ] Status changed to "completed"
- [ ] Description updated
- [ ] Other fields unchanged
- [ ] updated_at is newer than created_at

---

### Scenario 4: Validation - Invalid Classification

**Test:** Try to create project with invalid classification

```bash
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Invalid Test", "classification": "wrong_value"}' | python -m json.tool
```

**Expected Result:**
- Status: 400 Bad Request
- Error message mentions valid classification values

**Verify:**
- [ ] Status code is 400
- [ ] Error message is clear
- [ ] Lists valid values: primary, secondary, archive, maintenance

---

### Scenario 5: Validation - Invalid Status

**Test:** Try to update with invalid status

```bash
curl -X PATCH http://localhost:5000/api/projects/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "invalid_status"}' | python -m json.tool
```

**Expected Result:**
- Status: 400 Bad Request
- Error message mentions valid status values

**Verify:**
- [ ] Status code is 400
- [ ] Error message lists valid values: active, paused, completed, cancelled

---

### Scenario 6: Validation - Duplicate Path

**Test:** Try to create project with duplicate path

```bash
# First, note an existing path from previous tests
# Then try to create another project with same path:
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Duplicate Test", "path": "/test/full"}' | python -m json.tool
```

**Expected Result:**
- Status: 409 Conflict
- Error message about duplicate path

**Verify:**
- [ ] Status code is 409
- [ ] Error message mentions path already exists

---

### Scenario 7: CLI - Create Project

**Test:** Create project using CLI tool

```bash
cd /Users/cdwilson/Projects/work-prod
./scripts/project_cli/proj create \
  --name "CLI Created Project" \
  --organization "personal" \
  --classification "secondary" \
  --description "Testing CLI create"
```

**Expected Result:**
- Green checkmark with success message
- Beautiful table showing project details
- All fields displayed correctly

**Verify:**
- [ ] Success message shows ✓
- [ ] Project details in formatted table
- [ ] Fields match input

---

### Scenario 8: CLI - Update Project

**Test:** Update a project using CLI (use ID from previous test)

```bash
./scripts/project_cli/proj update <PROJECT_ID> \
  --status "paused" \
  --description "Updated via CLI"
```

**Expected Result:**
- Green checkmark with success message
- Table showing "Before" and "After" values
- Only changed fields displayed

**Verify:**
- [ ] Success message shows ✓
- [ ] Before/After comparison table
- [ ] Only status and description shown (changed fields)

---

### Scenario 9: CLI - List Projects

**Test:** List all projects to see created ones

```bash
./scripts/project_cli/proj list
```

**Expected Result:**
- Beautiful table with all projects
- Shows: ID, Name, Path, Created date
- All previously created projects visible

**Verify:**
- [ ] Table displays correctly
- [ ] All test projects are listed
- [ ] Formatting is clean and readable

---

### Scenario 10: CLI - Get Project Details

**Test:** Get details of a specific project

```bash
./scripts/project_cli/proj get 1
```

**Expected Result:**
- Project details in panel/box format
- All fields displayed

**Verify:**
- [ ] Details show correctly
- [ ] All fields present
- [ ] Formatting is clean

---

## ✅ Acceptance Criteria

Mark these as complete after testing:

### API Functionality
- [ ] POST /api/projects creates projects with minimal data
- [ ] POST /api/projects creates projects with full data
- [ ] PATCH /api/projects/<id> updates projects (partial updates work)
- [ ] Validation rejects invalid classification values
- [ ] Validation rejects invalid status values
- [ ] Duplicate path detection works (409 Conflict)
- [ ] 404 returned for non-existent projects

### CLI Functionality
- [ ] `proj create` command works with all options
- [ ] `proj update` command works with partial updates
- [ ] `proj list` shows all projects in table format
- [ ] `proj get` shows project details
- [ ] Error messages are clear and helpful
- [ ] Rich formatting displays correctly

### Data Integrity
- [ ] Created projects have auto-generated IDs
- [ ] Default status is "active" when not specified
- [ ] Timestamps (created_at, updated_at) are set correctly
- [ ] Updated projects have newer updated_at timestamp
- [ ] Path uniqueness is enforced

### User Experience
- [ ] All error messages are clear
- [ ] CLI output is beautiful and readable
- [ ] Tables format correctly
- [ ] Colors/symbols (✓/✗) display properly

---

## 🐛 Issues Found During Testing

**Document any issues here:**

| Issue # | Description | Severity | Status |
|---------|-------------|----------|--------|
| 1       |             |          |        |
| 2       |             |          |        |

---

## 📝 Test Results Summary

**Testing Completed:** [ ] Yes / [ ] No  
**Date Tested:** ___________  
**Tester:** ___________

**Overall Result:**
- [ ] ✅ All tests passed - Ready for PR
- [ ] ⚠️ Minor issues found - Fix before PR
- [ ] ❌ Major issues found - Requires rework

**Notes:**

---

## 🔄 Post-Testing Actions

If all tests pass:
1. Stop the backend server (Ctrl+C in Terminal 1)
2. Inform the developer that manual testing is complete
3. Proceed with PR creation

If issues are found:
1. Document issues in table above
2. Stop the backend server
3. Discuss issues with developer
4. Retest after fixes

