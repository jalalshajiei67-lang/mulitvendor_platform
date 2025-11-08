@echo off
REM Quick deployment script for delete functionality fix
REM Run this after pulling the changes

echo ========================================
echo DELETE FUNCTIONALITY FIX - DEPLOYMENT
echo ========================================
echo.

cd multivendor_platform\multivendor_platform

echo Step 1: Collecting static files...
python manage.py collectstatic --noinput
echo.

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to collect static files!
    pause
    exit /b 1
)

echo ========================================
echo SUCCESS! Static files collected.
echo ========================================
echo.
echo Next steps:
echo 1. Restart your Django server
echo 2. Clear browser cache (Ctrl+Shift+Delete)
echo 3. Hard refresh the page (Ctrl+F5)
echo 4. Test deletion in admin dashboard
echo.
echo Read DELETE_FIX_COMPLETE.md for detailed instructions
echo.
pause

