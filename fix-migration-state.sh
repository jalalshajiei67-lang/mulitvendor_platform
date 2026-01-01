#!/bin/bash
# Fix migration state for sms_newsletter app

set -e

echo "🔧 Fixing sms_newsletter migration state..."

# Connect to database and fix migration state
docker exec multivendor_db psql -U postgres -d multivendor_db << EOF
-- Check current migration state
SELECT * FROM django_migrations WHERE app='sms_newsletter' ORDER BY id;

-- If there's a mismatch, we'll fix it
-- First, check if the correct migration exists in the file system
-- The migration should be: 0002_alter_seller_mobile_number

-- Delete any incorrect migration records
DELETE FROM django_migrations 
WHERE app='sms_newsletter' 
AND name LIKE '%suppliersmsnewsletter%';

-- Ensure the correct migration is marked as applied if table exists
DO \$\$
BEGIN
    IF EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'sms_newsletter_seller'
    ) THEN
        -- Table exists, ensure migration is marked as applied
        INSERT INTO django_migrations (app, name, applied)
        SELECT 'sms_newsletter', '0002_alter_seller_mobile_number', NOW()
        WHERE NOT EXISTS (
            SELECT 1 FROM django_migrations 
            WHERE app='sms_newsletter' 
            AND name='0002_alter_seller_mobile_number'
        );
    END IF;
END \$\$;

-- Show final state
SELECT * FROM django_migrations WHERE app='sms_newsletter' ORDER BY id;
EOF

echo "✅ Migration state fixed!"
echo ""
echo "Next steps:"
echo "1. Restart the backend container: docker restart multivendor_backend"
echo "2. Check logs: docker logs multivendor_backend --tail 50"

