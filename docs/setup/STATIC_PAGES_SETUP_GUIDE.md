# راهنمای راه‌اندازی صفحات استاتیک (Static Pages Setup Guide)

## ✅ آنچه ایجاد شده است

یک سیستم کامل مدیریت صفحات استاتیک با ویژگی‌های زیر ایجاد شد:

### 📁 فایل‌های ایجاد شده:

```
multivendor_platform/multivendor_platform/pages/
├── __init__.py                    # فایل اولیه اپلیکیشن
├── apps.py                        # پیکربندی اپلیکیشن
├── models.py                      # مدل‌های AboutPage و ContactPage
├── admin.py                       # پنل ادمین با TinyMCE
├── serializers.py                 # سریالایزرها برای API
├── views.py                       # API ViewSets
├── urls.py                        # URL routing
├── tests.py                       # تست‌های اتوماتیک
├── README.md                      # مستندات کامل
└── migrations/
    ├── __init__.py
    └── 0001_initial.py            # مایگریشن اولیه
```

### 🎯 ویژگی‌های پیاده‌سازی شده:

1. ✅ دو مدل جداگانه: `AboutPage` و `ContactPage`
2. ✅ محتوای چند زبانه (فارسی/انگلیسی)
3. ✅ فیلدهای SEO کامل (Meta Title, Description, Keywords)
4. ✅ ویرایشگر WYSIWYG با TinyMCE (پشتیبانی RTL)
5. ✅ API endpoints برای فرانت‌اند
6. ✅ Singleton Pattern (فقط یک نمونه از هر صفحه)
7. ✅ محافظت در برابر حذف

---

## 🚀 مراحل راه‌اندازی

### مرحله 1️⃣: اجرای مایگریشن‌ها

در ترمینال، به پوشه پروژه بروید:

```bash
cd "/media/jalal/New Volume/project/mulitvendor_platform/multivendor_platform/multivendor_platform"

# اجرای مایگریشن‌ها
python3 manage.py migrate pages
```

**خروجی مورد انتظار:**
```
Operations to perform:
  Apply all migrations: pages
Running migrations:
  Applying pages.0001_initial... OK
```

### مرحله 2️⃣: راه‌اندازی سرور

```bash
python3 manage.py runserver
```

### مرحله 3️⃣: دسترسی به پنل ادمین

1. مرورگر خود را باز کنید و به آدرس زیر بروید:
   ```
   http://127.0.0.1:8000/admin/
   ```

2. وارد شوید با اکانت سوپریوزر خود

3. در منوی سمت چپ، بخش **"صفحات استاتیک (Static Pages)"** را پیدا کنید

4. دو بخش خواهید دید:
   - **صفحه درباره ما**
   - **صفحه تماس با ما**

### مرحله 4️⃣: ایجاد صفحات

#### ایجاد صفحه درباره ما:

1. روی **"صفحه درباره ما"** کلیک کنید
2. روی **"افزودن صفحه درباره ما"** کلیک کنید
3. فیلدهای زیر را پر کنید:

**محتوای فارسی (Persian Content):**
- عنوان (فارسی): مثال `درباره ما`
- محتوا (فارسی): از ویرایشگر TinyMCE استفاده کنید

**محتوای انگلیسی (English Content) - اختیاری:**
- Title (English): مثال `About Us`
- Content (English): محتوای انگلیسی

**سئو فارسی (Persian SEO):**
- عنوان متا (فارسی): مثال `درباره ما - فروشگاه چند فروشنده`
- توضیحات متا (فارسی): مثال `اطلاعات کامل درباره شرکت و تیم ما`
- کلمات کلیدی متا (فارسی): مثال `درباره ما, تیم ما, شرکت`

4. روی **"ذخیره"** کلیک کنید

#### ایجاد صفحه تماس با ما:

1. روی **"صفحه تماس با ما"** کلیک کنید
2. روی **"افزودن صفحه تماس با ما"** کلیک کنید
3. فیلدهای زیر را پر کنید:

**محتوای فارسی:**
- عنوان (فارسی): مثال `تماس با ما`
- محتوا (فارسی): محتوای اصلی صفحه

**اطلاعات تماس:**
- آدرس (فارسی): مثال `تهران، خیابان ولیعصر، پلاک 123`
- تلفن: مثال `021-12345678`
- ایمیل: مثال `info@indexo.ir`
- ساعات کاری (فارسی): مثال `شنبه تا چهارشنبه 9 الی 17`

**سئو فارسی:**
- عنوان متا، توضیحات متا، کلمات کلیدی

4. روی **"ذخیره"** کلیک کنید

---

## 🔌 API Endpoints

بعد از ایجاد صفحات، می‌توانید از طریق API به آنها دسترسی داشته باشید:

### درباره ما (About Us):
```
GET http://localhost:8000/api/pages/about/current/
```

### تماس با ما (Contact Us):
```
GET http://localhost:8000/api/pages/contact/current/
```

### تست API با curl:

```bash
# تست API درباره ما
curl http://localhost:8000/api/pages/about/current/

# تست API تماس با ما
curl http://localhost:8000/api/pages/contact/current/
```

---

## 📱 استفاده در فرانت‌اند (Vue.js/Nuxt)

### نمونه کد Nuxt 3 Composable:

```typescript
// composables/usePages.ts
export const useAboutPage = async () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBaseUrl || 'http://localhost:8000'
  
  const { data, error } = await useFetch(`${baseURL}/api/pages/about/current/`)
  
  return { data, error }
}

export const useContactPage = async () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBaseUrl || 'http://localhost:8000'
  
  const { data, error } = await useFetch(`${baseURL}/api/pages/contact/current/`)
  
  return { data, error }
}
```

### نمونه صفحه درباره ما:

