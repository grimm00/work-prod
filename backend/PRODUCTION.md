# Production Configuration Guide

**Purpose:** Guide for configuring the Flask backend for production deployment  
**Last Updated:** 2025-12-07

---

## 📋 Environment Variables

### Required Variables

#### `SECRET_KEY` (REQUIRED in production)

**Purpose:** Flask secret key for session management and security  
**Example:** `SECRET_KEY=your-secret-key-here-change-in-production`

**Generate a secure key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**⚠️ Security:** Never commit SECRET_KEY to version control. Use environment variables or secrets management.

---

### Optional Variables

#### `APP_CONFIG`

**Purpose:** Application configuration mode  
**Options:** `development`, `testing`, `production`  
**Default:** `development` (falls back to `FLASK_ENV` if set)

**Example:**
```bash
APP_CONFIG=production
```

**Note:** `APP_CONFIG` takes precedence over `FLASK_ENV` if both are set.

---

#### `FLASK_ENV` (Deprecated)

**Purpose:** Legacy Flask environment variable  
**Options:** `development`, `production`  
**Default:** `development`

**⚠️ Deprecated:** Use `APP_CONFIG` instead. `APP_CONFIG` takes precedence if both are set.

---

#### `DATABASE_URL`

**Purpose:** Database connection string  
**Default:** SQLite database at `backend/instance/work_prod.db`

**SQLite (default):**
```bash
DATABASE_URL=sqlite:///instance/work_prod.db
```

**PostgreSQL:**
```bash
DATABASE_URL=postgresql://user:password@localhost/dbname
```

**MySQL:**
```bash
DATABASE_URL=mysql://user:password@localhost/dbname
```

**Note:** For production, consider using PostgreSQL or MySQL instead of SQLite for better concurrency and performance.

---

#### `CORS_ALLOWED_ORIGINS`

**Purpose:** Comma-separated list of allowed CORS origins  
**Default:** Empty (no CORS allowed)

**Example:**
```bash
CORS_ALLOWED_ORIGINS=https://example.com,https://app.example.com
```

**Development:** CORS is automatically configured for `localhost:5173` and `localhost:3000`  
**Production:** Must be explicitly set if frontend is on different domain

---

## 🔧 Configuration Setup

### 1. Create `.env` File

Create a `.env` file in the `backend/` directory:

```bash
cd backend
cp .env.example .env  # If .env.example exists
# Or create .env manually
```

### 2. Set Environment Variables

**Option A: Using `.env` file (Development)**

Create `backend/.env`:
```bash
APP_CONFIG=production
SECRET_KEY=your-generated-secret-key-here
DATABASE_URL=sqlite:///instance/work_prod.db
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

**Option B: Using System Environment Variables (Production)**

Set environment variables in your deployment platform:
- Heroku: `heroku config:set SECRET_KEY=...`
- Docker: Use `-e` flags or `docker-compose.yml`
- Systemd: Use `Environment=` in service file
- Cloud platforms: Use platform-specific secrets management

### 3. Verify Configuration

Test configuration loading:
```bash
cd backend
source ../venv/bin/activate
python -c "from app import create_app; app = create_app('production'); print('Config loaded:', app.config['DEBUG'])"
```

Should output: `Config loaded: False`

---

## 📝 Example `.env` File

```bash
# Flask Application Configuration
# DO NOT commit this file to version control

# Application Configuration
APP_CONFIG=production

# Secret Key (REQUIRED in production)
# Generate with: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-secret-key-here-change-in-production

# Database Configuration
DATABASE_URL=sqlite:///instance/work_prod.db

