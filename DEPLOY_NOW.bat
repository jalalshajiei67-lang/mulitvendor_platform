@echo off
REM ===================================================================
REM  QUICK DEPLOY - One-Click Deployment for Windows
REM ===================================================================

COLOR 0A
echo.
echo ================================================================
echo      MULTIVENDOR PLATFORM - ONE-CLICK DEPLOYMENT
echo ================================================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo [STEP 1/3] Creating environment file...
    copy env.production .env >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo   ✓ Environment file created
    ) else (
        echo   ✗ Error creating .env file
        pause
        exit /b 1
    )
) else (
    echo [STEP 1/3] Environment file already exists
    echo   ✓ Using existing .env
)

echo.
echo [STEP 2/3] Deploying to VPS...
echo   This will upload files to your VPS
echo   You'll be prompted for SSH password: e^<c6w:1EDupHjf4*
echo.
pause

call deploy-windows.bat

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ✗ Deployment failed
    pause
    exit /b 1
)

echo.
echo ================================================================
echo  FILES UPLOADED SUCCESSFULLY!
echo ================================================================
echo.
echo [STEP 3/3] Now SSH to your VPS and complete setup:
echo.
echo   1. Open a new terminal/PowerShell
echo.
echo   2. Run: ssh root@158.255.74.123
echo      Password: e^<c6w:1EDupHjf4*
echo.
echo   3. On VPS, run these commands:
echo      cd /opt/multivendor_platform
echo      chmod +x *.sh
echo      ./server-deploy.sh
echo.
echo   4. Create admin user:
echo      docker-compose exec backend python manage.py createsuperuser
echo.
echo   5. Access your site:
echo      http://158.255.74.123
echo.
echo ================================================================
echo.
pause



