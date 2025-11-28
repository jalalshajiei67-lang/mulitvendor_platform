# سیستم گفتگوی آنلاین - راهنمای کامل

## 📋 خلاصه

سیستم گفتگوی آنلاین کامل با قابلیت WebSocket برای ارتباط بلادرنگ بین خریداران و فروشندگان پیاده‌سازی شده است.

## ✨ قابلیت‌های پیاده‌سازی شده

### Backend (Django)
- ✅ مدل‌های دیتابیس کامل (ChatRoom, ChatMessage, ChatParticipant, GuestSession, TypingStatus)
- ✅ پشتیبانی از WebSocket با Django Channels
- ✅ نشانگر تایپ کردن (Typing Indicators)
- ✅ رسید خواندن پیام (Read Receipts)
- ✅ پشتیبانی از کاربران مهمان (Guest Users)
- ✅ API های RESTful برای مدیریت چت
- ✅ پنل مدیریت برای ادمین و فروشندگان
- ✅ دستور مدیریتی برای پاک‌سازی پیام‌های قدیمی (3 ماه)
- ✅ سیستم مجوزها (Permissions)

### Frontend (Nuxt 3)
- ✅ Pinia Store برای مدیریت وضعیت چت
- ✅ مدیریت اتصال WebSocket با Reconnect خودکار
- ✅ کامپوننت‌های UI با پشتیبانی RTL و فارسی
- ✅ دکمه چت در صفحات محصول
- ✅ پنل ادمین برای نظارت بر چت‌ها
- ✅ صفحه صف چت برای فروشندگان
- ✅ ویجت چت شناور در کل سایت

### Infrastructure
- ✅ Redis برای Channel Layer
- ✅ پیکربندی Nginx برای WebSocket
- ✅ Docker Compose با Redis

---

## 📁 ساختار فایل‌ها

### Backend Files
```
multivendor_platform/multivendor_platform/chat/
├── __init__.py
├── apps.py
├── models.py              # مدل‌های دیتابیس
├── admin.py               # پنل ادمین Django
├── consumers.py           # WebSocket Consumer
├── serializers.py         # DRF Serializers
├── views.py               # API Views
├── urls.py                # URL Routing
├── permissions.py         # Custom Permissions
├── routing.py             # WebSocket Routing
└── management/
    └── commands/
        └── cleanup_old_messages.py
```

### Frontend Files
```
front_end/nuxt/
├── stores/
│   └── chat.ts            # Pinia Store
├── components/
│   ├── chat/
│   │   ├── ChatWidget.vue       # ویجت شناور
│   │   ├── ChatPanel.vue        # لیست اتاق‌ها
│   │   └── ChatRoom.vue         # صفحه گفتگو
│   └── product/
│       └── ProductChatButton.vue
└── pages/
    ├── admin/
    │   └── chats.vue            # پنل ادمین
    └── vendor/
        └── chats.vue            # صف چت فروشنده
```

---

## 🚀 راه‌اندازی و استقرار

### 1. نصب بسته‌های پایتون
```bash
pip install -r requirements.txt
```

بسته‌های جدید اضافه شده:
- `channels==4.0.0`
- `channels-redis==4.1.0`
- `daphne==4.0.0`
- `redis==5.0.1`

### 2. اجرای Migration های دیتابیس
```bash
cd multivendor_platform/multivendor_platform
python manage.py makemigrations chat
python manage.py migrate
```

### 3. راه‌اندازی با Docker
```bash
# Build و اجرای سرویس‌ها
docker-compose up -d --build

# بررسی لاگ‌ها
docker-compose logs -f backend
docker-compose logs -f redis
```

### 4. تنظیمات محیط (.env)
اضافه کردن متغیرهای زیر به فایل `.env`:
```env
# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
```

---

## 🔌 API Endpoints

### Chat Endpoints

#### 1. ایجاد Session مهمان
```http
POST /api/chat/guest-session/
Content-Type: application/json

{
  "identifier": "browser-fingerprint-or-identifier"
}

Response: {
  "session_id": "uuid",
  "identifier": "string",
  "created_at": "datetime"
}
```

#### 2. شروع گفتگو
```http
POST /api/chat/start/
Content-Type: application/json

{
  "vendor_id": 1,
  "product_id": 123,  // اختیاری
  "initial_message": "سلام",  // اختیاری
  "guest_session_id": "uuid"  // برای مهمان‌ها
}

Response: ChatRoom object
```

#### 3. لیست اتاق‌های چت
```http
GET /api/chat/rooms/
Authorization: Token <token>

Response: [ChatRoom, ...]
```

