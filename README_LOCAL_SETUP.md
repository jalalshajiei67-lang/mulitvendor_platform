# 🚀 Local Development Setup Guide

This guide will help you run the multivendor platform locally on Linux.

## Prerequisites

1. **Docker** - Version 20.10 or higher
2. **Docker Compose** - Version 2.0 or higher (or docker-compose v1.29+)
3. At least **4GB RAM** available for Docker
4. **Internet connection** (for downloading Docker images)

## Quick Start

### 1. Start Docker Service

If Docker is not running, start it:

```bash
# Check if Docker is running
docker info

# If not running, start Docker service (requires sudo)
sudo systemctl start docker
sudo systemctl enable docker

# Or if using Docker Desktop, launch it from your applications
```

**Note**: If you get permission denied errors, you may need to add your user to the docker group:

```bash
sudo usermod -aG docker $USER
# Then logout and login again, or run:
newgrp docker
```

### 2. Run the Project

```bash
# Navigate to project directory
cd /media/jalal/New\ Volume/project/mulitvendor_platform

# Run the setup script
./run-local.sh
```

This will:
- ✅ Check if Docker is installed and running
- ✅ Create `.env.local` file with local development settings
- ✅ Start PostgreSQL database
- ✅ Build and start Django backend
- ✅ Build and start Vue.js frontend
- ✅ Run database migrations
- ✅ Start all services

### 3. Access Your Application

Once all services are running (this may take 5-10 minutes on first build):

| Service | URL | Description |
|---------|-----|-------------|
| 🎨 Frontend | http://localhost:8080 | Your Vue.js app |
| ⚙️ Backend API | http://localhost:8000/api/ | REST API |
| 👤 Admin Panel | http://localhost:8000/admin/ | Django admin |
| 🗄️ Database | localhost:5432 | PostgreSQL |

## Common Commands

### View Logs
```bash
docker-compose -f docker-compose.local.yml logs -f
```

### Stop All Services
```bash
docker-compose -f docker-compose.local.yml down
```

### Stop and Remove All Data (Fresh Start)
```bash
docker-compose -f docker-compose.local.yml down -v
./run-local.sh
```

### Create Django Superuser
```bash
docker exec -it multivendor_backend_local python manage.py createsuperuser
```

### Restart a Specific Service
```bash
# Restart backend only
docker-compose -f docker-compose.local.yml restart backend

# Restart frontend only
docker-compose -f docker-compose.local.yml restart frontend

# Rebuild and restart backend
docker-compose -f docker-compose.local.yml up -d --build backend
```

### Check Service Status
```bash
docker-compose -f docker-compose.local.yml ps
```

## Environment Variables

The script creates a `.env.local` file with the following defaults:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=multivendor_db
DB_USER=postgres
DB_PASSWORD=local_dev_password_123
DB_HOST=db
DB_PORT=5432
SECRET_KEY=local-dev-secret-key-change-in-production-12345678910
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,backend
CORS_ALLOWED_ORIGINS=http://localhost,http://localhost:8080,http://localhost:3000
CORS_ALLOW_ALL_ORIGINS=True
```

You can edit `.env.local` to change these settings.

## Troubleshooting

### Docker is not running
```bash
# Check Docker status
sudo systemctl status docker

# Start Docker
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker
```

### Permission Denied
```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Apply the changes (logout/login or run)
newgrp docker
```

### Port Already in Use
If port 8000 or 8080 is already in use:

```bash
# Check what's using the port
sudo lsof -i :8000
sudo lsof -i :8080

# Stop the conflicting service or edit docker-compose.local.yml to use different ports
```

### Services Keep Restarting
Check the logs to see what's wrong:
```bash
docker-compose -f docker-compose.local.yml logs backend
docker-compose -f docker-compose.local.yml logs frontend
docker-compose -f docker-compose.local.yml logs db
```

### Database Connection Errors
Wait 30-60 seconds after starting. The database needs time to initialize on first run.

### Build Fails
```bash
# Clean build (removes cache)
docker-compose -f docker-compose.local.yml build --no-cache

# Remove all containers and volumes
docker-compose -f docker-compose.local.yml down -v

# Try again
./run-local.sh
```

### Out of Disk Space
```bash
# Clean up Docker system
docker system prune -a

# Remove unused volumes
docker volume prune
```

## Development Workflow

### Making Backend Changes
1. Edit your Django code
2. Restart the backend service:
   ```bash
   docker-compose -f docker-compose.local.yml restart backend
   ```
3. Or rebuild if you added dependencies:
   ```bash
   docker-compose -f docker-compose.local.yml up -d --build backend
   ```

### Making Frontend Changes
1. Edit your Vue.js code
2. Restart the frontend service:
   ```bash
   docker-compose -f docker-compose.local.yml restart frontend
   ```
3. Or rebuild if you added dependencies:
   ```bash
   docker-compose -f docker-compose.local.yml up -d --build frontend
   ```

### Database Migrations
```bash
# Create migrations (if you modified models)
docker exec -it multivendor_backend_local python manage.py makemigrations

# Apply migrations
docker exec -it multivendor_backend_local python manage.py migrate
```

### Accessing Database Directly
```bash
# Connect to PostgreSQL
docker exec -it multivendor_db_local psql -U postgres -d multivendor_db

# Or use a database client like pgAdmin, DBeaver, etc.
# Host: localhost
# Port: 5432
# Database: multivendor_db
# User: postgres
# Password: local_dev_password_123
```

## Project Structure

```
mulitvendor_platform/
├── run-local.sh              # Main script to run locally
├── docker-compose.local.yml  # Docker Compose configuration
├── Dockerfile                # Backend Docker image
├── requirements.txt          # Python dependencies
├── .env.local               # Local environment variables (auto-generated)
├── multivendor_platform/
│   ├── multivendor_platform/ # Django project
│   │   ├── settings.py       # Django settings
│   │   ├── urls.py           # URL configuration
│   │   └── manage.py         # Django management script
│   └── front_end/            # Vue.js frontend
│       ├── package.json      # Node.js dependencies
│       ├── Dockerfile        # Frontend Docker image
│       └── src/              # Vue.js source code
└── README_LOCAL_SETUP.md     # This file
```

## Next Steps

Once your local environment is running:

1. ✅ Create a superuser account
2. ✅ Test the frontend and backend
3. ✅ Verify API endpoints are working
4. ✅ Check admin panel functionality
5. 🚀 Ready for development!

## Need Help?

- Check the logs: `docker-compose -f docker-compose.local.yml logs -f`
- Review Docker documentation: https://docs.docker.com
- Check project documentation in the root directory

---

**Happy Coding! 🎉**


















