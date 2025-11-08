@echo off
REM Quick Start Script for Docker Desktop Local Development
REM This script starts the multivendor platform locally

echo ========================================
echo   Multivendor Platform - Docker Setup
echo ========================================
echo.

REM Check if Docker is running
echo [1/4] Checking Docker Desktop...
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Desktop is not running!
    echo.
    echo Please:
    echo   1. Open Docker Desktop
    echo   2. Wait for it to fully start
    echo   3. Run this script again
    echo.
    pause
    exit /b 1
)
echo [OK] Docker Desktop is running
echo.

REM Create .env.local if it doesn't exist
echo [2/4] Checking environment configuration...
if not exist ".env.local" (
    echo Creating .env.local file...
    (
        echo # Local Development Environment Variables
        echo DB_ENGINE=django.db.backends.postgresql
        echo DB_NAME=multivendor_db
        echo DB_USER=postgres
        echo DB_PASSWORD=local_dev_password_123
        echo DB_HOST=db
        echo DB_PORT=5432
        echo SECRET_KEY=local-dev-secret-key-change-in-production-12345678910
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1,backend
        echo CORS_ALLOWED_ORIGINS=http://localhost,http://localhost:8080,http://localhost:3000
        echo CORS_ALLOW_ALL_ORIGINS=True
    ) > .env.local
    echo [OK] Created .env.local
) else (
    echo [OK] .env.local already exists
)
echo.

REM Stop any existing containers
echo [3/4] Stopping existing containers (if any)...
docker-compose -f docker-compose.local.yml down >nul 2>&1
echo [OK] Cleaned up existing containers
echo.

REM Start services
echo [4/4] Starting services...
echo.
echo ========================================
echo   Starting Docker Containers
echo ========================================
echo.
echo This will start:
echo   - PostgreSQL Database (port 5432)
echo   - Django Backend (port 8000)
echo   - Vue.js Frontend (port 8080)
echo.
echo First build may take 5-10 minutes...
echo Subsequent builds will be faster.
echo.
echo ========================================
echo.
echo Access your application at:
echo   Frontend:  http://localhost:8080
echo   Backend:   http://localhost:8000
echo   API:       http://localhost:8000/api/
echo   Admin:     http://localhost:8080/admin/
echo.
echo ========================================
echo.
echo Press Ctrl+C to stop all services
echo.
echo ========================================
echo.

docker-compose -f docker-compose.local.yml up --build

echo.
echo ========================================
echo   Services Stopped
echo ========================================
echo.
pause