#### 4. پیام‌های یک اتاق
```http
GET /api/chat/rooms/{room_id}/messages/?page=1&page_size=50
Authorization: Token <token>

Response: {
  "count": 100,
  "next": "url",
  "previous": "url",
  "results": [ChatMessage, ...]
}
```

#### 5. علامت‌گذاری به عنوان خوانده شده
```http
POST /api/chat/rooms/{room_id}/mark_read/
Authorization: Token <token>
```

#### 6. لیست چت‌های فروشنده
```http
GET /api/chat/vendor/rooms/
Authorization: Token <vendor-token>
```

#### 7. لیست تمام چت‌ها (ادمین)
```http
GET /api/chat/admin/rooms/?search=query
Authorization: Token <admin-token>
```

#### 8. لینک کردن Session مهمان
```http
POST /api/chat/link-guest-session/
Authorization: Token <token>
Content-Type: application/json

{
  "guest_session_id": "uuid"
}
```

---

## 🔌 WebSocket Protocol

### اتصال
```javascript
const ws = new WebSocket('ws://domain.com/ws/chat/?token=AUTH_TOKEN')
// یا برای مهمان:
const ws = new WebSocket('ws://domain.com/ws/chat/?guest_session=GUEST_ID')
```

### پیام‌های ارسالی به سرور

#### Join Room
```json
{
  "type": "join_room",
  "room_id": "room-uuid"
}
```

#### Send Message
```json
{
  "type": "send_message",
  "room_id": "room-uuid",
  "content": "متن پیام"
}
```

#### Mark Read
```json
{
  "type": "mark_read",
  "room_id": "room-uuid"
}
```

#### Typing Indicator
```json
{
  "type": "typing",
  "room_id": "room-uuid",
  "is_typing": true
}
```

#### Leave Room
```json
{
  "type": "leave_room",
  "room_id": "room-uuid"
}
```

### پیام‌های دریافتی از سرور

#### Connection Established
```json
{
  "type": "connection_established",
  "user": "username",
  "guest_session": "uuid-if-guest"
}
```

#### New Message
```json
{
  "type": "message",
  "message_id": "uuid",
  "room_id": "room-uuid",
  "sender": 1,
  "sender_username": "username",
  "content": "text",
  "created_at": "iso-datetime",
  "is_read": false
}
```

#### Typing Status
```json
{
  "type": "typing",
  "room_id": "room-uuid",
  "user_id": 1,
  "username": "username",
  "is_typing": true
}
```

#### Read Receipt
```json
{
  "type": "read_receipt",
  "room_id": "room-uuid",
  "user_id": 1
}
```

---

## 💻 استفاده در Frontend

### استفاده از Pinia Store

```vue
<script setup>
import { useChatStore } from '~/stores/chat'

const chatStore = useChatStore()

// راه‌اندازی چت
onMounted(async () => {
  await chatStore.initializeChat()
})

// شروع گفتگو با فروشنده
const startChatWithVendor = async (vendorId, productId) => {
  const room = await chatStore.startChat(vendorId, productId)
  console.log('Chat started:', room)
}

// ارسال پیام
const sendMsg = () => {
  chatStore.sendMessage(roomId, messageText)
}

// نشان دادن نشانگر تایپ
const handleTyping = () => {
  chatStore.setTyping(roomId, true)
}
</script>
```

### استفاده از ChatWidget
```vue
<template>
  <div>
    <!-- ویجت چت به صورت خودکار در layout اضافه شده -->
    <ChatWidget />
  </div>
</template>
```

### استفاده از ProductChatButton
```vue
<template>
  <ProductChatButton 
    :product-id="product.id" 
    :vendor-id="product.vendor_id" 
  />
</template>
```

---

## 🔧 مدیریت و نگهداری

### پاک‌سازی پیام‌های قدیمی
```bash
# پاک کردن پیام‌های بیش از 90 روز
python manage.py cleanup_old_messages

# پاک کردن پیام‌های بیش از 30 روز
python manage.py cleanup_old_messages --days=30
```

### مانیتورینگ Redis
```bash
# وارد شدن به Redis Container
docker exec -it multivendor_redis redis-cli

# بررسی وضعیت
redis-cli> PING
redis-cli> INFO
redis-cli> CLIENT LIST
```

### بررسی لاگ‌های WebSocket
```bash
docker-compose logs -f backend | grep "WebSocket"
```

---

## 📱 صفحات مدیریتی

### پنل ادمین
- URL: `/admin/chats`
- دسترسی: فقط ادمین‌ها
- قابلیت‌ها:
  - مشاهده تمام گفتگوها
  - جستجو در گفتگوها
  - آمار کلی
  - نظارت بر مکالمات

### صفحه فروشنده
- URL: `/vendor/chats`
- دسترسی: فقط فروشندگان
- قابلیت‌ها:
  - صف گفتگوهای خودش
  - پیام‌های خوانده نشده
  - پاسخ‌های سریع
  - دسترسی به اطلاعات محصول

