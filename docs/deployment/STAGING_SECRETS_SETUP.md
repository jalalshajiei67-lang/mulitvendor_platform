# Staging Deployment - Required GitHub Secrets

## ⚠️ Error Fix: Missing Server Host

If you're seeing the error: **"missing server host"**, you need to add the required secrets to your GitHub repository.

## Required Secrets for Staging Deployment

Go to: **GitHub Repository → Settings → Secrets and variables → Actions → New repository secret**

### 1. `HOST` (Required)
- **Value:** Your VPS IP address
- **Example:** `185.208.172.76`
- **Used for:** SSH connection to deploy staging

### 2. `VPS_USER` (Required)
- **Value:** SSH username for your VPS
- **Example:** `root`
- **Used for:** SSH authentication

### 3. `VPS_SSH_KEY` (Required)
- **Value:** Your private SSH key for VPS access
- **How to get:** 
  ```bash
  # On your local machine:
  cat ~/.ssh/id_rsa
  # Or if you have a specific key:
  cat ~/.ssh/your_key_name
  ```
- **Used for:** SSH key authentication

## Quick Setup Steps

1. **Add HOST secret:**
   - Name: `HOST`
   - Value: `185.208.172.76` (or your VPS IP)

2. **Add VPS_USER secret:**
   - Name: `VPS_USER`
   - Value: `root` (or your SSH username)

3. **Add VPS_SSH_KEY secret:**
   - Name: `VPS_SSH_KEY`
   - Value: (paste your private SSH key content)

## After Adding Secrets

Once all secrets are added, the deployment should work. The workflow will automatically:
1. Build Docker images
2. Push to GitHub Container Registry
3. SSH to your VPS
4. Pull and deploy staging containers

## Verify Secrets

Make sure these secrets exist in your GitHub repository:
- ✅ `HOST`
- ✅ `VPS_USER`
- ✅ `VPS_SSH_KEY`


