# PowerShell Script to Download Online Database to Local Project
# Usage: .\download-database.ps1

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
Write-Host "║  Download Online Database to Local    ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Check if pg_dump is available
$pgDumpPath = Get-Command pg_dump -ErrorAction SilentlyContinue
if (-not $pgDumpPath) {
    Write-Host "⚠️  pg_dump not found. Checking common installation paths..." -ForegroundColor Yellow
    
    $possiblePaths = @(
        "C:\Program Files\PostgreSQL\*\bin\pg_dump.exe",
        "C:\Program Files (x86)\PostgreSQL\*\bin\pg_dump.exe",
        "$env:LOCALAPPDATA\Programs\postgresql\*\bin\pg_dump.exe"
    )
    
    $found = $false
    foreach ($path in $possiblePaths) {
        $files = Get-ChildItem -Path $path -ErrorAction SilentlyContinue
        if ($files) {
            $env:Path += ";$($files[0].DirectoryName)"
            $found = $true
            Write-Host "✓ Found pg_dump at: $($files[0].FullName)" -ForegroundColor Green
            break
        }
    }
    
    if (-not $found) {
        Write-Host "❌ pg_dump not found. Please install PostgreSQL client tools:" -ForegroundColor Red
        Write-Host "   Download from: https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
        Write-Host "   Or use Docker method (see download-database-docker.ps1)" -ForegroundColor Yellow
        exit 1
    }
}

# Create backup directory
if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir | Out-Null
    Write-Host "✓ Created backup directory: $BackupDir" -ForegroundColor Green
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = Join-Path $BackupDir "multivendor_db_$timestamp.sql"
$backupFileGz = "$backupFile.gz"

Write-Host ""
Write-Host "📥 Downloading database from server..." -ForegroundColor Yellow
Write-Host "   Server: $ServerIP" -ForegroundColor Gray
Write-Host "   Database: $DbName" -ForegroundColor Gray
Write-Host ""

# Set PGPASSWORD environment variable
$env:PGPASSWORD = $DbPassword

try {
    # Try direct connection first (if DB is exposed)
    Write-Host "Attempting direct connection..." -ForegroundColor Yellow
    $env:PGPASSWORD = $DbPassword
    & pg_dump -h $ServerIP -p $DbPort -U $DbUser -d $DbName -F p -f $backupFile 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Database downloaded successfully!" -ForegroundColor Green
    }
    else {
        throw "Direct connection failed"
    }
}
catch {
    Write-Host "⚠️  Direct connection failed. Trying SSH method..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📋 To download via SSH, you have two options:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Option 1: SSH into server and run pg_dump there" -ForegroundColor Yellow
    Write-Host "  ssh root@$ServerIP" -ForegroundColor Gray
    Write-Host "  docker exec srv-captain--postgres-db pg_dump -U postgres multivendor_db > backup.sql" -ForegroundColor Gray
    Write-Host "  # Then download the file using SCP or CapRover dashboard" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Option 2: Use CapRover CLI" -ForegroundColor Yellow
    Write-Host "  npm install -g caprover" -ForegroundColor Gray
    Write-Host "  caprover login -n captain" -ForegroundColor Gray
    Write-Host "  # Then use the download-database-caprover.ps1 script" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Option 3: Use Docker method (recommended for Windows)" -ForegroundColor Yellow
    Write-Host "  .\download-database-docker.ps1" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

# Compress the backup
Write-Host ""
Write-Host "📦 Compressing backup..." -ForegroundColor Yellow
try {
    # Try using 7-Zip if available
    $7zipPath = Get-Command 7z -ErrorAction SilentlyContinue
    if ($7zipPath) {
        & 7z a -tgzip "$backupFileGz" "$backupFile" | Out-Null
        Remove-Item $backupFile
        $finalFile = $backupFileGz
    }
    else {
        # Fallback: use .NET compression
        $bytes = [System.IO.File]::ReadAllBytes($backupFile)
        $compressed = [System.IO.Compression.GZipStream]::new(
            [System.IO.File]::Create($backupFileGz),
            [System.IO.Compression.CompressionLevel]::Optimal
        )
        $compressed.Write($bytes, 0, $bytes.Length)
        $compressed.Close()
        Remove-Item $backupFile
        $finalFile = $backupFileGz
    }
    Write-Host "✓ Backup compressed" -ForegroundColor Green
}
catch {
    Write-Host "⚠️  Compression failed, keeping uncompressed file" -ForegroundColor Yellow
    $finalFile = $backupFile
}

$fileSize = (Get-Item $finalFile).Length / 1MB
Write-Host ""
Write-Host "✅ Backup completed successfully!" -ForegroundColor Green
Write-Host "   File: $finalFile" -ForegroundColor Gray
Write-Host "   Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Gray
Write-Host ""

# Ask if user wants to restore to local database
Write-Host "📥 Do you want to restore this backup to your local database?" -ForegroundColor Cyan
$restore = Read-Host "Type 'yes' to restore (or press Enter to skip)"

if ($restore -eq "yes") {
    Write-Host ""
    Write-Host "🔄 Restoring to local database..." -ForegroundColor Yellow
    
    # Check if Docker is running
    $dockerRunning = docker ps 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Docker is running" -ForegroundColor Green
        
        # Check if local database container exists
        $dbContainer = docker ps -a --filter "name=multivendor_db" --format "{{.Names}}"
        if ($dbContainer) {
            Write-Host "✓ Found local database container" -ForegroundColor Green
            
            # Decompress if needed
            if ($finalFile.EndsWith(".gz")) {
                Write-Host "📦 Decompressing backup..." -ForegroundColor Yellow
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
            
            Write-Host "🗑️  Dropping existing local database..." -ForegroundColor Yellow
            docker exec multivendor_db psql -U postgres -c "DROP DATABASE IF EXISTS multivendor_db;" 2>&1 | Out-Null
            
            Write-Host "➕ Creating new local database..." -ForegroundColor Yellow
            docker exec multivendor_db psql -U postgres -c "CREATE DATABASE multivendor_db;" 2>&1 | Out-Null
            
            Write-Host "📥 Restoring backup..." -ForegroundColor Yellow
            Get-Content $restoreFile | docker exec -i multivendor_db psql -U postgres -d multivendor_db
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host ""
                Write-Host "✅ Local database restored successfully!" -ForegroundColor Green
                if ($restoreFile -ne $finalFile) {
                    Remove-Item $restoreFile
                }
            }
            else {
                Write-Host "❌ Restore failed" -ForegroundColor Red
            }
        }
        else {
            Write-Host "⚠️  Local database container not found. Please start Docker Compose first:" -ForegroundColor Yellow
            Write-Host "   docker-compose up -d db" -ForegroundColor Gray
        }
    }
    else {
        Write-Host "⚠️  Docker is not running. Please start Docker Desktop and try again." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✨ Done!" -ForegroundColor Green



