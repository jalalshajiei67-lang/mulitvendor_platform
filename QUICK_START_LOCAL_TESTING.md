# 🚀 Quick Start - Local Docker Testing

Test your multivendor platform locally before deploying to CapRover!

## Prerequisites

1. ✅ **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop/)
2. ✅ Make sure Docker Desktop is **running**
3. ✅ At least **4GB RAM** allocated to Docker

## Super Simple Start (Windows)

### Option 1: Double-Click to Run 🖱️

Just double-click one of these batch files:

- **`test-local.bat`** - Starts everything and shows logs (recommended for first time)
- **`test-local-background.bat`** - Starts in background (for regular use)

### Option 2: Command Line

```powershell
# Open PowerShell or Command Prompt in this folder and run:
test-local.bat
```

## What Happens?

The script will:

1. ✅ Check if Docker Desktop is running
2. ✅ Create environment file (`.env.local`)
3. ✅ Start PostgreSQL database
4. ✅ Build Django backend
5. ✅ Build Vue.js frontend
6. ✅ Run database migrations
7. ✅ Start all services

**First time will take 5-10 minutes** (downloading images and building). Subsequent runs are much faster!

## Access Your Application

Once you see "healthy" status for all services:

| Service | URL | Description |
|---------|-----|-------------|
| 🎨 Frontend | http://localhost:8080 | Your Vue.js app |
| ⚙️ Backend API | http://localhost:8000/api/ | REST API |
| 👤 Admin Panel | http://localhost:8000/admin/ | Django admin |
| 🗄️ Database | localhost:5432 | PostgreSQL (for DB tools) |

## Common Tasks

### View Logs
```powershell
# Double-click this file:
view-logs.bat

# Or run manually:
docker-compose -f docker-compose.local.yml logs -f
```

### Stop Everything
```powershell
# Double-click this file:
stop-local.bat

# Or run manually:
docker-compose -f docker-compose.local.yml down
```

### Create Django Superuser
```powershell
docker exec -it multivendor_backend_local python manage.py createsuperuser
```

### Restart After Code Changes

**Backend changes:**
```powershell
docker-compose -f docker-compose.local.yml up -d --build backend
```

**Frontend changes:**
```powershell
docker-compose -f docker-compose.local.yml up -d --build frontend
```

### Complete Fresh Start
```powershell
# Remove everything including database data
docker-compose -f docker-compose.local.yml down -v

# Start again
test-local.bat
```

## Troubleshooting

### "Docker is not running"
→ Start Docker Desktop and wait for it to fully start (whale icon in system tray)

### "Port already in use"
→ Another application is using port 8000 or 8080. Either:
- Close that application
- Or edit `docker-compose.local.yml` to use different ports

### "Cannot connect to database"
→ Wait 30 seconds. Database takes time to initialize on first run.

### Services keep restarting
→ Check logs: `view-logs.bat` to see error messages

### Build fails
→ Make sure you have good internet connection (downloading packages)
→ Try: `docker-compose -f docker-compose.local.yml build --no-cache`

## Testing Checklist

Before deploying to CapRover, verify:

- [ ] ✅ Frontend loads without errors
- [ ] ✅ Can login/create accounts
- [ ] ✅ Backend API returns data
- [ ] ✅ Admin panel accessible
- [ ] ✅ Database operations work
- [ ] ✅ No errors in logs

## Next Steps

Once local testing passes:

1. ✅ Everything works locally
2. 📝 Update CapRover environment variables
3. 🚀 Deploy to CapRover using deployment guides

## File Structure

```
.
├── test-local.bat                  ← START HERE (double-click)
├── test-local-background.bat       ← Run in background
├── stop-local.bat                  ← Stop services
├── view-logs.bat                   ← View logs
├── docker-compose.local.yml        ← Local config
├── .env.local                      ← Auto-generated env vars
├── TEST_LOCALLY.md                 ← Detailed guide
└── CAPROVER_DEPLOYMENT_GUIDE.md   ← Production deployment
```

## Tips

💡 **First run**: Use `test-local.bat` to see what's happening
💡 **Regular use**: Use `test-local-background.bat` for faster startup  
💡 **Check status**: Look at Docker Desktop dashboard
💡 **Data persists**: Database data is saved between restarts
💡 **Fresh start**: Use `down -v` to reset everything

## Need Help?

1. Check logs: `view-logs.bat`
2. Read detailed guide: `TEST_LOCALLY.md`
3. Check Docker Desktop dashboard for container status
4. Verify Docker Desktop has enough resources (Settings → Resources)

---

**Ready? Just double-click `test-local.bat` to start! 🚀**

