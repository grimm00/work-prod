# End-to-End Tests

**Purpose:** Full-stack integration tests using Playwright  
**Status:** 🔴 Not Started (Deferred - Phase 7 Complete, E2E tests deferred)  
**Last Updated:** 2025-12-07

---

## 📋 Overview

This directory contains **end-to-end (E2E) tests** that verify complete user workflows across both backend and frontend. These tests use **Playwright** for cross-browser testing.

**Note:** Unit and integration tests live with their respective codebases:

- **Backend tests:** `backend/tests/` (pytest)
- **Frontend tests:** `frontend/src/components/*.test.jsx` (Vitest)

See [ADR-0006: Testing Framework and TDD Approach](../docs/maintainers/decisions/ADR-0006-testing-framework-and-tdd-approach.md) for the complete testing strategy.

---

## 🎯 Testing Strategy

### Current Test Organization

1. **Backend Tests** (`backend/tests/`)

   - Unit tests for models and services
   - Integration tests for API endpoints
   - Framework: pytest + pytest-flask
   - Coverage: >80% target

2. **Frontend Tests** (`frontend/src/`)

   - Component tests (colocated with components)
   - Store tests (colocated with stores)
   - Framework: Vitest + React Testing Library
   - Coverage: >75% target

3. **E2E Tests** (`tests/e2e/`) - **This Directory**
   - Full user workflows across backend + frontend
   - Framework: Playwright
   - Cross-browser: Chromium, Firefox, WebKit
   - Status: Planned for Phase 7

---

## 📁 Planned Directory Structure

```
tests/
└── e2e/
    ├── projects/           # Projects feature E2E tests
    │   ├── list.spec.js
    │   ├── create.spec.js
    │   ├── update.spec.js
    │   └── delete.spec.js
    ├── fixtures/           # Shared test data
    ├── utils/              # Test helpers
    └── playwright.config.js
```

---

## 🚀 When to Add E2E Tests

E2E tests were planned for **Phase 7: Automated Testing & Bug Fixes** but were deferred in favor of comprehensive unit and integration test coverage.

**Current Status:**
- ✅ All features implemented (Phases 1-8)
- ✅ Unit and integration tests passing (97% coverage, 214 tests)
- ✅ Manual testing complete
- ✅ Critical user flows verified
- 🔴 E2E tests deferred (not critical for MVP)

E2E tests are slower and more brittle, so we focused on unit/integration tests first. E2E tests may be added in future releases if needed.

---

## 🔗 Related Documents

- [ADR-0006: Testing Framework and TDD Approach](../docs/maintainers/decisions/ADR-0006-testing-framework-and-tdd-approach.md)
- [Testing Strategy Research](../docs/maintainers/research/tech-stack/testing-strategy.md)
- [Backend Tests](../backend/tests/)
- [Phase 7: Manual Testing](../docs/maintainers/planning/features/projects/phase-7.md)

---

**Last Updated:** 2025-12-07  
**Status:** 🔴 Not Started (Deferred - MVP Complete)  
**Next:** E2E tests may be added in future releases if needed
