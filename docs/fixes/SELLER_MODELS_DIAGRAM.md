# Seller Models Relationship Diagram

## Before Fix ❌

```
User Registration (role='seller')
         ↓
┌─────────────────────┐
│       User          │
│  (Django Auth)      │
└─────────────────────┘
         ↓
┌─────────────────────┐
│    UserProfile      │
│  role = 'seller'    │
│  phone, address     │
└─────────────────────┘
         ↓
┌─────────────────────┐
│   VendorProfile     │ ✅ Created
│  store_name         │
│  is_approved=False  │
│  (for frontend)     │
└─────────────────────┘
         ↓
┌─────────────────────┐
│ VendorSubscription  │ ✅ Created
│  tier = free        │
└─────────────────────┘
         ↓
┌─────────────────────┐
│     Supplier        │ ❌ NOT Created!
│  (for products)     │    PROBLEM!
└─────────────────────┘
```

## After Fix ✅

```
User Registration (role='seller')
         ↓
┌─────────────────────┐
│       User          │
│  (Django Auth)      │
│  username, email    │
└─────────────────────┘
         ↓
┌─────────────────────┐
│    UserProfile      │ ✅ Created
│  role = 'seller'    │
│  phone, address     │
└─────────────────────┘
         ↓
    [SIGNAL TRIGGERED]
         ↓
    ┌────────────────────────┐
    │  Signal Handler        │
    │  (post_save)           │
    └────────────────────────┘
         ↓
    ┌────────────────────────┐
    │  1. VendorProfile      │ ✅ Created
    │     store_name (auto)  │
    │     is_approved=False  │
    │     Shows in /suppliers│
    └────────────────────────┘
         ↓
    ┌────────────────────────┐
    │  2. VendorSubscription │ ✅ Created
    │     tier = free        │
    │     limits, features   │
    └────────────────────────┘
         ↓
    ┌────────────────────────┐
    │  3. Supplier [NEW!]    │ ✅ NOW Created!
    │     name = store_name  │
    │     is_active = True   │
    │     For products/RFQs  │
    └────────────────────────┘
```

## Model Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                         User (Django)                        │
│                    username, email, password                 │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ↓                     ↓                     ↓
┌──────────────┐    ┌──────────────────┐    ┌──────────────┐
│ UserProfile  │    │  VendorProfile   │    │   Supplier   │
│ OneToOne     │    │  OneToOne        │    │  OneToOne    │
├──────────────┤    ├──────────────────┤    ├──────────────┤
│ role         │    │ store_name       │    │ name         │
│ phone        │    │ logo             │    │ website      │
│ address      │    │ description      │    │ phone        │
│ is_verified  │    │ is_approved ⭐   │    │ is_active    │
│ is_blocked   │    │ banner_image     │    │ logo         │
└──────────────┘    │ branding fields  │    │ description  │
                    │ portfolio        │    └──────────────┘
                    │ team members     │           │
                    └──────────────────┘           │
                            │                      │
                            │                      │
                    Used in Frontend       Used in Backend
                    (/suppliers list)      (Products, RFQs)
```

## Key Differences

### VendorProfile (Store/Shop)
- **Purpose:** Display in frontend, branding, mini-website
- **Approval:** Requires admin approval (`is_approved`)
- **Frontend:** Shows in `/suppliers` list
- **Fields:** Branding, portfolio, team, social media
- **Related:** SupplierComment, SupplierPortfolioItem, SupplierTeamMember

### Supplier (Company/Business)
- **Purpose:** Business entity for products and RFQs
- **Activation:** Auto-active (`is_active=True`)
- **Backend:** Used by Product, Order, CategoryRequest
- **Fields:** Basic company info, contact details
- **Related:** Product.supplier, Order.suppliers

## Data Flow

### Frontend Supplier List
```
GET /api/auth/suppliers/
         ↓
SupplierViewSet (views.py)
         ↓
VendorProfile.objects.filter(is_approved=True)
         ↓
VendorProfileSerializer
         ↓
JSON Response → Frontend displays
```

### Product Creation
```
Seller creates product
         ↓
Product.supplier = user.supplier
         ↓
If Supplier missing → ERROR ❌
         ↓
[NOW FIXED] ✅
```

### RFQ Assignment
```
Admin assigns RFQ to suppliers
         ↓
Order.suppliers.add(user.supplier)
         ↓
If Supplier missing → ERROR ❌
         ↓
[NOW FIXED] ✅
```

## Complete Object Tree

```
User (jalal)
├── UserProfile
│   ├── role: 'seller'
│   ├── phone: '09123456789'
│   └── is_verified: False
│
├── VendorProfile (Store Display)
│   ├── store_name: 'فروشگاه_jalal_a1b2c3'
│   ├── is_approved: False (needs admin approval)
│   ├── description: ''
│   ├── SupplierPortfolioItems: []
│   ├── SupplierTeamMembers: []
│   └── SupplierComments: []
│
├── Supplier (Company Entity) [NOW CREATED!]
│   ├── name: 'فروشگاه_jalal_a1b2c3'
│   ├── is_active: True
│   ├── Products: []
│   └── Orders (RFQs): []
│
├── VendorSubscription
│   ├── tier: PricingTier (free)
│   ├── is_active: True
│   └── features: [...]
│
└── BuyerProfile (if role='both')
    ├── shipping_address: ''
    └── orders: []
```

## Signal Flow Detail

```python
# users/signals.py

@receiver(post_save, sender=UserProfile)
def create_or_update_role_profiles(sender, instance, created, **kwargs):
    
    if instance.role in ['seller', 'both']:
        
        # Step 1: Create VendorProfile
        vendor_profile, vendor_created = VendorProfile.objects.get_or_create(
            user=instance.user,
            defaults={
                'store_name': _generate_unique_store_name(instance.user.username),
                'description': ''
            }
        )
        
        # Step 2: Create VendorSubscription
        VendorSubscription.for_user(instance.user)
        
        # Step 3: Create Supplier [NEW!]
        supplier, supplier_created = Supplier.objects.get_or_create(
            vendor=instance.user,
            defaults={
                'name': vendor_profile.store_name,
                'is_active': True,
            }
        )
```

## Why Two Models?

### Historical Context
1. **VendorProfile** was created first for seller profiles
2. **Supplier** was added later for scraped company data
3. Both evolved to serve different purposes
4. Now both are needed for complete seller functionality

### Design Decision
- Keep both models for separation of concerns
- VendorProfile = User-facing store
- Supplier = System-level business entity
- Could be merged in future, but would require major refactoring

## Migration Path

### For Existing Users
```bash
# Find users missing Supplier
python3 manage.py create_missing_seller_objects --dry-run

# Create missing Supplier objects
python3 manage.py create_missing_seller_objects

# Verify
python3 manage.py shell
>>> from users.models import UserProfile, Supplier
>>> UserProfile.objects.filter(role__in=['seller','both']).count()
>>> Supplier.objects.count()
# Should be equal!
```

### For New Users
- Signal automatically creates both
- No manual intervention needed
- All objects created atomically

## Summary

| Aspect | Before | After |
|--------|--------|-------|
| VendorProfile | ✅ Created | ✅ Created |
| Supplier | ❌ Missing | ✅ Created |
| Products work | ❌ No | ✅ Yes |
| RFQs work | ❌ No | ✅ Yes |
| Frontend lists | ✅ Yes | ✅ Yes |
| Complete flow | ❌ Broken | ✅ Fixed |


