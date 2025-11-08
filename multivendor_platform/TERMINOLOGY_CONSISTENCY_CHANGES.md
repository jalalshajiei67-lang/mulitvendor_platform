# Terminology Consistency Changes

## Summary
Changed all "Seller" references to "Supplier" throughout the Django admin and system for consistency.

## Changes Made

### 1. **models.py** - UserProfile
```python
ROLE_CHOICES = (
    ('buyer', 'Buyer'),
    ('seller', 'Supplier'),  # Changed from 'Seller'
    ('both', 'Both'),
)
```

### 2. **models.py** - VendorProfile
- **Docstring**: Changed from "Vendor/Seller specific information" to "Supplier/Vendor specific information"
- **Help text**: Changed `is_approved` from "Approved by admin to sell" to "Approved by admin as supplier"
- **Added Meta class**:
  ```python
  class Meta:
      verbose_name = "Supplier Profile"
      verbose_name_plural = "Supplier Profiles"
  ```

### 3. **models.py** - SellerAd
- **Docstring**: Changed from "Advertisement created by sellers" to "Advertisement created by suppliers"
- **Added Meta class**:
  ```python
  class Meta:
      ordering = ['-created_at']
      verbose_name = "Supplier Advertisement"
      verbose_name_plural = "Supplier Advertisements"
  ```

### 4. **models.py** - SellerAdImage
- **Docstring**: Changed from "Images for seller advertisements" to "Images for supplier advertisements"
- **Added Meta class**:
  ```python
  class Meta:
      ordering = ['sort_order', 'created_at']
      verbose_name = "Supplier Ad Image"
      verbose_name_plural = "Supplier Ad Images"
  ```

### 5. **models.py** - UserProfile & BuyerProfile
- **Added Meta classes** for consistency:
  ```python
  class Meta:
      verbose_name = "User Profile"
      verbose_name_plural = "User Profiles"
  ```

### 6. **admin.py** - VendorProfileAdmin
- **Action description**: Changed from "Approve selected vendors" to "Approve selected suppliers"

### 7. **admin.py** - Admin Classes Renamed
- **SellerAdImageInline** → **SupplierAdImageInline**
- **SellerAdAdmin** → **SupplierAdAdmin**
- Added verbose names to inline:
  ```python
  verbose_name = "Supplier Ad Image"
  verbose_name_plural = "Supplier Ad Images"
  ```

## Impact

### Django Admin Display Names
Now shows:
- ✅ **Supplier Profiles** (instead of "Vendor profiles")
- ✅ **Supplier Advertisements** (instead of "Seller ads")
- ✅ **Supplier Ad Images**
- ✅ User role shows as **"Supplier"** (instead of "Seller")

### Database
- ⚠️ **No database changes required** - Only display names and help text were changed
- ⚠️ **No migrations needed** - Database schema remains the same
- ✅ Backward compatible with existing data

### Frontend
- Frontend already uses "Supplier" terminology (e.g., `/suppliers` route)
- Now consistent with backend

## Restart Required

**Yes** - Django server needs to be restarted to see the changes:
```bash
# Stop server (Ctrl+C)
python manage.py runserver
```

## Testing Checklist

After restart, verify in Django Admin:
- [ ] Navigate to http://127.0.0.1:8000/admin/
- [ ] Check "Users" section shows:
  - [ ] "User Profiles"
  - [ ] "Buyer Profiles"
  - [ ] "Supplier Profiles" (not "Vendor profiles")
  - [ ] "Supplier Advertisements" (not "Seller ads")
  - [ ] "Supplier Comments"
- [ ] Create/edit a user with role "Supplier" (not "Seller")
- [ ] Verify action "Approve selected suppliers" works

---

**Status**: ✅ Complete  
**Date**: October 18, 2025  
**Backward Compatible**: Yes  
**Database Migration Required**: No

