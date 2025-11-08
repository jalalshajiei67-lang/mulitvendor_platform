@echo off
title Deploy Delete Button Fix to Production
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║  🚀 DEPLOY DELETE BUTTON FIX TO PRODUCTION                   ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo Issue: CSS files (custom_admin.css, force_action_button.css)
echo        returning 404 on production server
echo.
echo Fix Applied: Updated Dockerfile.backend to run collectstatic
echo.
echo Status: ✅ Code fixed, ⏳ Needs deployment
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

:MENU
echo SELECT DEPLOYMENT METHOD:
echo.
echo [1] Deploy via Git Push (Recommended)
echo [2] Show Manual Deployment Instructions
echo [3] Test Locally First
echo [4] Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto GIT_DEPLOY
if "%choice%"=="2" goto MANUAL_INSTRUCTIONS
if "%choice%"=="3" goto LOCAL_TEST
if "%choice%"=="4" goto END

echo Invalid choice. Please try again.
goto MENU

:GIT_DEPLOY
echo.
echo ═══════════════════════════════════════════════════════════════
echo 🚀 DEPLOYING VIA GIT...
echo ═══════════════════════════════════════════════════════════════
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed or not in PATH!
    echo.
    echo Please install Git or use option [2] for manual deployment.
    pause
    goto MENU
)

echo Step 1: Checking git status...
git status

echo.
echo Step 2: Staging changes...
git add Dockerfile.backend fix_delete_button.bat 🔧_FIX_STATIC_FILES_404.md

echo.
echo Step 3: Creating commit...
git commit -m "Fix: Include collectstatic in Dockerfile to serve CSS files (fixes delete button 404)"

echo.
echo Step 4: Pushing to CapRover...
echo.
echo ⚠️  This will trigger automatic rebuild and deployment (2-5 minutes)
echo.
set /p confirm="Continue with push? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo.
    echo Deployment cancelled.
    pause
    goto MENU
)

git push caprover master

if errorlevel 1 (
    echo.
    echo ❌ Push failed! Check the error messages above.
    echo.
    echo Common issues:
    echo - CapRover remote not configured: git remote add caprover [url]
    echo - Authentication required: Check your SSH key or token
    echo - Network issues: Check your internet connection
    echo.
    pause
    goto MENU
) else (
    echo.
    echo ✅ Push successful! Deployment started.
    echo.
    goto DEPLOYMENT_SUCCESS
)

:MANUAL_INSTRUCTIONS
echo.
echo ═══════════════════════════════════════════════════════════════
echo 📋 MANUAL DEPLOYMENT INSTRUCTIONS
echo ═══════════════════════════════════════════════════════════════
echo.
echo Method 1: Git Command Line
echo -----------------------------------------------------------
echo 1. Open terminal/command prompt
echo 2. Navigate to project: cd C:\Users\F003\Desktop\damirco
echo 3. Stage files: git add Dockerfile.backend
echo 4. Commit: git commit -m "Fix: Add collectstatic to Dockerfile"
echo 5. Push: git push caprover master
echo.
echo Method 2: CapRover CLI
echo -----------------------------------------------------------
echo 1. Install CLI: npm install -g caprover
echo 2. Deploy: caprover deploy
echo 3. Select app: multivendor-backend
echo.
echo Method 3: CapRover Dashboard
echo -----------------------------------------------------------
echo 1. Open: https://captain.your-domain.com
echo 2. Go to Apps ^> multivendor-backend
echo 3. Click "Deployment" tab
echo 4. Click "Force Rebuild" or use Git integration
echo.
pause
goto MENU

:LOCAL_TEST
echo.
echo ═══════════════════════════════════════════════════════════════
echo 🧪 TESTING LOCALLY FIRST
echo ═══════════════════════════════════════════════════════════════
echo.

cd multivendor_platform\multivendor_platform

echo Collecting static files...
python manage.py collectstatic --noinput --clear

if errorlevel 1 (
    echo.
    echo ❌ collectstatic failed! Check Python/Django installation.
    cd ..\..
    pause
    goto MENU
)

echo.
echo ✅ Static files collected successfully!
echo.
echo To test locally:
echo 1. Start server: python manage.py runserver
echo 2. Open: http://localhost:8000/admin/products/product/
echo 3. Select products and test delete action
echo 4. The "Run" button should appear when action is selected
echo.
echo If working locally, proceed with production deployment (option 1).
echo.

cd ..\..
pause
goto MENU

:DEPLOYMENT_SUCCESS
echo ═══════════════════════════════════════════════════════════════
echo ✅ DEPLOYMENT IN PROGRESS
echo ═══════════════════════════════════════════════════════════════
echo.
echo CapRover is now building and deploying your application.
echo.
echo What's happening:
echo 1. ⏳ Building Docker image (includes collectstatic)
echo 2. ⏳ Starting new container
echo 3. ⏳ Health check
echo 4. ⏳ Zero-downtime switch
echo.
echo Estimated time: 2-5 minutes
echo.
echo ═══════════════════════════════════════════════════════════════
echo AFTER DEPLOYMENT COMPLETES:
echo ═══════════════════════════════════════════════════════════════
echo.
echo 1. Clear browser cache: Ctrl + Shift + Delete
echo 2. Hard refresh page: Ctrl + F5
echo 3. Open DevTools: F12
echo 4. Check Network tab:
echo    - custom_admin.css should be Status 200 ✅
echo    - force_action_button.css should be Status 200 ✅
echo 5. Test delete action:
echo    - Select products
echo    - Choose "Delete selected products"
echo    - "Run" button should appear ✅
echo.
echo ═══════════════════════════════════════════════════════════════
echo 🌐 VERIFY AT:
echo ═══════════════════════════════════════════════════════════════
echo.
echo https://multivendor-backend.indexo.ir/admin/products/product/
echo.
pause
goto END

:END
echo.
echo Thank you for using the deployment script!
echo.
pause

