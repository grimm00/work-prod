# PR #38 Fix Tracking

**PR:** #38 - chore: Remove CLI and inventory scripts migrated to proj-cli  
**Type:** Chore (Cleanup)  
**Merged:** 2025-12-23  
**Status:** ✅ Complete

---

## 📋 Overview

This PR removed the CLI and inventory scripts from work-prod that were migrated to the proj-cli repository.

---

## 📋 Deferred Issues

**Date:** 2025-12-23  
**Review:** PR #38 Sourcery feedback  
**Status:** 🟡 **DEFERRED** - All LOW/MEDIUM priority documentation issues

**Deferred Issues:**

| ID | Issue | Priority | Effort | Notes |
|----|-------|----------|--------|-------|
| PR38-#1 | API URL consistency | 🟢 LOW | 🟢 LOW | README documents `PROJ_API_URL` without `/api` suffix while API paths use `/api`; consider standardizing |
| PR38-#2 | Version pinning | 🟡 MEDIUM | 🟢 LOW | Installation examples use unpinned `git+https` URL; defer until PyPI publish |

**Action Plan:** These are documentation improvements that can be addressed:
- PR38-#1: Can be fixed opportunistically in any future docs update
- PR38-#2: Should be addressed when proj-cli is published to PyPI

---

## 📊 Summary

| Category | Count |
|----------|-------|
| Individual Comments | 0 |
| Overall Comments | 2 |
| CRITICAL/HIGH | 0 |
| MEDIUM/LOW Deferred | 2 |

---

## 🔗 Related

- [Sourcery Review](../../../../feedback/sourcery/pr38.md)
- [Feature Hub](../../README.md)
- [Fix Hub](../README.md)

---

**Last Updated:** 2025-12-23


