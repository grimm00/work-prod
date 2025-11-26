# Python Flask Backend Architecture Research

**Status:** 🟠 In Progress  
**Priority:** 🔴 CRITICAL  
**Category:** Technology Stack  
**Timeline:** Week 1  
**Last Updated:** 2025-11-26

---

## 📋 Research Questions

1. What is the best project structure for Flask applications in 2024?
2. How to implement RESTful API design with Flask?
3. Best practices for Flask configuration management (dev vs. production)?
4. How to structure Flask apps for scalability?
5. What Flask extensions are needed for our use case?

---

## 🎯 Research Objectives

**Goal:** Establish a robust, maintainable Flask backend architecture that:
- Supports local-first SQLite database
- Provides RESTful API for React frontend
- Handles authentication and authorization
- Manages configuration across environments
- Scales from MVP to full feature set
- Integrates with Microsoft Graph API and potentially Miro API

---

## 🔍 Research Methodology

1. **Documentation Review**
   - Flask official documentation (v3.0+)
   - Flask-SQLAlchemy documentation
   - Flask-Migrate documentation
   - Community best practices

2. **Pattern Analysis**
   - Application Factory pattern
   - Blueprint organization
   - Configuration management patterns
   - RESTful API design patterns

3. **Extension Evaluation**
   - Review required Flask extensions
   - Evaluate integration complexity
   - Consider maintenance and support

---

## 📚 Findings

### 1. Flask Project Structure (2024 Best Practices)

**Application Factory Pattern** - Recommended approach for Flask applications:

**Benefits:**
- Supports multiple configurations (dev, test, production)
- Easier testing with different configurations
- Blueprints can be registered conditionally
- Avoids circular imports
- Better separation of concerns

**Recommended Structure:**

```
backend/
├── app/
│   ├── __init__.py           # Application factory
│   ├── config.py             # Configuration classes
│   ├── models/               # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── learning.py
│   │   ├── skill.py
│   │   └── meeting.py
│   ├── api/                  # API blueprints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   ├── learnings.py
│   │   ├── skills.py
│   │   ├── meetings.py
│   │   └── goals.py
│   ├── services/             # Business logic
│   │   ├── __init__.py
│   │   ├── task_service.py
│   │   ├── learning_service.py
│   │   └── outlook_service.py
│   ├── utils/                # Utility functions
│   │   ├── __init__.py
│   │   └── validators.py
│   └── extensions.py         # Flask extensions initialization
├── instance/                 # Instance-specific files
│   └── config.py             # Local config (gitignored)
├── migrations/               # Database migrations
├── tests/                    # Test suite
│   ├── unit/
│   └── integration/
├── .env                      # Environment variables (gitignored)
├── .env.example              # Environment template
├── requirements.txt          # Dependencies
├── run.py                    # Application entry point
└── README.md                 # Setup instructions
```

### 2. Application Factory Implementation

**Core Pattern:**

```python
# app/__init__.py
from flask import Flask
from app.extensions import db, migrate, cors

def create_app(config_name='development'):
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration
    app.config.from_object(f'app.config.{config_name.title()}Config')
    app.config.from_pyfile('config.py', silent=True)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    
    # Register blueprints
    from app.api import tasks_bp, learnings_bp, skills_bp
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(learnings_bp, url_prefix='/api/learnings')
    app.register_blueprint(skills_bp, url_prefix='/api/skills')
    
    return app
```

### 3. Configuration Management

**Multi-Environment Configuration:**

```python
# app/config.py
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        f'sqlite:///{os.path.join(os.path.dirname(__file__), "..", "instance", "dev.db")}'
    SQLALCHEMY_ECHO = True  # Log all SQL queries
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

### 4. RESTful API Design

**Blueprint Organization:**

Each major feature area gets its own blueprint:
- `/api/tasks` - Daily focus and task management
- `/api/learnings` - Learning journal entries
- `/api/skills` - Skills matrix
- `/api/meetings` - Meeting tracking and preparation
- `/api/goals` - Goal and hiring readiness tracking
- `/api/feedback` - Feedback capture
- `/api/energy` - Energy and engagement tracking

**API Design Principles:**
- Use HTTP methods correctly (GET, POST, PUT, PATCH, DELETE)
- Return appropriate status codes
- Consistent JSON response format
- API versioning (future-proofing)
- Error handling with meaningful messages

**Example Blueprint:**

```python
# app/api/tasks.py
from flask import Blueprint, jsonify, request
from app.models import Task
from app.services.task_service import TaskService
from app.extensions import db

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    """Get all tasks for today"""
    date = request.args.get('date')  # Optional filter
    tasks = TaskService.get_tasks_by_date(date)
    return jsonify([task.to_dict() for task in tasks]), 200

