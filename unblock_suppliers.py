#!/usr/bin/env python3
"""
Quick script to unblock all supplier accounts
Run this from the project root directory
"""
import os
import sys
import django

# Setup Django environment
project_path = os.path.join(os.path.dirname(__file__), 'multivendor_platform', 'multivendor_platform')
sys.path.insert(0, project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multivendor_platform.settings')
django.setup()

from users.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()


def main():
    print("=" * 60)
    print("UNBLOCK USERS SCRIPT")
    print("=" * 60)
    
    # Get all blocked users
    blocked_profiles = UserProfile.objects.filter(is_blocked=True)
    
    if not blocked_profiles.exists():
        print("\n✅ No blocked users found!")
        return
    
    print(f"\n📋 Found {blocked_profiles.count()} blocked user(s):\n")
    for i, profile in enumerate(blocked_profiles, 1):
        print(f"{i}. Username: {profile.user.username}")
        print(f"   Phone: {profile.phone or 'N/A'}")
        print(f"   Email: {profile.user.email or 'N/A'}")
        print(f"   Role: {profile.get_role_display()}")
        print(f"   User ID: {profile.user.id}")
        print()
    
    # Ask for confirmation
    response = input("Do you want to unblock ALL these users? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        # Unblock all
        count = blocked_profiles.update(is_blocked=False)
        print(f"\n✅ Successfully unblocked {count} user(s)!")
    else:
        print("\n❌ Operation cancelled.")


if __name__ == '__main__':
    main()

