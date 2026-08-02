#!/bin/bash
# HRMS System Startup Script for macOS/Linux

echo "================================================"
echo "  Enterprise HRMS System - Startup Script"
echo "================================================"
echo ""

# Check if Docker is installed
echo "[1/5] Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "✗ Docker not found. Please install Docker."
    exit 1
fi
echo "✓ Docker found: $(docker --version)"

# Check if Docker is running
echo "[2/5] Checking Docker daemon..."
if ! docker ps &> /dev/null; then
    echo "✗ Docker daemon is not running. Please start Docker."
    exit 1
fi
echo "✓ Docker daemon is running"

# Build Docker images
echo "[3/5] Building Docker images..."
echo "This may take a few minutes..."
docker-compose build
if [ $? -ne 0 ]; then
    echo "✗ Failed to build Docker images"
    exit 1
fi
echo "✓ Docker images built successfully"

# Start services
echo "[4/5] Starting Docker services..."
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "✗ Failed to start Docker services"
    exit 1
fi
echo "✓ Docker services started"

# Wait for services to be ready
echo "[5/5] Waiting for services to be ready..."
echo "Waiting 30 seconds for services to initialize..."
sleep 30

# Check if services are running
docker ps | grep -q "hrms-backend" && echo "✓ Backend container is running" || echo "✗ Backend container failed to start"

echo ""
echo "================================================"
echo "  HRMS System is Starting!"
echo "================================================"
echo ""

# Initialize database
echo "Initializing database..."
if [ -f backend/.env ]; then
    ADMIN_EMAIL=$(grep -E '^ADMIN_EMAIL=' backend/.env | cut -d'=' -f2- | tr -d '\r')
    ADMIN_PASSWORD=$(grep -E '^ADMIN_PASSWORD=' backend/.env | cut -d'=' -f2- | tr -d '\r')
fi

if [ -z "$ADMIN_EMAIL" ] || [[ "$ADMIN_EMAIL" == '<'* ]]; then
    echo "⚠ ADMIN_EMAIL is not configured. Set ADMIN_EMAIL in backend/.env or your environment before running init_db.py."
fi
if [ -z "$ADMIN_PASSWORD" ] || [[ "$ADMIN_PASSWORD" == '<'* ]]; then
    echo "⚠ ADMIN_PASSWORD is not configured or uses a placeholder. init_db.py will generate a secure password if needed."
fi

docker-compose exec backend python init_db.py
if [ $? -eq 0 ]; then
    echo "✓ Database initialized successfully"
else
    echo "⚠ Database initialization may need manual setup"
fi

echo ""
echo "✓ System startup complete!"
echo ""
echo "Access the application:"
echo "  Frontend: http://localhost"
echo "  Backend API: http://localhost:5000/api"
echo ""
echo "Admin credentials are loaded from backend/.env or environment variables."
echo "Do not rely on hardcoded defaults in production."
echo ""
echo "Useful Commands:"
echo "  View logs: docker-compose logs -f backend"
echo "  Stop system: docker-compose down"
echo "  Restart system: docker-compose restart"
echo ""
echo "For more information, see README.md"
echo ""
