# PowerShell Script to Download Database Using Docker (No PostgreSQL Installation Required)
# Usage: .\download-database-docker.ps1

param(
    [string]$ServerIP = "185.208.172.76",
    [string]$DbName = "multivendor_db",
    [string]$DbUser = "postgres",
    [string]$DbPassword = "1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^",
    [int]$DbPort = 5432,
    [string]$BackupDir = ".\database_backups"
)

$ErrorActionPreference = "Stop"

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  Download Database (Docker Method)    ║" -ForegroundColor Green
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

# Create backup directory
if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir | Out-Null
    Write-Host "[OK] Created backup directory: $BackupDir" -ForegroundColor Green
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = Join-Path $BackupDir "multivendor_db_$timestamp.sql"

Write-Host ""
Write-Host "[*] Downloading database from server..." -ForegroundColor Yellow
Write-Host "   Server: $ServerIP" -ForegroundColor Gray
Write-Host "   Database: $DbName" -ForegroundColor Gray
Write-Host ""

# Use Docker to run pg_dump
try {
    # Set password via environment variable
    $env:PGPASSWORD = $DbPassword
    
    Write-Host "[*] Connecting to remote database..." -ForegroundColor Yellow
    
    # Try direct connection first
    docker run --rm -e PGPASSWORD=$DbPassword `
        postgres:15-alpine `
        pg_dump -h $ServerIP -p $DbPort -U $DbUser -d $DbName -F p `
    | Out-File -FilePath $backupFile -Encoding utf8
    
    # Check if file was created and has content
    if (Test-Path $backupFile) {
        $fileSize = (Get-Item $backupFile).Length
        if ($fileSize -gt 0) {
            Write-Host "[OK] Database downloaded successfully!" -ForegroundColor Green
        }
        else {
            throw "Downloaded file is empty"
        }
    }
    else {
        throw "Backup file was not created"
    }
}
catch {
    Write-Host "[X] Direct connection failed: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "[*] Alternative methods:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Method 1: SSH into server and dump from there" -ForegroundColor Yellow
    Write-Host "  1. SSH: ssh root@$ServerIP" -ForegroundColor Gray
    Write-Host "  2. Run: docker exec srv-captain--postgres-db pg_dump -U postgres multivendor_db > backup.sql" -ForegroundColor Gray
    $scpCmd = "scp root@${ServerIP}:/root/backup.sql ."
    Write-Host "  3. Download via SCP: $scpCmd" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Method 2: Use CapRover dashboard" -ForegroundColor Yellow
    Write-Host "  1. Open https://captain.indexo.ir" -ForegroundColor Gray
    Write-Host "  2. Go to postgres-db app" -ForegroundColor Gray
    Write-Host "  3. Use terminal/one-click command to export" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Method 3: Use Django dumpdata (if you have backend access)" -ForegroundColor Yellow
    Write-Host "  See download-database-django.ps1" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

# Compress the backup
Write-Host ""
Write-Host "[*] Compressing backup..." -ForegroundColor Yellow
try {
    $backupFileGz = "$backupFile.gz"
    $bytes = [System.IO.File]::ReadAllBytes($backupFile)
    $compressed = [System.IO.Compression.GZipStream]::new(
        [System.IO.File]::Create($backupFileGz),
        [System.IO.Compression.CompressionLevel]::Optimal
    )
    $compressed.Write($bytes, 0, $bytes.Length)
    $compressed.Close()
    Remove-Item $backupFile
    $finalFile = $backupFileGz
    Write-Host "[OK] Backup compressed" -ForegroundColor Green
}
catch {
    Write-Host "[!] Compression failed, keeping uncompressed file" -ForegroundColor Yellow
    $finalFile = $backupFile
}

$fileSize = (Get-Item $finalFile).Length / 1MB
Write-Host ""
Write-Host "[OK] Backup completed successfully!" -ForegroundColor Green
Write-Host "   File: $finalFile" -ForegroundColor Gray
Write-Host "   Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Gray
Write-Host ""

# Ask if user wants to restore to local database
Write-Host "[?] Do you want to restore this backup to your local database?" -ForegroundColor Cyan
$restore = Read-Host "Type 'yes' to restore (or press Enter to skip)"

if ($restore -eq "yes") {
    Write-Host ""
    Write-Host "[*] Restoring to local database..." -ForegroundColor Yellow
    
    # Check if local database container exists
    $dbContainer = docker ps -a --filter "name=multivendor_db" --format "{{.Names}}"
    if (-not $dbContainer) {
        Write-Host "[!] Local database container not found. Starting Docker Compose..." -ForegroundColor Yellow
        docker-compose up -d db
        Start-Sleep -Seconds 5
    }
    
    # Decompress if needed
    if ($finalFile.EndsWith(".gz")) {
        Write-Host "[*] Decompressing backup..." -ForegroundColor Yellow
        $uncompressedFile = $finalFile -replace '\.gz$', ''
        $input = New-Object System.IO.FileStream($finalFile, [System.IO.FileMode]::Open)
        $gzip = New-Object System.IO.Compression.GZipStream($input, [System.IO.Compression.CompressionMode]::Decompress)
        $output = New-Object System.IO.FileStream($uncompressedFile, [System.IO.FileMode]::Create)
        $gzip.CopyTo($output)
        $output.Close()
        $gzip.Close()
        $input.Close()
        $restoreFile = $uncompressedFile
    }
    else {
        $restoreFile = $finalFile
    }
    
    Write-Host "[*] Dropping existing local database..." -ForegroundColor Yellow
    docker exec multivendor_db psql -U postgres -c "DROP DATABASE IF EXISTS multivendor_db;" 2>&1 | Out-Null
    
    Write-Host "[*] Creating new local database..." -ForegroundColor Yellow
    docker exec multivendor_db psql -U postgres -c "CREATE DATABASE multivendor_db;" 2>&1 | Out-Null
    
    Write-Host "[*] Restoring backup..." -ForegroundColor Yellow
    Get-Content $restoreFile | docker exec -i multivendor_db psql -U postgres -d multivendor_db
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "[OK] Local database restored successfully!" -ForegroundColor Green
        if ($restoreFile -ne $finalFile) {
            Remove-Item $restoreFile
        }
    }
    else {
        Write-Host "[X] Restore failed" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "[OK] Done!" -ForegroundColor Green

