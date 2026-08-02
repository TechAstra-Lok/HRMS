# 🚀 HRMS System Launch Guide

## ⚡ Quick Start (5 Minutes)

### Step 1: Start Docker Desktop
1. Open **Docker Desktop** application
2. Wait for it to fully start (you'll see the Docker icon in the taskbar)
3. Verify it's running by opening PowerShell and running:
   ```powershell
   docker --version
   ```

### Step 2: Launch the System (Windows)
```powershell
# Open PowerShell as Administrator
cd "d:\Project\HRMS System"
.\startup.ps1
```

### Step 3: Access the Application
- **Frontend**: http://localhost (Port 80)
- **Backend API**: http://localhost:5000/api (Port 5000)
- **Database**: localhost:5432 (PostgreSQL)
- **Cache**: localhost:6379 (Redis)

### Step 4: Login
- **Email**: Use the value from `ADMIN_EMAIL` in `backend/.env`
- **Password**: Use the value from `ADMIN_PASSWORD` in `backend/.env`

---

## 📋 Detailed Step-by-Step Guide

### Prerequisites Installation

#### Windows
1. **Download Docker Desktop**
   - Go to https://www.docker.com/products/docker-desktop
   - Download for Windows
   - Install and restart your computer

2. **Verify Installation**
   ```powershell
   docker --version
   docker-compose --version
   ```

#### macOS
```bash
# Using Homebrew
brew install --cask docker

# Start Docker Desktop
open /Applications/Docker.app
```

#### Linux (Ubuntu/Debian)
```bash
# Install Docker
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
```

---

### Full Startup Process

#### Windows (PowerShell)

```powershell
# 1. Navigate to project directory
cd "d:\Project\HRMS System"

# 2. Verify Docker is running
docker ps

# 3. Build Docker images (first time only, takes 5-10 minutes)
docker-compose build

# 4. Start all services
docker-compose up -d

# 5. Wait 30 seconds for services to initialize
Start-Sleep -Seconds 30

# 6. Initialize database
docker-compose exec backend python init_db.py

# 7. Verify services are running
docker ps

# 8. Check service logs
docker-compose logs
```

#### macOS/Linux (Terminal)

```bash
# 1. Navigate to project directory
cd ~/HRMS\ System

# 2. Verify Docker is running
docker ps

# 3. Build Docker images (first time only, takes 5-10 minutes)
docker-compose build

# 4. Start all services
docker-compose up -d

# 5. Wait 30 seconds for services to initialize
sleep 30

# 6. Initialize database
docker-compose exec backend python init_db.py

# 7. Verify services are running
docker ps

# 8. Check service logs
docker-compose logs
```

---

## 🌐 Accessing the Application

### Frontend Application
- **URL**: http://localhost
- **Browser**: Any modern browser (Chrome, Firefox, Safari, Edge)
- **Default Resolution**: Responsive (mobile-friendly)

### Backend API
- **URL**: http://localhost:5000/api
- **Health Check**: http://localhost:5000/health
- **API Docs**: Endpoint documentation in `docs/api/`

### Database (Direct Access - Optional)
- **Host**: localhost
- **Port**: 5432
- **Database**: hrms
- **User**: postgres
- **Password**: postgres
- **Tool**: Use pgAdmin or DBeaver

### Redis Cache (Optional)
- **Host**: localhost
- **Port**: 6379
- **Tool**: Use Redis Desktop Manager or redis-cli

---

## 🔑 Default Login

| Field | Value |
|-------|-------|
| **Email** | Set `ADMIN_EMAIL` in `backend/.env` |
| **Password** | Set `ADMIN_PASSWORD` in `backend/.env` or leave blank to generate a secure password |
| **Role** | Super Admin |

> ⚠️ **IMPORTANT**: Use a strong password and rotate credentials before production deployment.

---

## 📊 Testing the System

### 1. Frontend Test
```
1. Go to http://localhost
2. You should see the HRMS login screen
3. Use the configured `ADMIN_EMAIL` and `ADMIN_PASSWORD`
4. Click Dashboard
5. Should see statistics and charts
```

### 2. API Test (Using cURL or Postman)
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "<ADMIN_EMAIL>",
    "password": "<ADMIN_PASSWORD>"
  }'

# Expected Response:
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "user": {
    "id": "...",
    "email": "<ADMIN_EMAIL>",
    "first_name": "Admin",
    "last_name": "User"
  },
  "tenant_id": "..."
}
```

### 3. Database Test
```bash
# Connect to PostgreSQL
psql -h localhost -U postgres -d hrms

# List tables
\dt

# Verify data
SELECT * FROM users LIMIT 5;
```

### 4. Real-time Test
```
1. Open browser DevTools (F12)
2. Go to Console tab
3. You should see WebSocket connection messages
4. Changes on one page should update in real-time
```

---

## 🛠️ Useful Commands

### Docker Management
```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View service logs
docker-compose logs -f backend

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Remove everything (clean slate)
docker-compose down -v
```

### Database Management
```bash
# Connect to database
docker-compose exec postgres psql -U postgres -d hrms

# Backup database
docker-compose exec postgres pg_dump -U postgres hrms > backup.sql

