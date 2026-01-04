# Seller Signup Flow Fix

## Issue Summary
Users who registered as sellers were missing required objects:
- ✅ **UserProfile** - Created correctly
- ✅ **VendorProfile** - Created correctly (shows in frontend lists)
- ❌ **Supplier** - Was NOT being created automatically

## Root Cause
The signal handler in `users/signals.py` was only creating `VendorProfile` but not the `Supplier` model when a user registered as a seller.

### Model Relationships
The system has TWO related but distinct models for sellers:

1. **VendorProfile** (users.VendorProfile)
   - OneToOne with User (related_name='vendor_profile')
   - Store/shop information for display
   - Has `is_approved` field for admin approval
   - **Shows in frontend supplier lists** (/suppliers)
   - Contains branding, portfolio, team members

2. **Supplier** (users.Supplier)
   - OneToOne with User (related_name='supplier')
   - Company/business entity information
   - Used for Products (Product.supplier ForeignKey)
   - Used for RFQs (Order.suppliers ManyToMany)
   - Used for category requests

## Changes Made

### 1. Updated Signal Handler (`users/signals.py`)

**Added Supplier model import:**
```python
from .models import UserProfile, BuyerProfile, VendorProfile, VendorSubscription, Supplier
```

**Added Supplier creation in signal:**
```python
# Create Supplier model (company/supplier info)
# This is required for products and RFQ system
try:
    supplier, supplier_created = Supplier.objects.get_or_create(
        vendor=instance.user,
        defaults={
            'name': vendor_profile.store_name,  # Use store name as default company name
            'is_active': True,
        }
    )
    if supplier_created:
        logger.info(f"Created Supplier for user {instance.user.id} ({instance.user.username}) with name: {supplier.name}")
except IntegrityError as e:
    logger.error(f"IntegrityError creating Supplier for user {instance.user.id}: {e}")
    # Try to get existing supplier
    try:
        supplier = Supplier.objects.get(vendor=instance.user)
        logger.info(f"Supplier already exists for user {instance.user.id}")
    except Supplier.DoesNotExist:
        logger.error(f"Supplier does not exist and could not be created for user {instance.user.id}")
        # Don't raise here - vendor can add supplier later
except Exception as e:
    logger.warning(f"Failed to create Supplier for user {instance.user.id}: {e}")
    # Don't raise - this is not critical for initial registration
```

### 2. Added Supplier Serializer (`users/serializers.py`)

**Added import:**
```python
from .models import (
    UserProfile, BuyerProfile, VendorProfile, Supplier, SellerAd, SellerAdImage, 
    # ... other imports
)
```

**Created SupplierSerializer:**
```python
class SupplierSerializer(serializers.ModelSerializer):
    """Serializer for Supplier (Company) model"""
    vendor_username = serializers.CharField(source='vendor.username', read_only=True)
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Supplier
        fields = [
            'id', 'vendor', 'vendor_username', 'name', 'website', 'phone', 'mobile',
            'email', 'address', 'description', 'logo', 'is_active', 
            'product_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['vendor', 'product_count', 'created_at', 'updated_at']
```

### 3. Created Management Command

**File:** `users/management/commands/create_missing_seller_objects.py`

This command fixes existing users who don't have all required objects.

**Usage:**
```bash
# Dry run (check what would be created)
python manage.py create_missing_seller_objects --dry-run

# Actually create missing objects
python manage.py create_missing_seller_objects
```

**What it does:**
- Finds all users with role 'seller' or 'both'
- Checks for missing VendorProfile, Supplier, and VendorSubscription
- Creates missing objects with proper defaults
- Reports detailed results

## Testing

### For New Registrations
1. Register a new user with role='seller'
2. Verify the following are created:
   - UserProfile (role='seller')
   - VendorProfile (with auto-generated store_name)
   - Supplier (with name=store_name)
   - VendorSubscription (free tier)

### For Existing Users
1. Run the management command:
   ```bash
   python manage.py create_missing_seller_objects --dry-run
   ```
2. Review the output to see what's missing
3. Run without --dry-run to fix:
   ```bash
   python manage.py create_missing_seller_objects
   ```

### Verification Queries

**Check seller users and their objects:**
```python
from django.contrib.auth.models import User
from users.models import UserProfile, VendorProfile, Supplier

# Find all sellers
sellers = UserProfile.objects.filter(role__in=['seller', 'both']).select_related('user')

for profile in sellers:
    user = profile.user
    has_vendor = hasattr(user, 'vendor_profile')
    has_supplier = hasattr(user, 'supplier')
    
    print(f"User: {user.username}")
    print(f"  - VendorProfile: {'✓' if has_vendor else '✗'}")
    print(f"  - Supplier: {'✓' if has_supplier else '✗'}")
```

