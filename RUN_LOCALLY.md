# 🚀 Run Project Locally - Complete Guide

This guide provides two methods to run the multivendor platform locally on Linux.

## Option 1: Using Docker (Recommended)

### Prerequisites
- Docker installed and running
- Docker Compose (v2 or v1.29+)

### Quick Start

1. **Fix Docker Permissions** (if needed):
   ```bash
   # Add your user to docker group
   sudo usermod -aG docker $USER
   newgrp docker
   
   # Or logout and login again
   ```

2. **Start Docker Service** (if not running):
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. **Run the Project**:
   ```bash
   cd /media/jalal/New\ Volume/project/mulitvendor_platform
   ./run-local.sh
   ```

4. **Access the Application**:
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000/api/
   - Admin Panel: http://localhost:8000/admin/

### Docker Commands

```bash
# View logs
docker-compose -f docker-compose.local.yml logs -f

# Stop services
docker-compose -f docker-compose.local.yml down

# Create superuser
docker exec -it multivendor_backend_local python manage.py createsuperuser

# Restart services
docker-compose -f docker-compose.local.yml restart
```

---

## Option 2: Without Docker (Native Python/Node.js)

### Prerequisites
- Python 3.9+ 
- Node.js 20.19+ or 22.12+
- PostgreSQL (or use SQLite for development)
- pip and virtualenv (or venv)

### Step 1: Set Up Backend

```bash
# Navigate to project directory
cd /media/jalal/New\ Volume/project/mulitvendor_platform

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Navigate to Django project
cd multivendor_platform/multivendor_platform
```

### Step 2: Configure Database

**Option A: Use SQLite (Easiest - No setup needed)**
- Django will use SQLite by default if PostgreSQL is not configured
- Database file will be created at: `multivendor_platform/multivendor_platform/db.sqlite3`

**Option B: Use PostgreSQL**
```bash
# Install PostgreSQL (if not installed)
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres psql
CREATE DATABASE multivendor_db;
CREATE USER postgres WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE multivendor_db TO postgres;
\q

# Set environment variables
export DB_ENGINE=django.db.backends.postgresql
export DB_NAME=multivendor_db
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
```

### Step 3: Run Database Migrations

```bash
# Make sure you're in the Django project directory
cd multivendor_platform/multivendor_platform

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### Step 4: Start Django Backend

```bash
# Set environment variables (if using PostgreSQL)
export SECRET_KEY=dev-secret-key-change-in-production
export DEBUG=True
export ALLOWED_HOSTS=localhost,127.0.0.1
export CORS_ALLOW_ALL_ORIGINS=True

# Start Django development server
python manage.py runserver
```

Backend will be available at: http://127.0.0.1:8000

### Step 5: Set Up Frontend

Open a new terminal window:

```bash
# Navigate to frontend directory
cd /media/jalal/New\ Volume/project/mulitvendor_platform/multivendor_platform/front_end

# Install Node.js dependencies
npm install

# Start Vite development server
npm run dev
```

Frontend will be available at: http://localhost:5173

The frontend is configured to proxy API requests to the backend at http://127.0.0.1:8000

### Step 6: Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://127.0.0.1:8000/api/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## Troubleshooting

### Docker Issues

**Permission Denied:**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

**Docker Not Running:**
```bash
sudo systemctl start docker
sudo systemctl status docker
```

**Port Already in Use:**
```bash
# Check what's using the port
sudo lsof -i :8000
sudo lsof -i :8080

# Kill the process or change ports in docker-compose.local.yml
```

### Native Setup Issues

**Python Virtual Environment:**
```bash
# If venv doesn't work, try:
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Node.js Version:**
```bash
# Check Node.js version
node --version

# Should be 20.19+ or 22.12+
# If not, install nvm:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20
```

**Database Connection (PostgreSQL):**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql

# Test connection
psql -U postgres -d multivendor_db
```

**CORS Issues:**
- Make sure `CORS_ALLOW_ALL_ORIGINS=True` is set in environment
- Or add your frontend URL to `CORS_ALLOWED_ORIGINS`

---

## Quick Reference

### Docker Method
```bash
./run-local.sh                    # Start all services
docker-compose -f docker-compose.local.yml logs -f  # View logs
docker-compose -f docker-compose.local.yml down     # Stop services
```

### Native Method
```bash
# Terminal 1: Backend
source venv/bin/activate
cd multivendor_platform/multivendor_platform
python manage.py runserver

# Terminal 2: Frontend
cd multivendor_platform/front_end
npm run dev
```

---

## Which Method Should I Use?

**Use Docker if:**
- ✅ You want the easiest setup
- ✅ You want to match production environment
- ✅ You don't want to install PostgreSQL separately
- ✅ You want isolated environments

**Use Native Setup if:**
- ✅ You prefer running services directly
- ✅ You want faster development iteration
- ✅ You need to debug specific issues
- ✅ You're more comfortable with native tools

---

## Next Steps

1. ✅ Choose your preferred method (Docker or Native)
2. ✅ Follow the setup steps
3. ✅ Create a superuser account
4. ✅ Test the application
5. 🚀 Start developing!

For more details, see:
- `README_LOCAL_SETUP.md` - Detailed Docker setup
- `multivendor_platform/front_end/README.md` - Frontend details
- Project documentation in root directory

---

**Happy Coding! 🎉**

















