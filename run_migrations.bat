@echo off
echo Running database migrations...
python manage.py makemigrations users
python manage.py makemigrations orders
python manage.py migrate
echo.
echo Migrations completed!
echo.
echo Now you can run: python manage.py runserver
pause