```vue
<!-- pages/about-us.vue -->
<template>
  <v-container>
    <v-row v-if="page">
      <v-col cols="12">
        <h1 class="text-h3 mb-4">{{ page.title_fa }}</h1>
        <div v-html="page.content_fa" class="page-content"></div>
      </v-col>
    </v-row>
    <v-row v-else-if="error">
      <v-col cols="12">
        <v-alert type="error">خطا در بارگذاری صفحه</v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
const { data: page, error } = await useAboutPage()

// تنظیم SEO
useHead({
  title: page.value?.meta_title_fa || 'درباره ما',
  meta: [
    {
      name: 'description',
      content: page.value?.meta_description_fa || ''
    },
    {
      name: 'keywords',
      content: page.value?.meta_keywords_fa || ''
    }
  ]
})
</script>

<style scoped>
.page-content {
  direction: rtl;
  text-align: justify;
}
</style>
```

### نمونه صفحه تماس با ما:

```vue
<!-- pages/contact-us.vue -->
<template>
  <v-container>
    <v-row v-if="page">
      <v-col cols="12" md="8">
        <h1 class="text-h3 mb-4">{{ page.title_fa }}</h1>
        <div v-html="page.content_fa" class="page-content mb-6"></div>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>اطلاعات تماس</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item v-if="page.address_fa">
                <template #prepend>
                  <v-icon>mdi-map-marker</v-icon>
                </template>
                <v-list-item-title>{{ page.address_fa }}</v-list-item-title>
              </v-list-item>
              
              <v-list-item v-if="page.phone">
                <template #prepend>
                  <v-icon>mdi-phone</v-icon>
                </template>
                <v-list-item-title>{{ page.phone }}</v-list-item-title>
              </v-list-item>
              
              <v-list-item v-if="page.email">
                <template #prepend>
                  <v-icon>mdi-email</v-icon>
                </template>
                <v-list-item-title>{{ page.email }}</v-list-item-title>
              </v-list-item>
              
              <v-list-item v-if="page.working_hours_fa">
                <template #prepend>
                  <v-icon>mdi-clock</v-icon>
                </template>
                <v-list-item-title>{{ page.working_hours_fa }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
const { data: page, error } = await useContactPage()

// تنظیم SEO
useHead({
  title: page.value?.meta_title_fa || 'تماس با ما',
  meta: [
    {
      name: 'description',
      content: page.value?.meta_description_fa || ''
    },
    {
      name: 'keywords',
      content: page.value?.meta_keywords_fa || ''
    }
  ]
})
</script>
```

---

## 🧪 تست عملکرد

### تست مایگریشن:

```bash
python3 manage.py showmigrations pages
```

**خروجی مورد انتظار:**
```
pages
 [X] 0001_initial
```

### تست Django Shell:

```bash
python3 manage.py shell
```

```python
from pages.models import AboutPage, ContactPage

# ایجاد صفحه درباره ما
about = AboutPage.objects.create(
    title_fa='درباره ما',
    content_fa='<p>محتوای تست</p>',
    meta_title_fa='درباره ما - تست'
)

# ایجاد صفحه تماس با ما
contact = ContactPage.objects.create(
    title_fa='تماس با ما',
    content_fa='<p>محتوای تست</p>',
    phone='021-12345678',
    email='info@test.com'
)

# بررسی
print(AboutPage.objects.count())  # باید 1 باشد
print(ContactPage.objects.count())  # باید 1 باشد
```

### اجرای تست‌های واحد:

```bash
python3 manage.py test pages
```

---

## 📝 نکات مهم

### ⚠️ محدودیت‌ها:

1. **فقط یک نمونه از هر صفحه:** تلاش برای ایجاد نمونه دوم، نمونه قبلی را به‌روزرسانی می‌کند
2. **حذف غیرممکن است:** صفحات نمی‌توانند از پنل ادمین حذف شوند
3. **فیلدهای اجباری:** `title_fa` و `content_fa` باید پر شوند

### 💡 توصیه‌های SEO:

- **Meta Title:** حداکثر 60 کاراکتر
- **Meta Description:** حداکثر 160 کاراکتر
- **Meta Keywords:** حداکثر 300 کاراکتر (کلمات را با کاما جدا کنید)

### 🎨 استفاده از TinyMCE:

- ویرایشگر به صورت خودکار با RTL پیکربندی شده
- می‌توانید تصویر، جدول، لینک و ... اضافه کنید
- از فونت وزیر برای فارسی پشتیبانی می‌شود

---

## 🐛 عیب‌یابی (Troubleshooting)

### خطا: "No module named 'pages'"
```bash
# مطمئن شوید که در INSTALLED_APPS اضافه شده است
python3 manage.py migrate pages
```

### خطا: "No such table: pages_about"
```bash
# مایگریشن‌ها را اجرا کنید
python3 manage.py migrate
```

### خطا در TinyMCE:
```bash
# فایل‌های استاتیک را collect کنید
python3 manage.py collectstatic --noinput
```

---

## ✅ چک‌لیست نهایی

- [ ] مایگریشن‌ها اجرا شده
- [ ] صفحه درباره ما در ادمین ایجاد شده
- [ ] صفحه تماس با ما در ادمین ایجاد شده
- [ ] API endpoint درباره ما کار می‌کند
- [ ] API endpoint تماس با ما کار می‌کند
- [ ] فیلدهای SEO پر شده
- [ ] محتوای فارسی با ویرایشگر WYSIWYG اضافه شده

---

## 📞 سوالات؟

اگر سوال یا مشکلی دارید، لطفاً موارد زیر را بررسی کنید:
- مستندات کامل در `pages/README.md`
- لاگ‌های Django در ترمینال
- پیام‌های خطا در پنل ادمین

---

**موفق باشید! 🚀**

