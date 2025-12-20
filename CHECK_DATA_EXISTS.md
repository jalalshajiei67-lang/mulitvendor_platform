# Check If Data Exists in Tables

## Quick Data Check Commands

Run these to see if your tables have data:

```bash
# 1. Check migrations (should have many rows)
docker exec multivendor_db psql -U postgres -d multivendor_db -c "SELECT COUNT(*) FROM django_migrations;"

# 2. Check auth_user (Django's default user table)
docker exec multivendor_db psql -U postgres -d multivendor_db -c "SELECT COUNT(*) FROM auth_user;"

# 3. Check blog posts
docker exec multivendor_db psql -U postgres -d multivendor_db -c "SELECT COUNT(*) FROM blog_blogpost;"

# 4. Check products (if you have products app)
docker exec multivendor_db psql -U postgres -d multivendor_db -c "SELECT COUNT(*) FROM products_product;" 2>/dev/null || echo "Products table might not exist"

# 5. List all table names to find your user table
docker exec multivendor_db psql -U postgres -d multivendor_db -c "\dt" | grep -i user
```

## What to Look For

- **If COUNT(*) = 0** → Tables are empty, need to restore from backup
- **If COUNT(*) > 0** → Data exists, but might be a different issue

## If Data is Missing

If all counts are 0, restore from backup:

```bash
./restore-production-db.sh
```


