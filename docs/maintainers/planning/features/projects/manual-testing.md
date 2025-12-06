# Projects Feature Manual Testing Guide

**Phases:** Phase 2, Phase 3, Phase 4, Phase 5 & Phase 6 - Create, Update, Delete, Archive, Search & Filter, Import, CLI Enhancement  
**Phase 5 (PR #16):** Import functionality - Scenarios 29-33  
**Phase 6 (PR #24):** CLI Enhancement & Daily Use Tools - Scenarios 38-45  
**Phase 7 (PR #29):** Automated Testing & Bug Fixes - No new user-facing features (test coverage, documentation, code quality improvements only)  
**Fixes:**

- PR #17 - Request body validation improvements (Scenarios 34-37)
- PR #18 - CLI table display improvements (Scenario 24 updated, Scenario 27a added)
- PR #19 - Test expectations tightened for invalid filter values (test-only, no manual testing scenarios needed)
- PR #20 - Test quality improvements (test-only, no manual testing scenarios needed)
- PR #21 - Quick wins batch 2 - code quality improvements (test-only, no manual testing scenarios needed)
- PR #22 - Code refactoring - extract helpers (test-only, no manual testing scenarios needed)
- PR #25 - Bug risk fixes - guard invalid config, fix health URL, use .get() for path (Scenarios 47-49)
- PR #27 - Configuration improvements - use configured URLs, show defaults (Scenarios 50-51)
- PR #28 - Error handler improvements - extract health URL helper, validate URLs (Scenarios 52-55)
- PR #29 - Phase 7: Test coverage improvements, API/user documentation, code quality (test-only, documentation-only, no manual testing scenarios needed)
- PR #30 - Bulk import IntegrityError handling - per-project error handling (Scenario 56)  
  **Last Updated:** 2025-12-06  
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

## Phase 4: Search & Filter Scenarios

### Scenario 16: Filter Projects by Status (API)

**Test:** Filter projects using status query parameter

**Prerequisites:** At least 2 projects with different statuses

```bash
# Create projects with different statuses first (if needed)
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Active Project", "status": "active"}'

curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Paused Project", "status": "paused"}'

# Filter by active status
curl "http://localhost:5000/api/projects?status=active" | jq
# Expected: Only projects with status="active" returned
```

**Verification:**

```bash
# Verify only active projects returned
curl "http://localhost:5000/api/projects?status=active" | jq '.[] | .status'
# Expected: All values are "active"
```

**Expected Result:** ✅ Filter returns only projects matching status

---

### Scenario 17: Filter Projects by Organization (API)

**Test:** Filter projects using organization query parameter

**Prerequisites:** At least 2 projects with different organizations

```bash
# Create projects with different organizations (if needed)
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Work Project", "organization": "work"}'

curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Personal Project", "organization": "personal"}'

# Filter by work organization
curl "http://localhost:5000/api/projects?organization=work" | jq
# Expected: Only projects with organization="work" returned
```

**Verification:**

```bash
# Verify only work projects returned
curl "http://localhost:5000/api/projects?organization=work" | jq '.[] | .organization'
# Expected: All values are "work"
```

**Expected Result:** ✅ Filter returns only projects matching organization

---

### Scenario 18: Filter Projects by Classification (API)

**Test:** Filter projects using classification query parameter

**Prerequisites:** At least 2 projects with different classifications

```bash
# Create projects with different classifications (if needed)
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Primary Project", "classification": "primary"}'

curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Secondary Project", "classification": "secondary"}'

# Filter by primary classification
curl "http://localhost:5000/api/projects?classification=primary" | jq
# Expected: Only projects with classification="primary" returned
```

**Verification:**

```bash
# Verify only primary projects returned
curl "http://localhost:5000/api/projects?classification=primary" | jq '.[] | .classification'
# Expected: All values are "primary"
```

**Expected Result:** ✅ Filter returns only projects matching classification

---

### Scenario 19: Multiple Filters Combined (API)

**Test:** Combine multiple filters with AND logic

**Prerequisites:** Projects with various combinations of status, organization, and classification

```bash
# Create test projects (if needed)
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Work Active Primary", "status": "active", "organization": "work", "classification": "primary"}'

curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Work Active Secondary", "status": "active", "organization": "work", "classification": "secondary"}'

curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Work Paused Primary", "status": "paused", "organization": "work", "classification": "primary"}'

# Filter by status AND organization AND classification
curl "http://localhost:5000/api/projects?status=active&organization=work&classification=primary" | jq
# Expected: Only projects matching ALL filters returned
```

**Verification:**

```bash
# Verify all filters applied
curl "http://localhost:5000/api/projects?status=active&organization=work&classification=primary" | jq '.[] | {status, organization, classification}'
# Expected: All projects have status="active", organization="work", classification="primary"
```

**Expected Result:** ✅ Multiple filters combine correctly with AND logic

---

### Scenario 20: Text Search in Names (API)

**Test:** Search for projects by name using text search

**Prerequisites:** Projects with various names

```bash
# Create test projects (if needed)
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Productivity Tool", "description": "A tool for work"}'

curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Product Manager", "description": "Manager role"}'

curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Personal Blog", "description": "My blog"}'

# Search for "product" in names
curl "http://localhost:5000/api/projects?search=product" | jq
# Expected: Projects with "product" in name or description returned
```

**Verification:**

```bash
# Verify search results
curl "http://localhost:5000/api/projects?search=product" | jq '.[] | .name'
# Expected: All returned projects have "product" in name (case-insensitive)
```

**Expected Result:** ✅ Search finds projects with matching text in names

---

### Scenario 21: Text Search in Descriptions (API)

**Test:** Search for projects by description using text search

**Prerequisites:** Projects with various descriptions

```bash
# Create test projects (if needed)
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Project A", "description": "A productivity tool for work"}'

curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Project B", "description": "A personal blog"}'

curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Project C", "description": "Work tracking system"}'

# Search for "work" in descriptions
curl "http://localhost:5000/api/projects?search=work" | jq
# Expected: Projects with "work" in name or description returned
```

**Verification:**

```bash
# Verify search results include description matches
curl "http://localhost:5000/api/projects?search=work" | jq '.[] | {name, description}'
# Expected: All returned projects have "work" in name or description
```

**Expected Result:** ✅ Search finds projects with matching text in descriptions

---

### Scenario 22: Case-Insensitive Search (API)

**Test:** Verify search is case-insensitive

**Prerequisites:** Projects with mixed-case names

```bash
# Create test projects (if needed)
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Productivity Tool", "description": "A tool"}'

curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "PRODUCTIVITY APP", "description": "An app"}'

curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Productivity System", "description": "A system"}'

# Search with uppercase
curl "http://localhost:5000/api/projects?search=PRODUCTIVITY" | jq
# Expected: All projects with "productivity" (any case) returned
```

**Verification:**

```bash
# Verify case-insensitive matching
curl "http://localhost:5000/api/projects?search=PRODUCTIVITY" | jq '.[] | .name'
# Expected: Projects with "productivity" in any case returned
```

**Expected Result:** ✅ Search is case-insensitive

---

### Scenario 23: Search Combined with Filters (API)

**Test:** Combine text search with filters

**Prerequisites:** Projects with various attributes

```bash
# Create test projects (if needed)
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Work Productivity Tool", "status": "active", "organization": "work"}'

curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Personal Productivity App", "status": "active", "organization": "personal"}'

curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Work Tracker", "status": "paused", "organization": "work"}'

# Search for "productivity" AND filter by status="active" AND organization="work"
curl "http://localhost:5000/api/projects?search=productivity&status=active&organization=work" | jq
# Expected: Only projects matching search AND all filters returned
```

**Verification:**

```bash
# Verify combined search and filters
curl "http://localhost:5000/api/projects?search=productivity&status=active&organization=work" | jq '.[] | {name, status, organization}'
# Expected: All projects have "productivity" in name/description, status="active", organization="work"
```

**Expected Result:** ✅ Search and filters combine correctly with AND logic

---

### Scenario 24: CLI - Filter by Status

**Test:** Use CLI to filter projects by status

**Prerequisites:** At least 2 projects with different statuses

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# Filter by active status (Status column auto-shown - 5 columns)
./proj list --status active

# Expected Output:
# Shows only projects with status="active" in table format
# Table uses full terminal width (expand=True)
# Columns: ID, Name, Status, Path, Created
# Note: Status column automatically visible when filtering by status

# Filter by active status with --wide flag (7 columns)
./proj list --status active --wide

# Expected Output:
# Shows only projects with status="active" in table format
# Table uses full terminal width (expand=True)
# Columns: ID, Name, Status, Org, Classification, Path, Created
# Note: --wide flag shows all columns regardless of filters
```

**Verification:**

```bash
# Verify filtered results (Status column auto-shown)
./proj list --status active
# Check that all displayed projects have status="active"
# Verify Status column is visible (auto-shown when filtering)
# Verify Status column shows "active" for all projects
# Verify table uses full width and columns don't truncate

# Verify filtered results (wide view)
./proj list --status active --wide
# Check that all displayed projects have status="active"
# Verify all 7 columns are visible (--wide shows all)
# Verify Status column shows "active" for all projects
```

**Expected Result:** ✅ CLI filter flag works correctly, Status column auto-shown when filtering, table uses full width, --wide flag shows all columns

---

### Scenario 25: CLI - Filter by Organization

**Test:** Use CLI to filter projects by organization

**Prerequisites:** At least 2 projects with different organizations

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# Filter by work organization (Org column auto-shown - 5 columns)
./proj list --org work

# Expected Output:
# Shows only projects with organization="work" in table format
# Columns: ID, Name, Org, Path, Created
# Note: Org column automatically visible when filtering by organization
```

**Verification:**

```bash
# Verify filtered results
./proj list --org work
# Check that all displayed projects have organization="work"
# Verify Org column is visible (auto-shown when filtering)
# Verify Org column shows "work" for all projects
```

**Expected Result:** ✅ CLI organization filter works correctly, Org column auto-shown when filtering

---

### Scenario 26: CLI - Filter by Classification

**Test:** Use CLI to filter projects by classification

**Prerequisites:** At least 2 projects with different classifications

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# Filter by primary classification (Classification column auto-shown - 5 columns)
./proj list --classification primary

# Expected Output:
# Shows only projects with classification="primary" in table format
# Columns: ID, Name, Classification, Path, Created
# Note: Classification column automatically visible when filtering by classification
```

**Verification:**

```bash
# Verify filtered results
./proj list --classification primary
# Check that all displayed projects have classification="primary"
# Verify Classification column is visible (auto-shown when filtering)
# Verify Classification column shows "primary" for all projects
```

**Expected Result:** ✅ CLI classification filter works correctly, Classification column auto-shown when filtering

---

### Scenario 27a: CLI - Wide View

**Test:** Use CLI with --wide flag to show all columns

**Prerequisites:** Projects with various attributes

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# List all projects with --wide flag
./proj list --wide

# Expected Output:
# Table with 7 columns: ID, Name, Status, Org, Classification, Path, Created
# Table uses full terminal width
# Columns wrap instead of truncate
```

**Verification:**

```bash
# Verify wide view shows all columns
./proj list --wide
# Check that Status, Org, and Classification columns are visible
# Verify table uses full terminal width
# Verify long names/paths wrap instead of truncate

# Compare with default view
./proj list
# Verify default view shows only 4 columns (ID, Name, Path, Created)
# Verify both views use full terminal width
```

**Expected Result:** ✅ --wide flag shows all 7 columns, default view shows 4 columns, filtered columns auto-shown, both use full width

---

### Scenario 27b: CLI - Invalid Status Value (click.Choice Validation)

**Test:** Verify that invalid status values are rejected at CLI level with clear error message

**Prerequisites:** Backend server running

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# Try to use invalid status value
./proj list --status invalid_status

# Expected Output:
# Error: Invalid value for '--status' / '-s': 'invalid_status' is not one of 'active', 'paused', 'completed', 'cancelled'.
# Usage: proj list [OPTIONS]
# Try 'proj list --help' for help.
```

**Verification:**

```bash
# Test with invalid status
./proj list --status invalid_status
# Expected: Error message showing valid choices, exit code != 0

# Test with valid status (should still work)
./proj list --status active
# Expected: Works correctly, shows filtered results
```

**Expected Result:** ✅ Invalid status values rejected at CLI with clear error message showing valid choices

---

### Scenario 27c: CLI - Invalid Classification Value (click.Choice Validation)

**Test:** Verify that invalid classification values are rejected at CLI level with clear error message

**Prerequisites:** Backend server running

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# Try to use invalid classification value
./proj list --classification invalid_class

# Expected Output:
# Error: Invalid value for '--classification' / '-c': 'invalid_class' is not one of 'primary', 'secondary', 'archive', 'maintenance'.
# Usage: proj list [OPTIONS]
# Try 'proj list --help' for help.
```

**Verification:**

```bash
# Test with invalid classification
./proj list --classification invalid_class
# Expected: Error message showing valid choices, exit code != 0

# Test with valid classification (should still work)
./proj list --classification primary
# Expected: Works correctly, shows filtered results
```

**Expected Result:** ✅ Invalid classification values rejected at CLI with clear error message showing valid choices

---

### Scenario 27: CLI - Text Search

**Test:** Use CLI to search projects by name/description

**Prerequisites:** Projects with various names and descriptions

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# Search for "productivity" (Description column auto-shown - 5 columns)
./proj list --search productivity

# Expected Output:
# Shows only projects with "productivity" in name or description
# Columns: ID, Name, Path, Description, Created
# Note: Description column automatically visible when searching to show where match occurred
```

**Verification:**

```bash
# Verify search results
./proj list --search productivity
# Check that all displayed projects have "productivity" in name or description
# Verify Description column is visible (auto-shown when searching)
# Verify you can see where "productivity" appears (in name or description)
```

**Expected Result:** ✅ CLI search flag works correctly, Description column auto-shown when searching to provide context for matches

---

### Scenario 28: CLI - Multiple Filters Combined

**Test:** Use CLI with multiple filter flags

**Prerequisites:** Projects with various combinations of attributes

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# Filter by status AND organization AND search
./proj list --status active --org work --search work

# Expected Output:
# Shows only projects matching ALL filters and search term
```

**Verification:**

```bash
# Verify combined filters
./proj list --status active --org work --search work
# Check that all displayed projects match all criteria
```

**Expected Result:** ✅ CLI multiple filters combine correctly

---

## Phase 5: Import Projects Scenarios

### Scenario 29: API - Import Single Project

**Test:** Import a single project via the API.

**Prerequisites:** Backend server running.

**API Test:**

```bash
curl -X POST http://localhost:5000/api/projects/import \
  -H "Content-Type: application/json" \
  -d '{
    "projects": [
      {
        "name": "Imported Project A",
        "path": "/imported/project/a",
        "remote_url": "http://github.com/imported/project-a",
        "classification": "primary",
        "status": "active"
      }
    ]
  }'
# Expected: {"imported": 1, "skipped": 0, "errors": []}
```

**Verification:**

```bash
curl http://localhost:5000/api/projects | jq '.[] | select(.name == "Imported Project A")'
# Check that "Imported Project A" is in the list
```

**Expected Result:** ✅ API import endpoint successfully imports a single project.

---

### Scenario 30: API - Import Multiple Projects

**Test:** Import multiple projects via the API.

**Prerequisites:** Backend server running.

**API Test:**

```bash
curl -X POST http://localhost:5000/api/projects/import \
  -H "Content-Type: application/json" \
  -d '{
    "projects": [
      {
        "name": "Imported Project B",
        "remote_url": "http://github.com/imported/project-b",
        "classification": "primary",
        "status": "active"
      },
      {
        "name": "Imported Project C",
        "remote_url": "http://github.com/imported/project-c",
        "classification": "secondary",
        "status": "paused"
      }
    ]
  }'
# Expected: {"imported": 2, "skipped": 0, "errors": []}
```

**Verification:**

```bash
curl http://localhost:5000/api/projects | jq '.[] | select(.name | startswith("Imported Project"))'
# Check that both projects are in the list
```

**Expected Result:** ✅ API import endpoint successfully imports multiple projects.

---

### Scenario 31: API - Import Duplicate Handling

**Test:** Import projects with duplicates (same remote_url).

**Prerequisites:** Backend server running. Project with remote_url "http://github.com/imported/duplicate" already exists.

**API Test:**

```bash
# First, create a project manually
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Existing Project",
    "remote_url": "http://github.com/imported/duplicate",
    "classification": "primary",
    "status": "active"
  }'

# Then try to import the same project
curl -X POST http://localhost:5000/api/projects/import \
  -H "Content-Type: application/json" \
  -d '{
    "projects": [
      {
        "name": "Duplicate Project",
        "remote_url": "http://github.com/imported/duplicate",
        "classification": "primary",
        "status": "active"
      }
    ]
  }'
# Expected: {"imported": 0, "skipped": 1, "errors": []}
```

**Verification:**

```bash
curl http://localhost:5000/api/projects | jq '.[] | select(.remote_url == "http://github.com/imported/duplicate")'
# Check that only one project with this remote_url exists
```

**Expected Result:** ✅ Duplicate projects are skipped (not re-imported).

---

### Scenario 32: API - Import Error Handling

**Test:** Import projects with some invalid data.

**Prerequisites:** Backend server running.

**API Test:**

```bash
curl -X POST http://localhost:5000/api/projects/import \
  -H "Content-Type: application/json" \
  -d '{
    "projects": [
      {
        "name": "Valid Project",
        "remote_url": "http://github.com/valid/project",
        "classification": "primary",
        "status": "active"
      },
      {
        "name": "Invalid Project",
        "classification": "invalid_classification",
        "status": "active"
      }
    ]
  }'
# Expected: {"imported": 1, "skipped": 0, "errors": [{"project": "Invalid Project", "error": "..."}]}
```

**Verification:**

```bash
curl http://localhost:5000/api/projects | jq '.[] | select(.name == "Valid Project")'
# Check that only the valid project was imported
```

**Expected Result:** ✅ Valid projects imported, errors reported but import continues.

---

### Scenario 33: CLI - Import Projects

**Test:** Import projects using CLI command.

**Prerequisites:** Backend server running. JSON file with projects data exists.

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# Create a test JSON file
cat > /tmp/test-projects.json << 'EOF'
{
  "projects": [
    {
      "name": "CLI Imported Project",
      "remote_url": "http://github.com/cli/imported",
      "classification": "primary",
      "status": "active"
    }
  ]
}
EOF

# Import using CLI
./proj import /tmp/test-projects.json

# Expected Output:
# Importing 1 project(s) from /tmp/test-projects.json...
# [Rich formatted table showing import statistics]
# ✓ Successfully imported project(s)
```

**Verification:**

```bash
./proj list | grep "CLI Imported Project"
# Check that the imported project appears in the list
```

**Expected Result:** ✅ CLI import command works correctly with Rich formatting.

---

### Scenario 34: API - Import Validation: Missing 'projects' Field

**Test:** Validate that missing 'projects' field returns 400 Bad Request.

**Prerequisites:** Backend server running.

**API Test:**

```bash
curl -X POST http://localhost:5000/api/projects/import \
  -H "Content-Type: application/json" \
  -d '{
    "wrong_key": [
      {"name": "Test Project"}
    ]
  }'
# Expected: 400 Bad Request with {"error": "Missing 'projects' field"}
```

**Verification:**

```bash
# Check response status and error message
curl -X POST http://localhost:5000/api/projects/import \
  -H "Content-Type: application/json" \
  -d '{"wrong_key": []}' -w "\nHTTP Status: %{http_code}\n"
# Expected: HTTP Status: 400
```

**Expected Result:** ✅ Missing 'projects' field returns 400 with clear error message.

---

### Scenario 35: API - Import Validation: Non-Dict Request Body

**Test:** Validate that non-dict request body returns 400 Bad Request.

**Prerequisites:** Backend server running.

**API Test:**

```bash
curl -X POST http://localhost:5000/api/projects/import \
  -H "Content-Type: application/json" \
  -d '["not", "a", "dict"]'
# Expected: 400 Bad Request with {"error": "Request body must be a JSON object"}
```

**Verification:**

```bash
# Check response status and error message
curl -X POST http://localhost:5000/api/projects/import \
  -H "Content-Type: application/json" \
  -d '["not", "a", "dict"]' -w "\nHTTP Status: %{http_code}\n"
# Expected: HTTP Status: 400
```

**Expected Result:** ✅ Non-dict request body returns 400 with clear error message.

---

### Scenario 36: API - Import Validation: Non-List 'projects' Field

**Test:** Validate that non-list 'projects' field returns 400 Bad Request.

**Prerequisites:** Backend server running.

**API Test:**

```bash
curl -X POST http://localhost:5000/api/projects/import \
  -H "Content-Type: application/json" \
  -d '{
    "projects": "not a list"
  }'
# Expected: 400 Bad Request with {"error": "'projects' field must be a list"}
```

**Verification:**

```bash
# Check response status and error message
curl -X POST http://localhost:5000/api/projects/import \
  -H "Content-Type: application/json" \
  -d '{"projects": "not a list"}' -w "\nHTTP Status: %{http_code}\n"
# Expected: HTTP Status: 400
```

**Expected Result:** ✅ Non-list 'projects' field returns 400 with clear error message.

---

### Scenario 37: API - Import Validation: Non-JSON Content-Type

**Test:** Validate that non-JSON Content-Type returns 400 Bad Request.

**Prerequisites:** Backend server running.

**API Test:**

```bash
curl -X POST http://localhost:5000/api/projects/import \
  -H "Content-Type: text/plain" \
  -d 'not json'
# Expected: 400 Bad Request with {"error": "Content-Type must be application/json"}
```

**Verification:**

```bash
# Check response status and error message
curl -X POST http://localhost:5000/api/projects/import \
  -H "Content-Type: text/plain" \
  -d 'not json' -w "\nHTTP Status: %{http_code}\n"
# Expected: HTTP Status: 400
```

**Expected Result:** ✅ Non-JSON Content-Type returns 400 with clear error message.

---

## Phase 6: CLI Enhancement & Daily Use Tools

**PR:** #24  
**Scenarios:** 38-46  
**Features:** Configuration file, convenience commands, error handling, progress indicators, help system

---

### Scenario 38: CLI - Configuration Show

**Test:** Display current configuration settings

**Prerequisites:**

- CLI installed and working
- Optional: Configuration file exists at `~/.projrc`

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli
./proj config show
```

**Expected:**

- Displays configuration in a formatted table
- Shows sections: `api`, `display`
- Shows keys: `base_url`, `max_rows`, `color`
- Shows current values or defaults
- Displays configuration file path at bottom

**Verification:**

- [ ] Table displays correctly with Rich formatting
- [ ] All sections and keys shown
- [ ] Values are readable
- [ ] Configuration file path shown

**Expected Result:** ✅ Configuration displayed in formatted table with all settings visible

---

### Scenario 39: CLI - Configuration Set

**Test:** Set a configuration value

**Prerequisites:**

- CLI installed and working
- Backend server running (for verification)

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli
./proj config set display max_rows 100
./proj config show
```

**Expected:**

- First command: Shows success message "✓ Set display.max_rows = 100"
- Second command: Shows updated value in configuration table
- Value persists in `~/.projrc` file

**Verification:**

```bash
# Check config file directly
cat ~/.projrc
# Expected: Contains [display] section with max_rows = 100
```

**Verification:**

- [ ] Success message displayed
- [ ] Value updated in config show
- [ ] Value saved to `~/.projrc` file
- [ ] File format is valid INI

**Expected Result:** ✅ Configuration value set successfully and persisted to file

---

### Scenario 40: CLI - Configuration Get

**Test:** Get a specific configuration value

**Prerequisites:**

- CLI installed and working
- Configuration set (from Scenario 39)

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli
./proj config get display max_rows
```

**Expected:**

- Displays: `display.max_rows = 100` (or current value)
- Single line output with section.key = value format

**Verification:**

- [ ] Correct value displayed
- [ ] Format is `section.key = value`
- [ ] Works for all configuration keys

**Expected Result:** ✅ Configuration value retrieved and displayed correctly

---

### Scenario 41: CLI - Stats Command

**Test:** Display project statistics

**Prerequisites:**

- Backend server running
- At least some projects in database

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli
./proj stats
```

**Expected:**

- Shows "Project Statistics" header
- Displays total project count
- Shows breakdown by status (active, paused, completed, cancelled) with symbols
- Shows breakdown by organization (sorted by count)
- Shows breakdown by classification (primary, secondary, archive, maintenance) with symbols
- Uses Rich formatting with colors and symbols

**Verification:**

- [ ] Total count matches actual projects
- [ ] Status breakdown shows correct counts
- [ ] Organization breakdown shows correct counts
- [ ] Classification breakdown shows correct counts
- [ ] Formatting is readable and well-organized
- [ ] Spinner shows "Calculating statistics..." during fetch

**Expected Result:** ✅ Statistics displayed correctly with accurate counts and Rich formatting

---

### Scenario 42: CLI - Recent Command

**Test:** Display recently updated projects

**Prerequisites:**

- Backend server running
- At least some projects in database

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli
./proj recent
./proj recent --limit 5
```

**Expected:**

- First command: Shows 10 most recently updated projects (default limit)
- Second command: Shows 5 most recently updated projects
- Displays projects in table format (using build_projects_table with wide=True)
- Shows all columns (ID, Name, Status, Org, Classification, Path, Description, Created)
- Projects sorted by created_at (most recent first)
- Spinner shows "Fetching recent projects..." during fetch

**Verification:**

- [ ] Default limit is 10 projects
- [ ] Custom limit works correctly
- [ ] Projects sorted correctly (most recent first)
- [ ] Table shows all columns
- [ ] Formatting is correct

**Expected Result:** ✅ Recent projects displayed correctly with proper limit and sorting

---

### Scenario 43: CLI - Active Command

**Test:** Display active projects (shortcut for `proj list --status active`)

**Prerequisites:**

- Backend server running
- At least some active projects in database

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli
./proj active
./proj active --wide
```

**Expected:**

- First command: Shows only active projects
- Second command: Shows active projects with all columns (wide view)
- Filters by status='active' automatically
- Table shows Status column (since status filter is used)
- Spinner shows "Fetching active projects..." during fetch

**Verification:**

- [ ] Only active projects shown
- [ ] Status column visible
- [ ] Wide flag works correctly
- [ ] Equivalent to `proj list --status active`

**Expected Result:** ✅ Active projects displayed correctly with proper filtering

---

### Scenario 44: CLI - Mine Command

**Test:** Display projects for current user/organization

**Prerequisites:**

- Backend server running
- At least some projects with organization='work' (or set PROJ_ORG env var)

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli
# Test with default (PROJ_ORG env var or "work")
./proj mine
# Test with explicit org
./proj mine --org learning
./proj mine --org work --wide
```

**Expected:**

- First command: Shows projects for default organization (PROJ_ORG or "work")
- Second command: Shows projects for "learning" organization
- Third command: Shows projects for "work" with wide view
- Filters by organization automatically
- Table shows Org column (since organization filter is used)
- Spinner shows "Fetching projects for [org]..." during fetch

**Verification:**

- [ ] Default organization works (PROJ_ORG or "work")
- [ ] Explicit org flag works
- [ ] Only projects for specified org shown
- [ ] Org column visible
- [ ] Wide flag works correctly

**Expected Result:** ✅ Organization-filtered projects displayed correctly with proper defaults

---

### Scenario 45: CLI - Error Handling (Backend Down)

**Test:** Verify friendly error messages when backend is unavailable

**Prerequisites:**

- Backend server NOT running
- CLI installed and working

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli
# Stop backend server if running
./proj list
./proj stats
./proj get 1
```

**Expected:**

- All commands show friendly error messages
- Error message includes:
  - Clear title: "Backend Connection Failed"
  - Possible reasons listed (server not running, incorrect URL, network issues)
  - Troubleshooting steps:
    - Start backend server command
    - Verify server command
    - Check API URL command
    - Set API URL via env var command
- Error displayed in Rich Panel with red border
- Technical details shown at bottom (dimmed)

**Verification:**

- [ ] Error message is user-friendly
- [ ] Troubleshooting steps are actionable
- [ ] Formatting is clear (Rich Panel)
- [ ] Technical details available but not overwhelming
- [ ] Same error handling for all commands

**Expected Result:** ✅ Friendly error messages displayed with clear troubleshooting steps

---

### Scenario 46: CLI - Help System

**Test:** Verify comprehensive help text for all commands

**Prerequisites:**

- CLI installed and working

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli
./proj --help
./proj list --help
./proj config --help
./proj stats --help
./proj recent --help
./proj active --help
./proj mine --help
```

**Expected:**

- Main help (`./proj --help`):
  - Shows quick start guide
  - Lists common commands
  - Shows configuration information
  - Includes examples
- Command help (`./proj [command] --help`):
  - Detailed description
  - All options listed with descriptions
  - Examples included
  - Valid values shown for choices

**Verification:**

- [ ] Main help is comprehensive
- [ ] All commands have detailed help
- [ ] Options are documented
- [ ] Examples are provided
- [ ] Help text is readable and formatted well

**Expected Result:** ✅ Comprehensive help text available for all commands with examples

---

## PR #25: Bug Risk Fixes

**Features:** Guard invalid config values, fix health URL construction, use .get() for path

### Scenario 47: CLI - Invalid Config Value Handling

**Test:** Verify CLI doesn't crash with invalid `display.max_rows` config value

**Prerequisites:**

- CLI installed and working
- Configuration file exists at `~/.projrc`

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# Set invalid config value (non-numeric)
./proj config set display max_rows invalid_value

# Try to use CLI command that uses max_rows (list command)
./proj list

# Expected: CLI doesn't crash, uses default value (50)
```

**Verification:**

- [x] CLI doesn't crash with invalid `max_rows` value
- [x] CLI uses default value (50) when config is invalid
- [x] No error message shown (graceful fallback)

**Expected Result:** ✅ CLI handles invalid config values gracefully without crashing

---

### Scenario 48: CLI - Health URL Construction

**Test:** Verify health check works with various base URL formats

**Prerequisites:**

- CLI installed and working
- Backend server running
- Can set custom API URL via environment variable

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# Test 1: Default URL (with /api, no trailing slash)
export PROJ_API_URL=http://localhost:5000/api
./proj list
# Expected: Works correctly, health check succeeds at http://localhost:5000/api/health

# Test 2: URL with trailing slash (should be stripped)
export PROJ_API_URL=http://localhost:5000/api/
./proj list
# Expected: Works correctly, health URL constructed as http://localhost:5000/api/health
# The rstrip('/') removes trailing slash before appending /health
```

**Verification:**

- [x] Health check works with default URL format (no trailing slash)
- [x] Health check works with URL with trailing slash (stripped correctly)
- [x] Health URL constructed correctly using `rstrip('/') + '/health'` pattern
- [x] No brittle string replacement (old `replace('/api', '/api/health')` was removed)

**Note:** The fix replaces the brittle `base_url.replace('/api', '/api/health')` with explicit path construction (`base_url.rstrip('/') + '/health'`), which works robustly with any base URL format. Testing with a non-existent custom path (like `/custom/api`) will always fail because the backend isn't running at that path - the test verifies the URL construction logic works correctly for realistic URL variations.

**Expected Result:** ✅ Health URL construction works robustly with various base URL formats (with/without trailing slash)

---

### Scenario 49: CLI - Missing Path Key Handling

**Test:** Verify CLI handles missing path key gracefully

**Prerequisites:**

- CLI installed and working
- Backend server running
- Projects exist in database

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# List projects (should handle missing path key if API response structure changes)
./proj list

# Expected: CLI doesn't crash if path key is missing from project dict
# Should display 'N/A' for missing path values
```

**Verification:**

- [x] CLI doesn't crash if path key is missing
- [x] Missing path displays as 'N/A'
- [x] Other fields still display correctly
- [x] No KeyError exceptions

**Note:** This is a defensive fix - testing requires simulating API response without path key, which is difficult. The fix ensures CLI won't crash if API structure changes in the future. Code review confirms `.get()` is used correctly.

**Expected Result:** ✅ CLI handles missing path key gracefully using .get() instead of direct dictionary access

---

## PR #27: Configuration Improvements

**Features:** Use configured URLs in error messages, show config defaults in config show

### Scenario 50: CLI - Config Show Displays Defaults

**Test:** Verify `proj config show` displays default values even when not in config file

**Prerequisites:**

- CLI installed and working
- Configuration file may or may not exist

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# Remove config file if it exists (to test defaults)
rm -f ~/.projrc

# Show configuration (should show defaults)
./proj config show

# Set one value
./proj config set display max_rows 100

# Show configuration again (should show defaults + override)
./proj config show
```

**Expected:**

- First `config show`: Displays all default values (api.base_url, display.max_rows, display.color)
- After setting max_rows: Shows default values PLUS the override (max_rows = 100)
- All sections and keys visible, including defaults not in config file

**Verification:**

- [x] Default values displayed when config file doesn't exist
- [x] Default values displayed when config file exists but doesn't have all keys
- [x] User overrides take precedence over defaults
- [x] All sections (api, display) shown
- [x] All keys shown (base_url, max_rows, color)

**Expected Result:** ✅ Config show displays effective configuration (defaults + overrides)

---

### Scenario 51: CLI - Error Messages Use Configured URLs

**Test:** Verify error messages show actual configured API URL, not hardcoded localhost

**Prerequisites:**

- CLI installed and working
- Backend server NOT running
- Can set custom API URL via environment variable

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# Test with default URL (localhost:5000)
./proj list
# Expected: Error message shows http://localhost:5000/api/health

# Set custom API URL via environment variable
export PROJ_API_URL=http://custom-server:8080/api
./proj list
# Expected: Error message shows http://custom-server:8080/api/health

# Set custom API URL via config file
unset PROJ_API_URL
./proj config set api base_url http://another-server:9000/api
./proj list
# Expected: Error message shows http://another-server:9000/api/health
```

**Expected:**

- Error messages show the actual configured API URL (not hardcoded localhost)
- Health URL is constructed correctly from configured base URL
- Troubleshooting steps show correct URLs
- Works with environment variable override
- Works with config file setting

**Verification:**

- [x] Error message shows configured URL (not hardcoded)
- [x] Health URL constructed correctly from base URL
- [x] Environment variable override reflected in error messages
- [x] Config file setting reflected in error messages
- [x] URL construction handles trailing slashes correctly

**Expected Result:** ✅ Error messages show actual configured URLs for accurate troubleshooting

---

## PR #28: Error Handler Improvements

**Features:** Extract health URL helper function, add URL validation with fallback

### Scenario 52: CLI - Error Handler Uses Health URL Helper

**Test:** Verify error handlers use centralized health URL helper function

**Prerequisites:**

- CLI installed and working
- Backend server NOT running
- Default configuration

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# Test connection error (backend down)
./proj list
# Expected: Error message shows health URL constructed correctly

# Test timeout error (if backend is slow/unresponsive)
# Note: This may require simulating a timeout, or can be verified by code inspection
```

**Expected:**

- Error messages show health URL constructed correctly
- Health URL is consistent across all error handlers
- URL format is correct (base URL + /health)
- No hardcoded URLs in error messages

**Verification:**

- [ ] Connection error shows correct health URL
- [ ] Health URL is constructed from configured base URL
- [ ] URL format is consistent (no trailing slashes issues)
- [ ] Error messages are helpful and actionable

**Expected Result:** ✅ Error handlers use centralized helper for consistent URL construction

---

### Scenario 53: CLI - Error Handler Handles Empty URL Configuration

**Test:** Verify error handler falls back to default URL when configured URL is empty

**Prerequisites:**

- CLI installed and working
- Backend server NOT running
- Can modify configuration

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# Set empty URL in config
./proj config set api base_url ""

# Try to use CLI (should use default URL)
./proj list

# Expected: Error message shows default URL (http://localhost:5000/api/health)
# Not: Error message shows empty or invalid URL
```

**Expected:**

- Empty URL configuration doesn't cause errors
- Error handler falls back to default URL
- Error message shows valid default health URL
- No unusable curl commands (like `curl /health`)

**Verification:**

- [x] Empty URL doesn't cause crash
- [x] Default URL is used (http://localhost:5000/api/health)
- [x] Error message shows valid health URL
- [x] Troubleshooting steps are still helpful

**Expected Result:** ✅ Error handler gracefully handles empty URL with default fallback

---

### Scenario 54: CLI - Error Handler Handles Invalid URL Format

**Test:** Verify error handler falls back to default URL when configured URL has invalid format

**Prerequisites:**

- CLI installed and working
- Backend server NOT running
- Can modify configuration

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# Set invalid URL format (missing http://)
./proj config set api base_url "localhost:5000/api"

# Try to use CLI (should use default URL)
./proj list

# Expected: Error message shows default URL (http://localhost:5000/api/health)
# Not: Error message shows invalid URL format
```

**Expected:**

- Invalid URL format doesn't cause errors
- Error handler validates URL format (must start with http:// or https://)
- Falls back to default URL if format is invalid
- Error message shows valid health URL

**Verification:**

- [x] Invalid URL format doesn't cause crash
- [x] URL format is validated (checks for http:// or https://)
- [x] Default URL is used when format is invalid
- [x] Error message shows valid health URL
- [x] No unusable curl commands

**Expected Result:** ✅ Error handler validates URL format and falls back to default when invalid

---

### Scenario 55: CLI - Error Handler Consistency Across All Handlers

**Test:** Verify all error handlers use the same health URL helper function

**Prerequisites:**

- CLI installed and working
- Backend server NOT running
- Custom API URL configured

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/work-prod/scripts/project_cli

# Set custom API URL
./proj config set api base_url "http://custom-server:8080/api"

# Test different error scenarios
# Connection error
./proj list
# Expected: Shows http://custom-server:8080/api/health

# Timeout error (if backend is slow/unresponsive)
# Note: May require simulating timeout or code inspection

# Generic error (if backend returns unexpected error)
# Note: May require simulating error or code inspection
```

**Expected:**

- All error handlers show consistent health URL
- Health URL is constructed from same configured base URL
- URL format is consistent across all handlers
- No duplication of URL construction logic

**Verification:**

- [x] Connection error handler uses helper
- [x] Timeout error handler uses helper
- [x] Generic error handler uses helper
- [x] All handlers show same health URL format
- [x] URL construction is centralized (no duplication)

**Expected Result:** ✅ All error handlers use centralized helper for consistent behavior

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
- [ ] POST /api/projects/import imports projects successfully
- [ ] Import duplicate detection works (skips duplicates)
- [ ] Import error handling works (reports errors but continues)
- [ ] Import validation rejects missing 'projects' field (400)
- [ ] Import validation rejects non-dict request body (400)
- [ ] Import validation rejects non-list 'projects' field (400)
- [ ] Import validation rejects non-JSON Content-Type (400)

### CLI Functionality

- [ ] `proj create` command works with all options
- [ ] `proj update` command works with partial updates
- [ ] `proj delete` command works with confirmation
- [ ] `proj archive` command works
- [ ] `proj import` command works with JSON files
- [ ] `proj list` shows all projects in table format
- [ ] `proj list --wide` shows all columns including Description (Status, Org, Classification, Description)
- [ ] `proj list --status X` auto-shows Status column (5 columns)
- [ ] `proj list --org X` auto-shows Org column (5 columns)
- [ ] `proj list --classification X` auto-shows Classification column (5 columns)
- [ ] `proj list --search X` auto-shows Description column (5 columns) to show where match occurred
- [ ] `proj list` table uses full terminal width (no truncation)
- [ ] `proj list` columns wrap instead of truncate
- [ ] CLI validates status values (click.Choice - rejects invalid)
- [ ] CLI validates classification values (click.Choice - rejects invalid)
- [ ] `proj get` shows project details
- [ ] Error messages are clear and helpful
- [ ] Rich formatting displays correctly
- [ ] `proj config show` displays configuration in formatted table
- [ ] `proj config set` updates configuration and persists to file
- [ ] `proj config get` retrieves specific configuration values
- [ ] `proj stats` displays project statistics with breakdowns
- [ ] `proj recent` shows recently updated projects with limit option
- [ ] `proj active` filters and displays active projects
- [ ] `proj mine` filters and displays projects for user's organization
- [ ] Error handling shows friendly messages when backend is down
- [ ] Progress indicators (spinners) show during API calls
- [ ] Help system (`--help`) is comprehensive for all commands

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
| ------- | ----------- | -------- | ------ |
| 1       |             |          |        |
| 2       |             |          |        |

---

## 📝 Test Results Summary

**Testing Completed:** [ ] Pending  
**Date Tested:** [Pending]  
**Tester:** User verification before PR merge

**Overall Result:**

- [ ] ✅ All tests passed - Ready for PR
- [ ] ⚠️ Minor issues found - Fix before PR
- [ ] ❌ Major issues found - Requires rework

**Notes:**

- Phase 5 scenarios (29-33) all tested and verified
- Import endpoint working correctly
- Duplicate detection working (skips by remote_url)
- Error handling working (reports errors but continues)
- CLI import command working (Rich formatting displays correctly)
- Import statistics verified: 48 projects imported successfully
- **Phase 6 scenarios (38-46) added - pending testing**
- **PR #25 scenarios (47-49) tested and verified ✅**
- **PR #29 (Phase 7): No new user-facing features - automated tests, documentation, and code quality improvements only. No manual testing scenarios needed.**

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
