@echo off
echo ========================================
echo Running Django Admin Tests
echo ========================================
echo.

REM Activate virtual environment
call multivendor_platform\venv\Scripts\activate.bat

REM Run tests
python test_admin_fixes.py

echo.
echo ========================================
echo Test Complete!
echo ========================================
pause

