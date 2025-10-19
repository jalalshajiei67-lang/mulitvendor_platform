# راهنمای نقشه سایت پویا (Dynamic Sitemap Guide)

## 📋 خلاصه

یک سیستم نقشه سایت **کاملاً خودکار و پویا** برای پلتفرم چند فروشنده ایجاد شده است که شامل:

1. **XML Sitemap** برای موتورهای جستجو (SEO)
2. **صفحه نقشه سایت بصری** برای کاربران

## ✅ ویژگی‌های کلیدی

### 🤖 کاملاً خودکار (Auto-Update)
- **هیچ نیاز به به‌روزرسانی دستی ندارد**
- با اضافه شدن محصولات، بلاگ‌ها، تامین‌کنندگان جدید، خودکار در sitemap قرار می‌گیرند
- با حذف یا تغییر وضعیت محتوا، sitemap خودکار به‌روز می‌شود

### 📊 پوشش کامل
سیستم sitemap شامل موارد زیر است:
- ✅ محصولات (فقط محصولات فعال)
- ✅ بخش‌ها (Departments)
- ✅ دسته‌بندی‌ها (Categories)
- ✅ زیردسته‌ها (Subcategories)
- ✅ تامین‌کنندگان (فقط تامین‌کنندگان تایید شده)
- ✅ مقالات بلاگ (فقط مقالات منتشر شده)
- ✅ صفحات استاتیک (خانه، درباره ما، و غیره)

## 🔧 پیاده‌سازی Backend (Django)

### 1. فایل‌های Sitemap ایجاد شده

#### `products/sitemaps.py`
```python
- ProductSitemap: محصولات فعال با اولویت 0.8
- DepartmentSitemap: بخش‌ها با اولویت 0.7
- CategorySitemap: دسته‌بندی‌ها با اولویت 0.6
- SubcategorySitemap: زیردسته‌ها با اولویت 0.5
- StaticViewSitemap: صفحات استاتیک با اولویت 0.5
```

#### `blog/sitemaps.py`
```python
- BlogSitemap: مقالات منتشر شده با اولویت 0.7
```

#### `users/sitemaps.py`
```python
- SupplierSitemap: تامین‌کنندگان تایید شده با اولویت 0.6
```

### 2. تنظیمات (settings.py)

```python
INSTALLED_APPS = [
    ...
    'django.contrib.sitemaps',  # اضافه شده
    ...
]
```

### 3. URL Configuration (urls.py)

```python
from django.contrib.sitemaps.views import sitemap
from products.sitemaps import ProductSitemap, DepartmentSitemap, ...
from blog.sitemaps import BlogSitemap
from users.sitemaps import SupplierSitemap

sitemaps = {
    'products': ProductSitemap,
    'departments': DepartmentSitemap,
    'categories': CategorySitemap,
    'subcategories': SubcategorySitemap,
    'blog': BlogSitemap,
    'suppliers': SupplierSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, ...),
]
```

## 🎨 پیاده‌سازی Frontend (Vue.js)

### 1. صفحه نقشه سایت بصری (`SiteMap.vue`)

**مسیر:** `/sitemap`

**ویژگی‌ها:**
- 📊 نمایش تمام بخش‌های سایت در کارت‌های دسته‌بندی شده
- 🔐 نمایش هوشمند بر اساس وضعیت احراز هویت
- 📈 نمایش آمار زنده (تعداد محصولات، بخش‌ها، تامین‌کنندگان، مقالات)
- 🎯 لینک مستقیم به sitemap.xml برای SEO
- 📱 طراحی Responsive با Vuetify Material Design 3
- 🌐 پشتیبانی کامل از RTL و فارسی

**بخش‌های نمایش داده شده:**
1. **صفحات عمومی**: خانه، درباره ما، نقشه سایت
2. **محصولات**: لیست محصولات، افزودن محصول (فروشندگان)
3. **بخش‌ها و دسته‌بندی‌ها**: لیست بخش‌ها + نمایش 5 بخش برتر
4. **تامین‌کنندگان**: لیست تامین‌کنندگان + نمایش 5 تامین‌کننده برتر
5. **وبلاگ**: لیست مقالات، داشبورد، افزودن مقاله
6. **احراز هویت / داشبورد**: بر اساس نقش کاربر

