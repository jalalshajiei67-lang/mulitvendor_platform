# Simple Integration Test Script

Write-Host "=== MULTIVENDOR PLATFORM - INTEGRATION TEST ===" -ForegroundColor Cyan

$passed = 0
$failed = 0

# Test 1: Database
Write-Host "`n[1/5] Database..." -ForegroundColor Yellow
docker exec multivendor_db_local pg_isready -U postgres
if ($LASTEXITCODE -eq 0) { Write-Host "PASS" -ForegroundColor Green; $passed++ } else { Write-Host "FAIL" -ForegroundColor Red; $failed++ }

# Test 2: Backend API
Write-Host "`n[2/5] Backend API..." -ForegroundColor Yellow
try {
    $r = Invoke-WebRequest -Uri http://localhost:8000/api/products/ -UseBasicParsing
    Write-Host "Status: $($r.StatusCode) - PASS" -ForegroundColor Green
    $passed++
}
catch {
    Write-Host "FAIL: $_" -ForegroundColor Red
    $failed++
}

# Test 3: Frontend
Write-Host "`n[3/5] Frontend..." -ForegroundColor Yellow
try {
    $r = Invoke-WebRequest -Uri http://localhost:8080 -UseBasicParsing
    Write-Host "Status: $($r.StatusCode) - PASS" -ForegroundColor Green
    $passed++
}
catch {
    Write-Host "FAIL: $_" -ForegroundColor Red
    $failed++
}

# Test 4: Backend-Database
Write-Host "`n[4/5] Backend-Database Connection..." -ForegroundColor Yellow
docker exec multivendor_backend_local python manage.py check
if ($LASTEXITCODE -eq 0) { Write-Host "PASS" -ForegroundColor Green; $passed++ } else { Write-Host "FAIL" -ForegroundColor Red; $failed++ }

# Test 5: Frontend-Backend
Write-Host "`n[5/5] Frontend-Backend Communication..." -ForegroundColor Yellow
docker exec multivendor_frontend_local wget -qO- http://backend:80/api/products/
if ($LASTEXITCODE -eq 0) { Write-Host "PASS" -ForegroundColor Green; $passed++ } else { Write-Host "FAIL" -ForegroundColor Red; $failed++ }

# Summary
Write-Host "`n=== RESULTS ===" -ForegroundColor Cyan
Write-Host "Passed: $passed/5" -ForegroundColor Green
Write-Host "Failed: $failed/5" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Red" })

if ($failed -eq 0) {
    Write-Host "`nAll tests PASSED!" -ForegroundColor Green
}
else {
    Write-Host "`nSome tests FAILED!" -ForegroundColor Red
}

