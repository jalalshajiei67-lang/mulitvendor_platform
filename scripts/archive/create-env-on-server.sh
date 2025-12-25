#!/bin/bash

# Script to create .env file on the server
# Run this on your VPS at /home/multivendor_platform/

ENV_FILE="/home/multivendor_platform/.env"

echo "Creating .env file at $ENV_FILE..."

cat > "$ENV_FILE" << 'EOF'
# Database Configuration (for Docker Compose)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=1mWL!8qU%_I(si@4Hyvo3txPo3@q3FF+9!e#K44^
DB_HOST=db
DB_PORT=5432

# Django Configuration
SECRET_KEY=tfu9y@exp6tdda$%f_+u&o80jd!%ld5@y=iua)$176x5bf(aut
DEBUG=False
ALLOWED_HOSTS=46.249.101.84,indexo.ir,www.indexo.ir,multivendor-backend.indexo.ir,multivendor-frontend.indexo.ir

# CORS Configuration
CORS_ALLOWED_ORIGINS=https://indexo.ir,https://www.indexo.ir,https://multivendor-frontend.indexo.ir,http://46.249.101.84
CORS_ALLOW_ALL_ORIGINS=False
CSRF_TRUSTED_ORIGINS=https://multivendor-backend.indexo.ir,https://indexo.ir,https://www.indexo.ir

# Domain Configuration (for SSL)
API_DOMAIN=multivendor-backend.indexo.ir
MAIN_DOMAIN=indexo.ir
DOMAIN=indexo.ir
EMAIL=jalal.shajiei67@gmail.com

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379

# Zibal Payment Gateway
ZIBAL_MERCHANT=zibal
SITE_URL=https://indexo.ir
EOF

# Set proper permissions
chmod 600 "$ENV_FILE"

echo "✅ .env file created successfully at $ENV_FILE"
echo "⚠️  Make sure to review and update the file with your actual production values!"