---

## 🎨 سفارشی‌سازی UI

### تغییر موقعیت ویجت چت
در فایل `ChatWidget.vue`:
```css
.chat-widget {
  position: fixed;
  bottom: 20px;
  left: 20px;  /* تغییر به right برای سمت راست */
}
```

### تغییر رنگ‌ها
پیام‌های خودی (Own Messages):
```css
.message-own .message-bubble {
  background-color: #4caf50;  /* تغییر رنگ */
}
```

### تغییر اندازه پنل
در فایل `ChatWidget.vue`:
```css
.chat-panel {
  width: 380px;  /* تغییر عرض */
  height: 500px;  /* تغییر ارتفاع */
}
```

---

## 🐛 عیب‌یابی (Troubleshooting)

### WebSocket اتصال برقرار نمی‌کند
1. بررسی Redis:
```bash
docker exec multivendor_redis redis-cli ping
```

2. بررسی لاگ‌های Backend:
```bash
docker-compose logs backend | tail -100
```

3. بررسی پیکربندی Nginx:
```bash
docker exec multivendor_nginx nginx -t
```

### پیام‌ها ارسال نمی‌شوند
1. بررسی اتصال WebSocket در Console مرورگر
2. بررسی Token یا Guest Session
3. بررسی Permissions در Backend

### مشکل در نمایش پیام‌ها
1. پاک کردن Cache مرورگر
2. بررسی لاگ‌های Console برای خطاهای JavaScript
3. بررسی API Response ها در Network Tab

---

## 📊 مدل‌های دیتابیس

### ChatRoom
- `room_id`: UUID یکتا
- `participants`: کاربران عضو (M2M)
- `product`: محصول مرتبط (nullable)
- `guest_session`: Session مهمان (nullable)
- `is_archived`: آرشیو شده
- `created_at`, `updated_at`

### ChatMessage
- `id`: UUID
- `room`: اتاق چت
- `sender`: فرستنده (nullable برای مهمان)
- `guest_session`: Session مهمان
- `content`: متن پیام
- `is_read`: خوانده شده
- `read_at`: زمان خواندن
- `created_at`

### GuestSession
- `session_id`: UUID
- `identifier`: شناسه مرورگر
- `linked_user`: کاربر لینک شده
- `created_at`

### ChatParticipant
- `room`: اتاق
- `user`: کاربر
- `joined_at`: زمان پیوستن
- `last_read_at`: آخرین زمان خواندن

---

## 🔐 امنیت

### احراز هویت
- کاربران ثبت‌شده: Token Authentication
- مهمان‌ها: Guest Session با UUID

### مجوزها
- کاربران فقط چت‌های خودشان را می‌بینند
- فروشندگان فقط چت‌های محصولات خودشان
- ادمین‌ها دسترسی به همه

### اعتبارسنجی
- بررسی دسترسی به Room در WebSocket
- اعتبارسنجی ورودی‌ها در API
- محدودیت اندازه پیام

---

## 🚀 بهینه‌سازی و عملکرد

### Redis Configuration
برای Production، تنظیمات زیر را در نظر بگیرید:
```bash
# در فایل redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
```

### Database Indexing
Index های مهم اضافه شده:
- `ChatRoom.room_id`
- `ChatRoom.updated_at`
- `ChatMessage.created_at`
- `ChatMessage.room + created_at`

### WebSocket Connection Pooling
تنظیمات Nginx برای مقیاس‌پذیری:
```nginx
upstream backend {
    least_conn;
    server backend1:8000;
    server backend2:8000;
}
```

---

## 📝 TODO های آینده (اختیاری)

- [ ] فایل و تصویر در چت
- [ ] Voice Messages
- [ ] Video Chat
- [ ] Push Notifications (برای اپلیکیشن Flutter)
- [ ] Chat Encryption (E2E)
- [ ] Message Search
- [ ] Chat Export
- [ ] Scheduled Messages
- [ ] Auto-responses
- [ ] Chat Analytics Dashboard

---

## 📞 پشتیبانی

برای مشکلات و سوالات:
1. بررسی لاگ‌های Docker
2. بررسی Console مرورگر
3. مطالعه Troubleshooting Guide
4. بررسی Django Admin برای داده‌های چت

---

## 📚 منابع مفید

- [Django Channels Documentation](https://channels.readthedocs.io/)
- [Redis Documentation](https://redis.io/documentation)
- [WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Vuetify Components](https://vuetifyjs.com/)

---

**تاریخ ایجاد**: {{ current_date }}  
**وضعیت**: ✅ آماده برای استفاده در Production  
**نسخه**: 1.0.0





