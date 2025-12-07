# Testing Strategy Research

**Status:** 🟡 Planned  
**Priority:** High - Prerequisite for MVP implementation  
**Created:** 2025-12-02  
**Category:** Tech Stack  
**Deliverable:** ADR-0006: Testing Framework and TDD Approach

---

## 📋 Overview

This research explores testing frameworks and strategies for the work-prod application, with a focus on supporting Test-Driven Development (TDD) using vertical slice architecture. The goal is to select appropriate testing tools for backend (Python/Flask), frontend (React/Vite), and end-to-end testing.

## 🎯 Research Questions

1. **Backend Testing Framework**
   - Which Python testing framework best suits Flask applications?
   - Options: pytest vs unittest vs nose2
   - Considerations: fixtures, mocking, SQLAlchemy testing, Flask context management

2. **Frontend Testing Framework**
   - Which testing framework works best with Vite + React?
   - Options: Vitest vs Jest vs React Testing Library
   - Considerations: Vite integration, component testing, Zustand store testing

3. **End-to-End Testing**
   - Which E2E framework provides the best developer experience?
   - Options: Playwright vs Cypress vs Selenium
   - Considerations: Flask + React integration testing, cross-browser support, debugging

4. **TDD Patterns for Vertical Slices**
   - How to structure tests for vertical slice development?
   - Test organization: by feature vs by layer
   - Integration test strategies between backend and frontend

5. **Test Organization and Fixtures**
   - Directory structure for tests
   - Shared fixtures and test data management
   - Database setup/teardown for tests

6. **Coverage Requirements and CI Integration**
   - Code coverage thresholds
   - CI/CD integration (GitHub Actions)
   - Pre-commit hooks for testing

## 📝 Methodology

1. Review official documentation for each framework
2. Analyze community adoption and maintenance status
3. Evaluate integration with our tech stack (Flask, React, Vite, SQLAlchemy, Zustand)
4. Consider TDD workflow and developer experience
5. Test migration path and learning curve
6. Performance and speed of test execution

## 🔍 Research Areas

### Backend Testing: pytest vs unittest vs nose2

**Criteria to evaluate:**
- Flask application factory testing support
- SQLAlchemy model testing
- API endpoint testing
- Fixtures and dependency injection
- Mocking capabilities
- Test discovery and execution speed
- Community plugins (Flask-specific)
- Documentation quality

### Frontend Testing: Vitest vs Jest vs React Testing Library

**Criteria to evaluate:**
- Vite integration (native support vs configuration)
- React component testing
- Zustand store testing
- Async/await handling
- Mock API responses
- Test execution speed
- Hot module replacement for tests
- TypeScript support (future consideration)

### E2E Testing: Playwright vs Cypress vs Selenium

**Criteria to evaluate:**
- Flask + React integration testing
- Browser automation capabilities
- Debugging tools
- CI/CD integration
- Parallel test execution
- API mocking/intercept capabilities
- Test maintenance burden
- Video/screenshot capture for debugging

### TDD Vertical Slice Patterns

**Topics to research:**
- Test structure for vertical slices (backend → API → frontend flow)
- Integration test vs unit test balance
- Test data management across layers
- Continuous testing workflow (watch mode)
- Test isolation and cleanup strategies

## 📊 Evaluation Criteria

Each option will be scored on:
1. **Integration** - How well it works with our stack
2. **Developer Experience** - Ease of writing and debugging tests
3. **Performance** - Test execution speed
4. **Community Support** - Documentation, plugins, ecosystem
5. **Maintenance** - Long-term viability and updates
6. **TDD Support** - Suitability for test-first development

## 🎯 Success Criteria

This research is complete when we can answer:
- Which backend testing framework to use (ADR-0006 Part 1)
- Which frontend testing framework to use (ADR-0006 Part 2)
- Which E2E testing framework to use (ADR-0006 Part 3)
- How to structure tests for vertical slice TDD (ADR-0006 Part 4)
- Test organization conventions (ADR-0006 Part 5)
- Coverage requirements and CI strategy (ADR-0006 Part 6)

## 📅 Timeline

**Estimated Duration:** 2-3 days (Week 2 research)

**Breakdown:**
- Day 1: Backend testing research (pytest ecosystem)
- Day 2: Frontend testing research (Vitest/Jest comparison)
- Day 3: E2E testing + TDD patterns + documentation

**Deliverable:** ADR-0006 documenting all testing decisions

## 🔗 Related Documents

- [ADR-0001: Flask Backend Architecture](../../decisions/ADR-0001-flask-backend-architecture.md)
- [ADR-0002: React Frontend Architecture](../../decisions/ADR-0002-react-frontend-architecture.md)
- [ADR-0004: Flask-React Integration Strategy](../../decisions/ADR-0004-flask-react-integration-strategy.md)
- [Projects MVP Roadmap](../../planning/mvp-roadmap.md)

## 🔬 Findings and Analysis

