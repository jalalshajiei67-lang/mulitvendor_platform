# 📤 How to Transfer Files to VPS

## Method 1: Using SCP (Recommended - Simple)

### Transfer Single File

```bash
# From your local machine
scp diagnose-api-404.sh root@91.107.172.234:/root/indexo-production/
scp FIX_API_404_DOCKER_COMPOSE.md root@91.107.172.234:/root/indexo-production/
```

### Transfer Multiple Files

```bash
# Transfer both files at once
scp diagnose-api-404.sh FIX_API_404_DOCKER_COMPOSE.md root@91.107.172.234:/root/indexo-production/
```

### Make Script Executable After Transfer

```bash
# SSH to VPS first
ssh root@91.107.172.234

# Then make executable
cd /root/indexo-production
chmod +x diagnose-api-404.sh
```

## Method 2: Using the Transfer Script

I've created a helper script for you:

```bash
# Run from your local project directory
./transfer-to-vps.sh
```

This will automatically transfer both files to your VPS.

## Method 3: Using rsync (Better for Multiple Files)

```bash
# Sync files to VPS
rsync -avz diagnose-api-404.sh FIX_API_404_DOCKER_COMPOSE.md root@91.107.172.234:/root/indexo-production/
```

## Method 4: Manual Copy-Paste (For Small Files)

### For the Script (diagnose-api-404.sh)

1. Open the file locally
2. Copy all contents
3. SSH to VPS:
   ```bash
   ssh root@91.107.172.234
   ```
4. Create the file:
   ```bash
   cd /root/indexo-production
   nano diagnose-api-404.sh
   ```
5. Paste contents, save (Ctrl+O, Enter, Ctrl+X)
6. Make executable:
   ```bash
   chmod +x diagnose-api-404.sh
   ```

## Method 5: Using Git (If You Have Git on VPS)

### Push to Git Repository

```bash
# On local machine
git add diagnose-api-404.sh FIX_API_404_DOCKER_COMPOSE.md
git commit -m "Add API diagnostic tools"
git push
```

### Pull on VPS

```bash
# SSH to VPS
ssh root@91.107.172.234
cd /root/indexo-production
git pull
chmod +x diagnose-api-404.sh
```

## Quick One-Liner (All-in-One)

If you just want to transfer and run immediately:

```bash
# Transfer, make executable, and run in one command
scp diagnose-api-404.sh root@91.107.172.234:/root/indexo-production/ && \
ssh root@91.107.172.234 "cd /root/indexo-production && chmod +x diagnose-api-404.sh && ./diagnose-api-404.sh"
```

## Verify Files Are Transferred

After transferring, verify on VPS:

```bash
ssh root@91.107.172.234
cd /root/indexo-production
ls -lh diagnose-api-404.sh FIX_API_404_DOCKER_COMPOSE.md
```

Should show:
```
-rwxr-xr-x 1 root root ... diagnose-api-404.sh
-rw-r--r-- 1 root root ... FIX_API_404_DOCKER_COMPOSE.md
```

## Troubleshooting

### If SCP asks for password repeatedly:

Set up SSH key authentication:

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t rsa -b 4096

# Copy key to VPS
ssh-copy-id root@91.107.172.234
```

### If "Permission denied" error:

Check:
1. VPS user has write access to `/root/indexo-production/`
2. Directory exists on VPS
3. Correct path (maybe it's `/root/multivendor_platform` or different)

### If file path is different on VPS:

Find your project directory first:

```bash
ssh root@91.107.172.234
find /root -name "docker-compose.production.yml" 2>/dev/null
```

Then use that path in SCP command.

## Recommended Approach

**Easiest method for you:**

```bash
# 1. Transfer files
scp diagnose-api-404.sh FIX_API_404_DOCKER_COMPOSE.md root@91.107.172.234:/root/indexo-production/

# 2. SSH and run
ssh root@91.107.172.234
cd /root/indexo-production
chmod +x diagnose-api-404.sh
./diagnose-api-404.sh
```

That's it! 🚀

