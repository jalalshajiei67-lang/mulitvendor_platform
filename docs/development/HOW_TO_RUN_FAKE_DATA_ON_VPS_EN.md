# 📋 How to Run Fake Data Script on VPS

## 🎯 Quick Methods

---

## Method 1: Docker Exec (For Staging with Docker Compose) ⭐ RECOMMENDED

### Step 1: Connect to VPS

```bash
ssh root@185.208.172.76
```

### Step 2: Check running containers

```bash
docker ps | grep backend
```

You should see container `indexo_backend_staging`.

### Step 3: Run the script

#### Option A: Direct execution

```bash
docker exec -it indexo_backend_staging python manage.py shell < /app/multivendor_platform/multivendor_platform/populate_fake_data.py
```

#### Option B: Interactive shell

```bash
# Enter container shell
docker exec -it indexo_backend_staging bash

# Inside container:
cd /app/multivendor_platform
python manage.py shell
```

Then in Django shell:

```python
from multivendor_platform.populate_fake_data import main
main()
```

---

## Method 2: CapRover CLI

### Step 1: Install CapRover CLI (if needed)

```bash
npm install -g caprover
```

### Step 2: Login to CapRover

```bash
caprover login
```

Enter:
- **CapRover Machine**: `https://captain.indexo.ir`
- **Password**: [your CapRover password]

### Step 3: Run the script

```bash
caprover apps:exec multivendor-backend --command "cd /app/multivendor_platform && python -c \"from multivendor_platform.populate_fake_data import main; main()\""
```

Or interactive:

```bash
caprover apps:exec multivendor-backend --command "bash"
```

Then:

```bash
cd /app/multivendor_platform
python manage.py shell
```

In Django shell:

```python
from multivendor_platform.populate_fake_data import main
main()
```

---

## Method 3: CapRover Dashboard

1. Open: `https://captain.indexo.ir`
2. Go to **Apps** → **multivendor-backend** → **Terminal**
3. Run:

```bash
cd /app/multivendor_platform
python manage.py shell
```

Then:

```python
from multivendor_platform.populate_fake_data import main
main()
```

---

## ⚠️ Important Notes

### 1. Verify script exists

```bash
docker exec indexo_backend_staging ls -la /app/multivendor_platform/multivendor_platform/populate_fake_data.py
```

### 2. Check Faker is installed

```bash
docker exec indexo_backend_staging pip list | grep Faker
```

If not installed:

```bash
docker exec indexo_backend_staging pip install Faker>=24.0.0
```

### 3. Backup database first (recommended)

```bash
docker exec indexo_db_staging pg_dump -U postgres multivendor_db > backup_before_fake_data.sql
```

### 4. Check database connection

```bash
docker exec indexo_backend_staging python manage.py check --database default
```

---

## 🚀 Quick Commands

### For Docker Compose Staging:

```bash
# Connect to VPS
ssh root@185.208.172.76

# Run script
docker exec -it indexo_backend_staging python manage.py shell < /app/multivendor_platform/multivendor_platform/populate_fake_data.py

# Check logs
docker logs indexo_backend_staging --tail 50
```

### For CapRover:

```bash
# Login
caprover login

# Run script
caprover apps:exec multivendor-backend --command "cd /app/multivendor_platform && python -c \"from multivendor_platform.populate_fake_data import main; main()\""

# Check logs
caprover apps:logs multivendor-backend --tail 50
```

---

## 📊 Verify Results

```bash
docker exec indexo_backend_staging python manage.py shell -c "
from products.models import Department, Category, Subcategory, Product
from blog.models import BlogCategory, BlogPost
from users.models import VendorProfile, Supplier
print(f'Departments: {Department.objects.count()}')
print(f'Categories: {Category.objects.count()}')
print(f'Subcategories: {Subcategory.objects.count()}')
print(f'Products: {Product.objects.count()}')
print(f'Vendors: {VendorProfile.objects.count()}')
print(f'Suppliers: {Supplier.objects.count()}')
print(f'Blog Categories: {BlogCategory.objects.count()}')
print(f'Blog Posts: {BlogPost.objects.count()}')
"
```

---

## ✅ Pre-flight Checklist

- [ ] Connected to VPS
- [ ] Backend container is running
- [ ] Script exists in correct path
- [ ] Faker is installed
- [ ] Database connection works
- [ ] Database backup taken (recommended)
- [ ] Using staging environment (NOT production!)

---

## 📝 Notes

- **Default vendor password**: `testpass123`
- Script asks for confirmation if data exists
- All data is in Persian (Farsi)
- **DO NOT use in production!** Only for staging/testing

---

**Good luck! 🚀**

