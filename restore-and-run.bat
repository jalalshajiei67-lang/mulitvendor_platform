@echo off
REM Quick script to restore database and run project
echo ========================================
echo   Restore Database and Run Project
echo ========================================
echo.

REM Check if Docker is running
echo [1/5] Checking Docker...
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Desktop is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo [OK] Docker is running
echo.

REM Check if backup exists
echo [2/5] Checking backup file...
if not exist "database_backups\multivendor_db_backup.sql.gz" (
    echo [ERROR] Backup file not found!
    echo Expected: database_backups\multivendor_db_backup.sql.gz
    echo.
    echo Available files:
    dir /b database_backups\*.sql* 2>nul
    pause
    exit /b 1
)
echo [OK] Backup file found
echo.

REM Start database container
echo [3/5] Starting database container...
docker-compose -f docker-compose.local.yml up -d db
if errorlevel 1 (
    echo [ERROR] Failed to start database container
    pause
    exit /b 1
)
echo [OK] Database container starting...
echo Waiting for database to be ready...
timeout /t 10 /nobreak >nul
echo.

REM Decompress backup
echo [4/5] Preparing backup file...
powershell -Command "$backup = 'database_backups\multivendor_db_backup.sql.gz'; $uncompressed = 'database_backups\multivendor_db_backup.sql'; if (Test-Path $backup) { $input = New-Object System.IO.FileStream($backup, [System.IO.FileMode]::Open); $gzip = New-Object System.IO.Compression.GZipStream($input, [System.IO.Compression.CompressionMode]::Decompress); $output = New-Object System.IO.FileStream($uncompressed, [System.IO.FileMode]::Create); $gzip.CopyTo($output); $output.Close(); $gzip.Close(); $input.Close(); Write-Host 'Backup decompressed' }"
if errorlevel 1 (
    echo [ERROR] Failed to decompress backup
    pause
    exit /b 1
)
echo.

REM Restore database
echo [5/5] Restoring database...
echo This may take a minute...
powershell -Command "$sql = Get-Content 'database_backups\multivendor_db_backup.sql' -Raw -Encoding UTF8; $sql = $sql -replace 'multivendor-db', 'multivendor_db'; Set-Content -Path 'database_backups\multivendor_db_backup_modified.sql' -Value $sql -Encoding UTF8 -NoNewline; docker exec multivendor_db_local psql -U postgres -c 'DROP DATABASE IF EXISTS multivendor_db;' 2>nul; docker exec multivendor_db_local psql -U postgres -c 'CREATE DATABASE multivendor_db;' 2>nul; Get-Content 'database_backups\multivendor_db_backup_modified.sql' | docker exec -i multivendor_db_local psql -U postgres -d multivendor_db"
if errorlevel 1 (
    echo [ERROR] Failed to restore database
    pause
    exit /b 1
)
echo.
echo ========================================
echo   DATABASE RESTORED SUCCESSFULLY!
echo ========================================
echo.
echo Starting project...
echo.
echo Access your application at:
echo   Frontend: http://localhost:8080
echo   Backend:  http://localhost:8000
echo   Admin:    http://localhost:8000/admin/
echo.
echo Press Ctrl+C to stop all services
echo.

REM Start project
docker-compose -f docker-compose.local.yml up --build

pause