@tasks_bp.route('/', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.get_json()
    task = TaskService.create_task(data)
    return jsonify(task.to_dict()), 201

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    data = request.get_json()
    task = TaskService.update_task(task_id, data)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    success = TaskService.delete_task(task_id)
    if not success:
        return jsonify({'error': 'Task not found'}), 404
    return '', 204
```

### 5. Required Flask Extensions

**Essential Extensions for Our Use Case:**

1. **Flask-SQLAlchemy** (v3.1+)
   - Purpose: ORM for database interactions
   - Why: Simplifies SQLite database operations
   - Installation: `pip install Flask-SQLAlchemy`

2. **Flask-Migrate** (v4.0+)
   - Purpose: Database migrations using Alembic
   - Why: Manage schema changes over time
   - Installation: `pip install Flask-Migrate`

3. **Flask-CORS** (v4.0+)
   - Purpose: Cross-Origin Resource Sharing
   - Why: Allow React frontend to call Flask API
   - Installation: `pip install Flask-CORS`

4. **Flask-JWT-Extended** (v4.5+)
   - Purpose: JWT token authentication
   - Why: Secure API authentication (future use)
   - Installation: `pip install Flask-JWT-Extended`

5. **python-dotenv** (v1.0+)
   - Purpose: Load environment variables from .env file
   - Why: Manage secrets and configuration
   - Installation: `pip install python-dotenv`

6. **marshmallow** (v3.20+) or **Flask-Marshmallow** (v0.15+)
   - Purpose: Object serialization/deserialization, validation
   - Why: Clean data validation and API responses
   - Installation: `pip install marshmallow` or `pip install flask-marshmallow`

**Optional but Recommended:**

7. **Flask-Limiter** (v3.5+)
   - Purpose: Rate limiting
   - Why: Prevent API abuse
   
8. **pytest** + **pytest-flask** (v7.4+)
   - Purpose: Testing framework
   - Why: Write comprehensive tests

### 6. Extensions Initialization Pattern

**Centralized Extension Management:**

```python
# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Initialize extensions without app instance
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

# Extensions are bound to app in create_app() factory function
```

### 7. Service Layer Pattern

**Benefits:**
- Separates business logic from routes
- Easier to test
- Reusable across different API endpoints
- Cleaner code organization

**Example Service:**

```python
# app/services/task_service.py
from app.extensions import db
from app.models import Task
from datetime import datetime, date

class TaskService:
    @staticmethod
    def get_tasks_by_date(date_str=None):
        """Get tasks for a specific date (defaults to today)"""
        target_date = date.fromisoformat(date_str) if date_str else date.today()
        return Task.query.filter_by(date=target_date).all()
    
    @staticmethod
    def create_task(data):
        """Create a new task"""
        task = Task(
            title=data['title'],
            description=data.get('description'),
            priority=data.get('priority', 'medium'),
            date=data.get('date', date.today())
        )
        db.session.add(task)
        db.session.commit()
        return task
    
    @staticmethod
    def update_task(task_id, data):
        """Update an existing task"""
        task = Task.query.get(task_id)
        if not task:
            return None
        
        for key, value in data.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        db.session.commit()
        return task
    
    @staticmethod
    def delete_task(task_id):
        """Delete a task"""
        task = Task.query.get(task_id)
        if not task:
            return False
        
        db.session.delete(task)
        db.session.commit()
        return True
```

### 8. Error Handling

**Global Error Handlers:**

```python
# In create_app() factory
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400
```

---

## 📊 Analysis

### Strengths of Recommended Approach

1. **Scalability**
   - Modular blueprint structure allows adding features incrementally
   - Service layer separates concerns
   - Easy to add new API endpoints

2. **Maintainability**
   - Clear directory structure
   - Separation of concerns (models, services, APIs)
   - Configuration management supports multiple environments

3. **Testability**
   - Application factory pattern enables testing with different configs
   - Service layer can be tested independently
   - Blueprint organization makes integration testing easier

4. **Developer Experience**
   - Hot reload in development mode
   - SQLAlchemy ORM simplifies database operations
   - Migrations track schema changes

5. **Security**
   - Environment-based configuration
   - CORS protection
   - JWT authentication support
   - Secret key management

### Potential Challenges

1. **Learning Curve**
   - Application factory pattern may be unfamiliar
   - Blueprint organization requires understanding
   - Mitigation: Clear documentation and examples

2. **Overhead for Small App**
   - Might seem complex for initial MVP
   - Mitigation: Worth it for long-term maintainability

3. **Extension Management**
   - Multiple dependencies to manage
   - Mitigation: Use requirements.txt and virtual environment

---

## 💡 Recommendations

### 1. Adopt Application Factory Pattern

**Recommendation:** Use the application factory pattern from the start

**Rationale:**
- Essential for multi-environment support (dev, test, production)
- Makes testing significantly easier
- Standard Flask best practice in 2024
- Avoids circular import issues

### 2. Implement Blueprint Organization

**Recommendation:** Organize API by feature area using blueprints

**Rationale:**
- Maps well to user's feature priorities (daily focus, learning, skills, meetings, goals, feedback, energy)
- Easy to add new features without touching existing code
- Clear separation of concerns

### 3. Use Service Layer Pattern

**Recommendation:** Implement business logic in service classes

**Rationale:**
- Keeps route handlers thin and focused
- Easier to test business logic independently
- Reusable across different API endpoints
- Better code organization

### 4. Essential Extensions Only (MVP)

**Recommendation:** Start with core extensions, add others as needed

**MVP Extensions:**
- Flask-SQLAlchemy (database)
- Flask-Migrate (migrations)
- Flask-CORS (React integration)
- python-dotenv (configuration)

**Later Additions:**
- Flask-JWT-Extended (authentication - when needed)
- marshmallow (validation - as complexity grows)

### 5. Configuration Strategy

**Recommendation:** Use environment-based configuration with .env files

**Rationale:**
- Keeps secrets out of code
- Easy to switch between development and production
- Standard practice for modern web apps

---

## 🚀 Implementation Plan

### Phase 1: Project Setup (Week 1 - Day 1-2)

1. **Create Project Structure**
   - Set up directory structure as documented
   - Initialize virtual environment
   - Create requirements.txt

2. **Install Dependencies**
   ```bash
   pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-CORS python-dotenv
   ```

3. **Create Application Factory**
   - Implement `create_app()` function
   - Set up configuration classes
   - Initialize extensions

4. **Create Entry Point**
   - Implement `run.py`
   - Test basic Flask app runs

### Phase 2: Database Setup (Week 1 - Day 2-3)

1. **Initialize Database**
   - Set up Flask-Migrate
   - Create initial migration
   - Test database creation

2. **Create First Model**
   - Implement Task model (for daily focus)
   - Test model creation and queries

### Phase 3: First API Endpoint (Week 1 - Day 3-4)

1. **Create Tasks Blueprint**
   - Implement basic CRUD operations
   - Test with curl or Postman

2. **Implement Task Service**
   - Move business logic to service layer
   - Write unit tests

### Phase 4: CORS Setup (Week 1 - Day 4-5)

1. **Configure CORS**
   - Allow React frontend origin
   - Test from React app

---

## 📦 Deliverables

### 1. Backend Architecture Decision Document

**Status:** ✅ This document

**Content:**
- Recommended Flask project structure
- Application factory pattern implementation
- Blueprint organization strategy
- Required extensions list
- Configuration management approach

### 2. Initial Project Structure

**Status:** 🔴 To Do

**Deliverable:**
- Complete backend/ directory structure
- All necessary files created
- Virtual environment set up
- Dependencies installed

### 3. Development Environment Setup Guide

**Status:** 🔴 To Do

**Deliverable:**
- Step-by-step setup instructions
- Environment configuration examples
- Troubleshooting common issues

### 4. Code Templates

**Status:** 🔴 To Do

**Deliverable:**
- Blueprint template
- Model template
- Service template
- Test template

---

## 🔗 References

### Official Documentation

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)

### Best Practices

- Flask Mega-Tutorial by Miguel Grinberg
- Flask Application Factory Pattern
- RESTful API Design Guidelines
- Python Web Development Best Practices

### Related Research

- [React Frontend Architecture](react-frontend-architecture.md) - To Do
- [SQLite Database Design](sqlite-database-design.md) - To Do
- [Flask + React Integration](flask-react-integration.md) - To Do

---

## ✅ Decision

**Decision:** Adopt the Application Factory pattern with Blueprint organization and Service layer

**Rationale:**
- Industry best practice for Flask applications in 2024
- Scales from MVP to full application
- Supports our requirement for local-first architecture
- Facilitates testing and maintenance
- Maps well to our feature-based development approach

**Next Steps:**
1. Create initial project structure
2. Set up development environment
3. Implement application factory
4. Create first model and API endpoint
5. Test CORS with React frontend

---

**Last Updated:** 2025-11-26  
**Status:** 🟠 In Progress  
**Next:** Begin implementation of project structure

