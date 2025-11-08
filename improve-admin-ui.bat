@echo off
echo ========================================
echo Django Admin UI Improvement
echo ========================================
echo.
echo This will install Django Unfold - a modern admin theme
echo.

REM Activate virtual environment
call multivendor_platform\venv\Scripts\activate.bat

echo Installing Django Unfold...
pip install django-unfold

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Open: multivendor_platform\multivendor_platform\multivendor_platform\settings.py
echo 2. Add 'unfold' to the TOP of INSTALLED_APPS (before 'django.contrib.admin')
echo 3. Run: python manage.py collectstatic --noinput
echo 4. Restart your server
echo.
echo See IMPROVE_ADMIN_UI.md for full configuration instructions
echo.
pause

