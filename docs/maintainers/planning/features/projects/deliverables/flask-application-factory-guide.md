# Flask Application Factory Pattern - Implementation Guide

**Created:** 2025-12-02  
**Context:** Phase 0 - Development Environment Setup  
**Related:** [ADR-0001: Flask Backend Architecture](../../../decisions/ADR-0001-flask-backend-architecture.md)

---

## Overview

This guide explains the **Flask Application Factory Pattern** implemented in Phase 0, specifically how we use `backend/app/__init__.py` to create configurable Flask application instances.

---

## Python Package Fundamentals

### What `__init__.py` Does

The `__init__.py` file serves two purposes:

1. **Package Marker** - Turns a directory into a Python package (importable module)
2. **Package Initialization** - Runs when the package is imported

### Common Patterns

#### Pattern 1: Empty `__init__.py` (Simple Marker)
```python
# app/__init__.py
# (empty or just comments)
```

**Usage:** Import from submodules directly
```python
from app.api.health import health_bp
```

#### Pattern 2: Re-exports (Clean API)
```python
# app/__init__.py
from app.models import User
from app.views import index

__all__ = ['User', 'index']
```

**Usage:** Import from package directly
```python
from app import User, index
```

#### Pattern 3: Initialization Code (Our Implementation)
```python
# app/__init__.py
def create_app():
    # Setup code
    return app
```

**Usage:** Factory function creates app instances
```python
from app import create_app
app = create_app('development')
```

---

## Our Implementation

### File: `backend/app/__init__.py`

```python
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

# Initialize extensions (not yet bound to app)
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    """Application factory for creating Flask app instances."""
    app = Flask(__name__)
    
    # Load configuration from class
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Bind extensions to app
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register blueprints
    from app.api.health import health_bp
    app.register_blueprint(health_bp, url_prefix='/api')
    
    return app
```

### What This Exports

When you import from `app`, you get:

```python
from app import create_app    # Factory function
from app import db            # SQLAlchemy instance
from app import migrate       # Flask-Migrate instance
```

---

## Configuration Pattern Explained

### The Configuration Dictionary

**File:** `backend/config.py`

```python
class Config:
    """Base configuration."""
    SECRET_KEY = 'default-secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def init_app(app):
        """Override for config-specific initialization."""
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration registry
config = {
    'development': DevelopmentConfig,  # Class, not instance!
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

### How Configuration Loading Works

**Line:** `app.config.from_object(config[config_name])`

This single line does three things:

#### 1. Dictionary Lookup - `config[config_name]`

```python
config['development']  # Returns DevelopmentConfig class (not instance)
```

The dictionary stores **class references**, not instances.

#### 2. Class Introspection - `from_object(...)`

Flask's `from_object()` method:
1. Receives a class
2. Finds all UPPERCASE attributes
3. Copies them to `app.config` dictionary

**Example:**
```python
class DevelopmentConfig:
    DEBUG = True                    # ✅ UPPERCASE → copied
    SQLALCHEMY_DATABASE_URI = "..." # ✅ UPPERCASE → copied
    
    @staticmethod                   # ❌ Not uppercase → ignored
    def init_app(app):
        pass
```

**Result:**
```python
app.config['DEBUG'] == True
app.config['SQLALCHEMY_DATABASE_URI'] == "sqlite:///dev.db"
```

#### 3. Custom Initialization - `init_app(app)`

**Line:** `config[config_name].init_app(app)`

Calls the class method for environment-specific setup:

```python
DevelopmentConfig.init_app(app)  # Usually does nothing
ProductionConfig.init_app(app)   # Adds logging, monitoring, etc.
```

Since `init_app` is a `@staticmethod`, it can be called directly on the class.

---

## Benefits of This Pattern

### 1. Multiple Application Instances

Create different configs for different purposes:

```python
# Development server
app_dev = create_app('development')

# Testing
app_test = create_app('testing')

# Production
app_prod = create_app('production')
```

### 2. Avoids Circular Imports

Extensions are created but not bound until `create_app()` runs:

```python
# In app/__init__.py
db = SQLAlchemy()  # Created, but not bound to app

def create_app():
    db.init_app(app)  # Bound when app is created
```

This allows models to import `db` without circular dependency:

```python
# In app/models/project.py
from app import db  # ✅ Works! db exists, just not bound yet

class Project(db.Model):
    pass
```

### 3. Testing Benefits

Each test can get a fresh, isolated app instance:

```python
@pytest.fixture
def app():
    """Create a test app instance."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
```

### 4. Configuration Inheritance

Configs use class inheritance for DRY principle:

```python
class Config:
    SECRET_KEY = 'base-secret'  # Common to all

class DevelopmentConfig(Config):
    DEBUG = True  # Dev-specific, inherits SECRET_KEY

class ProductionConfig(Config):
    DEBUG = False  # Prod-specific, inherits SECRET_KEY
```

---

## Usage Examples

### Development Server

**File:** `backend/run.py`

```python
from app import create_app

app = create_app('development')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Testing

**File:** `backend/tests/conftest.py`

```python
import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
```

### Production Deployment

```python
# WSGI entry point (e.g., wsgi.py)
from app import create_app

app = create_app('production')
```

---

## Key Python Concepts

### 1. Classes as First-Class Objects

In Python, classes are objects that can be stored in variables/dictionaries:

```python
config = {
    'development': DevelopmentConfig  # The class itself
}

MyClass = config['development']  # Get the class
instance = MyClass()             # Create an instance
```

### 2. Attribute Introspection

Python can inspect objects to find their attributes:

```python
class MyClass:
    SETTING = 'value'

# Get all attributes
attrs = dir(MyClass)

# Get specific attribute
value = getattr(MyClass, 'SETTING')  # Returns 'value'
```

Flask's `from_object()` uses this to copy UPPERCASE attributes.

### 3. Static Methods

Static methods belong to the class, not instances:

```python
class Config:
    @staticmethod
    def init_app(app):
        pass

# Call without creating an instance
Config.init_app(app)  # ✅ Works
```

---

## Common Questions

### Q: Why not just use a dictionary for config?

**Answer:** Classes provide:
- Inheritance (share common settings)
- Type hints and IDE support
- Custom initialization methods (`init_app`)
- Better organization

### Q: Why create extensions outside `create_app()`?

**Answer:** So models can import them:

```python
# app/__init__.py
db = SQLAlchemy()  # Created here

# app/models/project.py
from app import db  # Models can import db

class Project(db.Model):
    pass
```

If `db` was created inside `create_app()`, models couldn't import it.

### Q: When does `init_app()` run?

**Answer:** Every time `create_app()` is called:

```python
def create_app(config_name):
    # ... setup ...
    config[config_name].init_app(app)  # Runs here
    return app
```

This allows environment-specific initialization.

---

## Further Reading

- [Flask Application Factories](https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/)
- [Flask Configuration Handling](https://flask.palletsprojects.com/en/3.0.x/config/)
- [Python Packages and __init__.py](https://docs.python.org/3/tutorial/modules.html#packages)
- [ADR-0001: Flask Backend Architecture](../../../decisions/ADR-0001-flask-backend-architecture.md)

---

**Last Updated:** 2025-12-02  
**Status:** ✅ Active Reference  
**Applies To:** Phase 0 and all subsequent phases