### Backend Testing: pytest (RECOMMENDED)

**Why pytest?**

pytest is the industry standard for Python testing and particularly well-suited for Flask applications:

**Strengths:**
- **Fixture System:** Powerful dependency injection for database setup, Flask app context, and test data
- **Flask Integration:** `pytest-flask` plugin provides Flask-specific fixtures (`client`, `app`, `db`)
- **SQLAlchemy Support:** Easy model testing with session management and rollback
- **Parameterization:** Test same logic with multiple inputs using `@pytest.mark.parametrize`
- **Plugin Ecosystem:** Rich plugins (pytest-cov for coverage, pytest-mock for mocking)
- **Readable Output:** Clear failure messages and stack traces
- **Community:** Massive adoption, excellent documentation

**vs unittest:**
- unittest requires more boilerplate (class-based tests, `self.assertEqual`)
- pytest is more Pythonic (simple functions, assert statements)
- pytest fixtures are more flexible than unittest setUp/tearDown

**vs nose2:**
- nose2 is in maintenance mode, pytest is actively developed
- pytest has larger community and plugin ecosystem

**Example pytest test:**
```python
def test_get_projects(client, db):
    """Test GET /api/projects endpoint."""
    # Setup
    project = Project(name="Test", path="/test")
    db.session.add(project)
    db.session.commit()
    
    # Execute
    response = client.get('/api/projects')
    
    # Assert
    assert response.status_code == 200
    assert len(response.json['projects']) == 1
    assert response.json['projects'][0]['name'] == "Test"
```

**Decision:** Use pytest with pytest-flask, pytest-cov, and pytest-mock

---

### Frontend Testing: Vitest (RECOMMENDED)

**Why Vitest?**

Vitest is purpose-built for Vite projects and offers the best integration:

**Strengths:**
- **Zero Config:** Works out-of-the-box with Vite projects
- **Fast:** Uses Vite's transform pipeline, instant HMR for tests
- **Jest-Compatible API:** Familiar API for developers who know Jest
- **ESM Support:** Native ES modules support, no transpilation needed
- **Watch Mode:** Lightning-fast test re-runs on file changes
- **UI Mode:** Optional test UI for visual debugging
- **Component Testing:** First-class React component testing support

**vs Jest:**
- Jest requires configuration for Vite (transform plugins, ESM handling)
- Vitest is 10-20x faster due to Vite's esbuild-based transforms
- Jest has larger ecosystem, but Vitest is compatible with most Jest plugins

**vs React Testing Library:**
- React Testing Library is a testing library, not a test runner
- We'll use React Testing Library WITH Vitest for component testing

**Example Vitest test:**
```jsx
import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import ProjectList from '../components/ProjectList'

describe('ProjectList', () => {
  it('renders empty state when no projects', () => {
    render(<ProjectList projects={[]} />)
    expect(screen.getByText(/no projects/i)).toBeInTheDocument()
  })
})
```

**Decision:** Use Vitest with @testing-library/react for component testing

---

### E2E Testing: Playwright (RECOMMENDED)

**Why Playwright?**

Playwright is the modern choice for end-to-end testing:

**Strengths:**
- **Modern Architecture:** Fast, reliable, less flaky than Selenium
- **Cross-Browser:** Chromium, Firefox, WebKit (Safari) support
- **Debugging Tools:** Trace Viewer, Inspector, VS Code extension
- **Auto-Wait:** Automatically waits for elements to be ready
- **Network Interception:** Mock API responses, test edge cases
- **Parallel Execution:** Run tests in parallel for speed
- **CI/CD Ready:** Excellent GitHub Actions integration
- **Screenshots/Videos:** Automatic capture on failure

**vs Cypress:**
- Playwright supports multiple browser engines (Cypress is Chromium-only by default)
- Playwright has better CI/CD integration and parallel execution
- Playwright Trace Viewer is superior for debugging
- Cypress has nicer syntax but Playwright is more powerful

**vs Selenium:**
- Selenium is older, more verbose, slower
- Playwright has auto-wait, reducing flaky tests
- Playwright has better developer experience

**Example Playwright test:**
```javascript
import { test, expect } from '@playwright/test'

test('create project flow', async ({ page }) => {
  await page.goto('http://localhost:5173')
  await page.click('text=New Project')
  await page.fill('input[name="name"]', 'My Project')
  await page.fill('input[name="path"]', '/projects/my-project')
  await page.click('button[type="submit"]')
  
  await expect(page.locator('text=My Project')).toBeVisible()
})
```

**Decision:** Use Playwright for E2E testing

---

### TDD Vertical Slice Patterns

**Test-First Development Flow:**

1. **Write Backend Test** → 2. **Implement Backend** → 3. **Write Frontend Test** → 4. **Implement Frontend** → 5. **Write E2E Test** → 6. **Verify Integration**

