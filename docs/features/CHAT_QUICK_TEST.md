# Chat System - Quick Testing Guide

## What Was Added

1. ✅ "گفتگو با فروشنده" button on all product pages
2. ✅ Button automatically opens chat widget when clicked
3. ✅ Improved chat widget with better state management
4. ✅ Success/error notifications

## Local Testing Steps

### Option 1: Without Docker (Faster for testing)

#### 1. Start Redis
```bash
# Install Redis if not installed
sudo apt-get install redis-server
sudo systemctl start redis-server

# Or use Docker just for Redis
docker run -d -p 6379:6379 --name redis-chat redis:7-alpine
```

#### 2. Start Backend
```bash
cd "/media/jalal/New Volume/project/mulitvendor_platform/multivendor_platform/multivendor_platform"

# Install new dependencies
pip install channels==4.0.0 channels-redis==4.1.0 daphne==4.0.0 redis==5.0.1

# Run migrations
python3 manage.py makemigrations chat
python3 manage.py migrate

# Start with Daphne (supports WebSocket)
daphne -b 0.0.0.0 -p 8000 multivendor_platform.asgi:application
```

#### 3. Start Frontend (New Terminal)
```bash
cd "/media/jalal/New Volume/project/mulitvendor_platform/multivendor_platform/front_end/nuxt"

npm run dev
```

#### 4. Test the Chat
1. Open browser: http://localhost:3000
2. Go to any product page
3. Look for "گفتگو با فروشنده" button (below "Request Quote" button)
4. Click it - chat widget should open automatically
5. Send a test message
6. Check floating chat button (bottom-left corner)

### Option 2: With Docker (Production-like)

```bash
cd "/media/jalal/New Volume/project/mulitvendor_platform"

# Build and start
docker-compose up --build

# Run migrations
docker-compose exec backend python manage.py makemigrations chat
docker-compose exec backend python manage.py migrate

# Access
# Frontend: http://localhost:80
```

## Testing Checklist

- [ ] Product page loads
- [ ] "گفتگو با فروشنده" button is visible (green, outlined)
- [ ] Clicking button shows "Chat started!" notification
- [ ] Chat widget opens automatically
- [ ] Can send messages
- [ ] Typing indicator works
- [ ] Floating chat button shows in bottom-left
- [ ] Unread count appears on floating button

## Troubleshooting

### Button Not Showing
**Problem**: Can't see the chat button on product page

**Solution**: 
- Make sure you're on a product detail page (e.g., `/products/some-product-slug`)
- Check browser console for errors
- Verify product has a vendor assigned

### Chat Won't Start
**Problem**: Button doesn't work or shows error

**Solution**:
1. Check Redis is running: `redis-cli ping` (should return PONG)
2. Check backend logs: `docker-compose logs backend`
3. Check browser console for WebSocket errors
4. Verify backend is running with Daphne (not Gunicorn)

### WebSocket Connection Failed
**Problem**: "WebSocket connection failed" in console

**Solution**:
- Backend must run with Daphne: `daphne multivendor_platform.asgi:application`
- NOT Gunicorn: ~~`gunicorn multivendor_platform.wsgi:application`~~
- Check Redis is accessible from backend
- Check port 8000 is not blocked

## Browser Console Checks

Open browser DevTools (F12) and check:

### Expected Console Messages
```
WebSocket connected
Chat connection established
Chat started successfully: {...}
```

### Network Tab
- WebSocket connection to `ws://localhost:8000/ws/chat/`
- Status should be "101 Switching Protocols"

## Quick Fixes

### Redis Not Running
```bash
# Ubuntu/Debian
sudo systemctl start redis-server
sudo systemctl status redis-server

# Docker
docker start redis-chat
```

### Backend Not Starting
```bash
# Check if port 8000 is in use
sudo lsof -i :8000

# Kill process if needed
kill -9 <PID>
```

### Frontend Not Starting
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## CapRover Deployment Notes

When deploying to CapRover (https://captain.indexo.ir):

1. **Add Redis One-Click App** in CapRover
2. **Update Backend Environment Variables**:
   ```
   REDIS_HOST=srv-captain--redis
   REDIS_PORT=6379
   ```
3. **Backend must use Daphne** (update Dockerfile CMD):
   ```dockerfile
   CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "multivendor_platform.asgi:application"]
   ```
4. **Configure Nginx** in CapRover for WebSocket support

## File Changes Summary

### New Files
- `chat/` - Complete Django app
- `components/chat/` - Chat UI components
- `components/product/ProductChatButton.vue` - Button component
- `stores/chat.ts` - Chat state management
- `pages/admin/chats.vue` - Admin dashboard
- `pages/vendor/chats.vue` - Vendor dashboard

### Modified Files
- `layouts/default.vue` - Added ChatWidget
- `pages/products/[slug].vue` - Added chat button
- `docker-compose.yml` - Added Redis service
- `nginx/conf.d/default.conf` - Added WebSocket proxy
- `requirements.txt` - Added Channels packages

## Next Steps

After successful local testing:

1. ✅ Commit changes: `git add . && git commit -m "Add chat system"`
2. 🚀 Deploy to CapRover
3. 🧪 Test on production
4. 📱 Start Flutter app development (chat API is ready)

## Support

For issues, check:
- Django logs: `docker-compose logs backend`
- Browser console (F12)
- Redis status: `redis-cli ping`
- WebSocket connection in Network tab

---

**Test Date**: {{ current_date }}
**Status**: Ready for Testing







