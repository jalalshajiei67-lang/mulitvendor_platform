# 🐳 Local Docker Testing Guide

This guide will help you test your project locally with Docker Desktop before deploying to CapRover.

## Prerequisites

✅ Docker Desktop installed and running
✅ At least 4GB RAM allocated to Docker
✅ Port 8000 and 8080 available on your machine

## Quick Start

### 1. Start Docker Desktop
Make sure Docker Desktop is running on your Windows machine.

### 2. Build and Run Locally

```powershell
# Load environment variables and start all services
docker-compose --env-file .env.local -f docker-compose.local.yml up --build
```

**This will:**
- Build your Django backend
- Build your Vue.js frontend  
- Start PostgreSQL database
- Run migrations automatically
- Collect static files

### 3. Access Your Application

Once all services are running (watch for "healthy" status):

- **Frontend (Vue.js)**: http://localhost:8080
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **PostgreSQL Database**: localhost:5432 (for DB clients)

## Common Commands

### Start Services (Detached Mode)
```powershell
docker-compose --env-file .env.local -f docker-compose.local.yml up -d
```

### View Logs
```powershell
# All services
docker-compose -f docker-compose.local.yml logs -f

# Specific service
docker-compose -f docker-compose.local.yml logs -f backend
docker-compose -f docker-compose.local.yml logs -f frontend
docker-compose -f docker-compose.local.yml logs -f db
```

### Stop Services
```powershell
docker-compose -f docker-compose.local.yml down
```

### Stop and Remove All Data (Clean Slate)
```powershell
docker-compose -f docker-compose.local.yml down -v
```

### Rebuild After Code Changes
```powershell
# Rebuild specific service
docker-compose -f docker-compose.local.yml up --build backend

# Rebuild all services
docker-compose -f docker-compose.local.yml up --build
```

### Execute Commands Inside Containers
```powershell
# Django shell
docker exec -it multivendor_backend_local python manage.py shell

# Create superuser
docker exec -it multivendor_backend_local python manage.py createsuperuser

# Run migrations manually
docker exec -it multivendor_backend_local python manage.py migrate

# Access database
docker exec -it multivendor_db_local psql -U postgres -d multivendor_db
```

## Troubleshooting

### Port Already in Use
If you get "port already allocated" error:

```powershell
# Check what's using the port
netstat -ano | findstr :8000
netstat -ano | findstr :8080

# Kill the process or change ports in docker-compose.local.yml
```

### Database Connection Issues
```powershell
# Check if database is healthy
docker-compose -f docker-compose.local.yml ps

# Restart database
docker-compose -f docker-compose.local.yml restart db
```

### Backend Won't Start
```powershell
# Check backend logs
docker-compose -f docker-compose.local.yml logs backend

# Common issues:
# - Database not ready: Wait for db healthcheck to pass
# - Missing dependencies: Rebuild with --no-cache
docker-compose -f docker-compose.local.yml build --no-cache backend
```

### Frontend Build Fails
```powershell
# Check frontend logs
docker-compose -f docker-compose.local.yml logs frontend

# Rebuild frontend
docker-compose -f docker-compose.local.yml build --no-cache frontend
```

### Clear Everything and Start Fresh
```powershell
# Stop all containers
docker-compose -f docker-compose.local.yml down -v

# Remove all project containers
docker ps -a | findstr multivendor | foreach { docker rm -f $_.Split()[0] }

# Remove all project images
docker images | findstr multivendor | foreach { docker rmi -f $_.Split()[2] }

# Start again
docker-compose --env-file .env.local -f docker-compose.local.yml up --build
```

## Testing Checklist

Before deploying to CapRover, verify:

- [ ] Frontend loads at http://localhost:8080
- [ ] Backend API responds at http://localhost:8000/api/
- [ ] Database connections work
- [ ] Static files load correctly
- [ ] Media uploads work
- [ ] Admin panel accessible
- [ ] API endpoints return expected data
- [ ] Frontend can communicate with backend
- [ ] No errors in Docker logs

## Environment Variables

The `.env.local` file contains local development settings. For production deployment to CapRover, you'll use different values from `caprover-env-backend.txt` and `caprover-env-frontend.txt`.

## Next Steps

Once local testing is successful:

1. ✅ Application runs locally in Docker
2. ✅ All services communicate properly
3. ✅ Database migrations work
4. 🚀 Ready to deploy to CapRover!

Refer to `CAPROVER_DEPLOYMENT_GUIDE.md` for production deployment steps.

## CapRover vs Local Differences

| Aspect | Local Testing | CapRover Production |
|--------|---------------|---------------------|
| Ports | 8000, 8080 | 80, 443 |
| Database | Local PostgreSQL | CapRover PostgreSQL app |
| Domain | localhost | Your domain |
| SSL | Not needed | Let's Encrypt |
| Environment | .env.local | CapRover env vars |
| Deployment | docker-compose | captain-definition |

## Tips

- 💡 Keep Docker Desktop running while testing
- 💡 Use `-d` flag to run in background
- 💡 Use `docker-compose logs -f` to monitor in real-time
- 💡 Database data persists in volumes between restarts
- 💡 Use `down -v` to completely reset including data

