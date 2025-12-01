#!/bin/bash
# Quick script to create staging database if it doesn't exist

echo "=========================================="
echo "Creating Staging Database"
echo "=========================================="
echo ""
echo "This script will help you create the database."
echo "Choose an option:"
echo ""
echo "Option 1: Check PostgreSQL app environment variables"
echo "Option 2: Create database manually via SSH"
echo "Option 3: Show SQL commands to run"
echo ""

# For manual creation via SSH:
echo "=========================================="
echo "To create database manually via SSH:"
echo "=========================================="
echo ""
echo "1. SSH to your server:"
echo "   ssh root@185.208.172.76"
echo ""
echo "2. Connect to PostgreSQL:"
echo "   docker exec -it srv-captain--postgres-db-staging psql -U postgres"
echo ""
echo "3. Create the database:"
echo "   CREATE DATABASE \"multivendor-db-staging\";"
echo "   \\q"
echo ""
echo "4. Verify it exists:"
echo "   docker exec -it srv-captain--postgres-db-staging psql -U postgres -l"
echo ""
echo "=========================================="
echo "OR via CapRover Dashboard:"
echo "=========================================="
echo ""
echo "1. Go to: https://captain.indexo.ir"
echo "2. Apps → postgres-db-staging → App Configs"
echo "3. Add environment variable:"
echo "   POSTGRES_DB=multivendor-db-staging"
echo "4. Save & Update (if app was just created)"
echo "   OR create database manually if app already exists"
echo ""




