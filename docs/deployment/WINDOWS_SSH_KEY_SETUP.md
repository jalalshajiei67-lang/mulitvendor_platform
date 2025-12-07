# Windows SSH Key Setup for GitHub Actions

## Problem
On Windows, the `~/.ssh` directory might not exist, causing `ssh-keygen` to fail.

## Solution: Create SSH Key on Windows

### Method 1: Using PowerShell (Recommended)

```powershell
# 1. Create .ssh directory if it doesn't exist
$sshPath = "$env:USERPROFILE\.ssh"
if (!(Test-Path $sshPath)) {
    New-Item -ItemType Directory -Path $sshPath
}

# 2. Generate SSH key
ssh-keygen -t ed25519 -C "github-actions-production" -f "$sshPath\github_actions_production"

# When prompted for passphrase, just press Enter (empty passphrase for CI/CD)
```

### Method 2: Using Git Bash

If you have Git Bash installed:

```bash
# 1. Create .ssh directory
mkdir -p ~/.ssh

# 2. Generate SSH key
ssh-keygen -t ed25519 -C "github-actions-production" -f ~/.ssh/github_actions_production

# When prompted for passphrase, just press Enter twice (empty passphrase)
```

### Method 3: Manual Directory Creation

1. Open File Explorer
2. Navigate to `C:\Users\YourUsername\`
3. Create a new folder named `.ssh` (with the dot at the beginning)
4. Then run:
   ```powershell
   ssh-keygen -t ed25519 -C "github-actions-production" -f C:\Users\YourUsername\.ssh\github_actions_production
   ```

## After Generating Keys

You'll have two files:
- `github_actions_production` (private key - for GitHub Secret)
- `github_actions_production.pub` (public key - for VPS)

## Add Public Key to Production VPS

### Option A: Using ssh-copy-id (if available)

```powershell
# Install ssh-copy-id if needed (via Git Bash or WSL)
ssh-copy-id -i "$env:USERPROFILE\.ssh\github_actions_production.pub" root@91.107.172.234
```

### Option B: Manual Copy (Recommended for Windows)

1. **View your public key:**
   ```powershell
   Get-Content "$env:USERPROFILE\.ssh\github_actions_production.pub"
   ```

2. **Copy the entire output** (starts with `ssh-ed25519`)

3. **SSH to your production VPS:**
   ```powershell
   ssh root@91.107.172.234
   ```

4. **On the VPS, add the public key:**
   ```bash
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   echo "PASTE_YOUR_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   ```

## Add Private Key to GitHub Secrets

1. **View your private key:**
   ```powershell
   Get-Content "$env:USERPROFILE\.ssh\github_actions_production"
   ```

2. **Copy the entire output** (includes `-----BEGIN` and `-----END` lines)

3. **In GitHub:**
   - Go to your repository
   - **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `VPS_SSH_KEY`
   - Value: Paste the entire private key content
   - Click **Add secret**

## Verify Setup

Test SSH connection:
```powershell
ssh -i "$env:USERPROFILE\.ssh\github_actions_production" root@91.107.172.234
```

If this works, GitHub Actions should also work!

## For Staging (Separate Key)

If you want a separate key for staging:

```powershell
# Generate staging key
ssh-keygen -t ed25519 -C "github-actions-staging" -f "$env:USERPROFILE\.ssh\github_actions_staging"

# Add to staging VPS (185.208.172.76)
# Then add to GitHub Secret: STAGING_SSH_KEY
```

