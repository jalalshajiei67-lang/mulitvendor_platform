@echo off
echo ========================================
echo Starting Django Backend Server
echo ========================================
cd multivendor_platform
call ..\venv\Scripts\activate.bat
echo.
echo Backend starting at http://127.0.0.1:8000
echo API available at http://127.0.0.1:8000/api/products/
echo.
python manage.py runserver
pause

