# Flask + React Integration Research

**Status:** ✅ Complete  
**Priority:** 🔴 CRITICAL  
**Category:** Technology Stack  
**Timeline:** Week 1  
**Last Updated:** 2025-11-26

---

## 📋 Research Questions

1. How to serve React app from Flask in development?
2. What is the production deployment strategy?
3. How to configure CORS for local development?
4. What API authentication/authorization patterns should we use?
5. How to set up hot reload for optimal development experience?

---

## 🎯 Research Objectives

**Goal:** Establish seamless Flask + React integration that:
- Provides excellent developer experience (fast reload, easy debugging)
- Supports independent development of frontend and backend
- Handles CORS properly in development
- Prepares for simple production deployment
- Implements secure authentication when needed

---

## 🔍 Research Methodology

1. **Integration Pattern Analysis**
   - Development vs. production setup
   - CORS configuration options
   - Proxy vs. separate servers

2. **Best Practices Review**
   - Flask + React tutorials
   - Production deployment guides
   - Authentication patterns

3. **Tool Evaluation**
   - Development server options
   - Build and deployment tools

---

## 📚 Findings

### 1. Development Setup: Separate Servers (Recommended)

**Architecture:**

```
Development:
┌─────────────────┐         ┌──────────────────┐
│  React (Vite)   │         │  Flask API       │
│  localhost:5173 │◄────────│  localhost:5000  │
│  (Frontend)     │  CORS   │  (Backend)       │
└─────────────────┘ enabled └──────────────────┘
```

**Why Separate Servers:**

1. **Better Developer Experience**
   - Vite's fast HMR on port 5173
   - Flask debug mode on port 5000
   - Independent restarts
   - Better error messages

2. **Clear Separation**
   - Frontend and backend truly independent
   - Easier to debug
   - Matches production architecture

3. **Flexibility**
   - Can run frontend or backend alone
   - Easy to swap implementations
   - Better for team development (future)

**Flask Development Server:**

```python
# run.py
from app import create_app
import os

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
```

**Vite Development Server:**

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  }
})
```

**Benefits of Vite Proxy:**
- Frontend can use relative paths: `/api/tasks`
- No need to configure CORS in simple cases
- Simplifies frontend code
- Matches production URL structure

### 2. CORS Configuration

**For Development with Separate Servers:**

```python
# app/__init__.py
from flask_cors import CORS

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Configure CORS based on environment
    if app.config['ENV'] == 'development':
        # Allow React dev server
        CORS(app, origins=['http://localhost:5173'])
    else:
        # Production: serve from same origin
        CORS(app, origins=[app.config['FRONTEND_URL']])
    
    return app
```

**Alternative: More Granular CORS:**

```python
# For more control
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

**Best Practices:**
- Specific origins (not *)
- Limit methods to what's needed
- Specify allowed headers
- Different config for dev vs prod

### 3. API Communication Patterns

**Axios Base Configuration (Frontend):**

```javascript
// src/services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,  // 10 second timeout
})

// Request interceptor for auth tokens
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response
      
      if (status === 401) {
        // Unauthorized - redirect to login
        localStorage.removeItem('auth_token')
        window.location.href = '/login'
      } else if (status === 403) {
        // Forbidden
        console.error('Access denied')
      } else if (status === 500) {
        // Server error
        console.error('Server error:', data.error)
      }
    } else if (error.request) {
      // Request made but no response
      console.error('Network error - no response from server')
    } else {
      // Something else happened
      console.error('Error:', error.message)
    }
    
    return Promise.reject(error)
  }
)

export default api
```

**Environment Configuration:**

```bash
# frontend/.env.development
VITE_API_URL=http://localhost:5000/api

# frontend/.env.production
VITE_API_URL=/api
```

### 4. Authentication Strategy

**JWT Token Authentication (When Needed):**

**Backend Setup:**

```python
# app/__init__.py
from flask_jwt_extended import JWTManager

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or 'dev-jwt-secret'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    
    jwt = JWTManager(app)
    
    # Optional: Handle JWT errors
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return jsonify({'error': 'Missing or invalid token'}), 401
    
    return app

# app/api/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # For single-user MVP, simplified auth
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        access_token = create_access_token(identity={'id': user.id, 'username': user.username})
        return jsonify(access_token=access_token), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

# Protected route example
from flask_jwt_extended import jwt_required, get_jwt_identity

@tasks_bp.route('/', methods=['POST'])
@jwt_required()  # Only authenticated users
def create_task():
    current_user = get_jwt_identity()
    # ... create task ...
```

**Frontend Auth Service:**

```javascript
// src/services/authService.js
import api from './api'

export const authService = {
  login: async (username, password) => {
    const response = await api.post('/auth/login', { username, password })
    const { access_token } = response.data
    localStorage.setItem('auth_token', access_token)
    return access_token
  },
  
  logout: () => {
    localStorage.removeItem('auth_token')
    window.location.href = '/login'
  },
  
  isAuthenticated: () => {
    return !!localStorage.getItem('auth_token')
  }
}
```

