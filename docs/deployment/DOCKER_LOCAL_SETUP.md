# 🐳 Running the Project Locally with Docker Desktop

This guide will help you run the multivendor platform locally using Docker Desktop on Windows.

## Prerequisites

1. **Docker Desktop** - Download and install from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. **Git** (if cloning the repository)
3. **Windows 10/11** (64-bit)

## Quick Start

### Step 1: Start Docker Desktop

- Open Docker Desktop application
- Wait for it to fully start (whale icon in system tray should be steady)
- Verify Docker is running:
  ```powershell
  docker info
  ```

### Step 2: Navigate to Project Directory

```powershell
cd C:\Users\F003\Desktop\damirco
```

### Step 3: Start the Project

**Option A: Using the batch script (Recommended for Windows)**
```powershell
.\test-local.bat
```

**Option B: Using Docker Compose directly**
```powershell
docker-compose -f docker-compose.local.yml up --build
```

**Option C: Run in background (detached mode)**
```powershell
docker-compose -f docker-compose.local.yml up --build -d
```

### Step 4: Access the Application

After the containers start (wait 2-5 minutes for first build):

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8080/admin/ (proxied through frontend)
- **Direct Backend**: http://localhost:8000/admin/

## What Gets Started

The Docker Compose setup includes:

1. **PostgreSQL Database** (`multivendor_db_local`)
   - Port: 5432
   - Database: `multivendor_db`
   - User: `postgres`
   - Password: `local_dev_password_123`

2. **Django Backend** (`multivendor_backend_local`)
   - Port: 8000
   - Runs migrations automatically
   - Collects static files
   - Serves API and admin panel

3. **Vue.js Frontend** (`multivendor_frontend_local`)
   - Port: 8080
   - Nginx server
   - Proxies `/api/` requests to backend
   - Proxies `/admin/` and `/media/` to backend

## Common Commands

### View Logs

```powershell
# View all logs
docker-compose -f docker-compose.local.yml logs -f

# View specific service logs
docker-compose -f docker-compose.local.yml logs -f backend
docker-compose -f docker-compose.local.yml logs -f frontend
docker-compose -f docker-compose.local.yml logs -f db
```

### Stop Services

```powershell
# Stop services (keeps data)
docker-compose -f docker-compose.local.yml stop

# Stop and remove containers (keeps volumes/data)
docker-compose -f docker-compose.local.yml down

# Stop and remove everything including volumes (fresh start)
docker-compose -f docker-compose.local.yml down -v
```

### Create Admin User

```powershell
docker exec -it multivendor_backend_local python manage.py createsuperuser
```

### Access Database

```powershell
# Connect to PostgreSQL
docker exec -it multivendor_db_local psql -U postgres -d multivendor_db
```

### Run Django Commands

```powershell
# Run migrations manually
docker exec -it multivendor_backend_local python manage.py migrate

# Create superuser
docker exec -it multivendor_backend_local python manage.py createsuperuser

# Collect static files
docker exec -it multivendor_backend_local python manage.py collectstatic

# Django shell
docker exec -it multivendor_backend_local python manage.py shell
```

### Rebuild After Code Changes

```powershell
# Rebuild specific service
docker-compose -f docker-compose.local.yml up --build backend

# Rebuild all services
docker-compose -f docker-compose.local.yml up --build
```

## Project Structure

```
damirco/
├── docker-compose.local.yml    # Local Docker Compose configuration
├── Dockerfile                   # Backend Dockerfile
├── requirements.txt            # Python dependencies
├── multivendor_platform/
│   ├── multivendor_platform/   # Django project
│   └── front_end/              # Vue.js frontend
│       └── Dockerfile          # Frontend Dockerfile
└── .env.local                  # Local environment variables (auto-created)
```

## Environment Variables

