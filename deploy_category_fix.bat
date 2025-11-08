@echo off
echo ========================================
echo   DEPLOYING CATEGORY HIERARCHY FIX
echo ========================================
echo.

:: Set colors for better output
color 0A

echo [1/5] Adding changes to git...
git add multivendor_platform/multivendor_platform/products/views.py
git add multivendor_platform/front_end/src/views/DepartmentDetail.vue
git add multivendor_platform/front_end/src/views/CategoryDetail.vue
git add FIX_CATEGORY_HIERARCHY.md
git add deploy_category_fix.bat

echo.
echo [2/5] Committing changes...
git commit -m "Fix: Add filtering support for category hierarchy navigation"

echo.
echo [3/5] Pushing to repository...
git push origin main

if errorlevel 1 (
    echo.
    echo ❌ ERROR: Failed to push to repository!
    echo    Please check your git credentials and try again.
    pause
    exit /b 1
)

echo.
echo [4/5] Deploying to server...
echo    Connecting to 158.255.74.123...

:: Deploy to server
ssh root@158.255.74.123 "cd /root/damirco && git pull && docker-compose restart backend frontend"

if errorlevel 1 (
    echo.
    echo ❌ ERROR: Failed to deploy to server!
    echo    Please check your SSH connection.
    pause
    exit /b 1
)

echo.
echo [5/5] Checking deployment status...
timeout /t 10 /nobreak >nul

:: Show logs
echo.
echo Fetching latest logs...
ssh root@158.255.74.123 "cd /root/damirco && docker-compose logs --tail=30 backend frontend"

echo.
echo ========================================
echo   ✅ DEPLOYMENT COMPLETED!
echo ========================================
echo.
echo Please test the following:
echo   1. Visit: https://indexo.ir/departments
echo   2. Click on a department
echo   3. Verify categories are showing
echo   4. Click on a category
echo   5. Verify subcategories are showing
echo   6. Click on a subcategory
echo   7. Verify products are showing
echo.
echo Check browser console (F12) for any errors.
echo.

pause

