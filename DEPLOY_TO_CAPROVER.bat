@echo off
REM ============================================
REM   CapRover Deployment Script
REM   Deploys both backend and frontend
REM ============================================

echo.
echo ================================================
echo   CAPROVER DEPLOYMENT SCRIPT
echo ================================================
echo.

REM Check if caprover is installed
where caprover >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] CapRover CLI is not installed!
    echo.
    echo Please install it first:
    echo   npm install -g caprover
    echo.
    pause
    exit /b 1
)

echo [INFO] CapRover CLI found!
echo.

REM Show menu
echo What would you like to deploy?
echo.
echo 1. Backend only
echo 2. Frontend only
echo 3. Both (Backend + Frontend)
echo 4. Check app logs
echo 5. Run Django migrations
echo 6. Collect static files
echo 7. Create superuser
echo 8. Exit
echo.

set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto deploy_backend
if "%choice%"=="2" goto deploy_frontend
if "%choice%"=="3" goto deploy_both
if "%choice%"=="4" goto check_logs
if "%choice%"=="5" goto run_migrations
if "%choice%"=="6" goto collect_static
if "%choice%"=="7" goto create_superuser
if "%choice%"=="8" goto end

echo [ERROR] Invalid choice!
pause
exit /b 1

:deploy_backend
echo.
echo ================================================
echo   DEPLOYING BACKEND
echo ================================================
echo.
caprover deploy -a multivendor-backend
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Backend deployment failed!
    pause
    exit /b 1
)
echo.
echo [SUCCESS] Backend deployed successfully!
goto end_success

:deploy_frontend
echo.
echo ================================================
echo   DEPLOYING FRONTEND
echo ================================================
echo.
caprover deploy -a multivendor-frontend
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Frontend deployment failed!
    pause
    exit /b 1
)
echo.
echo [SUCCESS] Frontend deployed successfully!
goto end_success

:deploy_both
echo.
echo ================================================
echo   DEPLOYING BACKEND
echo ================================================
echo.
caprover deploy -a multivendor-backend
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Backend deployment failed!
    pause
    exit /b 1
)
echo.
echo [SUCCESS] Backend deployed successfully!
echo.
echo ================================================
echo   DEPLOYING FRONTEND
echo ================================================
echo.
caprover deploy -a multivendor-frontend
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Frontend deployment failed!
    pause
    exit /b 1
)
echo.
echo [SUCCESS] Both apps deployed successfully!
goto end_success

:check_logs
echo.
echo Which app logs do you want to check?
echo 1. Backend
echo 2. Frontend
echo 3. Database
echo.
set /p log_choice="Enter your choice (1-3): "

if "%log_choice%"=="1" (
    echo.
    echo ================================================
    echo   BACKEND LOGS
    echo ================================================
    echo.
    caprover apps:logs multivendor-backend
)
if "%log_choice%"=="2" (
    echo.
    echo ================================================
    echo   FRONTEND LOGS
    echo ================================================
    echo.
    caprover apps:logs multivendor-frontend
)
if "%log_choice%"=="3" (
    echo.
    echo ================================================
    echo   DATABASE LOGS
    echo ================================================
    echo.
    caprover apps:logs postgres-db
)
goto end

:run_migrations
echo.
echo ================================================
echo   RUNNING DJANGO MIGRATIONS
echo ================================================
echo.
caprover apps:exec multivendor-backend --command "python manage.py migrate"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Migration failed!
    pause
    exit /b 1
)
echo.
echo [SUCCESS] Migrations completed!
goto end_success

:collect_static
echo.
echo ================================================
echo   COLLECTING STATIC FILES
echo ================================================
echo.
caprover apps:exec multivendor-backend --command "python manage.py collectstatic --noinput --clear"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Collect static failed!
    pause
    exit /b 1
)
echo.
echo [SUCCESS] Static files collected!
goto end_success

:create_superuser
echo.
echo ================================================
echo   CREATE DJANGO SUPERUSER
echo ================================================
echo.
echo This will open an interactive prompt...
echo.
caprover apps:exec multivendor-backend --command "python manage.py createsuperuser"
echo.
goto end

:end_success
echo.
echo ================================================
echo   DEPLOYMENT COMPLETE!
echo ================================================
echo.
echo Your apps should be accessible at:
echo   Frontend: https://indexo.ir
echo   Backend:  https://multivendor-backend.indexo.ir
echo   Admin:    https://multivendor-backend.indexo.ir/admin
echo.
echo To check logs, run this script again and select option 4.
echo.

:end
pause


