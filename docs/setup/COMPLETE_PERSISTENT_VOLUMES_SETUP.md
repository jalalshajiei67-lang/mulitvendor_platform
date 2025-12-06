# Complete Persistent Volumes Setup - Action Required

## ✅ Current Status

You have correctly added persistent directories:
- ✅ `/app/staticfiles` (Label: `static-files`)
- ✅ `/app/media` (Label: `media-files`)

## ⚠️ Action Required: Set Host Paths

You need to **set specific host paths** for each directory. Currently, the "Set specific host path" buttons are visible, which means host paths are not configured yet.

## 🎯 Step-by-Step Instructions

### Step 1: Set Host Path for Static Files

1. **Click** the "Set specific host path" button next to `/app/staticfiles`
2. **Enter** the host path: `/captain/data/backend-static`
3. **Click Save** or **OK**

### Step 2: Set Host Path for Media Files

1. **Click** the "Set specific host path" button next to `/app/media`
2. **Enter** the host path: `/captain/data/backend-media`
3. **Click Save** or **OK**

### Step 3: Save and Update App

After setting both host paths:

1. **Scroll down** to find the **"Save & Update"** or **"Save & Restart"** button
2. **Click** it to apply the changes
3. **Wait** 1-2 minutes for CapRover to redeploy your app

## 📋 Final Configuration

After completing the setup, your persistent directories should look like:

| Path in App | Label | Host Path |
|-------------|-------|-----------|
| `/app/staticfiles` | `static-files` | `/captain/data/backend-static` |
| `/app/media` | `media-files` | `/captain/data/backend-media` |

## ✅ Verification

After deployment, verify the setup:

1. **Check App Logs** - Should show app started successfully
2. **Test Static Files** - Visit `https://multivendor-backend.indexo.ir/static/admin/css/base.css`
3. **Test Media Files** - Upload an image through Django admin and verify it persists after redeployment

## 🔍 Why Set Host Paths?

**Without host paths:**
- CapRover creates random volume names
- Harder to manage and backup
- Less predictable storage location

**With specific host paths:**
- ✅ Predictable storage location (`/captain/data/backend-static`)
- ✅ Easier to backup and manage
- ✅ Can be shared between apps if needed
- ✅ Better organization

## 📝 Notes

- The host paths (`/captain/data/backend-static` and `/captain/data/backend-media`) are on the **CapRover host server**, not inside the container
- These directories will be created automatically by CapRover if they don't exist
- Data in these directories will persist across container restarts and deployments
- Make sure you have enough disk space on your VPS

---

**Status**: Ready to complete setup
**Action**: Set host paths and save