## Frontend Impact

### Supplier Lists
The frontend `/suppliers` page uses **VendorProfile** model:
- API endpoint: `/api/auth/suppliers/`
- ViewSet: `SupplierViewSet` (uses VendorProfile queryset)
- Filters by `is_approved=True` for public listing
- Owners can see their own profile even if not approved

### Admin Dashboard
Both models are visible in Django admin:
- **VendorProfile** → "Supplier Profiles" section
- **Supplier** → "Suppliers/Companies" section

## Approval Flow

### VendorProfile Approval
- Field: `is_approved` (default=False)
- Controls visibility in frontend supplier lists
- Admin action: "Approve selected suppliers"

### Supplier Activation
- Field: `is_active` (default=True)
- Controls if supplier can be used for products/RFQs
- Created as active by default

## Registration Flow Diagram

```
User Registers (role='seller')
         ↓
RegisterSerializer.create()
         ↓
User.objects.create_user()
         ↓
UserProfile.objects.create(role='seller')
         ↓
[SIGNAL: post_save on UserProfile]
         ↓
    ┌────────────────────────┐
    │ create_or_update_role_ │
    │ profiles() signal      │
    └────────────────────────┘
         ↓
    ┌────────────────────────┐
    │ 1. Create/Get          │
    │    VendorProfile       │
    │    - store_name (auto) │
    │    - is_approved=False │
    └────────────────────────┘
         ↓
    ┌────────────────────────┐
    │ 2. Create/Get          │
    │    VendorSubscription  │
    │    - tier (free)       │
    └────────────────────────┘
         ↓
    ┌────────────────────────┐
    │ 3. Create/Get          │
    │    Supplier [NEW!]     │
    │    - name=store_name   │
    │    - is_active=True    │
    └────────────────────────┘
         ↓
Registration Complete ✓
```

## Files Modified

1. **users/signals.py**
   - Added Supplier import
   - Added Supplier creation logic in signal handler

2. **users/serializers.py**
   - Added Supplier import
   - Created SupplierSerializer class

3. **users/management/commands/create_missing_seller_objects.py** (NEW)
   - Management command to fix existing users

4. **docs/fixes/SELLER_SIGNUP_FIX.md** (NEW)
   - This documentation

## Deployment Steps

1. **Backup Database** (important!)
   ```bash
   python manage.py dumpdata > backup_before_fix.json
   ```

2. **Deploy Code Changes**
   - Pull latest code with signal changes
   - No migrations needed (models already exist)

3. **Fix Existing Users**
   ```bash
   # Check what needs to be fixed
   python manage.py create_missing_seller_objects --dry-run
   
   # Apply fixes
   python manage.py create_missing_seller_objects
   ```

4. **Verify**
   ```bash
   # Check in Django shell
   python manage.py shell
   >>> from users.models import UserProfile, Supplier
   >>> sellers = UserProfile.objects.filter(role__in=['seller', 'both']).count()
   >>> suppliers = Supplier.objects.count()
   >>> print(f"Sellers: {sellers}, Suppliers: {suppliers}")
   ```

5. **Test New Registration**
   - Register a new seller account
   - Verify all objects are created
   - Check admin panel shows all objects

## Rollback Plan

If issues occur:

1. **Restore database from backup:**
   ```bash
   python manage.py flush  # WARNING: Deletes all data
   python manage.py loaddata backup_before_fix.json
   ```

2. **Revert code changes:**
   ```bash
   git revert <commit-hash>
   ```

## Notes

- The signal is non-blocking for Supplier creation - if it fails, registration still succeeds
- VendorProfile is critical (blocks registration if fails)
- Supplier can be added manually later via admin if signal fails
- Store names are auto-generated with UUID to ensure uniqueness
- All new sellers get free tier subscription by default

## Related Models

- **BuyerProfile**: Created for role='buyer' or 'both'
- **VendorSubscription**: Manages subscription tiers and limits
- **Product**: Links to Supplier (not VendorProfile)
- **Order**: Can have multiple Suppliers for RFQs
- **CategoryRequest**: Links to Supplier

## Future Improvements

1. Add Supplier info to seller dashboard
2. Allow sellers to edit Supplier details separately from VendorProfile
3. Add Supplier approval workflow (currently auto-active)
4. Sync VendorProfile and Supplier fields automatically
5. Add data migration to merge duplicate suppliers (if any)

