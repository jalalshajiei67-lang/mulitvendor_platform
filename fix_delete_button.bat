@echo off
echo ========================================
echo Fixing Delete Button on Product List
echo ========================================
echo.

cd multivendor_platform\multivendor_platform

echo Collecting static files (including the fix)...
python manage.py collectstatic --noinput

echo.
echo ========================================
echo Fix Applied!
echo ========================================
echo.
echo Next steps:
echo 1. Clear your browser cache (Ctrl + Shift + Delete)
echo 2. Refresh the product list page (Ctrl + F5)
echo 3. Select products and try the delete action
echo.
echo The "Run" button should now appear!
echo ========================================
pause

