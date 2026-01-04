#!/bin/bash
# Test script to check seller signup flow

echo "=========================================="
echo "Testing Seller Signup Flow"
echo "=========================================="
echo ""

cd /media/jalal/New\ Volume/project/mulitvendor_platform/multivendor_platform

echo "1. Checking existing seller users..."
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
from users.models import UserProfile, VendorProfile, Supplier

# Find all sellers
seller_profiles = UserProfile.objects.filter(role__in=['seller', 'both']).select_related('user')
print(f"\nTotal seller profiles: {seller_profiles.count()}")

missing_vendor = []
missing_supplier = []

for profile in seller_profiles:
    user = profile.user
    has_vendor = hasattr(user, 'vendor_profile')
    has_supplier = hasattr(user, 'supplier')
    
    if not has_vendor:
        missing_vendor.append(user.username)
    if not has_supplier:
        missing_supplier.append(user.username)

print(f"\nUsers missing VendorProfile: {len(missing_vendor)}")
if missing_vendor:
    print(f"  Users: {', '.join(missing_vendor[:10])}" + (" ..." if len(missing_vendor) > 10 else ""))

print(f"\nUsers missing Supplier: {len(missing_supplier)}")
if missing_supplier:
    print(f"  Users: {', '.join(missing_supplier[:10])}" + (" ..." if len(missing_supplier) > 10 else ""))

EOF

echo ""
echo "2. Running management command to create missing objects (dry-run)..."
python manage.py create_missing_seller_objects --dry-run

echo ""
echo "=========================================="
echo "To fix missing objects, run:"
echo "  python manage.py create_missing_seller_objects"
echo "=========================================="

