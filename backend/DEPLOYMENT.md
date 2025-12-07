# Production Deployment Guide

**Purpose:** Complete guide for deploying the Flask backend to production  
**Last Updated:** 2025-12-07  
**Status:** ✅ Ready for Production

---

## 📋 Prerequisites

Before deploying, ensure you have:

- ✅ Python 3.11+ installed
- ✅ Virtual environment created
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ✅ Database migrations ready
- ✅ Environment variables configured
- ✅ Production configuration verified

---

## 🚀 Deployment Steps

### 1. Prepare Deployment Environment

#### Set Up Server

```bash
# Create deployment directory
mkdir -p /opt/work-prod
cd /opt/work-prod

# Clone repository (or copy files)
git clone <repository-url> .
# Or: Copy project files to server

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt
```

#### Configure Environment Variables

Create `.env` file in `backend/` directory:

```bash
cd backend
cat > .env << EOF
APP_CONFIG=production
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
DATABASE_URL=sqlite:///instance/work_prod.db
CORS_ALLOWED_ORIGINS=https://yourdomain.com
EOF
```

**⚠️ Security:** Never commit `.env` to version control. Use secrets management in production.

---

### 2. Initialize Database

```bash
cd backend
source ../venv/bin/activate

# Set production config
export APP_CONFIG=production

# Initialize database
flask db upgrade

# Verify database created
ls -lh instance/work_prod.db
```

---

### 3. Test Production Configuration

```bash
# Test production config loading
python -c "from app import create_app; app = create_app('production'); print('DEBUG:', app.config['DEBUG']); print('DB:', app.config['SQLALCHEMY_DATABASE_URI'])"

# Expected output:
# DEBUG: False
# DB: sqlite:///.../instance/work_prod.db
```

---

### 4. Start Production Server

#### Option A: Using Gunicorn (Recommended)

```bash
# Install Gunicorn
pip install gunicorn

# Start server
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile - --error-logfile - "app:create_app('production')"
```

**Gunicorn Options:**
- `-w 4`: 4 worker processes
- `-b 0.0.0.0:5000`: Bind to all interfaces on port 5000
- `--access-logfile -`: Log access to stdout
- `--error-logfile -`: Log errors to stdout

#### Option B: Using Production Startup Script

```bash
# Use provided startup script
cd backend
./start_production.sh
```

#### Option C: Using Systemd Service

