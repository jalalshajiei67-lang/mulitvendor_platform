# Verify Staging GitHub Secrets

## ⚠️ Required GitHub Secrets

The workflows are looking for these secrets. They **MUST** match your CapRover app names exactly:

### Secret Names (Case-sensitive):

1. **`CAPROVER_URL`**
   - Value should be: `https://captain.indexo.ir`

2. **`CAPROVER_PASSWORD`**
   - Value: Your CapRover dashboard password

3. **`CAPROVER_BACKEND_STAGING_APP_NAME`**
   - Value should be: `multivendor-backend-staging` (exact match)
   - This must match the app name in CapRover

4. **`CAPROVER_FRONTEND_STAGING_APP_NAME`**
   - Value should be: `multivendor-frontend-staging` (exact match)
   - This must match the app name in CapRover

## 🔍 How to Check/Set Secrets

1. Go to your GitHub repository
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Verify each secret exists and has the correct value
4. If missing, click **New repository secret** and add them

## ✅ Verification Checklist

- [ ] `CAPROVER_URL` = `https://captain.indexo.ir`
- [ ] `CAPROVER_PASSWORD` = (your actual password)
- [ ] `CAPROVER_BACKEND_STAGING_APP_NAME` = `multivendor-backend-staging`
- [ ] `CAPROVER_FRONTEND_STAGING_APP_NAME` = `multivendor-frontend-staging`

## 🚨 Common Issues

1. **Secret not set**: Add the missing secret
2. **Wrong app name**: Ensure it matches exactly (case-sensitive)
3. **Typo in secret name**: The secret name must be exact: `CAPROVER_BACKEND_STAGING_APP_NAME`
4. **Wrong password**: Verify your CapRover password is correct

## 🔄 After Fixing Secrets

Once secrets are set correctly:
- Re-run the failed workflow in GitHub Actions, OR
- Push another commit to trigger a new deployment



