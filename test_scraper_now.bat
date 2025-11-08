@echo off
echo ========================================
echo Testing Universal Scraper
echo ========================================
echo.

cd multivendor_platform\multivendor_platform
python test_universal_scraper.py

echo.
echo ========================================
echo Test Complete!
echo Check scraper_test_results.txt for details
echo ========================================
pause

