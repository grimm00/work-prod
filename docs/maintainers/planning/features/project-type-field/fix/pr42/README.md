# PR #42 - Deferred Issues

**Feature:** Project Type Field  
**Phase:** 3 (API Updates)  
**PR:** #42  
**Date:** 2025-12-29  
**Status:** 🟡 **DEFERRED** - All issues are LOW priority and can be handled opportunistically.

---

## 📋 Overview

This document lists the LOW priority issues identified during the Sourcery code review for PR #42. These issues were deemed non-critical and have been deferred to be addressed in future development cycles or dedicated refactoring efforts.

---

## 📝 Deferred Issues

### PR42-#1: Parametrize Test for All project_type Values

- **Source:** Sourcery Comment #1
- **Location:** `backend/tests/integration/api/test_projects.py:903-912`
- **Priority:** 🟢 LOW
- **Impact:** 🟢 LOW (Test coverage enhancement)
- **Effort:** 🟢 LOW (Simple pytest parametrization)
- **Description:** Test only uses `project_type=Work` while the implementation defines all four valid types. Consider parametrizing the test over all valid values or adding dedicated tests for each type. Also add case-sensitivity check.
- **Action:** Defer to a future test enhancement task.

### PR42-Overall-#1: Centralize VALID_PROJECT_TYPES Constant

- **Source:** Sourcery Overall Comment #1
- **Location:** `backend/app/api/projects.py` and `backend/openapi.yaml`
- **Priority:** 🟢 LOW
- **Impact:** 🟡 MEDIUM (DRY principle, prevents drift)
- **Effort:** 🟡 MEDIUM (Create shared module, update imports)
- **Description:** The list of valid project types is duplicated between `VALID_PROJECT_TYPES` in the API code and the enums in `openapi.yaml`. Consider centralizing these values to avoid drift.
- **Action:** Defer to a future code quality initiative.

### PR42-Overall-#2: Structured Error Response

- **Source:** Sourcery Overall Comment #2
- **Location:** `backend/app/api/projects.py`
- **Priority:** 🟢 LOW
- **Impact:** 🟢 LOW (API consistency)
- **Effort:** 🟡 MEDIUM (Would require updating all error responses)
- **Description:** For the `project_type` 400 error response, consider adding a structured error code or type field in addition to the human-readable error message.
- **Action:** Defer - broader API error handling standardization consideration.

---

## 🚀 Next Steps

- These issues will be reviewed periodically and addressed as part of general code quality improvements or when relevant code sections are being modified.

---

**Last Updated:** 2025-12-29

