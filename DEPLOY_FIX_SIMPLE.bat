@echo off
title Deploy Static Files Fix to CapRover
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║  🚀 DEPLOY DELETE BUTTON FIX - SIMPLE METHOD                 ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo Your changes are ready! Now let's deploy them to CapRover.
echo.

REM First, commit the changes if not already committed
echo Checking for uncommitted changes...
git add -A
git commit -m "Fix: Include collectstatic in Dockerfile to serve CSS files" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Changes committed
) else (
    echo ℹ️  No new changes to commit
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo DEPLOYMENT OPTIONS:
echo ═══════════════════════════════════════════════════════════════
echo.
echo [1] Deploy using CapRover CLI (Recommended)
echo [2] Deploy using CapRover Web Dashboard
echo [3] Set up Git Remote and Push
echo [4] Exit
echo.

set /p choice="Select option (1-4): "

if "%choice%"=="1" goto CAPROVER_CLI
if "%choice%"=="2" goto WEB_DASHBOARD
if "%choice%"=="3" goto GIT_SETUP
if "%choice%"=="4" goto END

echo Invalid choice
pause
goto END

:CAPROVER_CLI
echo.
echo ═══════════════════════════════════════════════════════════════
echo METHOD 1: CapRover CLI Deployment
echo ═══════════════════════════════════════════════════════════════
echo.
echo Checking if CapRover CLI is installed...
caprover --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ CapRover CLI is not installed!
    echo.
    echo Installing CapRover CLI...
    call npm install -g caprover
    if errorlevel 1 (
        echo.
        echo ❌ Failed to install CapRover CLI
        echo    Please install Node.js first: https://nodejs.org
        pause
        goto END
    )
)

echo ✅ CapRover CLI is ready
echo.
echo Starting deployment...
echo.
caprover deploy

if errorlevel 1 (
    echo.
    echo ❌ Deployment failed!
    echo.
    echo This might be your first time using CapRover CLI.
    echo You need to login first:
    echo.
    echo Run these commands:
    echo   1. caprover login
    echo   2. Enter your CapRover URL (e.g., captain.your-domain.com)
    echo   3. Enter your password
    echo   4. Run this script again
    echo.
    pause
    goto END
)

echo.
echo ✅ Deployment successful!
goto SUCCESS

:WEB_DASHBOARD
echo.
echo ═══════════════════════════════════════════════════════════════
echo METHOD 2: CapRover Web Dashboard Deployment
echo ═══════════════════════════════════════════════════════════════
echo.
echo Follow these steps:
echo.
echo 1. Open your CapRover dashboard in a web browser
echo    URL: https://captain.indexo.ir (or your CapRover URL)
echo.
echo 2. Login with your credentials
echo.
echo 3. Go to "Apps" section
echo.
echo 4. Click on "multivendor-backend" app
echo.
echo 5. Go to "Deployment" tab
echo.
echo 6. Choose ONE of these options:
echo.
echo    Option A - Upload tar file:
echo    • Click "Upload .tar File"
echo    • We'll create the tar file now...
echo.

REM Create tar file for deployment
echo Creating deployment package...
tar -czf caprover-deploy.tar.gz ^
    captain-definition-backend ^
    Dockerfile.backend ^
    multivendor_platform/

if errorlevel 0 (
    echo ✅ Deployment package created: caprover-deploy.tar.gz
    echo.
    echo    • Upload this file in the CapRover dashboard
    echo    • Click "Deploy"
    echo    • Wait 2-5 minutes for build to complete
) else (
    echo ❌ Failed to create tar file
)

echo.
echo    Option B - Git/GitHub:
echo    • First push changes to GitHub: git push origin main
echo    • Then in CapRover, select "Deploy from GitHub"
echo    • Select your repository and branch
echo    • Click "Deploy"
echo.
pause
goto END

:GIT_SETUP
echo.
echo ═══════════════════════════════════════════════════════════════
echo METHOD 3: Git Remote Setup
echo ═══════════════════════════════════════════════════════════════
echo.
echo To set up git remote for CapRover, you need:
echo.
echo 1. Your CapRover server address
echo 2. Your app name: multivendor-backend
echo.
echo The git remote format is:
echo   ssh://captain@YOUR-SERVER:YOUR-APP-NAME.git
echo.
echo Example:
echo   git remote add caprover ssh://captain@captain.indexo.ir:multivendor-backend.git
echo.
echo After adding the remote, you can push with:
echo   git push caprover main:master
echo.
echo Note: You're on 'main' branch but CapRover expects 'master'
echo.
set /p setup_remote="Do you want to set up the remote now? (Y/N): "
if /i "%setup_remote%"=="Y" (
    set /p server="Enter your CapRover server (e.g., captain.indexo.ir): "
    echo.
    echo Adding git remote...
    git remote add caprover ssh://captain@!server!:multivendor-backend.git
    if errorlevel 0 (
        echo ✅ Remote added successfully!
        echo.
        echo Now pushing to CapRover...
        git push caprover main:master
        if errorlevel 0 (
            echo ✅ Push successful!
            goto SUCCESS
        ) else (
            echo ❌ Push failed. Check your SSH keys or authentication.
        )
    ) else (
        echo ❌ Failed to add remote. It might already exist.
        echo Try: git remote remove caprover
        echo Then run this script again.
    )
)
pause
goto END

:SUCCESS
echo.
echo ═══════════════════════════════════════════════════════════════
echo ✅ DEPLOYMENT SUCCESSFUL!
echo ═══════════════════════════════════════════════════════════════
echo.
echo Your changes are being deployed. This takes 2-5 minutes.
echo.
echo What's happening:
echo • Building Docker image with updated Dockerfile
echo • Running migrations
echo • Collecting static files (THIS IS THE FIX!)
echo • Starting new container
echo • Health check and zero-downtime switch
echo.
echo ═══════════════════════════════════════════════════════════════
echo VERIFY THE FIX:
echo ═══════════════════════════════════════════════════════════════
echo.
echo 1. Wait 3-5 minutes for deployment to complete
echo.
echo 2. Open: https://multivendor-backend.indexo.ir/admin/products/product/
echo.
echo 3. Clear browser cache:
echo    • Press Ctrl + Shift + Delete
echo    • Select "Cached images and files"
echo    • Click "Clear data"
echo.
echo 4. Hard refresh the page: Ctrl + F5
echo.
echo 5. Open DevTools (F12) → Network tab
echo    • Check that these load with Status 200:
echo      ✅ custom_admin.css
echo      ✅ force_action_button.css
echo.
echo 6. Test delete functionality:
echo    • Select products
echo    • Choose "Delete selected products"
echo    • "Run" button should appear ✅
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

pause
goto END

:END
echo.
echo Done!

