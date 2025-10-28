@echo off
REM Stop Local Docker Testing

echo ================================
echo   Stopping Local Services
echo ================================
echo.

docker-compose -f docker-compose.local.yml down

echo.
echo [OK] All services stopped
echo.
echo To remove all data (clean slate):
echo   docker-compose -f docker-compose.local.yml down -v
echo.

pause

