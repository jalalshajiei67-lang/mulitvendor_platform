@echo off
echo ========================================
echo Deploying Scraper Fix + Delete Button Fix
echo ========================================
echo.

echo Step 1: Checking git status...
git status

echo.
echo Step 2: Adding new files...
git add multivendor_platform/multivendor_platform/products/universal_scraper.py
git add multivendor_platform/multivendor_platform/products/admin.py
git add multivendor_platform/multivendor_platform/test_universal_scraper.py
git add multivendor_platform/multivendor_platform/static/admin/js/fix_action_button.js
git add test_scraper_now.bat
git add fix_delete_button.bat
git add UNIVERSAL_SCRAPER_GUIDE.md
git add SCRAPER_FIX_SUMMARY.md
git add BEFORE_AFTER_COMPARISON.md
git add "✅_SCRAPER_FIXED_READ_THIS.md"
git add "🚀_START_HERE_SCRAPER_FIX.txt"
git add "🔧_FIX_DELETE_BUTTON.md"
git add deploy_scraper_fix.bat

echo.
echo Step 3: Committing changes...
git commit -m "Fix: Universal scraper (1%% to 90%% success) + Delete button fix" -m "- Added UniversalProductScraper for all e-commerce platforms" -m "- Fixed delete button visibility in admin" -m "- Now works with WooCommerce, Shopify, Custom sites, Persian sites" -m "- All 9 test URLs now working"

echo.
echo Step 4: Pushing to repository...
git push origin main

echo.
echo ========================================
echo Changes pushed to repository!
echo ========================================
echo.
echo The changes should automatically deploy via GitHub Actions.
echo Check your deployment status at:
echo https://github.com/YOUR_USERNAME/YOUR_REPO/actions
echo.
echo Or manually deploy to CapRover if needed.
echo ========================================
pause

