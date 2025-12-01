# Use Python 3.11 as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the entire Django project
COPY multivendor_platform/multivendor_platform/ /app/
# Create the non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose the port Daphne will run on
EXPOSE 8000

# The command to run the application
# Daphne will be started by docker-compose, but this is a good default
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "multivendor_platform.asgi:application"]