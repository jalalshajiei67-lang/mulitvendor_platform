@echo off
REM View Logs from Local Docker Services

echo ================================
echo   Viewing Service Logs
echo ================================
echo.
echo Press Ctrl+C to exit logs view
echo.

docker-compose -f docker-compose.local.yml logs -f