### 2. Router Configuration

```javascript
// router/index.js
import SiteMap from '../views/SiteMap.vue'

routes: [
  {
    path: '/sitemap',
    name: 'SiteMap',
    component: SiteMap
  },
  ...
]
```

### 3. Navigation Links

**فوتر سایت (App.vue):**
- لینک "نقشه سایت" اضافه شده به بخش "لینک‌های سریع"

## 📍 دسترسی به Sitemap

### برای موتورهای جستجو (XML):
```
http://127.0.0.1:8000/sitemap.xml
```

این فایل XML شامل تمام URL‌های سایت با اطلاعات زیر است:
- `<loc>`: آدرس صفحه
- `<lastmod>`: آخرین تغییر
- `<changefreq>`: دفعات تغییر
- `<priority>`: اولویت (0.0 - 1.0)

### برای کاربران (Visual):
```
http://localhost:5173/sitemap
```

صفحه بصری با دسترسی آسان به تمام بخش‌های سایت

## 🚀 نحوه استفاده

### 1. برای توسعه‌دهندگان

**هیچ کار اضافی لازم نیست!**

وقتی محصول، مقاله یا تامین‌کننده جدیدی اضافه می‌کنید:
- ✅ خودکار در `sitemap.xml` قرار می‌گیرد
- ✅ خودکار در صفحه بصری نمایش داده می‌شود
- ✅ آمار به‌روز می‌شود

### 2. افزودن ماژول جدید (اختیاری)

اگر می‌خواهید ماژول جدیدی به sitemap اضافه کنید:

**مرحله 1: ایجاد فایل sitemap در app جدید**

```python
# your_app/sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import YourModel

class YourModelSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    
    def items(self):
        return YourModel.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return f'/your-model/{obj.slug}'
```

**مرحله 2: اضافه کردن به `urls.py`**

```python
from your_app.sitemaps import YourModelSitemap

sitemaps = {
    ...
    'your_model': YourModelSitemap,
}
```

**مرحله 3: اضافه کردن به صفحه بصری (اختیاری)**

در `SiteMap.vue` یک کارت جدید اضافه کنید.

**تمام!** ✅

## 🎯 مزایا

### 1. برای SEO
- ✅ موتورهای جستجو تمام صفحات را پیدا می‌کنند
- ✅ اطلاعات دقیق از اولویت و تاریخ به‌روزرسانی
- ✅ به‌روزرسانی خودکار بدون دخالت دستی

### 2. برای کاربران
- ✅ دسترسی آسان به تمام بخش‌های سایت
- ✅ نمایش هوشمند بر اساس نقش کاربر
- ✅ آمار زنده از محتوای سایت
- ✅ رابط کاربری زیبا و ریسپانسیو

### 3. برای توسعه‌دهندگان
- ✅ بدون نیاز به نگهداری دستی
- ✅ مقیاس‌پذیری بالا
- ✅ افزودن آسان ماژول‌های جدید
- ✅ کد تمیز و ماژولار

## 📊 آمار و اطلاعات

صفحه بصری sitemap به صورت **زنده** اطلاعات زیر را نمایش می‌دهد:

| آیتم | منبع | API |
|------|------|-----|
| تعداد محصولات | Products API | `/api/products/` |
| تعداد بخش‌ها | Departments API | `/api/departments/` |
| تعداد تامین‌کنندگان | Suppliers API | `/api/users/suppliers/` |
| تعداد مقالات | Blog API | `/api/blog/posts/` |

## 🔐 سطوح دسترسی

### صفحه نقشه سایت بصری:
- ✅ **عمومی**: همه می‌توانند ببینند
- 🎨 **نمایش هوشمند**: بخش‌های خصوصی فقط برای کاربران احراز هویت شده نمایش داده می‌شوند

### XML Sitemap:
- ✅ **کاملاً عمومی**: برای موتورهای جستجو
- 📱 **فقط محتوای عمومی**: محصولات فعال، مقالات منتشر شده، تامین‌کنندگان تایید شده

## 🧪 تست

