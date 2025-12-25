#!/usr/bin/env python
"""
Script to create Django superuser non-interactively for production
Usage with Docker Compose:
  docker-compose exec backend python create_superuser_production.py
  
Or with environment variables:
  docker-compose exec backend bash -c "SUPERUSER_USERNAME=admin SUPERUSER_EMAIL=admin@indexo.ir SUPERUSER_PASSWORD=your_secure_password python create_superuser_production.py"

Usage with Docker directly:
  docker exec -it multivendor_backend python create_superuser_production.py
"""
import os
import sys
import django

# Setup Django with production settings
sys.path.insert(0, '/app')
# Use default settings (multivendor_platform.settings) which reads from environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Get credentials from environment or use defaults
username = os.environ.get('SUPERUSER_USERNAME', 'admin')
email = os.environ.get('SUPERUSER_EMAIL', 'admin@indexo.ir')
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

print("\n" + "="*50)
print("Superuser credentials:")
print(f"  Username: {username}")
print(f"  Email: {email}")
print(f"  Password: {password}")
print("="*50)

# Get API domain from environment or use default
api_domain = os.environ.get('API_DOMAIN', 'multivendor-backend.indexo.ir')
print(f"\nAdmin URL: https://{api_domain}/admin/")
print("="*50)

