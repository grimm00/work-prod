# Additional Tech Stack Libraries

**Status:** 🟠 In Progress  
**Category:** Technology Stack Enhancement  
**Created:** 2025-12-01  
**Last Updated:** 2025-12-01

---

## 📋 Overview

This document catalogsadditional libraries beyond the core Flask + React + SQLite stack (defined in ADR-0001, ADR-0002, ADR-0003). These are implementation-level dependencies that enhance functionality but don't constitute architectural decisions.

**Core Stack (Decided Week 1):**

- Backend: Python + Flask + SQLAlchemy + SQLite
- Frontend: React 18 + Vite + Zustand + React Router v6
- Integration: Vite proxy (dev), Flask serves React (prod)

**This Document:** Additional libraries for search, validation, UI components, and utilities.

---

## 🐍 Backend (Python/Flask) Libraries

### Search & Filtering

**SQLite FTS5** (Built-in to SQLite 3.9+)

- **Purpose:** Full-text search for project names, descriptions, tech stack
- **Why:** Zero dependencies, fast for <1000 records, simple integration
- **Usage:** Create FTS5 virtual table for projects
- **Documentation:** https://www.sqlite.org/fts5.html
- **Decision:** Recommended in Week 2 research (section 2.3)

**Alternative Considered:** Whoosh (pure Python search)

- **Why Not:** SQLite FTS5 is simpler and sufficient for 59 projects

### Data Validation

**marshmallow** (Schema validation and serialization)

- **Purpose:** Validate API request/response data, serialize SQLAlchemy models
- **Why:** Industry standard, integrates well with Flask and SQLAlchemy
- **Usage:** Define schemas for Projects, Skills, Learning classifications
- **Documentation:** https://marshmallow.readthedocs.io/
- **Install:** `pip install marshmallow marshmallow-sqlalchemy`

**Alternative:** pydantic

- **Pros:** Type hints, FastAPI integration
- **Cons:** Less SQLAlchemy integration than marshmallow
- **Decision:** Prefer marshmallow for Flask + SQLAlchemy projects

### API Enhancements

**flask-restful** or **flask-smorest**

- **Purpose:** REST API helpers (resource routing, request parsing, response formatting)
- **Why:** Reduces boilerplate for REST endpoints
- **Decision:** Defer until API complexity requires it (Phase 2+)

**apispec** (OpenAPI/Swagger documentation)

- **Purpose:** Auto-generate API documentation from code
- **Why:** Improves developer experience, documents API contract
- **Decision:** Add in Phase 3 when API stabilizes

### Utilities

**python-dotenv** (Environment variable management)

- **Purpose:** Load configuration from `.env` files
- **Why:** Separate config from code, manage secrets safely
- **Usage:** Already recommended in ADR-0001
- **Documentation:** https://pypi.org/project/python-dotenv/
- **Install:** `pip install python-dotenv`

**click** (CLI tools)

- **Purpose:** Create management commands (e.g., `flask init-db`, `flask import-projects`)
- **Why:** Better than argparse, integrates with Flask
- **Usage:** Database migrations, data import scripts
- **Documentation:** https://click.palletsprojects.com/
- **Install:** `pip install click` (Flask includes it)

---

## ⚛️ Frontend (React) Libraries

### Search & Filtering

**react-select** (Multi-select dropdowns and tag inputs)

- **Purpose:** Filtering by tech stack, organization, learning type
- **Why:** Accessible, customizable, widely used
- **Usage:** Filter panel for project search
- **Documentation:** https://react-select.com/
- **Install:** `npm install react-select`
- **Priority:** HIGH - Critical for MVP filtering UX

**react-search-autocomplete** (Search bars with suggestions)

- **Purpose:** Project name autocomplete, tech stack suggestions
- **Why:** Good UX, reduces typing, helps discovery
- **Usage:** Main search bar in Projects view
- **Documentation:** https://www.npmjs.com/package/react-search-autocomplete
- **Install:** `npm install react-search-autocomplete`
- **Priority:** MEDIUM - Nice-to-have for Phase 1

**use-debounce** (Debounce hook for search input)

- **Purpose:** Reduce API calls while user types
- **Why:** Performance optimization, reduces server load
- **Usage:** Debounce search input by 300-500ms
- **Documentation:** https://www.npmjs.com/package/use-debounce
- **Install:** `npm install use-debounce`
- **Priority:** HIGH - Essential for search performance

### UI Components

**@tanstack/react-table** (Advanced table with filtering/sorting)

- **Purpose:** Project table view with built-in filtering, sorting, pagination
- **Why:** Flexible, headless, performant for large datasets
- **Usage:** Alternative to card view for project lists
- **Documentation:** https://tanstack.com/table/latest
- **Install:** `npm install @tanstack/react-table`
- **Priority:** MEDIUM - Phase 2+ (after basic card view works)

**react-toastify** (Toast notifications)

- **Purpose:** User feedback (success, error, info messages)
- **Why:** Better UX than alerts, customizable, accessible
- **Usage:** "Project created", "Classification updated", error messages
- **Documentation:** https://fkhadra.github.io/react-toastify/
- **Install:** `npm install react-toastify`
- **Priority:** MEDIUM - Phase 2

**Component Library (Optional):**

Options: **shadcn/ui** or **Mantine**

**shadcn/ui:**

- **Pros:** Copy-paste components, full control, Tailwind-based, modern
- **Cons:** More setup, need to customize
- **Best For:** Custom design systems

**Mantine:**

- **Pros:** Comprehensive, out-of-box styling, hooks library, accessibility
- **Cons:** Opinionated styling, harder to customize deeply
- **Best For:** Rapid prototyping

**Decision:** Defer until Phase 2. Start with custom components + Tailwind CSS (already in ADR-0002).