# Restore database
docker-compose exec -T postgres psql -U postgres hrms < backup.sql
```

### Backend Management
```bash
# View backend logs
docker-compose logs -f backend

# Execute Python command
docker-compose exec backend python -c "print('Hello')"

# Run tests
docker-compose exec backend pytest

# Run migrations (Alembic)
docker-compose exec backend alembic upgrade head
```

---

## 🐛 Troubleshooting

### Docker daemon not running
```powershell
# Windows - Open Docker Desktop application
# Should see whale icon in taskbar

# Verify
docker ps
```

### Port already in use
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Stop process (replace PID)
taskkill /PID 1234 /F

# Or change port in docker-compose.yml
```

### Database connection fails
```bash
# Check PostgreSQL container
docker-compose logs postgres

# Verify service health
docker-compose ps

# Restart services
docker-compose down
docker-compose up -d
```

### Permission denied (macOS/Linux)
```bash
# Make scripts executable
chmod +x startup.sh
chmod +x Makefile

# Or run with sudo
sudo docker-compose up
```

### Frontend shows blank page
```bash
# Check frontend container logs
docker-compose logs frontend

# Clear browser cache (Ctrl+Shift+Delete)
# Or try incognito mode
```

### API returns 502 Bad Gateway
```bash
# Wait a few more seconds for backend to start
sleep 30

# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

---

## 📈 System Performance

### Expected Performance (First Launch)
- Docker build time: 5-10 minutes
- Services startup: 30-60 seconds
- Frontend load time: < 2 seconds
- API response time: < 500ms
- Database query time: < 100ms

### Resources Required
- **RAM**: Minimum 4GB, Recommended 8GB
- **Disk**: Minimum 2GB for Docker images + data
- **CPU**: 2 cores minimum, 4+ cores recommended
- **Internet**: Required for Docker image download (first time)

---

## 🔐 Security Notes

### Before Production Deployment
1. **Change Secret Keys**
   ```env
   SECRET_KEY=<strong-random-key>
   JWT_SECRET_KEY=<strong-random-key>
   ENCRYPTION_KEY=<strong-random-key>
   ```

2. **Change Database Password**
   ```env
   POSTGRES_PASSWORD=<strong-password>
   ```

3. **Update CORS Origins**
   ```env
   CORS_ORIGINS=your-domain.com
   ```

4. **Enable HTTPS/SSL**
   - Generate SSL certificates
   - Update nginx configuration
   - Update docker-compose to use certificates

5. **Review Security Policies**
   - See `/docs/security/security_policy.md`
   - Check role-based access control
   - Review audit logging

---

## 📱 Mobile App Testing

### Android
```bash
cd mobile
npm install
npm run android
```

### iOS (macOS only)
```bash
cd mobile
npm install
npm run ios
```

### Configure API URL
Edit `mobile/src/api/client.ts`:
- Android: `10.0.2.2:5000` (Docker host)
- iOS: `localhost:5000` (Simulator) or `<your-ip>:5000` (Device)

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview and setup guide |
| `IMPLEMENTATION_SUMMARY.md` | Technical implementation details |
| `AUDIT_REPORT.md` | System audit findings |
| `CONTRIBUTING.md` | Development guidelines |
| `docs/api/` | API endpoint documentation |
| `docs/development/` | Development guides |
| `docs/guides/` | User and admin guides |

---

## 🎯 Next Steps

### Day 1 - Setup & Verify
- [ ] Start Docker Desktop
- [ ] Run startup script
- [ ] Login to system
- [ ] Verify all pages load
- [ ] Test API endpoints

### Day 2 - Explore Features
- [ ] Create test employees
- [ ] Test attendance check-in/out
- [ ] Apply for leave
- [ ] View payroll
- [ ] Check reports

### Day 3 - Configuration
- [ ] Update company settings
- [ ] Configure email notifications
- [ ] Set up biometric integration
- [ ] Configure backup strategy
- [ ] Set up monitoring

### Production Deployment
- [ ] Review AUDIT_REPORT.md
- [ ] Update all secret keys
- [ ] Configure SSL certificates
- [ ] Set up external database
- [ ] Configure Redis cluster
- [ ] Set up backup system
- [ ] Deploy to server

---

## 📞 Getting Help

### Common Resources
1. Check `README.md` for general information
2. See `AUDIT_REPORT.md` for known issues
3. Review error logs: `docker-compose logs`
4. Check API documentation in `docs/api/`

### If Something Goes Wrong
1. **Restart services**: `docker-compose restart`
2. **Check logs**: `docker-compose logs -f`
3. **Clean rebuild**: `docker-compose down -v && docker-compose build --no-cache`
4. **Check system requirements**: 8GB RAM, 2GB free disk

---

## ✅ Launch Checklist

Before launching, verify:
- [ ] Docker Desktop installed and running
- [ ] Docker Compose available
- [ ] Internet connection (for image download)
- [ ] Ports 80, 5000, 5432, 6379 are available
- [ ] At least 4GB RAM available
- [ ] At least 2GB free disk space

---

**You're all set! Launch the system and enjoy the Enterprise HRMS System! 🎉**

For questions or issues, refer to the documentation or check the audit report.
