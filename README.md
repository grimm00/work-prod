# work-prod

**Purpose:** Manage Productivity and Engagement for Work  
**Version:** v0.1.0 (Phase 0 Complete)  
**Last Updated:** 2025-12-02  
**Status:** 🟠 In Development (Backend MVP - Phase 1 Next)  
**Approach:** Backend-First API Development with CLI

---

## 🎯 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm 8+
- Git

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd work-prod

# Backend Setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
cd backend
pip install -r requirements.txt

# Frontend Setup (in a new terminal)
cd frontend
npm install
```

### Running the Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
source ../venv/bin/activate  # Activate virtual environment
python run.py
# Backend runs on http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Frontend runs on http://localhost:5173
```

### First Steps

1. Start both backend and frontend servers as shown above
2. Open http://localhost:5173 in your browser
3. You should see "✓ Flask backend is running" message
4. Run tests: `cd backend && pytest` and `cd frontend && npm test`

---

## 📁 Project Structure

This project follows a **hub-and-spoke documentation pattern**:

- **Hub Files** (README.md) serve as entry points and navigation guides
- **Spoke Directories** contain detailed implementation and specialized documentation
- **Maintainers Directory** manages project planning, feedback, and decision tracking

### Key Directories

- **`docs/maintainers/`** - Project management hub ([Maintainers Guide](docs/maintainers/README.md))
- **`backend/`** - Backend application ([Backend Guide](backend/README.md))
- **`frontend/`** - Frontend application ([Frontend Guide](frontend/README.md))
- **`tests/`** - Centralized testing ([Testing Guide](tests/README.md))
- **`scripts/`** - Automation scripts ([Scripts Guide](scripts/README.md))
- **`docs/`** - User documentation ([Documentation Guide](docs/README.md))

---

## 🚀 Development Workflow

### Git Flow

- **`main`** - Production releases only
- **`develop`** - Ongoing development
- **`feat/*`** - Feature branches (require PRs)
- **`fix/*`** - Bug fixes (require PRs)
- **`docs/*`** - Documentation (can push directly)
- **`chore/*`** - Maintenance (can push directly)

### Branch Requirements

- Feature branches: Full testing, linting, external reviews
- Documentation branches: Minimal validation
- Release branches: Full validation + external reviews

---

## 🛠️ Technology Stack

### Backend

- **Python 3.11+** - Programming language
- **Flask 3.0** - Web framework with application factory pattern
- **SQLAlchemy** - ORM for database operations
- **Flask-Migrate** - Database migrations
- **SQLite** - Local-first database
- **pytest** - Testing framework with pytest-flask and pytest-cov

### Frontend

- **React 18** - UI framework
- **Vite** - Build tool and development server
- **Zustand** - State management
- **React Router v6** - Client-side routing
- **Axios** - HTTP client for API calls
- **Vitest** - Testing framework with React Testing Library

### Integration

- **Vite Proxy** - Development proxy from frontend to backend
- **Flask-CORS** - Cross-origin resource sharing support

---

## 📊 Project Status

### ✅ Completed (Phase 0)

- Flask backend with application factory pattern
- Health check API endpoint
- Backend testing infrastructure (pytest, 100% coverage)
- Hot reload for backend
- React frontend skeleton (deferred to Phase 8)

### 🟡 Next (Phase 1 - Backend API)

- Projects data model and database schema
- GET /api/projects endpoint (list all)
- GET /api/projects/<id> endpoint (get single)
- CLI `proj list` command
- Backend tests with TDD

### 🟡 Planned (Phases 2-7 - Backend MVP)

- Full CRUD API operations (create, update, delete, archive)
- Search and filter functionality
- Import 59 projects from inventory
- Enhanced CLI with rich output
- API documentation (OpenAPI spec)

### 🟡 Deferred (Phase 8 - Frontend Learning Project)

- React UI for project management
- Build on working backend API
- Learn JavaScript/React without deadline pressure

---

## 📚 Documentation

### Quick References

- [Setup Guide](docs/SETUP.md)
- [API Documentation](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Contributing Guide](CONTRIBUTING.md)

### Planning Documents

- [Project Roadmap](docs/maintainers/planning/roadmap.md)
- [Feature Plans](docs/maintainers/planning/features/)
- [Release History](docs/maintainers/planning/releases/)

---

## 🔧 Development Commands

### Backend

```bash
# Run development server
cd backend
source ../venv/bin/activate
python run.py

# Run tests
cd backend
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/integration/api/test_health.py
```

### Frontend

```bash
# Run development server
cd frontend
npm run dev

# Run tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage

# Build for production
npm run build
```

---

## 📈 Metrics

- [Key metric 1]
- [Key metric 2]
- [Key metric 3]

---

## 🎊 Key Achievements

1. [Achievement 1]
2. [Achievement 2]
3. [Achievement 3]

---

## 📞 Support

- [Documentation](docs/)
- [Issues]([issues-url])
- [Discussions]([discussions-url])

---

**Last Updated:** 2025-11-26  
**Status:** [Status]  
**Next:** [Next milestone]