### State Management (Already Decided: Zustand)

**zustand** (Global state management)

- **Purpose:** Manage project list, filters, user preferences
- **Why:** Simpler than Redux, less boilerplate
- **Documentation:** https://zustand-demo.pmnd.rs/
- **Install:** `npm install zustand`
- **Status:** ✅ Decided in ADR-0002

**zustand/middleware** (Persistence, devtools, immer)

- **Purpose:** Persist filter preferences to localStorage, debugging
- **Usage:** `import { persist, devtools } from 'zustand/middleware'`
- **Priority:** LOW - Phase 3

### Form Handling

**react-hook-form** (Form state management)

- **Purpose:** Manage project creation/editing forms
- **Why:** Performance (uncontrolled inputs), less re-renders, easy validation
- **Documentation:** https://react-hook-form.com/
- **Install:** `npm install react-hook-form`
- **Priority:** HIGH - Needed for Phase 1 (Projects CRUD)

**zod** (Schema validation for forms)

- **Purpose:** Validate form inputs (works with react-hook-form)
- **Why:** Type-safe, composable, better errors than manual validation
- **Documentation:** https://zod.dev/
- **Install:** `npm install zod`
- **Priority:** HIGH - Pair with react-hook-form

### Utilities

**date-fns** (Date manipulation)

- **Purpose:** Format dates (created_at, last_modified), relative time ("2 days ago")
- **Why:** Lighter than moment.js, tree-shakeable, modern
- **Documentation:** https://date-fns.org/
- **Install:** `npm install date-fns`
- **Priority:** MEDIUM - Phase 2

**clsx** (Conditional className utility)

- **Purpose:** Dynamically apply CSS classes
- **Why:** Cleaner than string concatenation or template literals
- **Usage:** `clsx('btn', isActive && 'btn-active', isPrimary && 'btn-primary')`
- **Documentation:** https://www.npmjs.com/package/clsx
- **Install:** `npm install clsx`
- **Priority:** MEDIUM - Useful throughout

---

## 📦 Implementation Recommendations

### Phase 1 (MVP - Projects CRUD):

**Backend:**

- `python-dotenv` - Configuration management
- `marshmallow` + `marshmallow-sqlalchemy` - API validation
- SQLite FTS5 (built-in) - Search functionality

**Frontend:**

- `react-select` - Filtering UI (HIGH priority)
- `use-debounce` - Search performance (HIGH priority)
- `react-hook-form` - Form management (HIGH priority)
- `zod` - Form validation (HIGH priority)

### Phase 2 (Enhanced UX):

**Backend:**

- `click` - Management CLI commands

**Frontend:**

- `react-toastify` - User feedback
- `@tanstack/react-table` - Table view option
- `date-fns` - Date formatting
- `clsx` - Dynamic classes

### Phase 3 (Polish & Scale):

**Backend:**

- `flask-restful` or `flask-smorest` - REST helpers (if needed)
- `apispec` - API documentation

**Frontend:**

- Component library (shadcn/ui or Mantine) - If custom components become repetitive
- `zustand/middleware` - State persistence
- `react-search-autocomplete` - Enhanced search UX

---

## ⚠️ Impact on ADRs

**No New ADRs Required:** These are implementation details, not architectural decisions. The core architecture (Flask, React, SQLite, Zustand) is already defined in ADR-0001 through ADR-0004.

**ADR Updates:** Add note in ADR-0001 (Flask) and ADR-0002 (React) that additional libraries will be added during implementation, and reference this document.

---

## 📊 Dependency Management

### Backend (`requirements.txt`)

```
# Core (from ADR-0001)
Flask==3.0.0
SQLAlchemy==2.0.23
Flask-Migrate==4.0.5
python-dotenv==1.0.0

# Phase 1 additions
marshmallow==3.20.1
marshmallow-sqlalchemy==0.30.0

# Phase 2 additions
# click is included with Flask

# Phase 3 additions (defer)
# flask-restful==0.3.10
# flask-smorest==0.42.1
# apispec==6.3.1
```

### Frontend (`package.json`)

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "zustand": "^4.4.7",
    "axios": "^1.6.2",

    // Phase 1 additions
    "react-select": "^5.8.0",
    "use-debounce": "^10.0.0",
    "react-hook-form": "^7.48.2",
    "zod": "^3.22.4"

    // Phase 2 additions (defer)
    // "@tanstack/react-table": "^8.10.7",
    // "react-toastify": "^9.1.3",
    // "date-fns": "^3.0.0",
    // "clsx": "^2.0.0"
  }
}
```

---

## 🔗 Related Documentation

- **[ADR-0001: Flask Backend Architecture](../../decisions/ADR-0001-flask-backend-architecture.md)** - Core backend decisions
- **[ADR-0002: React Frontend Architecture](../../decisions/ADR-0002-react-frontend-architecture.md)** - Core frontend decisions (Zustand already chosen)
- **[Week 2 Research: Project Search and Filtering](../research-register.md#23-project-search-and-filtering-architecture)** - Search library research
- **[Learning Project Taxonomy](../data-models/learning-project-taxonomy.md)** - UI requirements for Learning filters

---

## ✅ Next Steps

1. **Phase 1 Setup:** Install Phase 1 dependencies when beginning implementation
2. **ADR Updates:** Add reference to this document in ADR-0001 and ADR-0002
3. **Dependency Lock:** Pin versions in requirements.txt and package-lock.json
4. **Documentation:** Update setup guides with new dependencies
5. **Phase Transitions:** Install Phase 2/3 libraries as features are built

---

**Status:** 🟠 In Progress - Libraries identified, awaiting Phase 1 implementation  
**Next:** Update ADR-0001 and ADR-0002 with reference to this document




