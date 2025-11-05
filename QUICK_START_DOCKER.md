# 🚀 Quick Start - Docker Desktop

Run your multivendor platform locally in 3 steps!

## Step 1: Start Docker Desktop
- Open Docker Desktop application
- Wait until it's fully running (check system tray)

## Step 2: Run the Project

**Windows (Double-click):**
```
START_DOCKER.bat
```

**Or use command line:**
```powershell
docker-compose -f docker-compose.local.yml up --build
```

## Step 3: Access Your Application

Wait 2-5 minutes for first build, then open:

- 🌐 **Frontend**: http://localhost:8080
- ⚙️ **Backend API**: http://localhost:8000/api/
- 👤 **Admin Panel**: http://localhost:8080/admin/

## Create Admin User

```powershell
docker exec -it multivendor_backend_local python manage.py createsuperuser
```

## Stop Services

Press `Ctrl+C` in the terminal, or:

```powershell
docker-compose -f docker-compose.local.yml down
```

## Troubleshooting

**Docker not running?** → Start Docker Desktop first

**Port in use?** → Close other apps using ports 8000/8080

**Services won't start?** → Check logs:
```powershell
docker-compose -f docker-compose.local.yml logs
```

For detailed guide, see: `DOCKER_LOCAL_SETUP.md`

---

**That's it! Happy coding! 🎉**

