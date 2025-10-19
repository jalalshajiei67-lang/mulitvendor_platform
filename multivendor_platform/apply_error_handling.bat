@echo off
echo ========================================
echo Applying Robust Error Handling System
echo ========================================
echo.

cd multivendor_platform

echo Step 1: Creating migrations...
python manage.py makemigrations products
echo.

echo Step 2: Applying migrations...
python manage.py migrate products
echo.

echo ========================================
echo Done! Error handling system is ready.
echo ========================================
echo.
echo Next steps:
echo 1. Restart your Django server
echo 2. Go to: http://127.0.0.1:8000/admin/products/productscrapejob/
echo 3. Retry your failed job
echo.
pause

