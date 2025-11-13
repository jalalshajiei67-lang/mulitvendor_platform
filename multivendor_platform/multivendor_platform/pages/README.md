# Static Pages Management App

این اپلیکیشن برای مدیریت صفحات استاتیک (درباره ما و تماس با ما) با پشتیبانی از محتوای چند زبانه و فیلدهای SEO طراحی شده است.

## ویژگی‌ها (Features)

- ✅ مدیریت صفحات **درباره ما** و **تماس با ما**
- ✅ پشتیبانی از محتوای **فارسی** و **انگلیسی**
- ✅ ویرایشگر WYSIWYG با TinyMCE (پشتیبانی از RTL)
- ✅ فیلدهای SEO کامل (Meta Title, Description, Keywords)
- ✅ API endpoints برای دسترسی از فرانت‌اند
- ✅ محدودیت یک نمونه برای هر صفحه (Singleton Pattern)
- ✅ جلوگیری از حذف صفحات از پنل ادمین

## نصب و راه‌اندازی (Installation)

### 1. اجرای مایگریشن‌ها (Run Migrations)

در ترمینال، به پوشه پروژه بروید و دستورات زیر را اجرا کنید:

```bash
cd /media/jalal/New\ Volume/project/mulitvendor_platform/multivendor_platform/multivendor_platform

# اجرای مایگریشن‌ها
python3 manage.py migrate pages

# (اختیاری) ایجاد سوپریوزر در صورت نیاز
python3 manage.py createsuperuser
```

### 2. راه‌اندازی سرور توسعه (Start Development Server)

```bash
python3 manage.py runserver
```

### 3. دسترسی به پنل ادمین (Access Admin Panel)

مرورگر خود را باز کنید و به آدرس زیر بروید:

```
http://127.0.0.1:8000/admin/
```

در بخش **صفحات استاتیک (Static Pages)** می‌توانید صفحات را مدیریت کنید:
- صفحه درباره ما
- صفحه تماس با ما

## ساختار مدل‌ها (Models Structure)

### AboutPage (صفحه درباره ما)

| فیلد | نوع | توضیحات |
|------|-----|---------|
| `title_fa` | CharField | عنوان فارسی |
| `content_fa` | HTMLField | محتوای فارسی (WYSIWYG) |
| `title_en` | CharField | عنوان انگلیسی (اختیاری) |
| `content_en` | HTMLField | محتوای انگلیسی (اختیاری) |
| `meta_title_fa` | CharField | عنوان متا فارسی (SEO) |
| `meta_description_fa` | TextField | توضیحات متا فارسی (SEO) |
| `meta_keywords_fa` | CharField | کلمات کلیدی فارسی (SEO) |
| `meta_title_en` | CharField | عنوان متا انگلیسی (SEO) |
| `meta_description_en` | TextField | توضیحات متا انگلیسی (SEO) |
| `meta_keywords_en` | CharField | کلمات کلیدی انگلیسی (SEO) |
| `created_at` | DateTimeField | تاریخ ایجاد |
| `updated_at` | DateTimeField | آخرین بروزرسانی |

### ContactPage (صفحه تماس با ما)

تمام فیلدهای AboutPage به اضافه:

| فیلد | نوع | توضیحات |
|------|-----|---------|
| `address_fa` | TextField | آدرس فارسی |
| `address_en` | TextField | آدرس انگلیسی |
| `phone` | CharField | شماره تلفن |
| `email` | EmailField | ایمیل |
| `working_hours_fa` | CharField | ساعات کاری فارسی |
| `working_hours_en` | CharField | ساعات کاری انگلیسی |

## API Endpoints

### 1. دریافت صفحه درباره ما (Get About Us Page)

**Endpoint:** `GET /api/pages/about/current/`

**پاسخ موفق (Success Response):**

```json
{
  "id": 1,
  "title_fa": "درباره ما",
  "content_fa": "<p>محتوای صفحه درباره ما...</p>",
  "title_en": "About Us",
  "content_en": "<p>About us page content...</p>",
  "meta_title_fa": "درباره ما - فروشگاه چند فروشنده",
  "meta_description_fa": "توضیحات درباره شرکت ما",
  "meta_keywords_fa": "درباره ما, تیم ما, شرکت",
  "meta_title_en": "About Us - Multivendor Platform",
  "meta_description_en": "Information about our company",
  "meta_keywords_en": "about us, team, company",
  "created_at": "2025-11-13T10:30:00Z",
  "updated_at": "2025-11-13T15:45:00Z"
}
```

**پاسخ خطا (Error Response):**

