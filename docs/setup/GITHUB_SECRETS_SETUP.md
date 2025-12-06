# GitHub Secrets Configuration Guide

## Required Secrets:

Set these in **GitHub → Settings → Secrets and variables → Actions → New repository secret**

1. **CAPROVER_SERVER** - Your CapRover dashboard URL
   - Value: `https://captain.indexo.ir`
   - Used by: GitHub Actions workflow

2. **CAPROVER_PASSWORD** - Your CapRover dashboard password
   - Value: Your CapRover login password
   - Used by: GitHub Actions workflow for authentication
   - How to get: Your CapRover dashboard password (set during initial setup)

3. **CAPROVER_BACKEND_APP_NAME** - Backend app name in CapRover
   - Value: `multivendor-backend`
   - Used by: GitHub Actions workflow to deploy backend

4. **CAPROVER_FRONTEND_APP_NAME** - Frontend app name in CapRover
   - Value: `multivendor-frontend`
   - Used by: GitHub Actions workflow to deploy frontend

## How to Get CapRover Password:

1. If you remember your password, use it directly
2. If you forgot, you can reset it:
   - SSH into your VPS: `ssh root@185.208.172.76`
   - Run: `docker exec captain-captain.1.<container-id> cat /captain/data/config-captain.json | grep password`
   - Or reset via CapRover dashboard if you have access

## Note:

The workflow uses **password-based authentication** (not app tokens). App tokens are not required for this setup.

