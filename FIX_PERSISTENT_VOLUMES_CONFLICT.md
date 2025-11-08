# Fix Persistent Volumes Conflict - CRITICAL ISSUE

## 🚨 Problem Identified

Your persistent directories are configured incorrectly:

**Current (WRONG) Configuration:**
- `/app/staticfiles` → `/captain/dat` ❌
- `/app/media` → `/captain/dat` ❌

**Both directories are pointing to the SAME host path!** This causes:
- ❌ Data corruption (files overwrite each other)
- ❌ Container crashes (volume mount conflicts)
- ❌ Backend won't start (`replicated 0/1`)

## ✅ Correct Configuration

Each directory needs a **unique** host path:

**Correct Configuration:**
- `/app/staticfiles` → `/captain/data/backend-static` ✅
- `/app/media` → `/captain/data/backend-media` ✅

## 🔧 Fix Steps

### Step 1: Remove Current Configuration

1. Go to CapRover Dashboard → Backend App → App Configs
2. Scroll to **Persistent Directories** section
3. **Remove both entries** (click delete/remove button for each)
4. Click **"Save & Update"**

### Step 2: Add Correct Configuration

1. **Add First Directory:**
   - Click **"Add Persistent Directory"**
   - **Path in App:** `/app/staticfiles`
   - **Label:** `static-files` (optional)
   - Click **"Set specific host path"**
   - **Host Path:** `/captain/data/backend-static` ⚠️ **NOT `/captain/dat`**
   - Click **Save**

2. **Add Second Directory:**
   - Click **"Add Persistent Directory"** again
   - **Path in App:** `/app/media`
   - **Label:** `media-files` (optional)
   - Click **"Set specific host path"**
   - **Host Path:** `/captain/data/backend-media` ⚠️ **NOT `/captain/dat`**
   - Click **Save**

### Step 3: Verify Configuration

Before saving, verify you have:

```
Path in App: /app/staticfiles
Path on Host: /captain/data/backend-static

Path in App: /app/media
Path on Host: /captain/data/backend-media
```

**Important:** Make sure the host paths are **different**!

### Step 4: Save and Restart

1. Click **"Save & Update"** or **"Save & Restart"**
2. Wait 2-3 minutes for deployment
3. Check app status - should show `1/1` (running)

## 🔍 Verify Fix

After deployment, check container status:

```bash
docker ps | grep multivendor-backend
```

Should show:
```
srv-captain--multivendor-backend   replicated   1/1   ...   Up X minutes
```

**Not:**
```
srv-captain--multivendor-backend   replicated   0/1   ...   (crashed)
```

## 📋 Common Mistakes to Avoid

### ❌ Wrong:
- Both directories → `/captain/dat`
- Both directories → `/captain/data`
- Both directories → Same path

### ✅ Correct:
- `/app/staticfiles` → `/captain/data/backend-static`
- `/app/media` → `/captain/data/backend-media`

## 🆘 If Container Still Won't Start

### Check Logs:

1. **Via CapRover Dashboard:**
   - Go to Backend App → App Logs
   - Look for volume mount errors

2. **Via SSH:**
   ```bash
   ssh root@185.208.172.76
   docker logs srv-captain--multivendor-backend.1.<container-id> --tail 100
   ```

### Common Errors:

1. **Volume mount conflict:**
   - Error: "Error response from daemon: invalid mount config"
   - **Fix:** Remove duplicate host paths

2. **Permission denied:**
   - Error: "Permission denied" or "Cannot access"
   - **Fix:** CapRover handles permissions automatically, but check if paths exist

3. **Path doesn't exist:**
   - Error: "No such file or directory"
   - **Fix:** CapRover creates paths automatically, but verify spelling

## ✅ Expected Result

After fixing:

1. ✅ Backend container shows `1/1` (running)
2. ✅ App logs are visible
3. ✅ Static files persist across deployments
4. ✅ Media files persist across deployments
5. ✅ No volume mount conflicts

---

**Status**: Critical fix required
**Priority**: High - Container won't start until fixed