**Note for MVP:** Authentication can be added later. Start with open API for simplicity (single-user local app).

### 5. Production Deployment Options

**Option 1: Flask Serves React (Simplest)**

```python
# Flask serves built React app
from flask import send_from_directory
import os

def create_app(config_name='development'):
    # Use static_folder to point to React build
    app = Flask(
        __name__,
        static_folder='../frontend/dist',  # Vite builds to 'dist'
        static_url_path=''
    )
    
    # ... register API blueprints ...
    
    # Catch-all route for React routing
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react(path):
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')
    
    return app
```

**Benefits:**
- Single server
- Simpler deployment
- No CORS issues
- Good for local use

**Option 2: Nginx Reverse Proxy (More Complex, Better for Scale)**

```nginx
server {
    listen 80;
    server_name localhost;
    
    # Serve React build files
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # Proxy API requests to Flask
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Benefits:**
- Better performance
- Can serve static files efficiently
- Better for future scaling

**Recommendation for MVP:** Option 1 (Flask serves React) - simpler, sufficient for single-user local app

### 6. Development Workflow

**Running Both Servers:**

**Terminal 1 - Flask Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
export FLASK_ENV=development
flask run
# Runs on http://localhost:5000
```

**Terminal 2 - React Frontend:**
```bash
cd frontend
npm run dev
# Runs on http://localhost:5173 with Vite
```

**Script for Convenience:**

```bash
# scripts/dev.sh
#!/bin/bash

# Start backend in background
cd backend
source venv/bin/activate
export FLASK_ENV=development
flask run &
FLASK_PID=$!

# Start frontend
cd ../frontend
npm run dev

# Cleanup on exit
trap "kill $FLASK_PID" EXIT
```

### 7. Error Handling & Debugging

**Consistent Error Response Format (Backend):**

```python
# app/utils/error_handlers.py
from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': str(error)
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'Resource not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500
```

**Frontend Error Handling:**

```javascript
// src/utils/errorHandler.js
export function handleApiError(error) {
  if (error.response) {
    // Server responded with error status
    const { status, data } = error.response
    
    switch (status) {
      case 400:
        return `Bad request: ${data.message}`
      case 401:
        return 'Please log in to continue'
      case 404:
        return 'Resource not found'
      case 500:
        return 'Server error. Please try again later.'
      default:
        return data.message || 'An error occurred'
    }
  } else if (error.request) {
    // Request made but no response
    return 'Cannot connect to server. Please check your connection.'
  } else {
    return error.message || 'An unexpected error occurred'
  }
}
```

### 8. Testing Integration

**Backend API Testing:**

```python
# tests/test_api.py
import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app('testing')
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_create_task(client):
    response = client.post('/api/tasks', json={
        'title': 'Test task',
        'priority': 'high'
    })
    
    assert response.status_code == 201
    assert response.json['title'] == 'Test task'
```

**Frontend Integration Testing:**

```javascript
// src/services/__tests__/tasksService.test.js
import { describe, it, expect, vi } from 'vitest'
import { tasksService } from '../tasksService'
import api from '../api'

vi.mock('../api')

describe('tasksService', () => {
  it('should fetch tasks', async () => {
    const mockTasks = [{ id: 1, title: 'Test' }]
    api.get.mockResolvedValue({ data: mockTasks })
    
    const result = await tasksService.getAll()
    
    expect(result).toEqual(mockTasks)
    expect(api.get).toHaveBeenCalledWith('/tasks', expect.anything())
  })
})
```

---

## 📊 Analysis

### Strengths of Recommended Approach

1. **Development Experience**
   - Fast HMR with Vite
   - Flask debug mode
   - Independent server restarts
   - Clear error messages

2. **Separation of Concerns**
   - Frontend and backend truly independent
   - Different tech stacks don't interfere
   - Easy to reason about

3. **Flexibility**
   - Can develop features independently
   - Easy to test in isolation
   - Simple to switch deployment strategies

4. **Production Ready**
   - Clean transition to production
   - Multiple deployment options
   - Scalable architecture

### Potential Challenges

1. **CORS Configuration**
   - Needs proper setup in development
   - Mitigation: Vite proxy handles most cases

2. **Two Servers to Manage**
   - More terminals/processes
   - Mitigation: Simple start script

3. **Port Configuration**
   - Need to manage ports
   - Mitigation: Standard conventions (5173, 5000)

---

## 💡 Recommendations

### 1. Development: Separate Servers with Vite Proxy

**Recommendation:** Run Flask on :5000, React on :5173 with Vite proxy

**Rationale:**
- Best developer experience
- Leverages Vite's performance
- Simple CORS via proxy
- Industry standard approach

**Setup:**
```javascript
// vite.config.js
export default defineConfig({
  server: {
    proxy: {
      '/api': 'http://localhost:5000'
    }
  }
})
```

### 2. Production: Flask Serves React Build

