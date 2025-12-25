#!/usr/bin/env python
"""
Script to create Django superuser non-interactively
Usage: python create_superuser.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'multivendor_platform', 'multivendor_platform'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Get credentials from environment or use defaults
username = os.environ.get('SUPERUSER_USERNAME', 'admin')
email = os.environ.get('SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('SUPERUSER_PASSWORD', 'admin123')

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f"User '{username}' already exists. Updating password...")
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"[OK] Updated password for user '{username}'")
else:
    # Create new superuser
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"[OK] Created superuser '{username}' with email '{email}'")

print("\nYou can now login to admin panel with:")
print(f"  Username: {username}")
print(f"  Password: {password}")
print(f"\nAdmin URL: http://127.0.0.1:8000/admin/")