The setup uses these default values for local development:

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
CORS_ALLOW_ALL_ORIGINS=True
```

You can override these by creating a `.env.local` file or modifying `docker-compose.local.yml`.

## Troubleshooting

### Docker Desktop Not Running

**Error**: `Cannot connect to the Docker daemon`

**Solution**: 
- Open Docker Desktop
- Wait for it to fully start
- Check system tray for Docker icon

### Port Already in Use

**Error**: `port is already allocated`

**Solution**:
- Find what's using the port:
  ```powershell
  netstat -ano | findstr :8000
  netstat -ano | findstr :8080
  ```
- Stop the process or change ports in `docker-compose.local.yml`

### Database Connection Errors

**Error**: `could not connect to server`

**Solution**:
- Wait 30-60 seconds for database to initialize
- Check database logs:
  ```powershell
  docker-compose -f docker-compose.local.yml logs db
  ```
- Verify database health:
  ```powershell
  docker exec multivendor_db_local pg_isready -U postgres
  ```

### Backend Won't Start

**Error**: Backend container keeps restarting

**Solution**:
1. Check backend logs:
   ```powershell
   docker-compose -f docker-compose.local.yml logs backend
   ```
2. Common issues:
   - Database not ready (wait longer)
   - Missing migrations (run manually)
   - Port conflict (check port 8000)

### Frontend Shows "Cannot GET /api/..."

**Error**: API requests fail

**Solution**:
- Verify backend is running: http://localhost:8000/api/
- Check frontend logs:
  ```powershell
  docker-compose -f docker-compose.local.yml logs frontend
  ```
- Verify nginx proxy configuration in frontend container

### Build Fails

**Error**: Build errors during `docker-compose up --build`

**Solution**:
1. Clean Docker cache:
   ```powershell
   docker system prune -a
   ```
2. Rebuild without cache:
   ```powershell
   docker-compose -f docker-compose.local.yml build --no-cache
   ```
3. Check specific service build:
   ```powershell
   docker-compose -f docker-compose.local.yml build backend
   ```

### Frontend Not Loading

**Error**: Blank page or 404 errors

**Solution**:
- Clear browser cache
- Check browser console for errors
- Verify frontend container is running:
  ```powershell
  docker ps | findstr frontend
  ```
- Check nginx logs:
  ```powershell
  docker exec multivendor_frontend_local cat /var/log/nginx/error.log
  ```

## Development Workflow

### Making Code Changes

1. **Backend Changes**:
   - Edit files in `multivendor_platform/multivendor_platform/`
   - Restart backend container:
     ```powershell
     docker-compose -f docker-compose.local.yml restart backend
     ```
   - Or rebuild:
     ```powershell
     docker-compose -f docker-compose.local.yml up --build backend
     ```

2. **Frontend Changes**:
   - Edit files in `multivendor_platform/front_end/`
   - Rebuild frontend:
     ```powershell
     docker-compose -f docker-compose.local.yml up --build frontend
     ```

### Database Migrations

Migrations run automatically on container start. To run manually:

```powershell
docker exec -it multivendor_backend_local python manage.py migrate
```

### Static Files

Static files are collected automatically. To refresh:

```powershell
docker exec -it multivendor_backend_local python manage.py collectstatic --noinput
```

## Useful Docker Commands

```powershell
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# View container resource usage
docker stats

# Execute command in running container
docker exec -it multivendor_backend_local bash

# View container details
docker inspect multivendor_backend_local

# Clean up unused resources
docker system prune

# Remove all stopped containers
docker container prune

# Remove unused volumes (CAREFUL: deletes data)
docker volume prune
```

## Next Steps

Once everything is running locally:

1. ✅ Test all features
2. ✅ Create admin user
3. ✅ Add sample data
4. ✅ Verify API endpoints
5. ✅ Test frontend-backend communication
6. 📖 Read deployment guides for CapRover deployment

## Additional Resources

- [Docker Desktop Documentation](https://docs.docker.com/desktop/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- Project deployment guide: `CAPROVER_DEPLOYMENT_GUIDE.md`

## Support

If you encounter issues:

1. Check logs: `docker-compose -f docker-compose.local.yml logs`
2. Verify Docker Desktop is running
3. Check port availability
4. Review troubleshooting section above
5. Check project documentation files

---

**Happy Coding! 🚀**

