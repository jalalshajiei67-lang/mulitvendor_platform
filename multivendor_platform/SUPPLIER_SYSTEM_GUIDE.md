# راهنمای سیستم تامین‌کنندگان (Supplier System Guide)

## 📋 خلاصه

یک سیستم کامل برای نمایش و مدیریت تامین‌کنندگان (فروشندگان) با امکان ثبت نظر توسط بازدیدکنندگان وب‌سایت ایجاد شده است.

## ✅ تغییرات Backend (Django)

### 1. مدل‌ها (Models)

#### VendorProfile - فیلدهای جدید:
```python
- address: آدرس فیزیکی تامین‌کننده
- work_resume: رزومه و سوابق کاری
- successful_projects: پروژه‌های موفق
- history: تاریخچه و پیشینه شرکت
- about: درباره تامین‌کننده/شرکت
```

#### SupplierComment - مدل جدید برای نظرات:
```python
- supplier: ForeignKey به VendorProfile
- user: کاربر ثبت‌کننده نظر
- rating: امتیاز (1-5)
- title: عنوان نظر (اختیاری)
- comment: متن نظر
- is_approved: تایید شده توسط ادمین
- supplier_reply: پاسخ فروشنده (اختیاری)
- supplier_replied_at: تاریخ پاسخ
```

### 2. Serializers

- **VendorProfileSerializer**: به‌روزرسانی شده با فیلدهای جدید + `product_count` و `rating_average`
- **SupplierCommentSerializer**: سریالایزر جدید برای نظرات

### 3. ViewSets و API Endpoints

#### SupplierViewSet
- `GET /api/users/suppliers/` - لیست تامین‌کنندگان
- `GET /api/users/suppliers/{id}/` - جزئیات تامین‌کننده
- `GET /api/users/suppliers/{id}/products/` - محصولات تامین‌کننده
- `GET /api/users/suppliers/{id}/comments/` - نظرات تامین‌کننده

#### SupplierCommentViewSet
- `GET /api/users/supplier-comments/` - لیست نظرات
- `POST /api/users/supplier-comments/` - ثبت نظر جدید (نیاز به احراز هویت)
- `GET /api/users/supplier-comments/{id}/` - جزئیات نظر
- `PUT/PATCH /api/users/supplier-comments/{id}/` - ویرایش نظر
- `DELETE /api/users/supplier-comments/{id}/` - حذف نظر

### 4. Django Admin

- **SupplierCommentAdmin** اضافه شده با امکانات:
  - نمایش لیست نظرات
  - فیلتر بر اساس امتیاز و وضعیت تایید
  - اکشن‌های تایید/عدم تایید دسته‌جمع

## ✅ تغییرات Frontend (Vue.js)

### 1. صفحات جدید

#### SupplierList.vue (`/suppliers`)
**ویژگی‌ها:**
- نمایش لیست تامین‌کنندگان در قالب Grid
- جستجو در نام، توضیحات و ایمیل
- مرتب‌سازی بر اساس:
  - نام (الف تا ی / ی تا الف)
  - بیشترین امتیاز
  - بیشترین محصولات
  - جدیدترین / قدیمی‌ترین
- نمایش لوگو، نام، توضیحات کوتاه
- نمایش امتیاز و تعداد محصولات
- نمایش شماره تماس
- دکمه مشاهده جزئیات
- لینک به وب‌سایت (در صورت وجود)
- طراحی RTL و فارسی با Vuetify Material Design 3
- Responsive برای موبایل، تبلت و دسکتاپ

#### SupplierDetail.vue (`/suppliers/:id`)
**ویژگی‌ها:**
- نمایش کامل اطلاعات تامین‌کننده
- تب‌های مختلف:
  1. **درباره**: اطلاعات عمومی و آدرس
  2. **رزومه کاری**: سوابق کاری
  3. **پروژه‌های موفق**: لیست پروژه‌های انجام شده
  4. **تاریخچه**: پیشینه و تاریخچه شرکت
  5. **محصولات**: نمایش Grid محصولات + لینک به صفحه محصول
  6. **نظرات**: نمایش و ثبت نظرات

