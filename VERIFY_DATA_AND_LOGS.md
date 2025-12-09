# ✅ Database Connection is Working - Verify Data

## Good News! 🎉

Your diagnostic shows:
- ✅ Database container: Running & Healthy
- ✅ Database exists: `multivendor_db` with **69 tables**
- ✅ Backend can connect successfully
- ✅ All environment variables are correct

## Next: Verify Data Exists

The tables exist, but let's check if they have data:

### Check if tables have data:

```bash
# Check a few key tables for data
docker exec multivendor_db psql -U postgres -d multivendor_db -c "SELECT COUNT(*) FROM django_migrations;"
docker exec multivendor_db psql -U postgres -d multivendor_db -c "SELECT COUNT(*) FROM users_user;"
docker exec multivendor_db psql -U postgres -d multivendor_db -c "SELECT COUNT(*) FROM products_product;"
```

### Check backend logs for errors:

```bash
# View recent backend logs
docker logs multivendor_backend --tail 100

# Look for specific errors
docker logs multivendor_backend --tail 100 | grep -i "error\|exception\|traceback"
```

### Test the API:

```bash
# Check if API is responding
curl http://localhost:8000/api/ || curl http://localhost/api/

# Or check from outside (replace with your domain)
curl https://multivendor-backend.indexo.ir/api/
```

## Possible Scenarios

### Scenario 1: Everything Works ✅
- Tables have data
- No errors in logs
- API responds correctly
→ **No action needed!** The deployment was successful.

### Scenario 2: Tables Exist But Empty ⚠️
- Tables exist but COUNT(*) returns 0
→ **Need to restore data from backup**

### Scenario 3: Connection Works But API Errors ⚠️
- Database connection works
- But API returns errors
→ **Check backend logs for specific errors**

## Quick Verification Commands

```bash
# 1. Check migrations (should show many rows)
docker exec multivendor_db psql -U postgres -d multivendor_db -c "SELECT COUNT(*) FROM django_migrations;"

# 2. Check users table (if you have users)
docker exec multivendor_db psql -U postgres -d multivendor_db -c "SELECT COUNT(*) FROM users_user;" 2>/dev/null || echo "Table might have different name"

# 3. List all tables to see what you have
docker exec multivendor_db psql -U postgres -d multivendor_db -c "\dt" | head -20

# 4. Check backend health endpoint
docker exec multivendor_backend python manage.py check --database default

# 5. View backend logs
docker logs multivendor_backend --tail 50
```

## If Data is Missing

If tables exist but are empty, restore from backup:

```bash
./restore-production-db.sh
```


