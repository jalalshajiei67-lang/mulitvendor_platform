# GitHub Secrets Setup for CI/CD

To enable automatic deployment to CapRover via GitHub Actions, you need to add these secrets to your GitHub repository.

## How to Add Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret below

## Required Secrets

### 1. CAPROVER_SERVER
The URL of your CapRover server
```
https://captain.indexo.ir
```

### 2. CAPROVER_APP_BACKEND
Your backend app name in CapRover
```
multivendor-backend
```

### 3. CAPROVER_APP_FRONTEND
Your frontend app name in CapRover
```
multivendor-frontend
```

### 4. CAPROVER_APP_TOKEN_BACKEND
App token for backend deployment

**How to get this:**
1. Go to CapRover Dashboard
2. Click on your backend app (`multivendor-backend`)
3. Go to **Deployment** tab
4. Find "App Token" section
5. Click "Enable App Token"
6. Copy the token

### 5. CAPROVER_APP_TOKEN_FRONTEND
App token for frontend deployment

**Follow the same steps as above, but for the frontend app**

## Testing the Deployment

After adding all secrets:

1. Make a change to your code
2. Commit and push to the `main` branch
3. Go to **Actions** tab in GitHub
4. Watch the deployment process
5. Check your CapRover apps for updates

## Manual Deployment Trigger

You can also manually trigger deployment:

1. Go to **Actions** tab
2. Click on "Deploy to CapRover" workflow
3. Click **Run workflow**
4. Select the `main` branch
5. Click **Run workflow**

## Troubleshooting

### Deployment Failed
- Check that all secrets are correctly added
- Verify your CapRover server is accessible
- Check CapRover app logs for errors

### App Token Invalid
- Regenerate the app token in CapRover
- Update the GitHub secret with the new token