# CORS Configuration (Production)
# Comma-separated list of allowed origins
CORS_ALLOWED_ORIGINS=https://example.com,https://app.example.com
```

---

## 🔒 Security Checklist

- [ ] `SECRET_KEY` is set to a secure random value
- [ ] `SECRET_KEY` is NOT committed to version control
- [ ] `APP_CONFIG=production` is set
- [ ] `DEBUG=False` in production (enforced by ProductionConfig)
- [ ] `CORS_ALLOWED_ORIGINS` is set appropriately (not too permissive)
- [ ] Database credentials are secure (if using PostgreSQL/MySQL)
- [ ] Environment variables are managed through secrets management

---

## 📊 Logging Configuration

### Production Logging

Production configuration automatically sets up logging:

- **Log Level:** INFO (set in `ProductionConfig.init_app()`)
- **Handler:** StreamHandler (logs to stdout/stderr)
- **Format:** `[%(asctime)s] %(levelname)s in %(module)s: %(message)s`

**Log Levels Used:**
- `INFO`: Normal operation messages
- `WARNING`: Non-critical issues (e.g., IntegrityError during import)
- `ERROR`: Errors with full exception context (using `exc_info=True`)

**Example Log Output:**
```
[2025-12-07 12:34:56] INFO in projects: Importing 10 projects
[2025-12-07 12:34:57] WARNING in projects: IntegrityError importing project Example: duplicate path
[2025-12-07 12:34:58] ERROR in projects: Unexpected error in create_project: ...
```

### Log Rotation

For production deployments, configure log rotation at the system level:

**Systemd:**
```ini
[Service]
StandardOutput=journal
StandardError=journal
```

**Docker:**
Use logging driver with rotation:
```bash
docker run --log-driver json-file --log-opt max-size=10m --log-opt max-file=3 ...
```

**Manual Rotation:**
Use `logrotate` or similar tools to rotate application logs.

---

## 🚨 Error Handling

### Production Error Responses

**Client-Facing Errors:**
- `400 Bad Request`: Validation errors (clear, user-friendly messages)
- `404 Not Found`: Resource not found
- `409 Conflict`: Duplicate path or integrity error
- `500 Internal Server Error`: Generic error (no sensitive details leaked)

**Server Logging:**
- All errors are logged with full exception context (`exc_info=True`)
- Sensitive information is NOT included in client responses
- Error messages are user-friendly and actionable

**Example Error Handling:**
```python
try:
    # Operation
except Exception as e:
    current_app.logger.error(f"Unexpected error: {e}", exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500
```

---

## 🧪 Testing Configuration

### Verify Production Configuration

```bash
# Test production config loading
python -c "from app import create_app; app = create_app('production'); print('DEBUG:', app.config['DEBUG']); print('DB:', app.config['SQLALCHEMY_DATABASE_URI'])"

# Expected output:
# DEBUG: False
# DB: sqlite:///.../instance/work_prod.db
```

### Test Environment Variables

```bash
# Test SECRET_KEY
export SECRET_KEY=test-key
python -c "from app import create_app; app = create_app('production'); print('Secret set:', bool(app.config['SECRET_KEY']))"

# Test DATABASE_URL
export DATABASE_URL=sqlite:///test.db
python -c "from app import create_app; app = create_app('production'); print('DB URL:', app.config['SQLALCHEMY_DATABASE_URI'])"
```

---

## 🚀 Deployment Checklist

### Pre-Deployment

- [ ] `SECRET_KEY` generated and set
- [ ] `APP_CONFIG=production` set
- [ ] `DATABASE_URL` configured (if not using default SQLite)
- [ ] `CORS_ALLOWED_ORIGINS` set (if frontend on different domain)
- [ ] Database migrations applied (`flask db upgrade`)
- [ ] Logging configured (automatic in ProductionConfig)
- [ ] Error handling verified (no sensitive data leaked)

### Post-Deployment

- [ ] Health check endpoint responds (`GET /api/health`)
- [ ] Logs are being captured and rotated
- [ ] Error responses are user-friendly
- [ ] No sensitive information in error messages
- [ ] CORS is configured correctly (if frontend deployed)

---

## 📚 Related Documentation

- **Configuration Code:** `backend/config.py`
- **Application Factory:** `backend/app/__init__.py`
- **API Documentation:** `backend/README.md`
- **OpenAPI Spec:** `backend/openapi.yaml`

---

**Last Updated:** 2025-12-07  
**Status:** ✅ Complete

