# 🐳 Docker Setup Without Docker Hub

This guide explains how to run the multivendor platform locally using Docker **without accessing Docker Hub**.

## How It Works

Instead of pulling pre-built images from Docker Hub, this setup:

1. **Uses Ubuntu 22.04 base image** - Available from Ubuntu repositories
2. **Installs Python from Ubuntu repos** - No external Python images needed
3. **Installs Node.js from NodeSource** - Direct installation, no Docker Hub
4. **Uses SQLite instead of PostgreSQL** - No database container needed
5. **Installs nginx from Ubuntu repos** - No nginx images from Docker Hub

## Quick Start

### Step 1: Run the Setup Script

```bash
./run-local-nohub.sh
```

This will:
- Build backend image from Ubuntu base
- Build frontend image from Ubuntu base
- Start both services
- Use SQLite for database (no PostgreSQL)

### Step 2: Access Your Application

Once services are running:

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/

## Files Created

1. **`docker-compose.local-nohub.yml`** - Docker Compose configuration (no PostgreSQL)
2. **`Dockerfile.local`** - Backend Dockerfile (builds from Ubuntu)
3. **`multivendor_platform/front_end/Dockerfile.local`** - Frontend Dockerfile (builds from Ubuntu)
4. **`run-local-nohub.sh`** - Script to start everything

## Important Notes

### First Build
- **Takes 10-15 minutes** on first run
- Downloads Ubuntu packages and builds images from scratch
- Subsequent builds are much faster (Docker caches layers)

### Database
- Uses **SQLite** instead of PostgreSQL
- Database file: `multivendor_platform/multivendor_platform/db.sqlite3`
- No separate database container needed
- Perfect for local development

### Ports
- Backend: `8000`
- Frontend: `8080`
- Make sure these ports are not in use

## Common Commands

### Start Services
```bash
./run-local-nohub.sh
```

### Stop Services
```bash
docker compose -f docker-compose.local-nohub.yml down
```

### View Logs
```bash
docker compose -f docker-compose.local-nohub.yml logs -f
```

### Rebuild Services
```bash
docker compose -f docker-compose.local-nohub.yml up --build
```

### Create Superuser
```bash
docker exec -it multivendor_backend_local python manage.py createsuperuser
```

### Run Migrations
```bash
docker exec -it multivendor_backend_local python manage.py migrate
```

### Access Backend Shell
```bash
docker exec -it multivendor_backend_local python manage.py shell
```

## Troubleshooting

### Build Fails
- Check internet connection (needs to download Ubuntu packages)
- Try: `docker compose -f docker-compose.local-nohub.yml build --no-cache`

### Port Already in Use
- Check what's using the port: `sudo lsof -i :8000` or `sudo lsof -i :8080`
- Stop the conflicting service or change ports in `docker-compose.local-nohub.yml`

### Services Won't Start
- Check logs: `docker compose -f docker-compose.local-nohub.yml logs`
- Verify Docker is running: `docker info`

### Database Issues
- SQLite database is created automatically
- If you need to reset: Stop containers and delete `db.sqlite3` file

### Out of Disk Space
- Clean Docker: `docker system prune -a`
- Remove old images: `docker image prune -a`

## Advantages of This Approach

✅ **No Docker Hub Required** - Works even if Docker Hub is blocked  
✅ **Uses SQLite** - Simpler setup, no database container  
✅ **Fast Development** - Changes to code are reflected immediately (volumes)  
✅ **Production-like** - Still uses Docker, just different base images  
✅ **Reliable** - Uses Ubuntu packages directly from repositories  

## Disadvantages

⚠️ **Larger Images** - Ubuntu base is larger than Alpine  
⚠️ **Longer Build Time** - First build takes longer  
⚠️ **SQLite Only** - Not using PostgreSQL (fine for local dev)  

## Next Steps

1. ✅ Run `./run-local-nohub.sh`
2. ✅ Wait for services to start
3. ✅ Create superuser: `docker exec -it multivendor_backend_local python manage.py createsuperuser`
4. ✅ Access http://localhost:8080
5. 🚀 Start developing!

## Comparison with Docker Hub Version

| Feature | Docker Hub Version | No Docker Hub Version |
|---------|-------------------|----------------------|
| Database | PostgreSQL (container) | SQLite (file) |
| Base Images | Pre-built (fast) | Built from Ubuntu (slower) |
| Build Time | ~5 minutes | ~10-15 minutes |
| Image Size | Smaller (Alpine) | Larger (Ubuntu) |
| Docker Hub | Required | Not required |
| Complexity | Higher (3 containers) | Lower (2 containers) |

---

**Ready to start? Run `./run-local-nohub.sh` now! 🚀**