**بخش نظرات:**
- فرم ثبت نظر برای کاربران احراز هویت شده
  - انتخاب امتیاز (1-5 ستاره)
  - عنوان نظر (اختیاری)
  - متن نظر
- نمایش لیست نظرات تایید شده
- نمایش پاسخ فروشنده (در صورت وجود)
- برای کاربران مهمان: لینک به صفحه ورود/ثبت‌نام

### 2. Router

مسیرهای جدید اضافه شده:
```javascript
{
  path: '/suppliers',
  name: 'SupplierList',
  component: SupplierList
},
{
  path: '/suppliers/:id',
  name: 'SupplierDetail',
  component: SupplierDetail,
  props: true
}
```

### 3. Navigation (App.vue)

لینک "تامین‌کنندگان" اضافه شده به:
- منوی دسکتاپ (Header)
- منوی موبایل (Navigation Drawer)
- فوتر سایت

## 🚀 نحوه اجرا

### 1. اجرای Migrations

```bash
cd multivendor_platform/multivendor_platform
python manage.py makemigrations users
python manage.py migrate
```

### 2. راه‌اندازی Backend

```bash
cd multivendor_platform/multivendor_platform
python manage.py runserver
```

### 3. راه‌اندازی Frontend

```bash
cd multivendor_platform/front_end
npm run dev
```

## 📝 نکات مهم

### دسترسی‌ها

1. **مشاهده لیست و جزئیات تامین‌کنندگان**: عمومی (نیاز به احراز هویت ندارد)
2. **ثبت نظر**: نیاز به احراز هویت دارد
3. **تایید/رد نظرات**: فقط از طریق Django Admin توسط مدیر

### فیلترینگ

- فقط تامین‌کنندگان تایید شده (`is_approved=True`) در لیست نمایش داده می‌شوند
- فقط نظرات تایید شده (`is_approved=True`) نمایش داده می‌شوند

### URL Structure

```
Frontend:
- /suppliers - لیست تامین‌کنندگان
- /suppliers/123 - جزئیات تامین‌کننده با ID=123

Backend API:
- GET /api/users/suppliers/ - لیست
- GET /api/users/suppliers/123/ - جزئیات
- GET /api/users/suppliers/123/products/ - محصولات
- GET /api/users/suppliers/123/comments/ - نظرات
- POST /api/users/supplier-comments/ - ثبت نظر
```

## 🎨 طراحی

- **RTL Support**: کامل
- **زبان**: فارسی
- **UI Framework**: Vuetify 3 (Material Design 3)
- **Responsive**: موبایل، تبلت، دسکتاپ
- **آیکون‌ها**: Material Design Icons
- **رنگ‌بندی**: از پالت اصلی پروژه استفاده می‌شود

## 🔧 توسعه‌های آینده (پیشنهادی)

1. **آپلود تصاویر پروژه‌ها**: امکان آپلود تصاویر برای پروژه‌های موفق
2. **گالری تصاویر**: گالری تصاویر برای هر تامین‌کننده
3. **فیلتر پیشرفته**: فیلتر بر اساس دسته‌بندی محصولات، محل قرارگیری، و غیره
4. **نمودار آماری**: نمایش آمار فروش و عملکرد تامین‌کننده
5. **سیستم پیام‌رسانی**: ارتباط مستقیم بین کاربران و تامین‌کنندگان
6. **امتیازدهی پیشرفته**: امکان امتیازدهی جداگانه برای کیفیت، قیمت، خدمات و ...

## 📞 پشتیبانی

در صورت بروز مشکل یا سوال:
1. بررسی Console مرورگر برای خطاهای Frontend
2. بررسی Terminal Django برای خطاهای Backend
3. اطمینان از اجرای migrations
4. بررسی اتصال Backend و Frontend (config.js)

---

**تاریخ ایجاد**: اکتبر 2025  
**نسخه**: 1.0.0  
**وضعیت**: آماده به استفاده ✅

