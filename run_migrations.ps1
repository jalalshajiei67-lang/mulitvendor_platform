Write-Host "Running database migrations..." -ForegroundColor Green

Write-Host "`nCreating migrations for users app..." -ForegroundColor Yellow
python manage.py makemigrations users

Write-Host "`nCreating migrations for orders app..." -ForegroundColor Yellow
python manage.py makemigrations orders

Write-Host "`nApplying all migrations..." -ForegroundColor Yellow
python manage.py migrate

Write-Host "`nMigrations completed successfully!" -ForegroundColor Green
Write-Host "`nYou can now run: python manage.py runserver" -ForegroundColor Cyan

Read-Host "`nPress Enter to continue"

