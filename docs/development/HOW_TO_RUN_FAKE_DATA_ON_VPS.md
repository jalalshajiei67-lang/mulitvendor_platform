# 📋 راهنمای اجرای اسکریپت تولید داده‌های تست در VPS

## 🎯 روش‌های اجرا

دو روش برای اجرای اسکریپت در VPS وجود دارد:

---

## روش 1: استفاده از Docker Exec (برای Staging با Docker Compose) ⭐

### مرحله 1: اتصال به VPS

```bash
ssh root@185.208.172.76
```

### مرحله 2: بررسی کانتینرهای در حال اجرا

```bash
docker ps | grep backend
```

باید کانتینر `indexo_backend_staging` را ببینید.

### مرحله 3: اجرای اسکریپت

#### گزینه A: اجرای مستقیم با Python

```bash
# کپی کردن اسکریپت به داخل کانتینر و اجرا
docker exec -it indexo_backend_staging python manage.py shell < populate_fake_data.py
```

یا اگر اسکریپت در مسیر دیگری است:

```bash
# اجرا از مسیر کامل
docker exec -it indexo_backend_staging bash -c "cd /app/multivendor_platform && python manage.py shell < multivendor_platform/populate_fake_data.py"
```

#### گزینه B: اجرا از طریق Django Shell

```bash
# ورود به shell کانتینر
docker exec -it indexo_backend_staging bash

# سپس در داخل کانتینر:
cd /app/multivendor_platform
python manage.py shell
```

سپس در Django shell:

```python
from multivendor_platform.populate_fake_data import main
main()
```

یا:

```python
exec(open('multivendor_platform/populate_fake_data.py').read())
```

---

## روش 2: استفاده از CapRover CLI (اگر از CapRover استفاده می‌کنید)

### مرحله 1: نصب CapRover CLI (در صورت نیاز)

```bash
npm install -g caprover
```

### مرحله 2: ورود به CapRover

```bash
caprover login
```

اطلاعات ورود:
- **CapRover Machine**: `https://captain.indexo.ir`
- **Password**: [رمز CapRover شما]

### مرحله 3: اجرای اسکریپت

```bash
# اجرای مستقیم
caprover apps:exec multivendor-backend --command "cd /app/multivendor_platform && python manage.py shell < multivendor_platform/populate_fake_data.py"
```

یا:

```bash
# ورود به shell و اجرای دستی
caprover apps:exec multivendor-backend --command "bash"
```

سپس در داخل shell:

```bash
cd /app/multivendor_platform
python manage.py shell
```

و در Django shell:

```python
from multivendor_platform.populate_fake_data import main
main()
```

---

## روش 3: اجرا از طریق CapRover Dashboard

### مرحله 1: ورود به داشبورد

1. باز کردن مرورگر: `https://captain.indexo.ir`
2. ورود با رمز CapRover

### مرحله 2: دسترسی به Terminal

1. رفتن به **Apps** → **multivendor-backend**
2. کلیک روی تب **Terminal**
3. اجرای دستورات:

```bash
cd /app/multivendor_platform
python manage.py shell
```

سپس در Django shell:

```python
from multivendor_platform.populate_fake_data import main
main()
```

---

## ⚠️ نکات مهم

### 1. بررسی وجود اسکریپت

قبل از اجرا، مطمئن شوید اسکریپت در کانتینر وجود دارد:

```bash
# برای Docker Compose
docker exec indexo_backend_staging ls -la /app/multivendor_platform/multivendor_platform/populate_fake_data.py

# برای CapRover
caprover apps:exec multivendor-backend --command "ls -la /app/multivendor_platform/multivendor_platform/populate_fake_data.py"
```

### 2. بررسی نصب بودن Faker

```bash
# برای Docker Compose
docker exec indexo_backend_staging pip list | grep Faker

# برای CapRover
caprover apps:exec multivendor-backend --command "pip list | grep Faker"
```

اگر Faker نصب نیست:

```bash
# برای Docker Compose
docker exec indexo_backend_staging pip install Faker>=24.0.0

# برای CapRover
caprover apps:exec multivendor-backend --command "pip install Faker>=24.0.0"
```

### 3. بررسی دسترسی به دیتابیس

```bash
# تست اتصال به دیتابیس
docker exec indexo_backend_staging python manage.py check --database default
```

### 4. پشتیبان‌گیری قبل از اجرا (توصیه می‌شود)

```bash
# برای Docker Compose
docker exec indexo_db_staging pg_dump -U postgres multivendor_db > backup_before_fake_data.sql

# برای CapRover
caprover apps:exec postgres-db --command "pg_dump -U postgres multivendor_db" > backup_before_fake_data.sql
```

---

## 🚀 دستورات سریع (Quick Commands)

### برای Staging با Docker Compose:

```bash
# 1. اتصال به VPS
ssh root@185.208.172.76

# 2. اجرای اسکریپت
docker exec -it indexo_backend_staging python manage.py shell < /app/multivendor_platform/multivendor_platform/populate_fake_data.py

# 3. بررسی لاگ‌ها
docker logs indexo_backend_staging --tail 50
```

### برای CapRover:

```bash
# 1. ورود به CapRover
caprover login

# 2. اجرای اسکریپت
caprover apps:exec multivendor-backend --command "cd /app/multivendor_platform && python -c \"from multivendor_platform.populate_fake_data import main; main()\""

# 3. بررسی لاگ‌ها
caprover apps:logs multivendor-backend --tail 50
```

---

## 📊 بررسی نتایج

بعد از اجرای اسکریپت، می‌توانید نتایج را بررسی کنید:

```bash
# شمارش تعداد رکوردها
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

## 🔧 عیب‌یابی

### مشکل: اسکریپت پیدا نمی‌شود

**راه حل:**
```bash
# بررسی مسیر فایل
docker exec indexo_backend_staging find /app -name "populate_fake_data.py"

# یا کپی کردن فایل به داخل کانتینر
docker cp populate_fake_data.py indexo_backend_staging:/app/multivendor_platform/
```

### مشکل: Faker نصب نیست

**راه حل:**
```bash
# نصب Faker
docker exec indexo_backend_staging pip install Faker>=24.0.0

# یا اگر از requirements.txt استفاده می‌کنید
docker exec indexo_backend_staging pip install -r requirements.txt
```

### مشکل: خطای دیتابیس

**راه حل:**
```bash
# بررسی اتصال
docker exec indexo_backend_staging python manage.py check --database default

# اجرای migrations
docker exec indexo_backend_staging python manage.py migrate
```

---

## ✅ چک‌لیست قبل از اجرا

- [ ] اتصال به VPS برقرار است
- [ ] کانتینر backend در حال اجرا است
- [ ] اسکریپت در مسیر صحیح قرار دارد
- [ ] Faker نصب شده است
- [ ] اتصال به دیتابیس برقرار است
- [ ] پشتیبان از دیتابیس گرفته شده است (توصیه می‌شود)
- [ ] از محیط staging استفاده می‌کنید (نه production!)

---

## 📝 یادداشت‌ها

- **رمز پیش‌فرض برای کاربران vendor**: `testpass123`
- اسکریپت قبل از اجرا از شما تایید می‌گیرد اگر داده‌ای وجود داشته باشد
- تمام داده‌ها به زبان فارسی (Farsi) تولید می‌شوند
- برای production استفاده نکنید! فقط برای staging/testing

---

**موفق باشید! 🚀**