See [Systemd Service Setup](#systemd-service-setup) section below.

---

### 5. Verify Deployment

```bash
# Health check
curl http://localhost:5000/api/health

# Expected response:
# {"status":"ok","message":"Flask backend is running"}

# Test API endpoint
curl http://localhost:5000/api/projects
```

---

## 🔧 Production Server Options

### Gunicorn (Recommended)

**Why Gunicorn:**
- Production-ready WSGI server
- Handles multiple worker processes
- Better performance than Flask dev server
- Process management and auto-restart

**Installation:**
```bash
pip install gunicorn
```

**Basic Usage:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app('production')"
```

**With Logging:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 \
  --access-logfile /var/log/work-prod/access.log \
  --error-logfile /var/log/work-prod/error.log \
  --log-level info \
  "app:create_app('production')"
```

### Waitress (Windows Alternative)

**Why Waitress:**
- Cross-platform WSGI server
- Good for Windows deployments
- Production-ready

**Installation:**
```bash
pip install waitress
```

**Usage:**
```bash
waitress-serve --host=0.0.0.0 --port=5000 "app:create_app('production')"
```

### uWSGI (Advanced)

**Why uWSGI:**
- High performance
- Advanced features
- More complex configuration

**Installation:**
```bash
pip install uwsgi
```

**Usage:**
```bash
uwsgi --http 0.0.0.0:5000 --module app:create_app('production') --processes 4
```

---

## 📝 Production Startup Script

Create `backend/start_production.sh`:

```bash
#!/bin/bash
# Production startup script for Flask backend

set -e  # Exit on error

# Change to backend directory
cd "$(dirname "$0")"

# Activate virtual environment
source ../venv/bin/activate

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Ensure production config
export APP_CONFIG=production

# Verify database exists
if [ ! -f instance/work_prod.db ]; then
    echo "Initializing database..."
    flask db upgrade
fi

# Start Gunicorn
exec gunicorn \
    -w 4 \
    -b 0.0.0.0:5000 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --timeout 120 \
    "app:create_app('production')"
```

**Make executable:**
```bash
chmod +x backend/start_production.sh
```

---

## 🔄 Systemd Service Setup

Create `/etc/systemd/system/work-prod.service`:

```ini
[Unit]
Description=Work Productivity Flask Backend
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/work-prod/backend
Environment="PATH=/opt/work-prod/venv/bin"
Environment="APP_CONFIG=production"
EnvironmentFile=/opt/work-prod/backend/.env
ExecStart=/opt/work-prod/venv/bin/gunicorn \
    -w 4 \
    -b 127.0.0.1:5000 \
    --access-logfile /var/log/work-prod/access.log \
    --error-logfile /var/log/work-prod/error.log \
    --log-level info \
    --timeout 120 \
    "app:create_app('production')"
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and Start:**
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable work-prod

# Start service
sudo systemctl start work-prod

# Check status
sudo systemctl status work-prod

# View logs
sudo journalctl -u work-prod -f
```

---

## 📊 Production Monitoring

### Health Check Endpoint

**Endpoint:** `GET /api/health`

**Usage:**
```bash
# Basic health check
curl http://localhost:5000/api/health

# With monitoring tool
# Configure monitoring to check this endpoint every 30 seconds
```

**Response:**
```json
{
  "status": "ok",
  "message": "Flask backend is running"
}
```

### Logging

**Log Location:**
- Systemd: `journalctl -u work-prod`
- Gunicorn: `/var/log/work-prod/access.log` and `/var/log/work-prod/error.log`
- Application: stdout/stderr (captured by systemd or process manager)

**Log Levels:**
- `INFO`: Normal operation
- `WARNING`: Non-critical issues
- `ERROR`: Errors with full exception context

**Log Format:**
```
[2025-12-07 12:34:56] INFO in projects: Importing 10 projects
[2025-12-07 12:34:57] WARNING in projects: IntegrityError importing project Example
[2025-12-07 12:34:58] ERROR in projects: Unexpected error in create_project: ...
```

### Monitoring Checklist

- [ ] Health check endpoint responding
- [ ] Logs being captured and rotated
- [ ] Error logs monitored for issues
- [ ] Database size monitored
- [ ] Response times monitored (< 100ms target)
- [ ] Disk space monitored
- [ ] Memory usage monitored

---

## 🔒 Security Checklist

- [ ] `SECRET_KEY` is set to secure random value
- [ ] `SECRET_KEY` is NOT in version control
- [ ] `APP_CONFIG=production` is set
- [ ] `DEBUG=False` in production (enforced)
- [ ] `CORS_ALLOWED_ORIGINS` is set appropriately
- [ ] Database file permissions secured (600 recommended)
- [ ] Server firewall configured
- [ ] HTTPS configured (via reverse proxy)
- [ ] Environment variables secured
- [ ] Logs don't contain sensitive information

---

## 🔄 Database Migrations

### Running Migrations in Production

```bash
cd backend
source ../venv/bin/activate
export APP_CONFIG=production

# Apply migrations
flask db upgrade

# Verify migration status
flask db current
```

### Migration Best Practices

1. **Test migrations in staging first**
2. **Backup database before migration**
3. **Run migrations during maintenance window**
4. **Verify application works after migration**
5. **Keep migration files in version control**

### Backup Database

```bash
# SQLite backup
cp backend/instance/work_prod.db backend/instance/work_prod.db.backup

# Or use SQLite backup command
sqlite3 backend/instance/work_prod.db ".backup backend/instance/work_prod.db.backup"
```

---

## 🌐 Reverse Proxy Setup (Nginx)

### Nginx Configuration

Create `/etc/nginx/sites-available/work-prod`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL certificates (Let's Encrypt recommended)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Proxy to Flask backend
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check endpoint
    location /api/health {
        proxy_pass http://127.0.0.1:5000/api/health;
        access_log off;
    }
}
```

**Enable Site:**
```bash
sudo ln -s /etc/nginx/sites-available/work-prod /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 📋 Deployment Checklist

### Pre-Deployment

- [ ] Code reviewed and tested
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] Production configuration verified
- [ ] Security checklist complete
- [ ] Backup strategy in place

### Deployment

- [ ] Server prepared (Python, venv, dependencies)
- [ ] Database initialized (`flask db upgrade`)
- [ ] Production server started (Gunicorn/systemd)
- [ ] Health check passing (`/api/health`)
- [ ] API endpoints responding
- [ ] Logs being captured
- [ ] Monitoring configured

### Post-Deployment

- [ ] Health check verified
- [ ] API endpoints tested
- [ ] Logs reviewed for errors
- [ ] Monitoring alerts configured
- [ ] Documentation updated
- [ ] Team notified of deployment

---

## 🐛 Troubleshooting

### Server Won't Start

**Check:**
```bash
# Check logs
sudo journalctl -u work-prod -n 50

# Check port availability
sudo lsof -i :5000

# Verify environment variables
env | grep APP_CONFIG
env | grep SECRET_KEY
```

### Database Errors

**Check:**
```bash
# Verify database exists
ls -lh backend/instance/work_prod.db

# Check database permissions
ls -l backend/instance/

# Test database connection
sqlite3 backend/instance/work_prod.db "SELECT 1;"
```

### High Memory Usage

**Solutions:**
- Reduce Gunicorn workers (`-w 2` instead of `-w 4`)
- Monitor memory usage
- Consider upgrading server resources

---

## 📚 Related Documentation

- **[Production Configuration Guide](PRODUCTION.md)** - Environment variables and configuration
- **[Backend README](README.md)** - Backend documentation
- **[OpenAPI Specification](openapi.yaml)** - API documentation

---

**Last Updated:** 2025-12-07  
**Status:** ✅ Ready for Production

