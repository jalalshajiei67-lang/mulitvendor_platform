@echo off
echo ========================================
echo Testing Django Unfold Admin Theme
echo ========================================
echo.

echo Checking Docker containers status...
docker ps --filter "name=multivendor" --format "table {{.Names}}\t{{.Status}}"
echo.

echo Waiting for backend to be ready...
timeout /t 5 /nobreak >nul

echo.
echo Testing admin endpoint...
echo Opening http://localhost:8000/admin/ in your browser...
echo.

start http://localhost:8000/admin/

echo.
echo ========================================
echo Instructions:
echo ========================================
echo 1. Your browser should open the admin login page
echo 2. You should see the NEW Django Unfold theme (modern, clean UI)
echo 3. Login with your admin credentials
echo 4. The admin interface should have a dark sidebar and modern design
echo.
echo If you see the OLD Django admin (blue/white), the theme didn't load
echo If you see the NEW Unfold theme (dark sidebar, modern), it worked!
echo.
echo To view backend logs: docker logs multivendor_backend_local
echo To view live logs: docker logs -f multivendor_backend_local
echo.
pause