**Recommendation:** Flask serves Vite build output for single-user local deployment

**Rationale:**
- Simplest production setup
- Single server to run
- Perfect for single-user local app
- Easy to distribute

**Configuration:**
```python
app = Flask(
    __name__,
    static_folder='../frontend/dist',
    static_url_path=''
)
```

### 3. CORS Strategy

**Recommendation:** Use Vite proxy in development, same-origin in production

**Development:**
- Vite proxy handles API requests
- Minimal CORS configuration needed
- Flask allows localhost:5173

**Production:**
- Same-origin (Flask serves React)
- No CORS needed

### 4. Authentication Approach

**Recommendation:** Defer authentication for MVP, design for future JWT

**MVP:**
- No authentication (single-user local app)
- Focus on features, not security

**Future:**
- Add JWT authentication
- Already prepared in architecture
- Easy to add later

### 5. Environment Configuration

**Recommendation:** Use .env files for both Flask and React

**Backend .env:**
```bash
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///instance/workprod.db
JWT_SECRET_KEY=jwt-secret-key
```

**Frontend .env:**
```bash
VITE_API_URL=http://localhost:5000/api
```

---

## 🚀 Implementation Plan

### Phase 1: Backend Setup (Day 1)

1. **Create Flask App with CORS**
   - Configure CORS for development
   - Set up environment configuration
   - Test basic route

2. **Verify API Responses**
   - Test with curl or Postman
   - Verify JSON responses
   - Check CORS headers

### Phase 2: Frontend Setup (Day 1)

1. **Create Vite Project**
   - Initialize React app
   - Configure proxy
   - Set up environment variables

2. **Test Proxy Configuration**
   - Make API call from React
   - Verify proxy works
   - Check error handling

### Phase 3: Integration Testing (Day 2)

1. **End-to-End Test**
   - Create task from frontend
   - Verify in backend
   - Check database

2. **Error Flow Testing**
   - Test network errors
   - Test API errors
   - Verify error messages

### Phase 4: Production Build (Day 2)

1. **Build React for Production**
   ```bash
   cd frontend
   npm run build
   ```

2. **Configure Flask to Serve Build**
   - Point static_folder to dist
   - Add catch-all route
   - Test production mode

3. **Test Production Setup**
   - Run Flask in production mode
   - Verify React app loads
   - Test API calls work

---

## 📦 Deliverables

### 1. Integration Architecture Document

**Status:** ✅ This document

**Content:**
- Development setup (separate servers)
- Production deployment (Flask serves React)
- CORS configuration
- API communication patterns
- Authentication strategy (deferred)

### 2. Development Environment Setup

**Status:** 🔴 To Do

**Deliverable:**
- Complete setup instructions
- Configuration files (.env examples)
- Start scripts
- Troubleshooting guide

### 3. Integration Tests

**Status:** 🔴 To Do

**Deliverable:**
- Backend API tests
- Frontend service tests
- End-to-end integration tests

### 4. Production Build Configuration

**Status:** 🔴 To Do

**Deliverable:**
- Production configuration
- Build scripts
- Deployment instructions

---

## 🔗 References

### Official Documentation

- [Vite Proxy Documentation](https://vitejs.dev/config/server-options.html#server-proxy)
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Axios Documentation](https://axios-http.com/)

### Best Practices

- Flask + React integration tutorials
- CORS best practices
- JWT authentication patterns
- Production deployment guides

### Related Research

- [Flask Backend Architecture](flask-backend-architecture.md) - Complete
- [React Frontend Architecture](react-frontend-architecture.md) - Complete
- [SQLite Database Design](sqlite-database-design.md) - Complete

---

## ✅ Decision

**Decision:** Separate servers in development (Vite proxy), Flask serves React in production

**Development Architecture:**
- **Backend:** Flask on localhost:5000 with CORS enabled
- **Frontend:** Vite on localhost:5173 with proxy to :5000
- **Communication:** Axios with interceptors
- **Authentication:** Deferred to post-MVP

**Production Architecture:**
- **Single Server:** Flask serves React build + API
- **Static Files:** Flask serves Vite dist/ folder
- **Routing:** Flask catch-all routes to React
- **CORS:** Not needed (same origin)

**Key Technologies:**
- **CORS:** Flask-CORS for development
- **Proxy:** Vite proxy configuration
- **API Client:** Axios with interceptors
- **Environment:** python-dotenv + Vite env

**Implementation Priority:**
1. Set up development environment (separate servers)
2. Configure Vite proxy
3. Test API communication
4. Implement error handling
5. Production build configuration (later)
6. Authentication (post-MVP)

**Next Steps:**
1. Create development setup guide
2. Initialize both projects (Flask + Vite)
3. Configure proxy and CORS
4. Test integration with simple API endpoint
5. Implement first feature end-to-end

---

**Last Updated:** 2025-11-26  
**Status:** ✅ Complete  
**Next:** Update research register, begin implementation setup

