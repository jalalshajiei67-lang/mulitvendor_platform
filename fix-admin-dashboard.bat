@echo off
REM Django Admin Dashboard Diagnostic and Fix Script
REM Windows batch file

echo ========================================
echo Django Admin Dashboard Diagnostic Tool
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "multivendor_platform" (
    echo ERROR: Please run this script from the project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo Step 1: Running diagnostic script...
echo.
python debug_admin.py
echo.

echo ========================================
echo Step 2: Checking database data...
echo ========================================
cd multivendor_platform\multivendor_platform
python manage.py shell -c "from products.models import Product, Department, Category; from django.contrib.auth.models import User; print(f'Products: {Product.objects.count()}'); print(f'Departments: {Department.objects.count()}'); print(f'Categories: {Category.objects.count()}'); print(f'Users: {User.objects.count()}')"
echo.

echo ========================================
echo Step 3: Checking for superuser...
echo ========================================
python manage.py shell -c "from django.contrib.auth.models import User; superusers = User.objects.filter(is_superuser=True); print(f'Superusers found: {superusers.count()}'); [print(f'  - {u.username} (active: {u.is_active})') for u in superusers]"
echo.

echo ========================================
echo Step 4: Checking migrations...
echo ========================================
python manage.py showmigrations | findstr /C:"[ ]"
if %ERRORLEVEL% EQU 0 (
    echo WARNING: There are unapplied migrations!
    echo.
    set /p apply="Do you want to apply migrations now? (y/n): "
    if /i "%apply%"=="y" (
        python manage.py migrate
    )
) else (
    echo All migrations are applied.
)
echo.

echo ========================================
echo Step 5: Checking static files...
echo ========================================
if not exist "static" (
    echo WARNING: Static files directory doesn't exist!
    echo.
    set /p collect="Do you want to collect static files now? (y/n): "
    if /i "%collect%"=="y" (
        python manage.py collectstatic --noinput
    )
) else (
    echo Static files directory exists.
)
echo.

cd ..\..

echo ========================================
echo Diagnostic Complete!
echo ========================================
echo.
echo Check the output above for any issues marked with:
echo   - ERROR: Critical issues
echo   - WARNING: Potential issues
echo   - Empty data counts: Need to create data
echo.
echo Next steps:
echo 1. If no superuser exists, run: python manage.py createsuperuser
echo 2. If no data exists, create test data via Django admin
echo 3. If migrations are pending, apply them with: python manage.py migrate
echo 4. Access admin at: http://localhost:8000/admin/
echo.
pause

