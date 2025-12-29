# Manual Testing Guide - Project Type Field

**Feature:** Project Type Field  
**Phases Covered:** 1, 2, 3  
**Last Updated:** 2025-12-29  
**Status:** ✅ Active

---

## 📋 Overview

This guide provides step-by-step instructions for manually verifying the `project_type` field feature. These tests are designed for **human testers** to validate functionality beyond what automated tests cover.

**Purpose:**
- Verify API filtering by `project_type` works correctly
- Test combined filters (`project_type` + other filters)
- Validate error handling for invalid `project_type` values
- Confirm response includes `project_type` field

**Prerequisites:**
- Backend server running: `cd backend && python run.py`
- Server accessible at `http://localhost:5000`
- Projects exist in database with `project_type` values (backfill completed in Phase 2)

---

## 🧪 Phase 3: API Updates

### Scenario 3.1: Filter by project_type=Work

**Objective:** Verify filtering projects by `project_type=Work` returns only Work projects.

**Steps:**

1. Query projects filtered by `project_type=Work`:
   ```bash
   curl -s http://localhost:5000/api/projects?project_type=Work | python -m json.tool
   ```

2. Verify response:
   - Status code: 200
   - All returned projects have `"project_type": "Work"`
   - No projects with other `project_type` values are returned

**Expected Result:** ✅ Only Work projects returned

---

### Scenario 3.2: Filter by project_type=Personal

**Objective:** Verify filtering projects by `project_type=Personal` returns only Personal projects.

**Steps:**

1. Query projects filtered by `project_type=Personal`:
   ```bash
   curl -s http://localhost:5000/api/projects?project_type=Personal | python -m json.tool
   ```

2. Verify response:
   - Status code: 200
   - All returned projects have `"project_type": "Personal"`

**Expected Result:** ✅ Only Personal projects returned

---

### Scenario 3.3: Invalid project_type returns 400

**Objective:** Verify invalid `project_type` values return a 400 error with clear message.

**Steps:**

1. Query with invalid `project_type`:
   ```bash
   curl -s -w "\n%{http_code}" http://localhost:5000/api/projects?project_type=InvalidType
   ```

2. Verify response:
   - Status code: 400
   - Response contains `error` field
   - Error message mentions valid project types

**Expected Result:** ✅ 400 error with clear message about valid values

---

### Scenario 3.4: Combined filter (project_type + status)

**Objective:** Verify combining `project_type` with other filters works correctly.

**Steps:**

1. Query with combined filters:
   ```bash
   curl -s "http://localhost:5000/api/projects?project_type=Personal&status=active" | python -m json.tool
   ```

2. Verify response:
   - Status code: 200
   - All returned projects have `"project_type": "Personal"` AND `"status": "active"`

**Expected Result:** ✅ Both filters applied correctly

---

### Scenario 3.5: Response includes project_type field

**Objective:** Verify `project_type` field is included in API responses.

**Steps:**

1. Get all projects:
   ```bash
   curl -s http://localhost:5000/api/projects | python -m json.tool | head -30
   ```

2. Get a single project:
   ```bash
   curl -s http://localhost:5000/api/projects/1 | python -m json.tool
   ```

3. Verify each response includes `project_type` field (may be null for some projects)

**Expected Result:** ✅ All project responses include `project_type` field

---

## 🧹 Cleanup

No cleanup required - testing uses existing database state.

---

## ✅ Acceptance Criteria Checklist

### Phase 3: API Updates
- [ ] Scenario 3.1: Filter by project_type=Work
- [ ] Scenario 3.2: Filter by project_type=Personal
- [ ] Scenario 3.3: Invalid project_type returns 400
- [ ] Scenario 3.4: Combined filter (project_type + status)
- [ ] Scenario 3.5: Response includes project_type field

---

## 📝 Notes for Testers

1. All projects should have `project_type` populated after Phase 2 backfill
2. Valid `project_type` values: `Work`, `Personal`, `Learning`, `Inactive`
3. `project_type` is case-sensitive (must match exactly)
4. **Report Issues:** If any scenario fails, document exact steps, expected vs actual results, and error messages.

---

## 🔗 Related Documents

- **Feature Plan:** `docs/maintainers/planning/features/project-type-field/feature-plan.md`
- **Phase 1:** `docs/maintainers/planning/features/project-type-field/phase-1.md` (Schema Migration)
- **Phase 2:** `docs/maintainers/planning/features/project-type-field/phase-2.md` (Data Backfill)
- **Phase 3:** `docs/maintainers/planning/features/project-type-field/phase-3.md` (API Updates)

---

**Last Updated:** 2025-12-29

