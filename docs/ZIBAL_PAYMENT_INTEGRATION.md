# راهنمای یکپارچه‌سازی درگاه پرداخت زیبال

## مقدمه

این مستند راهنمای کامل استفاده از سیستم پرداخت زیبال برای فعال‌سازی اشتراک پلن پریمیوم در پلتفرم Indexo را ارائه می‌دهد.

## فهرست مطالب

1. [پیش‌نیازها](#پیش-نیازها)
2. [نصب و راه‌اندازی](#نصب-و-راه-اندازی)
3. [تنظیمات محیطی](#تنظیمات-محیطی)
4. [فلوچارت فرآیند پرداخت](#فلوچارت-فرآیند-پرداخت)
5. [API Endpoints](#api-endpoints)
6. [استفاده از Frontend](#استفاده-از-frontend)
7. [مدیریت اشتراک‌ها](#مدیریت-اشتراک-ها)
8. [عیب‌یابی](#عیب-یابی)

---

## پیش‌نیازها

### نیازمندی‌های Backend

- Python 3.9+
- Django 4.0+
- Django REST Framework
- PostgreSQL
- کتابخانه‌های اضافی:
  ```bash
  pip install requests reportlab
  ```

### نیازمندی‌های Frontend

- Nuxt 3
- Vue 3
- Vuetify 3
- TypeScript

### حساب کاربری زیبال

- برای محیط تست: از merchant کد `zibal` استفاده کنید
- برای محیط production: باید حساب کاربری واقعی در زیبال ایجاد کنید

---

## نصب و راه‌اندازی

### 1. نصب وابستگی‌ها

```bash
# Backend
cd multivendor_platform/multivendor_platform
pip install requests reportlab

# Frontend - بدون نیاز به نصب اضافی
```

### 2. اعمال Migrations

```bash
python manage.py migrate
```

### 3. ایجاد Premium Tier

در Django shell یا از طریق Admin Panel یک PricingTier با مشخصات زیر ایجاد کنید:

```python
from users.models import PricingTier

premium_tier = PricingTier.objects.create(
    slug='premium',
    name='Premium',
    pricing_type='subscription',
    monthly_price=1500000,  # 1.5 million Toman
    monthly_price_rial=15000000,  # 15 million Rial for Zibal
    daily_customer_unlock_limit=0,  # Unlimited
    allow_marketplace_visibility=True,
    lead_exclusivity='exclusive'
)
```

---

## تنظیمات محیطی

### فایل `.env`

```env
# Zibal Payment Gateway
ZIBAL_MERCHANT=zibal  # برای تست - در production merchant واقعی خود را وارد کنید
SITE_URL=http://localhost:8000  # در production: https://indexo.ir
```

### فایل `settings.py`

تنظیمات زیر به صورت خودکار از environment variables خوانده می‌شوند:

```python
ZIBAL_MERCHANT = os.environ.get('ZIBAL_MERCHANT', 'zibal')
ZIBAL_API_BASE = 'https://gateway.zibal.ir'
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8000')
```

---

## فلوچارت فرآیند پرداخت

```
┌─────────────────────────────────────────────────────────────┐
│                    1. کاربر انتخاب پلن پریمیوم               │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  2. ارسال درخواست پرداخت به Backend                         │
│     POST /api/payments/premium/request/                     │
│     Body: {"billing_period": "monthly"}                     │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Backend درخواست به Zibal ارسال می‌کند                 │
│     POST https://gateway.zibal.ir/v1/request                │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  4. دریافت trackId و redirect به درگاه زیبال              │
│     https://gateway.zibal.ir/start/{trackId}                │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  5. کاربر اطلاعات کارت را وارد و پرداخت می‌کند             │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  6. Zibal کاربر را به callback برمی‌گرداند               │
│     GET /api/payments/premium/callback/?trackId=...         │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  7. Backend پرداخت را verify می‌کند                        │
│     POST https://gateway.zibal.ir/v1/verify                 │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  8. فعال‌سازی اشتراک و صدور فاکتور                        │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  9. نمایش صفحه نتیجه به کاربر                              │
│     /seller/payment-result?status=success                   │
└─────────────────────────────────────────────────────────────┘
```

---

## API Endpoints

### 1. درخواست پرداخت

**Endpoint:** `POST /api/payments/premium/request/`

**Headers:**
```
Authorization: Token {user_token}
Content-Type: application/json
```

**Body:**
```json
{
  "billing_period": "monthly"  // monthly | quarterly | semiannual | yearly
}
```

**Response (موفق):**
```json
{
  "success": true,
  "track_id": "123456",
  "payment_url": "https://gateway.zibal.ir/start/123456",
  "amount": 15000000,
  "amount_toman": 1500000,
  "order_id": "..."
}
```

### 2. Callback از زیبال

**Endpoint:** `GET /api/payments/premium/callback/`

**Query Parameters:**
- `trackId`: شناسه پیگیری
- `success`: 1 برای موفق، 0 برای ناموفق
- `status`: وضعیت پرداخت
- `orderId`: شناسه سفارش (اختیاری)

این endpoint به صورت خودکار توسط زیبال فراخوانی می‌شود و کاربر را به صفحه نتیجه هدایت می‌کند.

### 3. تاریخچه پرداخت‌ها

**Endpoint:** `GET /api/payments/history/`

**Headers:**
```
Authorization: Token {user_token}
```

**Query Parameters:**
- `status`: فیلتر بر اساس وضعیت (اختیاری)
- `page`: شماره صفحه
- `page_size`: تعداد آیتم در هر صفحه

**Response:**
```json
{
  "count": 10,
  "next": "...",
  "previous": null,
  "results": [
    {
      "id": 1,
      "billing_period": "monthly",
      "billing_period_display": "Monthly",
      "amount": 15000000,
      "amount_toman": 1500000.0,
      "status": "verified",
      "status_display": "Verified",
      "track_id": "123456",
      "ref_number": "REF789",
      "created_at": "2024-01-01T12:00:00Z",
      "paid_at": "2024-01-01T12:05:00Z"
    }
  ]
}
```

### 4. دانلود فاکتور

**Endpoint:** `GET /api/payments/invoice/{invoice_id}/download/`

**Headers:**
```
Authorization: Token {user_token}
```

**Response:** فایل PDF

---

## استفاده از Frontend

### 1. باز کردن دیالوگ پرداخت

```vue
<template>
  <PremiumPaymentDialog v-model="showDialog" @success="handleSuccess" />
  
  <v-btn @click="showDialog = true">
    ارتقاء به پریمیوم
  </v-btn>
</template>

<script setup>
const showDialog = ref(false)

function handleSuccess() {
  // پرداخت موفق بود
  console.log('Payment successful!')
}
</script>
```

### 2. استفاده از Composable

```typescript
import { usePaymentApi } from '~/composables/usePaymentApi'

const paymentApi = usePaymentApi()

// درخواست پرداخت
const response = await paymentApi.requestPremiumPayment('monthly')
if (response.success) {
  window.location.href = response.payment_url
}

// دریافت تاریخچه
const history = await paymentApi.getPaymentHistory()

// دانلود فاکتور
paymentApi.downloadInvoice(invoiceId)
```

---

## مدیریت اشتراک‌ها

### کامندهای Management

#### 1. بررسی اشتراک‌های منقضی شده

```bash
# اجرای واقعی
python manage.py check_subscription_expiry

# حالت Dry-run (بدون تغییر)
python manage.py check_subscription_expiry --dry-run
```

این کامند را روزانه اجرا کنید (با cron یا Celery Beat).

#### 2. ارسال یادآوری تمدید

```bash
# ارسال یادآوری 3 روز قبل از انقضا
python manage.py send_renewal_reminders --days=3

# حالت Dry-run
python manage.py send_renewal_reminders --days=3 --dry-run
```

### تنظیم Cron (Linux/Mac)

```bash
# ویرایش crontab
crontab -e

# اضافه کردن خطوط زیر:
# چک روزانه اشتراک‌های منقضی شده (هر روز ساعت 1 صبح)
0 1 * * * /path/to/venv/bin/python /path/to/manage.py check_subscription_expiry

# یادآوری تمدید (هر روز ساعت 9 صبح)
0 9 * * * /path/to/venv/bin/python /path/to/manage.py send_renewal_reminders --days=3
```

---

## عیب‌یابی

### مشکلات رایج

#### 1. خطا در درخواست به زیبال

**علت:** merchant نامعتبر یا اتصال به اینترنت قطع است

**راه‌حل:**
- بررسی کنید که `ZIBAL_MERCHANT` به درستی تنظیم شده باشد
- در محیط تست از `zibal` استفاده کنید
- اتصال به اینترنت را بررسی کنید

#### 2. Callback دریافت نمی‌شود

**علت:** URL callback قابل دسترسی نیست

**راه‌حل:**
- مطمئن شوید سرور شما از طریق HTTPS در دسترس است
- در محیط development می‌توانید از ngrok استفاده کنید
- بررسی کنید که `SITE_URL` به درستی تنظیم شده باشد

#### 3. فاکتور تولید نمی‌شود

**علت:** کتابخانه reportlab نصب نشده است

**راه‌حل:**
```bash
pip install reportlab
```

#### 4. پرداخت verify نمی‌شود

**علت:** trackId نامعتبر یا پرداخت قبلاً verify شده است

**راه‌حل:**
- لاگ‌های Django را بررسی کنید
- از endpoint inquiry برای بررسی وضعیت استفاده کنید

---

## لاگ‌گذاری

تمام عملیات مهم لاگ می‌شوند. برای مشاهده لاگ‌ها:

```bash
# مشاهده لاگ‌های Django
tail -f /path/to/logs/django.log

# یا در development
python manage.py runserver
```

---

## تغییر از Test به Production

### مراحل:

1. دریافت merchant واقعی از پنل زیبال
2. به‌روزرسانی environment variable:
   ```env
   ZIBAL_MERCHANT=your_real_merchant_id
   ```
3. مطمئن شوید `SITE_URL` به آدرس production اشاره می‌کند:
   ```env
   SITE_URL=https://indexo.ir
   ```
4. ریستارت سرور Django

---

## پشتیبانی

برای مشکلات مربوط به:
- **زیبال:** https://zibal.ir/support
- **پلتفرم Indexo:** support@indexo.ir

---

## نسخه

نسخه فعلی: 1.0.0  
تاریخ به‌روزرسانی: دسامبر 2024

