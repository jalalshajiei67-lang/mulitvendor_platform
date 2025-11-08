@echo off
echo ========================================
echo Fixing Delete Button - Static Files Issue
echo ========================================
echo.
echo ISSUE: CSS files (custom_admin.css, force_action_button.css) 
echo        are returning 404 errors on production server
echo.
echo ROOT CAUSE: Dockerfile.backend was not running collectstatic
echo.
echo SOLUTION: Updated Dockerfile.backend to include collectstatic
echo           Need to redeploy to CapRover server
echo.
echo ========================================
echo.
echo For LOCAL TESTING:
echo ========================================

cd multivendor_platform\multivendor_platform

echo Collecting static files locally...
python manage.py collectstatic --noinput --clear

echo.
echo ✓ Local static files collected!
echo.
echo To test locally:
echo 1. Run: python manage.py runserver
echo 2. Go to: http://localhost:8000/admin/products/product/
echo 3. Test delete action
echo.
echo ========================================
echo.
echo For PRODUCTION DEPLOYMENT:
echo ========================================
echo.
echo The Dockerfile.backend has been fixed to include collectstatic.
echo You need to REDEPLOY to CapRover for the fix to take effect.
echo.
echo DEPLOYMENT OPTIONS:
echo.
echo Option 1 - Deploy via Git (Recommended):
echo   1. Commit the changes:
echo      git add Dockerfile.backend
echo      git commit -m "Fix: Include collectstatic in Dockerfile"
echo   2. Push to CapRover:
echo      git push caprover master
echo   3. Wait for build to complete (2-5 minutes)
echo   4. Check: https://multivendor-backend.indexo.ir/admin/products/product/
echo.
echo Option 2 - Deploy via CapRover CLI:
echo   1. Install CapRover CLI (if not installed):
echo      npm install -g caprover
echo   2. Deploy:
echo      caprover deploy
echo   3. Wait for build to complete
echo.
echo Option 3 - Manual Docker Build on Server:
echo   Connect to server and rebuild the container
echo.
echo ========================================
echo After Deployment:
echo ========================================
echo 1. Clear browser cache (Ctrl + Shift + Delete)
echo 2. Hard refresh the page (Ctrl + F5)
echo 3. Check Network tab in DevTools (F12)
echo 4. Verify CSS files load with status 200
echo 5. Test delete action
echo.
echo ========================================
pause
