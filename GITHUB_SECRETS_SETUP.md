# GitHub Secrets Configuration Guide

## Required Secrets:

1. CAPROVER_SERVER - Your CapRover dashboard URL
   Example: https://captain.indexo.ir

2. CAPROVER_APP_BACKEND - Your backend app name
   Example: multivendor-backend

3. CAPROVER_APP_TOKEN_BACKEND - Backend app token
   Get from: CapRover Dashboard → Backend App → Deployment → Method 4

4. CAPROVER_APP_FRONTEND - Your frontend app name
   Example: multivendor-frontend

5. CAPROVER_APP_TOKEN_FRONTEND - Frontend app token
   Get from: CapRover Dashboard → Frontend App → Deployment → Method 4

## How to Get App Tokens:

1. Login to CapRover dashboard
2. Select your backend/frontend app
3. Go to Deployment tab
4. Look for 'Method 4: Deploy via webhook'
5. Copy the token from the webhook URL

Webhook URL format:
https://captain.indexo.ir/api/v2/user/apps/webhooks/triggerbuild?namespace=captain&token=YOUR_TOKEN_HERE