**Test Pyramid:**
- **Many Unit Tests** (fast, isolated, specific)
- **Some Integration Tests** (API endpoints with database)
- **Few E2E Tests** (critical user flows only)

**Vertical Slice Testing Strategy:**

For each feature slice (e.g., "List Projects"):
1. Backend model test → Implement model
2. Backend API test → Implement API endpoint
3. Frontend component test → Implement React component
4. Frontend store test → Implement Zustand store
5. E2E test → Verify end-to-end flow

**Test Isolation:**
- Each test has its own database transaction (rollback after test)
- Mock external APIs (GitHub, Microsoft)
- Use factory patterns for test data creation

---

### Test Organization

**Backend Structure:**
```
backend/
├── tests/
│   ├── conftest.py              # Shared fixtures (app, db, client)
│   ├── unit/
│   │   ├── models/
│   │   │   └── test_project.py  # Model unit tests
│   │   └── services/
│   │       └── test_github.py   # Service unit tests
│   ├── integration/
│   │   └── api/
│   │       └── test_projects.py # API integration tests
│   └── fixtures/
│       └── factories.py         # Test data factories
├── pytest.ini                   # pytest configuration
└── .coveragerc                  # Coverage settings
```

**Frontend Structure:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── ProjectList.jsx
│   │   └── ProjectList.test.jsx  # Colocated component tests
│   └── stores/
│       ├── projectsStore.js
│       └── projectsStore.test.js  # Colocated store tests
├── tests/
│   ├── setup.js                  # Test environment setup
│   └── mocks/
│       └── api.js                # Mock API responses
└── vitest.config.js              # Vitest configuration
```

**E2E Structure:**
```
tests/
├── e2e/
│   ├── projects/
│   │   ├── list-projects.spec.js
│   │   ├── create-project.spec.js
│   │   └── delete-project.spec.js
│   ├── fixtures/
│   │   └── test-data.json
│   └── utils/
│       └── helpers.js
└── playwright.config.js
```

---

### Coverage Requirements

**Target Coverage:** >80% overall

**By Layer:**
- Backend models: >90% (critical business logic)
- Backend API endpoints: >85% (core functionality)
- Frontend components: >75% (UI can have uncovered edge cases)
- Frontend stores: >90% (state management is critical)

**Coverage Tools:**
- Backend: pytest-cov (outputs to `htmlcov/`)
- Frontend: Vitest coverage via `v8` or `istanbul`

**CI Integration:**
- Run tests on every pull request
- Block merge if coverage drops below threshold
- Generate coverage reports in GitHub Actions

---

## 📊 Summary and Recommendations

### Final Decisions

| Layer | Framework | Key Plugins | Rationale |
|-------|-----------|-------------|-----------|
| Backend | pytest | pytest-flask, pytest-cov, pytest-mock | Industry standard, excellent Flask integration |
| Frontend | Vitest | @testing-library/react | Zero-config Vite integration, fast |
| E2E | Playwright | @playwright/test | Modern, reliable, great debugging tools |

### Configuration Files

**backend/pytest.ini:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

**frontend/vitest.config.js:**
```javascript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './tests/setup.js',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      lines: 75,
      functions: 75,
      branches: 75,
      statements: 75
    }
  }
})
```

**tests/playwright.config.js:**
```javascript
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure'
  },
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI
  }
})
```

### Installation Commands

**Backend:**
```bash
pip install pytest pytest-flask pytest-cov pytest-mock
```

**Frontend:**
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom
```

**E2E:**
```bash
npm install -D @playwright/test
npx playwright install
```

---

## 📚 References

### pytest Resources
- [pytest Documentation](https://docs.pytest.org/)
- [Flask Testing Documentation](https://flask.palletsprojects.com/en/stable/testing/)
- [Testing Flask Applications with pytest](https://testdriven.io/blog/flask-pytest/)
- [pytest-flask Plugin](https://pytest-flask.readthedocs.io/)

### Vitest Resources
- [Vitest Documentation](https://vitest.dev/)
- [Testing React with Vitest](https://www.robinwieruch.de/vitest-react-testing-library/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)

### Playwright Resources
- [Playwright Documentation](https://playwright.dev/)
- [Getting Started with Playwright](https://playwright.dev/docs/intro)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)

### Related ADRs
- [ADR-0001: Flask Backend Architecture](../../decisions/ADR-0001-flask-backend-architecture.md)
- [ADR-0002: React Frontend Architecture](../../decisions/ADR-0002-react-frontend-architecture.md)
- [ADR-0004: Flask-React Integration Strategy](../../decisions/ADR-0004-flask-react-integration-strategy.md)
- [ADR-0006: Testing Framework and TDD Approach](../../decisions/ADR-0006-testing-framework-and-tdd-approach.md) (This research supports this ADR)

---

**Last Updated:** 2025-12-02  
**Status:** ✅ Accepted  
**Decision:** pytest + Vitest + Playwright with >80% coverage target  
**Next:** Implement testing setup in Phase 0





