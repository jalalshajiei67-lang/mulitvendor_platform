# 📥 Guide: Download Online Database to Local Project

This guide explains multiple methods to download your production database from CapRover to your local development environment.

## 🎯 Quick Start (Recommended for Windows)

### Method 1: Using Docker (No PostgreSQL Installation Required)

1. **Make sure Docker Desktop is running**

2. **Run the PowerShell script:**
   ```powershell
   .\download-database-docker.ps1
   ```

3. **Follow the prompts** - The script will:
   - Download the database from your CapRover server
   - Save it to `database_backups/` folder
   - Optionally restore it to your local Docker database

---

## 📋 All Available Methods

### Method 1: Docker Method (Windows/Linux/Mac) ⭐ Recommended

**Advantages:**
- No need to install PostgreSQL client tools
- Works on any system with Docker
- Automatic compression

**Steps:**

**Windows:**
```powershell
.\download-database-docker.ps1
```

**Linux/Mac:**
```bash
chmod +x download-database.sh
./download-database.sh
```

---

### Method 2: Direct pg_dump Connection

**Requirements:**
- PostgreSQL client tools installed
- Database port must be accessible from your machine

**Windows (PowerShell):**
```powershell
.\download-database.ps1
```

**Linux/Mac:**
```bash
chmod +x download-database.sh
./download-database.sh
```

**Manual command:**
```bash
# Set password
export PGPASSWORD="1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^"

# Download database
pg_dump -h 185.208.172.76 -p 5432 -U postgres -d multivendor_db -F p -f backup.sql

# Compress
gzip backup.sql
```

---

### Method 3: SSH into Server and Dump

**Steps:**

1. **SSH into your VPS:**
   ```bash
   ssh root@185.208.172.76
   ```

2. **Dump the database from CapRover container:**
   ```bash
   docker exec srv-captain--postgres-db pg_dump -U postgres multivendor_db > backup.sql
   ```

3. **Download the file to your local machine:**
   ```bash
   # From your local machine (not SSH session)
   scp root@185.208.172.76:/root/backup.sql ./database_backups/
   ```

4. **Restore to local database:**
   ```bash
   # Make sure local Docker database is running
   docker-compose up -d db
   
   # Restore
   cat backup.sql | docker exec -i multivendor_db psql -U postgres -d multivendor_db
   ```

---

### Method 4: Using CapRover Dashboard

1. **Open CapRover dashboard:**
   - Go to: https://captain.indexo.ir
   - Login with your credentials

2. **Access PostgreSQL container:**
   - Click on **"Apps"** in sidebar
   - Find and click **"postgres-db"**
   - Click **"One-Click Apps/Databases"** tab
   - Or use the **"Terminal"** tab

3. **Export database:**
   ```bash
   # In the terminal
   pg_dump -U postgres multivendor_db > /captain/data/backup.sql
   ```

4. **Download via file manager or SCP**

---

### Method 5: Using Django dumpdata (Alternative)

**If you have backend access, you can use Django's management command:**

1. **SSH into backend container:**
   ```bash
   ssh root@185.208.172.76
   # Or access via CapRover dashboard
   ```

2. **Run dumpdata:**
   ```bash
   docker exec multivendor-backend python manage.py dumpdata > backup.json
   ```

3. **Download and restore locally:**
   ```bash
   # Download file
   scp root@185.208.172.76:/path/to/backup.json ./
   
   # Restore locally
   python manage.py loaddata backup.json
   ```

**Note:** This method only exports data, not the database schema. You'll need to run migrations first.

---

## 🔄 Restoring to Local Database

### Option A: Using the Scripts (Automatic)

The provided scripts will ask if you want to restore after downloading. Just type `yes` when prompted.

### Option B: Manual Restore

1. **Make sure local database is running:**
   ```bash
   docker-compose up -d db
   ```

2. **Drop and recreate database:**
   ```bash
   docker exec multivendor_db psql -U postgres -c "DROP DATABASE IF EXISTS multivendor_db;"
   docker exec multivendor_db psql -U postgres -c "CREATE DATABASE multivendor_db;"
   ```

3. **Restore backup:**
   ```bash
   # If compressed
   gunzip -c backup.sql.gz | docker exec -i multivendor_db psql -U postgres -d multivendor_db
   
   # If uncompressed
   cat backup.sql | docker exec -i multivendor_db psql -U postgres -d multivendor_db
   ```

4. **Run migrations (if needed):**
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

---

## 🔧 Configuration

You can customize the scripts by editing these variables:

**PowerShell scripts:**
```powershell
param(
    [string]$ServerIP = "185.208.172.76",
    [string]$DbName = "multivendor_db",
    [string]$DbUser = "postgres",
    [string]$DbPassword = "1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^",
    [int]$DbPort = 5432,
    [string]$BackupDir = ".\database_backups"
)
```

**Bash script:**
```bash
SERVER_IP="${SERVER_IP:-185.208.172.76}"
DB_NAME="${DB_NAME:-multivendor_db}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^}"
DB_PORT="${DB_PORT:-5432}"
BACKUP_DIR="${BACKUP_DIR:-./database_backups}"
```

---

## ⚠️ Troubleshooting

### Connection Refused Error

**Problem:** Can't connect to database directly

**Solutions:**
1. The database might not be exposed on port 5432. Use SSH method instead
2. Check firewall settings on your VPS
3. Use CapRover dashboard terminal method

### Docker Not Running

**Problem:** Docker commands fail

**Solution:**
- Windows: Start Docker Desktop
- Linux: `sudo systemctl start docker`
- Mac: Start Docker Desktop

### Permission Denied

**Problem:** Can't write to backup directory

**Solution:**
```bash
# Create directory with proper permissions
mkdir -p database_backups
chmod 755 database_backups
```

### Database Already Exists Error

**Problem:** Local database already exists when restoring

**Solution:**
The scripts automatically drop and recreate the database. If doing manually:
```bash
docker exec multivendor_db psql -U postgres -c "DROP DATABASE IF EXISTS multivendor_db;"
docker exec multivendor_db psql -U postgres -c "CREATE DATABASE multivendor_db;"
```

---

## 📁 Backup File Locations

All backups are saved to:
- **Windows:** `.\database_backups\`
- **Linux/Mac:** `./database_backups/`

Files are named: `multivendor_db_YYYYMMDD_HHMMSS.sql.gz`

---

## 🔐 Security Notes

⚠️ **Important:** The database password is hardcoded in the scripts for convenience. In production environments:

1. Use environment variables
2. Use `.env` files (and add them to `.gitignore`)
3. Use password managers or secure vaults
4. Never commit passwords to version control

---

## 🚀 Quick Reference

| Method | Windows | Linux/Mac | Requires |
|--------|---------|-----------|----------|
| Docker Script | ✅ `download-database-docker.ps1` | ✅ `download-database.sh` | Docker |
| Direct pg_dump | ✅ `download-database.ps1` | ✅ `download-database.sh` | PostgreSQL client |
| SSH Method | ✅ Manual | ✅ Manual | SSH access |
| CapRover Dashboard | ✅ Manual | ✅ Manual | Web access |
| Django dumpdata | ✅ Manual | ✅ Manual | Backend access |

---

## 💡 Tips

1. **Regular Backups:** Set up automated backups on your server (see `backup-database.sh`)
2. **Compression:** Always compress large databases to save space
3. **Test Restores:** Periodically test restoring backups to ensure they work
4. **Keep Multiple Versions:** Don't delete old backups immediately
5. **Document Changes:** Note any schema changes before restoring

---

## 📞 Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your database credentials
3. Ensure Docker/services are running
4. Check network connectivity to server




