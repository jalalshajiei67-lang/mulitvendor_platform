# How to Fix Merge Conflict in Main Branch

The `main` branch has merge conflict markers in `settings.py` at line 167. The fix is already committed on `staging` branch.

## Quick Fix (Recommended)

Since you can't checkout `main` due to the untracked file, use one of these methods:

### Method 1: Using GitHub Web Interface (Easiest)

1. Go to your repository on GitHub
2. Switch to the `main` branch
3. Navigate to `multivendor_platform/multivendor_platform/multivendor_platform/settings.py`
4. Click "Edit" (pencil icon)
5. Find line 167 and remove the merge conflict markers:
   - Remove lines 167-177 (the `<<<<<<< HEAD`, `=======`, and `>>>>>>> ...` lines)
   - Keep only: `print(f"[CORS] Allowed origins: {CORS_ALLOWED_ORIGINS}")`
6. Also remove duplicate `MEDIA_URL`/`MEDIA_ROOT` around line 284-286
7. Remove duplicate `CORS_EXPOSE_HEADERS` and `CORS_PREFLIGHT_MAX_AGE` (lines 211-218)
8. Commit directly to `main` branch

### Method 2: Using Git Commands

```powershell
# 1. Move or commit the untracked file first
git add fix-letsencrypt-rate-limit.sh
git commit -m "Add fix-letsencrypt-rate-limit.sh"

# 2. Now checkout main
git checkout main
git pull origin main

# 3. Merge the fix from staging
git merge staging

# 4. If merge conflict occurs, resolve it by keeping staging's version
# Then commit and push
git push origin main
```

### Method 3: Cherry-pick the Fix Commit

```powershell
# 1. Move the untracked file
git add fix-letsencrypt-rate-limit.sh
git commit -m "Add fix-letsencrypt-rate-limit.sh"

# 2. Checkout main
git checkout main
git pull origin main

# 3. Cherry-pick the fix commit (0415939)
git cherry-pick 0415939

# 4. Push to main
git push origin main
```

## What Needs to be Fixed

1. **Line 167-177**: Remove merge conflict markers and keep:
   ```python
   # Debug: Log CORS origins in development
   if DEBUG:
       print(f"[CORS] Allowed origins: {CORS_ALLOWED_ORIGINS}")
   ```

2. **Lines 284-286**: Remove duplicate `MEDIA_URL` and `MEDIA_ROOT` (already defined at lines 145-146)

3. **Lines 211-218**: Remove duplicate `CORS_EXPOSE_HEADERS` and `CORS_PREFLIGHT_MAX_AGE` (already defined at lines 220-229)

## Verify the Fix

After applying the fix, verify the file is valid:
```powershell
cd multivendor_platform/multivendor_platform
python -m py_compile multivendor_platform/settings.py
```

If no errors, the fix is correct!

