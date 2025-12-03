# Simple script to download database via SSH
# Make sure you have SSH access to the server

param(
    [string]$ServerIP = "185.208.172.76",
    [string]$BackupDir = ".\database_backups"
)

Write-Host "Downloading database from server via SSH..." -ForegroundColor Yellow
Write-Host ""

# Create backup directory
if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir | Out-Null
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = Join-Path $BackupDir "multivendor_db_$timestamp.sql"

Write-Host "Step 1: Dumping database on server..." -ForegroundColor Cyan
Write-Host "Please run this command on the server:" -ForegroundColor Yellow
Write-Host "ssh root@$ServerIP" -ForegroundColor White
Write-Host "docker exec srv-captain--postgres-db pg_dump -U postgres multivendor_db > /root/backup.sql" -ForegroundColor White
Write-Host ""
Write-Host "Step 2: Download the file..." -ForegroundColor Cyan
Write-Host "From your local machine, run:" -ForegroundColor Yellow
$scpCmd = "scp root@${ServerIP}:/root/backup.sql `"$backupFile`""
Write-Host $scpCmd -ForegroundColor White
Write-Host ""
Write-Host "Or if you have SCP available, I can try to download it now..." -ForegroundColor Yellow

# Try to check if scp is available
$scpCheck = Get-Command scp -ErrorAction SilentlyContinue
if ($scpCheck) {
    Write-Host "SCP found. Attempting download..." -ForegroundColor Green
    Write-Host "Note: You need to have SSH key set up or enter password when prompted" -ForegroundColor Yellow
    Write-Host ""
    
    # First, create the backup on server
    Write-Host "Creating backup on server (you may need to enter password)..." -ForegroundColor Yellow
    $sshCmd = "ssh root@${ServerIP} `"docker exec srv-captain--postgres-db pg_dump -U postgres multivendor_db > /root/backup.sql`""
    Invoke-Expression $sshCmd
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Downloading backup file (you may need to enter password)..." -ForegroundColor Yellow
        Invoke-Expression $scpCmd
        
        if (Test-Path $backupFile) {
            $fileSize = (Get-Item $backupFile).Length / 1MB
            Write-Host ""
            Write-Host "[OK] Database downloaded successfully!" -ForegroundColor Green
            Write-Host "   File: $backupFile" -ForegroundColor Gray
            Write-Host "   Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Gray
        } else {
            Write-Host "[X] Download failed. Please try manually using the commands above." -ForegroundColor Red
        }
    } else {
        Write-Host "[X] Could not create backup on server. Please run commands manually." -ForegroundColor Red
    }
} else {
    Write-Host "SCP not found. Please use manual method above or install OpenSSH client." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Done!" -ForegroundColor Green




