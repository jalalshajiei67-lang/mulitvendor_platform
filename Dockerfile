# Use Python 3.11 as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=multivendor_platform.settings

# Set work directory
WORKDIR /app

# Install system dependencies with retry logic
RUN for i in 1 2 3; do \
    apt-get update && \
    apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && break || sleep 5; \
    done

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy entire Django project
COPY multivendor_platform/multivendor_platform/ /app/

# Create necessary directories
RUN mkdir -p /app/static /app/media

# Collect static files (will run again in CMD with proper settings)
RUN python manage.py collectstatic --noinput || true

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/ || exit 1

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD python manage.py migrate --noinput --fake-initial; \
    python manage.py collectstatic --noinput && \
    gunicorn multivendor_platform.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120

