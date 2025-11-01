@echo off
REM ============================================
REM   CapRover Setup Verification Script
REM   Checks if everything is configured
REM ============================================

echo.
echo ================================================
echo   CAPROVER SETUP VERIFICATION
echo ================================================
echo.

REM Check if caprover is installed
where caprover >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [X] CapRover CLI is NOT installed
    echo     Install: npm install -g caprover
    echo.
) else (
    echo [OK] CapRover CLI is installed
)

echo.
echo Checking CapRover apps...
echo.

REM Check backend app
echo Checking multivendor-backend...
caprover apps:logs multivendor-backend --lines 5 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [X] Backend app not accessible
) else (
    echo [OK] Backend app is accessible
)

REM Check frontend app
echo Checking multivendor-frontend...
caprover apps:logs multivendor-frontend --lines 5 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [X] Frontend app not accessible
) else (
    echo [OK] Frontend app is accessible
)

REM Check database app
echo Checking postgres-db...
caprover apps:logs postgres-db --lines 5 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [X] Database app not accessible
) else (
    echo [OK] Database app is accessible
)

echo.
echo ================================================
echo   VERIFICATION COMPLETE
echo ================================================
echo.
echo Next steps:
echo.
echo 1. Configure environment variables in CapRover dashboard
echo    See: 🚀_CAPROVER_FRESH_SETUP_GUIDE.md
echo.
echo 2. Set up domains and SSL certificates
echo    Backend:  multivendor-backend.indexo.ir
echo    Frontend: indexo.ir
echo.
echo 3. Deploy your code:
echo    Run: DEPLOY_TO_CAPROVER.bat
echo.
echo 4. Run migrations and create superuser
echo    Run: DEPLOY_TO_CAPROVER.bat (choose option 5 and 7)
echo.
echo For detailed instructions, see:
echo   🚀_CAPROVER_FRESH_SETUP_GUIDE.md
echo.

pause