### تست XML Sitemap:
```bash
# مرور در مرورگر
http://127.0.0.1:8000/sitemap.xml

# یا با curl
curl http://127.0.0.1:8000/sitemap.xml
```

**خروجی مورد انتظار:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>http://127.0.0.1:8000/products/1</loc>
    <lastmod>2025-10-18</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
  ...
</urlset>
```

### تست Visual Sitemap:
```bash
# باز کردن در مرورگر
http://localhost:5173/sitemap
```

**چیزهایی که باید ببینید:**
- ✅ کارت‌های دسته‌بندی شده
- ✅ لیست بخش‌ها و تامین‌کنندگان
- ✅ آمار به‌روز
- ✅ لینک به sitemap.xml
- ✅ طراحی RTL فارسی

## 📝 نکات مهم

### 1. محتوای Sitemap
- فقط محصولات **فعال** (`is_active=True`) در sitemap قرار می‌گیرند
- فقط مقالات **منتشر شده** (`status='published'`) در sitemap قرار می‌گیرند
- فقط تامین‌کنندگان **تایید شده** (`is_approved=True`) در sitemap قرار می‌گیرند

### 2. به‌روزرسانی
- Sitemap **فوراً** با تغییرات دیتابیس به‌روز می‌شود
- نیازی به rebuild یا regenerate نیست
- هر بار که موتور جستجو sitemap.xml را می‌خواند، داده‌های جدید دریافت می‌کند

### 3. عملکرد (Performance)
- Sitemapها از کوئری‌های بهینه استفاده می‌کنند
- برای سایت‌های بزرگ، می‌توانید pagination اضافه کنید
- Django به صورت خودکار sitemap را cache می‌کند

## 🌐 SEO Tips

### 1. ثبت Sitemap در Search Console

**Google Search Console:**
1. به [Google Search Console](https://search.google.com/search-console) بروید
2. وب‌سایت خود را اضافه کنید
3. به بخش "Sitemaps" بروید
4. URL sitemap را وارد کنید: `https://yourdomain.com/sitemap.xml`
5. Submit کنید

### 2. افزودن به robots.txt

```txt
# robots.txt
User-agent: *
Allow: /

Sitemap: https://yourdomain.com/sitemap.xml
```

### 3. مانیتورینگ
- به صورت منظم Google Search Console را چک کنید
- اطمینان حاصل کنید که تمام URL‌ها index شده‌اند
- خطاها و هشدارها را بررسی کنید

## 📁 ساختار فایل‌ها

```
multivendor_platform/
├── multivendor_platform/
│   ├── products/
│   │   └── sitemaps.py          ✨ جدید
│   ├── blog/
│   │   └── sitemaps.py          ✨ جدید
│   ├── users/
│   │   └── sitemaps.py          ✨ جدید
│   ├── multivendor_platform/
│   │   ├── settings.py          📝 به‌روز شده
│   │   └── urls.py              📝 به‌روز شده
│
├── front_end/
│   └── src/
│       ├── views/
│       │   └── SiteMap.vue      ✨ جدید
│       ├── router/
│       │   └── index.js         📝 به‌روز شده
│       └── App.vue              📝 به‌روز شده
│
└── SITEMAP_GUIDE.md             ✨ این فایل
```

## ✅ وضعیت نهایی

- [x] Django sitemaps برای تمام ماژول‌ها ایجاد شد
- [x] XML sitemap در `/sitemap.xml` در دسترس است
- [x] صفحه بصری sitemap در `/sitemap` ایجاد شد
- [x] Router و navigation به‌روز شدند
- [x] آمار زنده پیاده‌سازی شد
- [x] طراحی RTL و فارسی
- [x] کاملاً خودکار و پویا
- [x] مستندات کامل

## 🎉 آماده استفاده!

سیستم sitemap **کاملاً خودکار** است و نیازی به نگهداری دستی ندارد. با اضافه شدن محتوای جدید، sitemap خودکار به‌روز می‌شود.

---

**تاریخ ایجاد**: اکتبر 2025  
**نسخه**: 1.0.0  
**وضعیت**: آماده به استفاده ✅  
**نوع**: Dynamic & Auto-updating  



