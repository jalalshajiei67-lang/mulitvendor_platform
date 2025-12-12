# Quick Fix: django_content_type Sequence

## Immediate Fix (Run Now)

Connect to your PostgreSQL database and run:

```sql
SELECT setval('django_content_type_id_seq', (SELECT MAX(id) FROM django_content_type) + 1, false);
```

### Via Docker

```bash
# Get the database container name
docker ps | grep postgres

# Connect to PostgreSQL (replace with your actual container name)
docker exec -it multivendor_db_staging psql -U postgres -d multivendor_db_staging

# Then run the SQL:
SELECT setval('django_content_type_id_seq', (SELECT MAX(id) FROM django_content_type) + 1, false);

# Exit psql
\q
```

### Or via Django shell

```bash
docker exec multivendor_backend_staging python manage.py shell
```

Then in Python:
```python
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT MAX(id) FROM django_content_type;")
    max_id = cursor.fetchone()[0]
    if max_id:
        cursor.execute(f"SELECT setval('django_content_type_id_seq', {max_id + 1}, false);")
        print(f"Fixed: sequence set to {max_id + 1}")
```

## After Fix

Run migrations again:
```bash
docker exec multivendor_backend_staging python manage.py migrate
```

## Long-term Fix

The updated `fix_migration_sequence` command will automatically fix both sequences. After deploying the new code, it will handle this automatically.



