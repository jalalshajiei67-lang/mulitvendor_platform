# GitHub Secrets Configuration for Production

## Required Secrets for Production Deployment

Go to: **GitHub Repository → Settings → Secrets and variables → Actions → New repository secret**

### Production Secrets (for `docker-deploy.yml`)

| Secret Name | Value | Description |
|------------|-------|-------------|
| `VPS_HOST` | `91.107.172.234` | Production VPS IP address |
| `VPS_USER` | `root` or `deploy` | SSH username for production VPS |
| `VPS_SSH_KEY` | Your private SSH key | Private key for production VPS access |

### Staging Secrets (for `deploy-staging.yml`)

| Secret Name | Value | Description |
|------------|-------|-------------|
| `STAGING_HOST` | `185.208.172.76` | Staging VPS IP address |
| `STAGING_USERNAME` | `root` | SSH username for staging VPS |
| `STAGING_SSH_KEY` | Your private SSH key | Private key for staging VPS access |

## Quick Setup Steps

### Step 1: Generate SSH Keys (Windows)

Open PowerShell and run:

```powershell
# Create .ssh directory if it doesn't exist
$sshPath = "$env:USERPROFILE\.ssh"
if (!(Test-Path $sshPath)) {
    New-Item -ItemType Directory -Path $sshPath
}

# Generate production SSH key
ssh-keygen -t ed25519 -C "github-actions-production" -f "$sshPath\github_actions_production"

# When prompted for passphrase, just press Enter (empty passphrase for CI/CD)
```

### Step 2: Add Public Key to Production VPS

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

### Step 3: Add Private Key to GitHub Secrets

1. **View your private key:**
   ```powershell
   Get-Content "$env:USERPROFILE\.ssh\github_actions_production"
   ```

2. **Copy the entire output** (includes `-----BEGIN` and `-----END` lines)

3. **In GitHub:**
   - Go to your repository
   - **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Add these secrets:

   **Secret 1:** (if not already set)
   - Name: `VPS_HOST`
   - Value: `91.107.172.234`

   **Secret 2:** (REQUIRED - add this)
   - Name: `VPS_USER`
   - Value: `root` (or your SSH username for production VPS)

   **Secret 3:** (if not already set)
   - Name: `VPS_SSH_KEY`
   - Value: Paste the entire private key content

### Step 4: Verify Setup

Test SSH connection:
```powershell
ssh -i "$env:USERPROFILE\.ssh\github_actions_production" root@91.107.172.234
```

If this works, GitHub Actions should also work!

## Separate Keys for Staging and Production

It's recommended to use separate SSH keys for staging and production:

### Generate Staging Key (if needed)

```powershell
ssh-keygen -t ed25519 -C "github-actions-staging" -f "$env:USERPROFILE\.ssh\github_actions_staging"
```

Then add the public key to staging VPS (`185.208.172.76`) and the private key to GitHub Secret `STAGING_SSH_KEY`.

## Summary

**Production VPS (91.107.172.234):**
- Uses secrets: `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY`
- Deployed via: `.github/workflows/docker-deploy.yml`
- Triggers on: Push to `main` branch

**Staging VPS (185.208.172.76):**
- Uses secrets: `STAGING_HOST`, `STAGING_USERNAME`, `STAGING_SSH_KEY`
- Deployed via: `.github/workflows/deploy-staging.yml`
- Triggers on: Push to `staging` branch

