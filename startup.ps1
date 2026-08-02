#!/usr/bin/env pwsh
# HRMS System Startup Script for Windows

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Enterprise HRMS System - Startup Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
Write-Host "[1/5] Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker not found. Please install Docker Desktop for Windows." -ForegroundColor Red
    exit 1
}

# Check if Docker is running
Write-Host "[2/5] Checking Docker daemon..." -ForegroundColor Yellow
try {
    docker ps > $null
    Write-Host "✓ Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker daemon is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Build Docker images
Write-Host "[3/5] Building Docker images..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Cyan
docker-compose build
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to build Docker images" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Docker images built successfully" -ForegroundColor Green

# Start services
Write-Host "[4/5] Starting Docker services..." -ForegroundColor Yellow
docker-compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to start Docker services" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Docker services started" -ForegroundColor Green

# Wait for services to be ready
Write-Host "[5/5] Waiting for services to be ready..." -ForegroundColor Yellow
Write-Host "Waiting 30 seconds for services to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 30

# Check if services are running
$postgresHealth = docker-compose exec -T postgres pg_isready -U postgres 2>&1
$redisHealth = docker-compose exec -T redis redis-cli ping 2>&1
$backendHealth = docker ps | Select-String "hrms-backend"

if ($postgresHealth -match 'accepting connections') {
    Write-Host "✓ Postgres is ready" -ForegroundColor Green
} else {
    Write-Host "✗ Postgres is not ready: $postgresHealth" -ForegroundColor Red
}

if ($redisHealth -eq 'PONG') {
    Write-Host "✓ Redis is ready" -ForegroundColor Green
} else {
    Write-Host "✗ Redis is not ready: $redisHealth" -ForegroundColor Red
}

if ($backendHealth) {
    Write-Host "✓ Backend container is running" -ForegroundColor Green
} else {
    Write-Host "✗ Backend container failed to start" -ForegroundColor Red
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  HRMS System is Starting!" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check admin credential configuration
$envPath = Join-Path $PSScriptRoot 'backend\.env'
$adminEmail = $env:ADMIN_EMAIL
$adminPassword = $env:ADMIN_PASSWORD
if (-not $adminEmail -and (Test-Path $envPath)) {
    $adminEmail = (Get-Content $envPath | Select-String '^ADMIN_EMAIL=' | ForEach-Object { $_ -replace '^ADMIN_EMAIL=', '' }).Trim()
}
if (-not $adminPassword -and (Test-Path $envPath)) {
    $adminPassword = (Get-Content $envPath | Select-String '^ADMIN_PASSWORD=' | ForEach-Object { $_ -replace '^ADMIN_PASSWORD=', '' }).Trim()
}

if (-not $adminEmail -or $adminEmail -like '<*>' -or $adminEmail -eq 'admin@example.com') {
    Write-Host "⚠ ADMIN_EMAIL is not configured or uses a placeholder. Set ADMIN_EMAIL in backend/.env or environment before running init_db.py." -ForegroundColor Yellow
}
if (-not $adminPassword -or $adminPassword -like '<*>' -or $adminPassword -eq 'Admin@123') {
    Write-Host "⚠ ADMIN_PASSWORD is not configured or uses a placeholder. init_db.py will generate a secure password if needed." -ForegroundColor Yellow
}

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Yellow
docker-compose exec -T backend python init_db.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Database initialized successfully" -ForegroundColor Green
} else {
    Write-Host "⚠ Database initialization may need manual setup" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✓ System startup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Access the application:" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost" -ForegroundColor White
Write-Host "  Backend API: http://localhost:5000/api" -ForegroundColor White
Write-Host ""
Write-Host "Admin credentials are loaded from backend/.env or environment variables." -ForegroundColor Cyan
Write-Host "Do not rely on hardcoded defaults in production." -ForegroundColor White
Write-Host ""
Write-Host "Useful Commands:" -ForegroundColor Cyan
Write-Host "  View logs: docker-compose logs -f backend" -ForegroundColor White
Write-Host "  Stop system: docker-compose down" -ForegroundColor White
Write-Host "  Restart system: docker-compose restart" -ForegroundColor White
Write-Host ""
Write-Host "For more information see README.md" -ForegroundColor Cyan
Write-Host ""