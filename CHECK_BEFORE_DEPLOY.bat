@echo off
REM Pre-deployment verification script

COLOR 0B
echo.
echo ================================================================
echo      PRE-DEPLOYMENT CHECK
echo ================================================================
echo.

set ERRORS=0

echo Checking required files...
echo.

REM Check configuration files
if exist "docker-compose.yml" (
    echo   ✓ docker-compose.yml
) else (
    echo   ✗ docker-compose.yml MISSING
    set /a ERRORS+=1
)

if exist "env.production" (
    echo   ✓ env.production
) else (
    echo   ✗ env.production MISSING
    set /a ERRORS+=1
)

if exist "Dockerfile" (
    echo   ✓ Dockerfile
) else (
    echo   ✗ Dockerfile MISSING
    set /a ERRORS+=1
)

REM Check deployment scripts
if exist "deploy-windows.bat" (
    echo   ✓ deploy-windows.bat
) else (
    echo   ✗ deploy-windows.bat MISSING
    set /a ERRORS+=1
)

if exist "server-deploy.sh" (
    echo   ✓ server-deploy.sh
) else (
    echo   ✗ server-deploy.sh MISSING
    set /a ERRORS+=1
)

REM Check nginx
if exist "nginx\nginx.conf" (
    echo   ✓ nginx configuration
) else (
    echo   ✗ nginx configuration MISSING
    set /a ERRORS+=1
)

REM Check project structure
if exist "multivendor_platform\multivendor_platform" (
    echo   ✓ Django backend
) else (
    echo   ✗ Django backend MISSING
    set /a ERRORS+=1
)

if exist "multivendor_platform\front_end" (
    echo   ✓ Vue.js frontend
) else (
    echo   ✗ Vue.js frontend MISSING
    set /a ERRORS+=1
)

echo.
echo Checking environment configuration...
echo.

if exist ".env" (
    echo   ✓ .env file exists
    findstr /C:"SECRET_KEY=" .env >nul
    if %ERRORLEVEL% EQU 0 (
        echo   ✓ SECRET_KEY configured
    ) else (
        echo   ✗ SECRET_KEY missing
        set /a ERRORS+=1
    )
    
    findstr /C:"DB_PASSWORD=" .env >nul
    if %ERRORLEVEL% EQU 0 (
        echo   ✓ DB_PASSWORD configured
    ) else (
        echo   ✗ DB_PASSWORD missing
        set /a ERRORS+=1
    )
) else (
    echo   ⚠ .env file not found
    echo   Run: copy env.production .env
    set /a ERRORS+=1
)

echo.
echo ================================================================

if %ERRORS% EQU 0 (
    COLOR 0A
    echo.
    echo   ✓✓✓ ALL CHECKS PASSED! READY TO DEPLOY! ✓✓✓
    echo.
    echo   Next step: Run DEPLOY_NOW.bat
    echo.
) else (
    COLOR 0C
    echo.
    echo   ✗✗✗ FOUND %ERRORS% ISSUE(S) - FIX BEFORE DEPLOYING ✗✗✗
    echo.
    echo   See errors above and fix them first.
    echo.
)

echo ================================================================
echo.
pause



