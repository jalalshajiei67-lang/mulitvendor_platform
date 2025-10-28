@echo off
REM Local Docker Testing Script for Windows
REM This script starts your multivendor platform locally with Docker Desktop

echo ================================
echo   Local Docker Testing
echo ================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Desktop is not running!
    echo Please start Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)

echo [OK] Docker Desktop is running
echo.

REM Create .env.local if it doesn't exist
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
    echo.
)

echo Starting services...
echo.
echo This will:
echo   - Start PostgreSQL database
echo   - Build and start Django backend
echo   - Build and start Vue.js frontend
echo.
echo Access your application at:
echo   Frontend: http://localhost:8080
echo   Backend:  http://localhost:8000
echo   API:      http://localhost:8000/api/
echo.
echo Press Ctrl+C to stop all services
echo.

docker-compose --env-file .env.local -f docker-compose.local.yml up --build

pause

