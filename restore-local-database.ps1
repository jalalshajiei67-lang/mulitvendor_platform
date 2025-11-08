# PowerShell Script to Restore Downloaded Database to Local Docker Database
# Usage: .\restore-local-database.ps1

param(
    [string]$BackupFile = ".\database_backups\multivendor_db_backup.sql.gz",
    [string]$DbContainer = "multivendor_db_local",
    [string]$DbName = "multivendor_db",
    [string]$DbUser = "postgres"
)

$ErrorActionPreference = "Stop"

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  Restore Database to Local Project    ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Check if Docker is running
Write-Host "[*] Checking Docker..." -ForegroundColor Yellow
$dockerCheck = docker ps 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[X] Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Docker is running" -ForegroundColor Green

# Check if backup file exists
if (-not (Test-Path $BackupFile)) {
    Write-Host "[X] Backup file not found: $BackupFile" -ForegroundColor Red
    Write-Host ""
    Write-Host "Available backups:" -ForegroundColor Yellow
    if (Test-Path ".\database_backups") {
        Get-ChildItem ".\database_backups" | Select-Object Name, Length, LastWriteTime
    }
    else {
        Write-Host "  No backup directory found" -ForegroundColor Gray
    }
    exit 1
}

Write-Host "[OK] Backup file found: $BackupFile" -ForegroundColor Green

# Check if database container exists or start it
Write-Host ""
Write-Host "[*] Checking database container..." -ForegroundColor Yellow
$containerExists = docker ps -a --filter "name=$DbContainer" --format "{{.Names}}"
if (-not $containerExists) {
    Write-Host "[!] Database container not found. Starting Docker Compose..." -ForegroundColor Yellow
    docker-compose -f docker-compose.local.yml up -d db
    Write-Host "[*] Waiting for database to be ready..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    
    # Wait for database to be healthy
    $maxRetries = 30
    $retry = 0
    while ($retry -lt $maxRetries) {
        $health = docker exec $DbContainer pg_isready -U $DbUser 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Database is ready" -ForegroundColor Green
            break
        }
        Start-Sleep -Seconds 2
        $retry++
    }
}
else {
    $isRunning = docker ps --filter "name=$DbContainer" --format "{{.Names}}"
    if (-not $isRunning) {
        Write-Host "[*] Starting database container..." -ForegroundColor Yellow
        docker start $DbContainer
        Start-Sleep -Seconds 5
    }
    Write-Host "[OK] Database container is running" -ForegroundColor Green
}

# Decompress backup if needed
Write-Host ""
Write-Host "[*] Preparing backup file..." -ForegroundColor Yellow
if ($BackupFile.EndsWith(".gz")) {
    $uncompressedFile = $BackupFile -replace '\.gz$', ''
    Write-Host "[*] Decompressing backup..." -ForegroundColor Yellow
    
    try {
        $input = New-Object System.IO.FileStream($BackupFile, [System.IO.FileMode]::Open)
        $gzip = New-Object System.IO.Compression.GZipStream($input, [System.IO.Compression.CompressionMode]::Decompress)
        $output = New-Object System.IO.FileStream($uncompressedFile, [System.IO.FileMode]::Create)
        $gzip.CopyTo($output)
        $output.Close()
        $gzip.Close()
        $input.Close()
        $restoreFile = $uncompressedFile
        Write-Host "[OK] Backup decompressed" -ForegroundColor Green
    }
    catch {
        Write-Host "[X] Failed to decompress: $_" -ForegroundColor Red
        exit 1
    }
}
else {
    $restoreFile = $BackupFile
}

# Modify SQL file to handle database name mismatch (multivendor-db -> multivendor_db)
Write-Host ""
Write-Host "[*] Adjusting database name references..." -ForegroundColor Yellow
$sqlContent = Get-Content $restoreFile -Raw -Encoding UTF8
# Replace database name references
$sqlContent = $sqlContent -replace 'multivendor-db', 'multivendor_db'
$sqlContent = $sqlContent -replace 'CREATE DATABASE "multivendor_db"', 'CREATE DATABASE multivendor_db'
$sqlContent = $sqlContent -replace 'CONNECT TO "multivendor_db"', 'CONNECT TO multivendor_db'

# Save modified SQL
$modifiedFile = $restoreFile -replace '\.sql$', '_modified.sql'
Set-Content -Path $modifiedFile -Value $sqlContent -Encoding UTF8 -NoNewline
Write-Host "[OK] Database name references updated" -ForegroundColor Green

# Drop and recreate database
Write-Host ""
Write-Host "[*] Dropping existing local database..." -ForegroundColor Yellow
docker exec $DbContainer psql -U $DbUser -c "DROP DATABASE IF EXISTS $DbName;" 2>&1 | Out-Null

Write-Host "[*] Creating new local database..." -ForegroundColor Yellow
docker exec $DbContainer psql -U $DbUser -c "CREATE DATABASE $DbName;" 2>&1 | Out-Null

if ($LASTEXITCODE -ne 0) {
    Write-Host "[X] Failed to create database" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Database created" -ForegroundColor Green

# Restore backup
Write-Host ""
Write-Host "[*] Restoring backup (this may take a minute)..." -ForegroundColor Yellow
Get-Content $modifiedFile | docker exec -i $DbContainer psql -U $DbUser -d $DbName

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[OK] Database restored successfully!" -ForegroundColor Green
    
    # Clean up temporary files
    if ($restoreFile -ne $BackupFile) {
        Remove-Item $restoreFile -ErrorAction SilentlyContinue
    }
    Remove-Item $modifiedFile -ErrorAction SilentlyContinue
    
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "  DATABASE RESTORED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Start your project: .\test-local.bat" -ForegroundColor Yellow
    Write-Host "  2. Or manually: docker-compose -f docker-compose.local.yml up" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Access your application:" -ForegroundColor Cyan
    Write-Host "  Frontend: http://localhost:8080" -ForegroundColor Gray
    Write-Host "  Backend:  http://localhost:8000" -ForegroundColor Gray
    Write-Host "  Admin:    http://localhost:8000/admin/" -ForegroundColor Gray
    Write-Host ""
}
else {
    Write-Host "[X] Restore failed. Check the error messages above." -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Done!" -ForegroundColor Green

