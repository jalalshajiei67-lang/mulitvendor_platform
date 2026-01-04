# Migration Idempotency Fix - Stateless Migrations

## Problem
Migrations 0014 and 0015 were failing in production because:
1. **Migration 0014**: Tried to rename indexes that didn't exist, and the `monthly_price_rial` column was missing
2. **Migration 0015**: Tried to remove a `unique_together` constraint that didn't exist

These migrations were marked as "applied" but the actual database changes weren't executed, causing runtime errors.

## Solution
Made both migrations **idempotent** and **stateless** so they can be safely run multiple times and handle missing indexes/constraints gracefully.

### Migration 0014 Changes

**Before**: Direct `RenameIndex` and `AddField` operations that would fail if indexes/columns already existed or didn't exist.

**After**: 
- Uses `RunPython` with conditional logic to:
  - Only rename indexes if the old index exists and new index doesn't
  - Only add `monthly_price_rial` column if it doesn't exist
- Uses `SeparateDatabaseAndState` to separate actual database operations from Django's state tracking
- Handles PostgreSQL-specific operations gracefully

**Key Functions**:
- `rename_indexes_conditionally()`: Checks index existence before renaming
- `add_monthly_price_rial_conditionally()`: Checks column existence before adding

### Migration 0015 Changes

**Before**: Direct `AlterUniqueTogether` operation that would fail if the constraint didn't exist.

**After**:
- Uses `RunPython` with conditional logic to:
  - Only remove `unique_together` constraint if it exists
- Uses `SeparateDatabaseAndState` to separate actual database operations from Django's state tracking
- Checks for constraints on `(name, website)` before attempting removal

**Key Functions**:
- `remove_unique_together_conditionally()`: Checks constraint existence before removing

## Benefits

1. **Idempotent**: Can be run multiple times without errors
2. **Stateless**: Works regardless of current database state
3. **Safe**: Handles missing indexes, columns, and constraints gracefully
4. **Production-ready**: Will work on fresh databases and existing databases

## Testing

To verify the migrations work correctly:

```bash
# Test on a fresh database
python manage.py migrate users zero
python manage.py migrate users

# Test on existing database (should be no-op)
python manage.py migrate users
```

## Files Modified

1. `multivendor_platform/users/migrations/0014_rename_users_conta_note_contact_idx_users_conta_contact_cc7c9b_idx_and_more.py`
2. `multivendor_platform/users/migrations/0015_change_supplier_to_onetoone.py`
3. `multivendor_platform/users/models.py` (exception handling fix - changed `OperationalError` to `DatabaseError`)

## Production Status

✅ **Fixed in production**: Column `monthly_price_rial` was manually added and migrations were marked as applied
✅ **Code fix applied**: Exception handling now catches `DatabaseError` instead of just `OperationalError`
✅ **Migrations updated**: Future deployments will use the idempotent versions

## Next Deployment

When these updated migrations are deployed, they will:
- Work correctly on fresh databases
- Work correctly on existing databases (no-op if already applied)
- Handle edge cases gracefully
- Not require manual intervention

