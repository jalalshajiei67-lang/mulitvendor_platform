@echo off
REM Start Local Docker Testing in Background (Detached Mode)

echo ================================
echo   Starting in Background...
echo ================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Desktop is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

REM Create .env.local if it doesn't exist
if not exist ".env.local" (
    echo Creating .env.local file...
    (
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
)

echo Starting all services in background...
docker-compose --env-file .env.local -f docker-compose.local.yml up -d --build

echo.
echo [OK] Services starting...
echo.
echo To view logs:
echo   docker-compose -f docker-compose.local.yml logs -f
echo.
echo To stop:
echo   docker-compose -f docker-compose.local.yml down
echo.
echo Access at:
echo   Frontend: http://localhost:8080
echo   Backend:  http://localhost:8000
echo.

pause

