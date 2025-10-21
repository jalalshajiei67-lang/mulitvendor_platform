# Use Python 3.11 as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=multivendor_platform.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files (in deploy-django branch, files are at root)
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/static /app/media

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 80

# Run migrations and start server
CMD python manage.py migrate --noinput && \
    gunicorn multivendor_platform.wsgi:application --bind 0.0.0.0:80 --workers 4 --timeout 120