```json
{
  "detail": "صفحه درباره ما هنوز ایجاد نشده است"
}
```

### 2. دریافت صفحه تماس با ما (Get Contact Us Page)

**Endpoint:** `GET /api/pages/contact/current/`

**پاسخ موفق (Success Response):**

```json
{
  "id": 1,
  "title_fa": "تماس با ما",
  "content_fa": "<p>محتوای صفحه تماس با ما...</p>",
  "address_fa": "تهران، خیابان ولیعصر، پلاک 123",
  "phone": "021-12345678",
  "email": "info@example.com",
  "working_hours_fa": "شنبه تا چهارشنبه 9 الی 17",
  "title_en": "Contact Us",
  "content_en": "<p>Contact us page content...</p>",
  "address_en": "Tehran, Vali Asr Street, No. 123",
  "working_hours_en": "Saturday to Wednesday 9 AM to 5 PM",
  "meta_title_fa": "تماس با ما - فروشگاه چند فروشنده",
  "meta_description_fa": "راه‌های ارتباطی با ما",
  "meta_keywords_fa": "تماس, آدرس, تلفن",
  "meta_title_en": "Contact Us - Multivendor Platform",
  "meta_description_en": "Get in touch with us",
  "meta_keywords_en": "contact, address, phone",
  "created_at": "2025-11-13T10:30:00Z",
  "updated_at": "2025-11-13T15:45:00Z"
}
```

## استفاده در Vue.js Frontend

### مثال: دریافت صفحه درباره ما

```javascript
// Using Fetch API
async function getAboutPage() {
  try {
    const response = await fetch('http://localhost:8000/api/pages/about/current/');
    const data = await response.json();
    
    // نمایش محتوای فارسی
    document.getElementById('about-title').innerHTML = data.title_fa;
    document.getElementById('about-content').innerHTML = data.content_fa;
    
    // تنظیم SEO tags
    document.title = data.meta_title_fa;
    document.querySelector('meta[name="description"]').setAttribute('content', data.meta_description_fa);
    document.querySelector('meta[name="keywords"]').setAttribute('content', data.meta_keywords_fa);
  } catch (error) {
    console.error('Error fetching about page:', error);
  }
}
```

### مثال: دریافت صفحه تماس با ما

```javascript
// Using Composable in Nuxt 3
export default {
  async setup() {
    const { data: contactPage, error } = await useFetch('http://localhost:8000/api/pages/contact/current/');
    
    return {
      contactPage
    };
  }
}
```

```vue
<template>
  <div v-if="contactPage">
    <h1>{{ contactPage.title_fa }}</h1>
    <div v-html="contactPage.content_fa"></div>
    
    <div class="contact-info">
      <p><strong>آدرس:</strong> {{ contactPage.address_fa }}</p>
      <p><strong>تلفن:</strong> {{ contactPage.phone }}</p>
      <p><strong>ایمیل:</strong> {{ contactPage.email }}</p>
      <p><strong>ساعات کاری:</strong> {{ contactPage.working_hours_fa }}</p>
    </div>
  </div>
</template>
```

## نکات مهم (Important Notes)

### 1. Singleton Pattern
- هر صفحه فقط یک نمونه دارد
- تلاش برای ایجاد نمونه دوم، نمونه موجود را به‌روزرسانی می‌کند
- در پنل ادمین، دکمه "افزودن" بعد از ایجاد اولین نمونه غیرفعال می‌شود

### 2. جلوگیری از حذف (Prevent Deletion)
- صفحات نمی‌توانند از پنل ادمین حذف شوند
- برای امنیت و جلوگیری از خطاهای API

### 3. فیلدهای اجباری
- `title_fa` و `content_fa` اجباری هستند
- بقیه فیلدها اختیاری

### 4. محدودیت‌های SEO
- Meta Title: حداکثر 60 کاراکتر
- Meta Description: حداکثر 160 کاراکتر
- Meta Keywords: حداکثر 300 کاراکتر

## تست‌ها (Testing)

برای اجرای تست‌ها:

```bash
python3 manage.py test pages
```

## استقرار (Deployment)

این اپلیکیشن به صورت خودکار با CI/CD پایپلاین در CapRover مستقر می‌شود.

اطمینان حاصل کنید که:
1. مایگریشن‌ها اجرا شده‌اند
2. فایل‌های استاتیک collect شده‌اند
3. TinyMCE به درستی پیکربندی شده است

## پشتیبانی (Support)

برای گزارش باگ یا درخواست ویژگی جدید، لطفاً یک Issue ایجاد کنید.

---

**نسخه:** 1.0.0  
**تاریخ:** نوامبر 2025

