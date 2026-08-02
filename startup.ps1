#!/usr/bin/env pwsh
# HRMS System Startup Script for Windows

$ErrorActionPreference = 'Stop'

function Invoke-Compose {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)

    if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
        & docker-compose @Arguments
    }
    else {
        & docker compose @Arguments
    }

    if ($LASTEXITCODE -ne 0) {
        throw "Docker Compose command failed: $Arguments"
    }
}

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Enterprise HRMS System - Startup Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/5] Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($dockerVersion)) {
        throw "Docker not available"
    }
    Write-Host "[OK] Docker found: $dockerVersion" -ForegroundColor Green
}
catch {
    Write-Host "[FAIL] Docker is not available. Install Docker Desktop for Windows." -ForegroundColor Red
    exit 1
}

Write-Host "[2/5] Checking Docker daemon..." -ForegroundColor Yellow
try {
    docker ps > $null 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Docker daemon not running"
    }
    Write-Host "[OK] Docker daemon is running" -ForegroundColor Green
}
catch {
    Write-Host "[FAIL] Docker daemon is not running. Start Docker Desktop." -ForegroundColor Red
    exit 1
}

Write-Host "[3/5] Building Docker images..." -ForegroundColor Yellow
try {
    Invoke-Compose -Arguments @('build')
    Write-Host "[OK] Docker images built successfully" -ForegroundColor Green
}
catch {
    Write-Host "[FAIL] Failed to build Docker images" -ForegroundColor Red
    exit 1
}

Write-Host "[4/5] Starting Docker services..." -ForegroundColor Yellow
try {
    Invoke-Compose -Arguments @('up', '-d')
    Write-Host "[OK] Docker services started" -ForegroundColor Green
}
catch {
    Write-Host "[FAIL] Failed to start Docker services" -ForegroundColor Red
    exit 1
}

Write-Host "[5/5] Waiting for services to be ready..." -ForegroundColor Yellow
Write-Host "Waiting 30 seconds for services to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 30

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  HRMS System is Starting!" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$envPath = Join-Path $PSScriptRoot 'backend/.env'
$adminEmail = $env:ADMIN_EMAIL
$adminPassword = $env:ADMIN_PASSWORD

if (-not $adminEmail -and (Test-Path $envPath)) {
    $adminEmail = (Get-Content $envPath | Select-String '^ADMIN_EMAIL=' | ForEach-Object { ($_ -replace '^ADMIN_EMAIL=', '').Trim() })
}
if (-not $adminPassword -and (Test-Path $envPath)) {
    $adminPassword = (Get-Content $envPath | Select-String '^ADMIN_PASSWORD=' | ForEach-Object { ($_ -replace '^ADMIN_PASSWORD=', '').Trim() })
}

if (-not $adminEmail -or $adminEmail -like '<*>' -or $adminEmail -eq 'admin@example.com') {
    Write-Host "[WARN] ADMIN_EMAIL is not configured or uses a placeholder. Set ADMIN_EMAIL in backend/.env or environment before running init_db.py." -ForegroundColor Yellow
}
if (-not $adminPassword -or $adminPassword -like '<*>' -or $adminPassword -eq 'Admin@123') {
    Write-Host "[WARN] ADMIN_PASSWORD is not configured or uses a placeholder. init_db.py will generate a secure password if needed." -ForegroundColor Yellow
}

Write-Host "Initializing database..." -ForegroundColor Yellow
try {
    Invoke-Compose -Arguments @('exec', '-T', 'backend', 'python', 'init_db.py')
    Write-Host "[OK] Database initialized successfully" -ForegroundColor Green
}
catch {
    Write-Host "[WARN] Database initialization may need manual setup" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[OK] System startup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Access the application:" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost" -ForegroundColor White
Write-Host "  Backend API: http://localhost:5000/api" -ForegroundColor White
Write-Host ""
Write-Host "Admin credentials are loaded from backend/.env or environment variables." -ForegroundColor Cyan
Write-Host "Do not rely on hardcoded defaults in production." -ForegroundColor White
Write-Host ""
Write-Host "Useful Commands:" -ForegroundColor Cyan
Write-Host "  View logs: docker compose logs -f backend" -ForegroundColor White
Write-Host "  Stop system: docker compose down" -ForegroundColor White
Write-Host "  Restart system: docker compose restart" -ForegroundColor White
Write-Host ""
Write-Host "For more information see README.md" -ForegroundColor Cyan
Write-Host ""