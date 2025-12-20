# 📚 Step-by-Step: Fix Database Connection Issue

## Understanding the Problem

**What happened:**
1. Your deployment finished
2. Backend lost connection to database
3. This usually means the database was recreated empty during deployment

**The line ending error:**
- Windows uses `\r\n` (CRLF) for line endings
- Linux uses `\n` (LF) only
- The `^M` you see is the Windows carriage return character

---

## Step 1: Fix Line Endings on Server

**Run these commands on your server:**

```bash
# Navigate to deployment directory (you're already there)
cd /home/deploy/docker-deploy

# Fix line endings - removes Windows carriage returns
sed -i 's/\r$//' diagnose-db-connection.sh
sed -i 's/\r$//' restore-production-db.sh

# Verify the fix worked (should show no ^M characters)
cat -A diagnose-db-connection.sh | head -1
# If you see $ at the end (not ^M$), it's fixed!

# Make scripts executable
chmod +x diagnose-db-connection.sh restore-production-db.sh
```

**What each command does:**
- `sed -i 's/\r$//' filename` - Removes `\r` from end of each line
- `chmod +x filename` - Makes file executable (allows running with `./`)

---

## Step 2: Run Diagnostic Script

```bash
# Run the diagnostic to see what's wrong
./diagnose-db-connection.sh
```

**What to look for:**
- ✅ Green checkmarks = Everything OK
- ❌ Red X = Problem found
- ⚠️ Yellow warnings = Potential issues

**Common issues you might see:**
1. **Database doesn't exist** → Need to restore from backup
2. **Database has 0 tables** → Database is empty, need to restore
3. **Backend can't connect** → Check environment variables

---

## Step 3: Check What the Diagnostic Found

**If database exists but has 0 tables:**
```bash
# Check what's in the database
docker exec multivendor_db psql -U postgres -d multivendor_db -c "\dt"
```

**If database doesn't exist:**
```bash
# List all databases
docker exec multivendor_db psql -U postgres -c "\l"
```

---

## Step 4: Restore Database (If Needed)

**Option A: If you have a backup on the server**

```bash
# List available backups
ls -lh /opt/multivendor_platform/backups/*.sql* 2>/dev/null
ls -lh /home/deploy/docker-deploy/database_backups/*.sql* 2>/dev/null
ls -lh *.sql* 2>/dev/null

# Run restore script
./restore-production-db.sh
```

**Option B: Upload backup from your local machine**

**From your Windows machine (PowerShell):**
```powershell
# Upload your backup file
scp database_backups/multivendor_db_backup.sql.gz root@185.208.172.76:/home/deploy/docker-deploy/
```

**Then on server:**
```bash
# Run restore script
./restore-production-db.sh
# When asked, enter: multivendor_db_backup.sql.gz
```

---

## Step 5: Verify Restoration

```bash
# Check backend logs for errors
docker logs multivendor_backend --tail 50

# Test database connection
docker exec multivendor_backend python manage.py check --database default

# Check if tables were restored
docker exec multivendor_db psql -U postgres -d multivendor_db -c "\dt" | head -20
```

---

## Step 6: Run Migrations (If Needed)

```bash
# Apply any pending migrations
docker exec multivendor_backend python manage.py migrate --noinput
```

---

## Understanding Docker Commands

**Common Docker commands you'll use:**

```bash
# List running containers
docker ps

# View logs
docker logs <container_name> --tail 50

# Execute command in container
docker exec <container_name> <command>

# Restart container
docker restart <container_name>

# Check container health
docker inspect <container_name> | grep -A 5 Health
```

---

## Prevention: Fix Line Endings Before Upload

**To prevent this issue in the future, fix files before uploading:**

**On Windows (PowerShell):**
```powershell
# Install dos2unix (if available) or use Git
# Or use this PowerShell command:
(Get-Content diagnose-db-connection.sh -Raw) -replace "`r`n", "`n" | Set-Content diagnose-db-connection.sh -NoNewline
```

**Or configure Git (already done - see .gitattributes):**
- Git will now automatically convert line endings for `.sh` files
- Just commit and push normally

---

## Quick Reference

**Fix line endings:**
```bash
sed -i 's/\r$//' filename.sh
```

**Make executable:**
```bash
chmod +x filename.sh
```

**Run script:**
```bash
./filename.sh
```

**Check line endings:**
```bash
cat -A filename.sh | head -1
# Should end with $ (not ^M$)
```


