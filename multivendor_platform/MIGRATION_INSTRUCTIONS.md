# Database Migration Instructions

## The Issue
You're getting the error: `no such table: users_userprofile` because the new database tables haven't been created yet.

## Solution - Run Migrations

You need to create and apply the database migrations for the new user models.

### Option 1: Manual Commands (Recommended)

**Stop your Django server first (Ctrl+C)**, then run these commands in the same terminal where you usually run your Django server:

```bash
cd C:\Users\F003\Desktop\damirco\multivendor_platform\multivendor_platform

# Create migrations for the users app
python manage.py makemigrations users

# Create migrations for orders app (in case there are changes)
python manage.py makemigrations orders

# Apply all migrations
python manage.py migrate

# Start the server again
python manage.py runserver
```

### Option 2: Use the Batch Script

Double-click the file: `run_migrations.bat` in the `multivendor_platform/multivendor_platform/` directory.

### Option 3: Use PowerShell Script

Right-click `run_migrations.ps1` and select "Run with PowerShell"

## Expected Output

When you run `makemigrations users`, you should see something like:

```
Migrations for 'users':
  users\migrations\0002_buyerprofile_productreview_selleradimage_and_more.py
    - Create model BuyerProfile
    - Create model ProductReview
    - Create model SellerAdImage
    - Create model UserActivity
    - Add field is_approved to vendorprofile
    ... etc
```

When you run `migrate`, you should see:

```
Running migrations:
  Applying users.0002_buyerprofile_productreview_selleradimage_and_more... OK
  ... etc
```

## After Migrations

Once migrations are complete:
1. Restart your Django server: `python manage.py runserver`
2. Try logging in again from the Vue.js frontend
3. If you don't have a user yet, you can:
   - Register through the frontend at `/register`
   - Or create a superuser: `python manage.py createsuperuser`

## Troubleshooting

### If you get "No changes detected"
This means migrations already exist. Just run:
```bash
python manage.py migrate
```

### If you get module errors
Make sure you're using the virtual environment. Look for `(venv)` at the start of your command prompt.

If not activated:
```bash
# On Windows
venv\Scripts\activate

# Or navigate to:
C:\Users\F003\Desktop\damirco\venv\Scripts\activate
```

### If migrations fail
1. Check if there are any syntax errors in the models
2. Make sure all dependencies are installed
3. Try: `python manage.py migrate --run-syncdb`

## Creating Your First Admin User

After migrations, create an admin user:

```bash
python manage.py createsuperuser
```

Follow the prompts to set:
- Username
- Email
- Password

This admin user can then:
- Access Django admin at `http://127.0.0.1:8000/admin/`
- Manage all users through the admin dashboard at `/admin/dashboard`
- Approve sellers, block users, etc.

---

**Once migrations are done, your user management system will be fully functional!**

