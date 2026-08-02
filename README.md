# Enterprise HRMS - Complete HR Management System

A comprehensive, scalable, and modern Human Resource Management System built with Python (Flask), HTML/CSS/JavaScript, PostgreSQL, and Docker. Includes 3D visualizations, real-time updates via WebSocket, AI-powered analytics, and biometric integration.

## Features

### Core HR Functions
- **Employee Management**: Complete employee lifecycle from onboarding to exit
- **Attendance Tracking**: Real-time check-in/check-out with geolocation and biometric support
- **Leave Management**: Apply, approve, and track leave requests with automated workflows
- **Payroll Processing**: Automated salary calculation, tax computation, and payslip generation
- **Performance Management**: Performance reviews, goals tracking (OKR), and ratings

### Advanced Features
- **Multi-Tenancy**: Isolated tenant databases with complete data separation
- **3D Visualizations**: Three.js-powered 3D attendance analytics and organizational charts
- **Real-time Updates**: Socket.IO WebSocket integration for instant notifications
- **AI Analytics**: 
  - Employee churn prediction with risk factors and recommendations
  - NLP chatbot for HR queries
  - Resume parsing and skill extraction
- **Biometric Integration**: ZKTeco device support and facial recognition API integration
- **Mobile App**: React Native mobile application for iOS and Android
- **Advanced Reports**: Attendance, payroll, leave, and custom analytics reports

### Security & Compliance
- JWT-based authentication with refresh tokens
- Multi-Factor Authentication (MFA/TOTP)
- Role-Based Access Control (RBAC) with granular permissions
- End-to-end encryption for sensitive data
- Comprehensive audit logging
- Rate limiting and DDoS protection

## Technology Stack

### Backend
- **Framework**: Flask 2.3+
- **Database**: PostgreSQL 15+
- **Cache/Session**: Redis 7+
- **Task Queue**: Celery with Redis broker
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT with Flask-JWT-Extended
- **WebSocket**: Flask-SocketIO
- **Server**: Gunicorn with Gevent workers

### Frontend
- **HTML/CSS/JavaScript**: Vanilla (no framework)
- **3D Graphics**: Three.js for 3D visualizations
- **Charts**: Chart.js for analytics
- **Real-time**: Socket.IO client
- **Responsive Design**: CSS Grid/Flexbox
- **Icons**: Font Awesome 6+

### Mobile
- **Framework**: React Native
- **Language**: TypeScript
- **State Management**: Zustand
- **Navigation**: React Navigation
- **HTTP Client**: Axios

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes-ready
- **Web Server**: Nginx (frontend)
- **WSGI Server**: Gunicorn (backend)
- **Monitoring**: Built-in health checks
- **Backup**: Automated database backups

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 16+ (for frontend development)
- PostgreSQL 15+ (for local development)
- Redis 7+ (for local development)

### Using Docker Compose (Recommended)

```bash
# Clone repository
git clone <repository-url>
cd hrms-system

# Create environment file
cp backend/.env.example backend/.env

# Start all services
docker-compose up -d

# Configure backend environment
# Make sure ADMIN_EMAIL is set in backend/.env or your environment before running init_db.py.
# ADMIN_PASSWORD is optional; if omitted, a secure password is generated and written to backend logs.

# Initialize database
docker-compose exec backend python init_db.py

# Access application
# Frontend: http://localhost
# Backend API: http://localhost:5000/api
```
### Local Development Setup

#### Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb hrms
python init_db.py

# Run development server
python app.py
```

#### Frontend
```bash
cd frontend

# Install dependencies (optional, uses CDN)
npm install

# Start local server
npm run dev

# Access at http://localhost:3000
```

#### Mobile
```bash
cd mobile

# Install dependencies
npm install

# Run on Android
npm run android

# Run on iOS
npm run ios
```

## API Documentation

### Authentication Endpoints
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/mfa/setup` - Setup MFA
- `POST /api/auth/mfa/verify` - Verify MFA code

### Employee Endpoints
- `GET /api/employees` - List all employees
- `POST /api/employees` - Create new employee
- `GET /api/employees/<id>` - Get employee details
- `PUT /api/employees/<id>` - Update employee
- `DELETE /api/employees/<id>` - Delete employee

### Attendance Endpoints
- `POST /api/attendance/check-in` - Check in
- `POST /api/attendance/check-out` - Check out
- `GET /api/attendance/daily?date=YYYY-MM-DD` - Daily attendance
- `GET /api/attendance/reports` - Attendance reports

### Leave Endpoints
- `POST /api/leaves/apply` - Apply for leave
- `GET /api/leaves` - List leave requests
- `PUT /api/leaves/<id>/approve` - Approve leave
- `PUT /api/leaves/<id>/reject` - Reject leave

### Payroll Endpoints
- `POST /api/payroll/calculate` - Calculate payroll
- `GET /api/payroll?month=M&year=Y` - Get payroll
- `GET /api/payroll/<id>` - Get payroll details
- `GET /api/payroll/<id>/pdf` - Download payslip

### Dashboard Endpoints
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/dashboard/charts` - Chart data

## Database Schema

### Core Tables
- `tenants` - Tenant information
- `users` - User accounts
- `employees` - Employee records
- `attendance` - Attendance logs
- `leave_requests` - Leave applications
- `payroll` - Payroll records
- `audit_logs` - Audit trail
- `notifications` - User notifications
- `performance_reviews` - Performance evaluations
- `goals` - OKR/Goals tracking

## Configuration

### Environment Variables
```bash
# Application
APP_ENV=development|production|staging
DEBUG=True|False
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=604800
CSRF_TOKEN=your-csrf-token

# Email (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# AI (Optional)
OPENAI_API_KEY=your-openai-api-key

# Biometric (Optional)
BIOMETRIC_DEVICE_IP=192.168.1.100
BIOMETRIC_DEVICE_PORT=4370
```

## Deployment

### Production Deployment with Docker

```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Create superuser
docker-compose -f docker-compose.prod.yml exec backend python init_db.py
```

### Kubernetes Deployment
Helm charts available in `/infrastructure/kubernetes` for production deployment.

## Testing

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/unit -v
pytest tests/integration -v

# Run with coverage
pytest --cov=src tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - See LICENSE file for details

## Support

For issues and feature requests, please use the GitHub Issues tab.

## Roadmap

- [ ] Advanced Analytics Dashboard
- [ ] Machine Learning Models for Predictive Analytics
- [ ] Mobile App v2 (Flutter)
- [ ] Blockchain-based Certificate System
- [ ] IoT Integration for Advanced Biometric
- [ ] GraphQL API
- [ ] Microservices Architecture

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Load Balancer (Nginx)                     │
└──────────────┬──────────────────────────────────────┬────────┘
               │                                      │
       ┌───────▼────────┐                    ┌──────▼────────┐
       │  Frontend App  │                    │  API Backend  │
       │  (Nginx/SPA)   │                    │ (Gunicorn)    │
       └────────┬───────┘                    └──────┬────────┘
                │                                   │
       ┌────────┴────────────────────────────────────┴────────┐
       │                                                      │
   ┌───▼───────┐    ┌──────────┐    ┌────────┐    ┌────────┐
   │PostgreSQL │    │  Redis   │    │ Celery │    │ WebIO  │
   │ Database  │    │  Cache   │    │ Tasks  │    │ Sockets│
   └───────────┘    └──────────┘    └────────┘    └────────┘
```

---

**Version**: 1.0.0  
**Last Updated**: 2024
