#!/bin/sh
set -e

LOG_PREFIX="[Entrypoint]"
echo "=========================================="
echo "$LOG_PREFIX Starting Multivendor Backend Application"
echo "=========================================="
echo

# Ensure required directories exist (especially when using persistent volumes)
echo "$LOG_PREFIX Ensuring media and static directories exist..."
mkdir -p /app/staticfiles /app/media /app/logs
mkdir -p \
    /app/media/category_images \
    /app/media/subcategory_images \
    /app/media/product_images \
    /app/media/department_images \
    /app/media/blog_images \
    /app/media/user_images
chmod -R 755 /app/media || true
echo "$LOG_PREFIX Media directories ready"
echo

# Wait for database if Postgres is configured
if [ "${DB_ENGINE}" = "django.db.backends.postgresql" ]; then
  echo "$LOG_PREFIX Waiting for PostgreSQL database to become available..."
  python <<'PY'
import os
import sys
import time
from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError

wait_timeout = int(os.environ.get("DB_WAIT_TIMEOUT", "60"))
wait_interval = int(os.environ.get("DB_WAIT_INTERVAL", "3"))
start_time = time.time()
connection = connections['default']

while True:
    try:
        connection.ensure_connection()
        break
    except OperationalError as exc:
        elapsed = time.time() - start_time
        if elapsed > wait_timeout:
            sys.stderr.write(
                f"Database unavailable after {wait_timeout}s: {exc}\n"
            )
            sys.exit(1)
        sys.stdout.write(
            f"Database unavailable ({exc}), waiting {wait_interval}s...\n"
        )
        sys.stdout.flush()
        time.sleep(wait_interval)

print("Database connection established.")
PY
  echo "$LOG_PREFIX Database is ready"
  echo
fi

# Apply database migrations
echo "$LOG_PREFIX Applying database migrations..."
python manage.py migrate --noinput
echo "$LOG_PREFIX Migrations complete"
echo

# Collect static files (don't crash the container if it fails)
echo "$LOG_PREFIX Collecting static files..."
if python manage.py collectstatic --noinput --clear; then
  echo "$LOG_PREFIX Static files collected"
else
  echo "$LOG_PREFIX ⚠️  Collectstatic failed, continuing without fresh static files" >&2
fi
echo

# Django system checks (non-fatal)
echo "$LOG_PREFIX Running Django system checks..."
if python manage.py check --deploy; then
  echo "$LOG_PREFIX Django checks passed"
else
  echo "$LOG_PREFIX ⚠️  Django deploy checks reported issues (continuing)" >&2
fi
echo

# Launch Gunicorn
WORKERS="${GUNICORN_WORKERS:-4}"
TIMEOUT="${GUNICORN_TIMEOUT:-120}"
echo "$LOG_PREFIX Starting Gunicorn with ${WORKERS} workers (timeout: ${TIMEOUT}s)"
echo "=========================================="
exec gunicorn multivendor_platform.wsgi:application \
    --bind 0.0.0.0:80 \
    --workers "$WORKERS" \
    --timeout "$TIMEOUT" \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output
