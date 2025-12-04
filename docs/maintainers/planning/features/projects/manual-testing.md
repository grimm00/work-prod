# Projects Feature Manual Testing Guide

**Phases:** Phase 2 & Phase 3 - Create, Update, Delete & Archive  
**Last Updated:** 2025-12-03  
**Tester:** User verification before PR merge

---

## ⚠️ Important Notes

**Run scenarios in order!** Some scenarios depend on data created by previous scenarios:
- Scenario 6 (duplicate path) requires Scenario 2 (full project creation) to be run first
- Scenario 8 (CLI update) requires Scenario 7 (CLI create) to be run first

**Database state matters:** If you restart the server or reset the database between scenarios, validation tests may not work as expected.

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

**Prerequisites:** Scenario 2 must be run first to create a project with path "/test/full"

**Test:** Try to create project with duplicate path

```bash
# This requires Scenario 2 to have created a project with path "/test/full"
# If Scenario 2 wasn't run, this will succeed (status 201) instead of failing
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Duplicate Test", "path": "/test/full"}' | python -m json.tool
```

**Expected Result:**
- Status: 409 Conflict
- Error message about duplicate path

**If you get 201 Created:** Scenario 2 wasn't run. Run Scenario 2 first, then run this scenario again.

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

## Phase 3: Delete & Archive Scenarios

### Scenario 11: Delete Project with curl

**Test:** Delete a project permanently via DELETE endpoint

**Prerequisites:** At least one project exists (run Scenario 1 or 2 first)

```bash
# First, get a project ID to delete
curl http://localhost:5000/api/projects | jq '.[0].id'
# Note the ID (e.g., 1)

# Delete the project
curl -X DELETE http://localhost:5000/api/projects/1 -v

# Expected Response:
# HTTP/1.1 204 No Content
# (No response body)
```

**Verification:**
```bash
# Verify project is deleted
curl http://localhost:5000/api/projects/1
# Expected: {"error": "Project not found"} with 404 status

# Verify project no longer appears in list
curl http://localhost:5000/api/projects | jq '.[] | select(.id == 1)'
# Expected: No results
```

**Expected Result:** ✅ Project deleted, returns 204, cannot be retrieved

---

### Scenario 12: Delete Non-Existent Project with curl

**Test:** DELETE endpoint returns 404 for non-existent project

```bash
curl -X DELETE http://localhost:5000/api/projects/9999 -v

# Expected Response:
# HTTP/1.1 404 Not Found
# {"error": "Project not found"}
```

**Expected Result:** ✅ Returns 404 with error message

---

### Scenario 13: Archive Project with curl

**Test:** Archive a project via PUT /archive endpoint

**Prerequisites:** At least one project exists (run Scenario 1 or 2 first)

```bash
# First, get a project ID to archive
curl http://localhost:5000/api/projects | jq '.[0].id'
# Note the ID (e.g., 2)

# Archive the project
curl -X PUT http://localhost:5000/api/projects/2/archive | jq

# Expected Response:
# {
#   "id": 2,
#   "name": "...",
#   "classification": "archive",
#   "status": "completed",
#   ...
# }
```

**Verification:**
```bash
# Verify project is archived
curl http://localhost:5000/api/projects/2 | jq '.classification, .status'
# Expected: "archive" and "completed"

# Verify archived project still appears in list
curl http://localhost:5000/api/projects | jq '.[] | select(.id == 2)'
# Expected: Project appears with classification="archive" and status="completed"
```

**Expected Result:** ✅ Project archived, classification='archive', status='completed', still in list

---

### Scenario 14: CLI - Delete Project

**Test:** Delete a project using CLI with confirmation

**Prerequisites:** At least one project exists

```bash
# List projects to get an ID
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli
./proj list

# Delete project (will prompt for confirmation)
./proj delete 3

# Expected Output:
# Warning: This will permanently delete project #3: Project Name
# Are you sure you want to delete this project? [y/N]: y
# ✓ Deleted project #3: Project Name
```

**Test with --yes flag:**
```bash
./proj delete 4 --yes

# Expected Output:
# ✓ Deleted project #4: Project Name
# (No confirmation prompt)
```

**Verification:**
```bash
# Verify project is deleted
./proj get 3
# Expected: Error: Project not found
```

**Expected Result:** ✅ Delete command works, shows confirmation, deletes project

---

### Scenario 15: CLI - Archive Project

**Test:** Archive a project using CLI

**Prerequisites:** At least one project exists

```bash
# List projects to get an ID
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli
./proj list

# Archive project
./proj archive 5

# Expected Output:
# ✓ Archived project #5: Project Name
#          Archived Project         
# ┌────────────────┬──────────────────┐
# │             ID │ 5                │
# │           Name │ Project Name      │
# │ Classification │ archive           │
# │         Status │ completed         │
# │        Updated │ 2025-12-03 21:15 │
# └────────────────┴──────────────────┘
```

**Verification:**
```bash
# Verify project is archived
./proj get 5
# Expected: Shows project with classification="archive" and status="completed"
```

**Expected Result:** ✅ Archive command works, displays archived project details

---

## ✅ Acceptance Criteria

Mark these as complete after testing:

### API Functionality
- [ ] POST /api/projects creates projects with minimal data
- [ ] POST /api/projects creates projects with full data
- [ ] PATCH /api/projects/<id> updates projects (partial updates work)
- [ ] DELETE /api/projects/<id> deletes projects (returns 204)
- [ ] PUT /api/projects/<id>/archive archives projects
- [ ] Validation rejects invalid classification values
- [ ] Validation rejects invalid status values
- [ ] Duplicate path detection works (409 Conflict)
- [ ] 404 returned for non-existent projects

### CLI Functionality
- [ ] `proj create` command works with all options
- [ ] `proj update` command works with partial updates
- [ ] `proj delete` command works with confirmation
- [ ] `proj archive` command works
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

