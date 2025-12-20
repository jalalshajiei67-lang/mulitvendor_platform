# Script to fix merge conflict in main branch
# This script will merge the fix from staging branch into main

Write-Host "🔧 Fixing merge conflict in main branch..." -ForegroundColor Cyan

# Stash any local changes
git stash

# Fetch latest from remote
git fetch origin main
git fetch origin staging

# Create a temporary branch from origin/main
git checkout -b fix-main-conflict origin/main

# Merge the fix commit from staging
git cherry-pick 0415939

# If cherry-pick fails, manually apply the fix
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Cherry-pick failed, applying manual fix..." -ForegroundColor Yellow
    
    # Read the current settings file
    $settingsPath = "multivendor_platform/multivendor_platform/multivendor_platform/settings.py"
    $content = Get-Content $settingsPath -Raw
    
    # Remove merge conflict markers (lines 167-177)
    $content = $content -replace '<<<<<<< HEAD.*?>>>>>>> [a-f0-9]+', ''
    $content = $content -replace '=======', ''
    
    # Remove duplicate MEDIA_URL/MEDIA_ROOT (around line 284-286)
    $content = $content -replace '(?s)# Media files configuration\s+MEDIA_URL = ''/media/''\s+MEDIA_ROOT = BASE_DIR / ''media''\s+', ''
    
    # Remove duplicate CORS_EXPOSE_HEADERS and CORS_PREFLIGHT_MAX_AGE
    $content = $content -replace '(?s)# Expose headers that frontend might need\s+CORS_EXPOSE_HEADERS = \[.*?\]\s+# Cache preflight requests for 1 hour\s+CORS_PREFLIGHT_MAX_AGE = 3600\s+', ''
    
    # Write back
    Set-Content -Path $settingsPath -Value $content -NoNewline
    
    # Verify syntax
    python -m py_compile $settingsPath
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ File syntax is valid" -ForegroundColor Green
        git add $settingsPath
        git commit -m "Fix: Resolve merge conflict in settings.py and remove duplicates"
    } else {
        Write-Host "❌ Syntax error in fixed file!" -ForegroundColor Red
        exit 1
    }
}

# Push to main (uncomment when ready)
# git push origin fix-main-conflict:main

Write-Host "✅ Fix applied! Review the changes and push to main when ready." -ForegroundColor Green
Write-Host "   To push: git push origin fix-main-conflict:main" -ForegroundColor Yellow






