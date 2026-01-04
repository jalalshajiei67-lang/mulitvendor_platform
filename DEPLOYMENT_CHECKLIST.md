# Seller Signup Fix - Deployment Checklist

## Pre-Deployment

- [ ] Review changes in `users/signals.py`
- [ ] Review changes in `users/serializers.py`
- [ ] Review new management command `create_missing_seller_objects.py`
- [ ] Read documentation in `docs/fixes/SELLER_SIGNUP_FIX.md`

## Backup (IMPORTANT!)

- [ ] Backup database before deployment
  ```bash
  python3 manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json
  ```
- [ ] Or use your VPS backup system

## Deployment

- [ ] Pull latest code from repository
- [ ] Restart Django application
  ```bash
  # If using systemd
  sudo systemctl restart your-django-service
  
  # If using Docker
  docker-compose restart backend
  
  # If using CapRover
  # Push to your git repository and CapRover will auto-deploy
  ```

## Fix Existing Users

- [ ] Check what needs to be fixed (dry run):
  ```bash
  cd /path/to/multivendor_platform/multivendor_platform
  python3 manage.py create_missing_seller_objects --dry-run
  ```

- [ ] Review the output - note how many objects are missing

- [ ] Run the fix command:
  ```bash
  python3 manage.py create_missing_seller_objects
  ```

- [ ] Verify the output shows successful creation

## Verification

### 1. Check Database
- [ ] Open Django admin panel
- [ ] Go to "User Profiles" - check seller count
- [ ] Go to "Supplier Profiles" - check VendorProfile count
- [ ] Go to "Suppliers/Companies" - check Supplier count
- [ ] Numbers should match!

### 2. Test New Registration
- [ ] Open `/register` in browser
- [ ] Register new test user with role='seller'
- [ ] Check Django admin - verify all objects created:
  - [ ] User
  - [ ] UserProfile (role=seller)
  - [ ] VendorProfile (with auto-generated store_name)
  - [ ] Supplier (with name=store_name)
  - [ ] VendorSubscription

### 3. Test Frontend
- [ ] Go to `/suppliers` page
- [ ] Verify suppliers are listed
- [ ] Click on a supplier - verify detail page works
- [ ] Login as seller - verify dashboard works

### 4. Test Product Creation
- [ ] Login as seller
- [ ] Try to create a product
- [ ] Verify Supplier dropdown shows your company
- [ ] Create product successfully

## Monitoring

- [ ] Check application logs for any errors
- [ ] Monitor for the next 24 hours
- [ ] Check error tracking (Sentry, etc.) if available

## Rollback Plan (If Issues)

If something goes wrong:

1. [ ] Stop application
2. [ ] Restore database from backup
3. [ ] Revert code changes
4. [ ] Restart application
5. [ ] Investigate issue

## Success Criteria

✅ All existing sellers have Supplier objects
✅ New seller registrations create all required objects
✅ No errors in application logs
✅ Frontend supplier lists work correctly
✅ Sellers can create products
✅ Admin panel shows all objects correctly

## Post-Deployment

- [ ] Document any issues encountered
- [ ] Update team on changes
- [ ] Monitor user feedback
- [ ] Archive backup file

## Notes

- Signal is non-blocking - registration won't fail if Supplier creation fails
- Management command is idempotent - safe to run multiple times
- No database migrations needed - models already exist

## Contact

If you encounter issues:
1. Check logs first
2. Run management command again
3. Check Django admin for missing objects
4. Refer to full docs: `docs/fixes/SELLER_SIGNUP_FIX.md`

---

**Date:** $(date)
**Fixed by:** AI Assistant
**Ticket:** Seller signup flow - missing Supplier objects

