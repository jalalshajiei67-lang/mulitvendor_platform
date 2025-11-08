# Testing Guide - Multivendor Platform

This guide explains how to test the communication between Backend, Frontend, and Database.

## Quick Test

Run the automated test script:

```powershell
.\test-simple.ps1
```

This will verify:
1. Database is accepting connections
2. Backend API is responding
3. Frontend is accessible
4. Backend can connect to Database
5. Frontend can communicate with Backend

## Manual Testing

### 1. Start the Stack

```bash
docker-compose -f docker-compose.local.yml up --build
```

### 2. Test Each Component

**Database:**
```bash
docker exec multivendor_db_local pg_isready -U postgres
# Expected: /var/run/postgresql:5432 - accepting connections
```

**Backend API:**
```powershell
Invoke-WebRequest -Uri http://localhost:8000/api/products/ -UseBasicParsing
# Expected: Status 200 OK
```

**Frontend:**
```powershell
Invoke-WebRequest -Uri http://localhost:8080 -UseBasicParsing
# Expected: Status 200 OK
```

**Backend→Database:**
```bash
docker exec multivendor_backend_local python manage.py check
# Expected: System check identified no issues
```

**Frontend→Backend:**
```bash
docker exec multivendor_frontend_local wget -qO- http://backend:80/api/products/
# Expected: JSON response with products data
```

## Access Points

- **Frontend:** http://localhost:8080
- **Backend API:** http://localhost:8000/api/
- **Django Admin:** http://localhost:8000/admin/
- **Database:** localhost:5432

## Database Access

```bash
# Connect to database
docker exec -it multivendor_db_local psql -U postgres -d multivendor_db

# List tables
\dt

# Count products
SELECT COUNT(*) FROM products_product;

# Exit
\q
```

## Troubleshooting

### Backend returns 400 Bad Request

Check ALLOWED_HOSTS environment variable:
```bash
docker exec multivendor_backend_local python -c "import os; print(os.environ.get('ALLOWED_HOSTS'))"
```

Should include: `localhost,127.0.0.1,backend,0.0.0.0`

### Frontend can't reach Backend

Check if containers are on the same network:
```bash
docker network inspect multivendor_network_local
```

### Database connection fails

Check database is healthy:
```bash
docker ps | grep multivendor_db_local
```

## Container Management

```bash
# View logs
docker-compose -f docker-compose.local.yml logs -f

# View specific service logs
docker logs multivendor_backend_local
docker logs multivendor_frontend_local
docker logs multivendor_db_local

# Restart a service
docker-compose -f docker-compose.local.yml restart backend

# Stop all services
docker-compose -f docker-compose.local.yml down

# Remove volumes (clean slate)
docker-compose -f docker-compose.local.yml down -v
```

## Test Results

All integration tests passed successfully on October 26, 2025.

See `TEST_RESULTS.md` for detailed test output.

