# Chat System - Quick Reference Guide

## 🚀 Quick Start

### Using Chat Widget (Global)
Add to your main layout:
```vue
<template>
  <div>
    <ChatWidget />
    <!-- Your content -->
  </div>
</template>
```

### Starting a Chat from Product
```vue
<template>
  <ProductChatButton 
    :product-id="123"
    :vendor-id="456"
    block
    outlined
  />
</template>
```

---

## 🎨 Component Props

### ProductChatButton
```typescript
{
  productId: number      // Required: Product ID
  vendorId: number       // Required: Vendor/Seller ID
  block?: boolean        // Optional: Full width button
  outlined?: boolean     // Optional: Outlined style
  size?: string          // Optional: Button size
}
```

### ChatRoom
```typescript
{
  roomId: string         // Required: Chat room ID
}

// Events
@back                    // Emitted when back button clicked
```

### ChatPanel
```typescript
// No props

// Events
@select-room: (roomId: string) => void
```

---

## 🔧 Store Methods

### useChatStore

#### Connection
```javascript
const chatStore = useChatStore()

// Initialize chat
await chatStore.initializeChat()

// Connect WebSocket
await chatStore.connectWebSocket()

// Disconnect
chatStore.disconnectWebSocket()
```

#### Rooms
```javascript
// Fetch all rooms
await chatStore.fetchRooms()

// Start new chat
const room = await chatStore.startChat(
  vendorId,          // Vendor ID
  productId,         // Optional: Product ID
  initialMessage     // Optional: First message
)

// Open specific room
chatStore.openRoom(roomId)

// Close widget
chatStore.closeWidget()

// Toggle widget
chatStore.toggleWidget()
```

#### Messages
```javascript
// Fetch messages for a room
await chatStore.fetchMessages(roomId)

// Send message
chatStore.sendMessage(roomId, content)

// Mark as read
chatStore.markAsRead(roomId)
```

#### Typing Status
```javascript
// Set typing status
chatStore.setTyping(roomId, isTyping)
```

#### Guest Sessions
```javascript
// Create guest session (for non-authenticated users)
await chatStore.createGuestSession()

// Link guest session to user account
await chatStore.linkGuestSession()
```

---

## 📊 Store State

### Accessing State
```javascript
const chatStore = useChatStore()

// Direct access
chatStore.rooms           // All chat rooms
chatStore.currentRoomId   // Currently open room
chatStore.messages        // Messages by room ID
chatStore.isConnected     // WebSocket status
chatStore.widgetOpen      // Widget open state

// Computed properties
chatStore.currentRoom     // Current room object
chatStore.totalUnreadCount // Total unread messages
chatStore.currentMessages  // Messages for current room
```

---

## 🎯 Common Patterns

### Check if User is Authenticated
```javascript
const authStore = useAuthStore()
if (authStore.isAuthenticated) {
  // User is logged in
} else {
  // Create guest session
  await chatStore.createGuestSession()
}
```

### Handle New Messages
```javascript
// Watch for new messages
watch(() => chatStore.totalUnreadCount, (newCount, oldCount) => {
  if (newCount > oldCount) {
    // New message received
    playNotificationSound()
  }
})
```

### Custom Quick Replies
```javascript
const quickReplies = [
  'سلام',
  'محصول موجود است؟',
  'قیمت؟',
  'زمان ارسال؟'
]
```

### Custom Emoji List
```javascript
const myEmojis = ['😀', '😍', '👍', '🎉', '✅']
```

---

## 🎨 Styling

### Custom Colors
Override in your component:
```vue
<style scoped>
.chat-widget {
  /* Your custom styles */
}

.chat-fab {
  background: linear-gradient(135deg, #your-color-1, #your-color-2);
}
</style>
```

### Custom Positioning
```vue
<style scoped>
.chat-widget {
  bottom: 20px;
  right: 20px;  /* Change to left: 20px for LTR */
}
</style>
```

---

## 🔊 Notification Sounds

### Setup
1. Place sound file: `/public/sounds/notification.mp3`
2. Automatic playback on new messages
3. User can toggle in settings

### Custom Sound
```javascript
const audio = new Audio('/sounds/custom-sound.mp3')
audio.volume = 0.5
audio.play()
```

### Check Sound Preference
```javascript
const soundEnabled = localStorage.getItem('chatSoundEnabled') === 'true'
```

---

## 📱 Responsive Breakpoints

```scss
// Desktop
@media (min-width: 961px) { }

// Tablet
@media (max-width: 960px) { }

// Mobile
@media (max-width: 600px) { }
```

---

## 🐛 Debugging

### Check WebSocket Connection
```javascript
console.log('Connected:', chatStore.isConnected)
console.log('WebSocket:', chatStore.websocket)
```

### Check Authentication
```javascript
const authStore = useAuthStore()
console.log('Is Authenticated:', authStore.isAuthenticated)
console.log('Token:', authStore.token)
console.log('Guest Session:', chatStore.guestSessionId)
```

### Monitor Messages
```javascript
watch(() => chatStore.messages, (newMessages) => {
  console.log('Messages updated:', newMessages)
}, { deep: true })
```

---

## ⚡ Performance Tips

1. **Lazy Load**: Chat widget only loads when needed
2. **Debounce**: Typing indicators debounced to 3s
3. **Virtual Scrolling**: Consider for 1000+ messages
4. **Pagination**: Load old messages on demand
5. **Auto-refresh**: Rooms refresh every 30s (vendor) / 45s (admin)

---

## 🎯 Best Practices

### 1. Always Initialize Chat
```javascript
onMounted(() => {
  chatStore.initializeChat()
})

onUnmounted(() => {
  chatStore.disconnectWebSocket()
})
```

### 2. Handle Errors
```javascript
try {
  await chatStore.startChat(vendorId, productId)
} catch (error) {
  console.error('Chat error:', error)
  // Show error message to user
}
```

### 3. Clean Up Resources
```javascript
onUnmounted(() => {
  if (typingTimeout.value) {
    clearTimeout(typingTimeout.value)
  }
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})
```

### 4. Optimize Scroll
```javascript
const scrollToBottom = (smooth = true) => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTo({
        top: messagesContainer.value.scrollHeight,
        behavior: smooth ? 'smooth' : 'auto'
      })
    }
  })
}
```

---

## 🔐 Security Notes

1. **Authentication**: Always validate on backend
2. **Guest Sessions**: Expire after 24 hours
3. **Message Content**: Sanitize on backend
4. **Rate Limiting**: Implement on API
5. **WebSocket**: Use WSS in production

---

## 📖 API Endpoints

### Chat Endpoints
```
GET    /api/chat/rooms/              - List all rooms
POST   /api/chat/start/               - Start new chat
GET    /api/chat/rooms/:id/messages/ - Get messages
POST   /api/chat/rooms/:id/mark_read/ - Mark as read
POST   /api/chat/guest-session/      - Create guest session
POST   /api/chat/link-guest-session/ - Link guest to user
```

### Vendor Endpoints
```
GET    /api/chat/vendor/rooms/       - Vendor's rooms
```

### Admin Endpoints
```
GET    /api/chat/admin/rooms/        - All rooms (admin)
```

---

## 🎨 Customization Examples

### Custom Avatar Colors
```javascript
const getAvatarColor = (user) => {
  const colors = ['#FF5733', '#33FF57', '#3357FF']
  const index = user.id % colors.length
  return colors[index]
}
```

### Custom Date Format
```javascript
const formatDate = (date) => {
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}
```

### Custom Empty State
```vue
<template>
  <div class="empty-state">
    <v-icon size="100">mdi-chat</v-icon>
    <h2>{{ customMessage }}</h2>
  </div>
</template>
```

---

## 🚨 Common Issues

### WebSocket Not Connecting
1. Check API URL configuration
2. Verify authentication token
3. Check CORS settings
4. Verify WebSocket path

### Messages Not Updating
1. Check WebSocket connection
2. Verify room ID is correct
3. Check message handler
4. Inspect network tab

### Sound Not Playing
1. Check file exists at `/public/sounds/notification.mp3`
2. Verify browser allows audio
3. Check sound preference
4. Test in user interaction context

---

## 📚 Additional Resources

- Main Documentation: `/docs/features/CHAT_SYSTEM_README.md`
- UI/UX Improvements: `/docs/CHAT_UI_UX_IMPROVEMENTS.md`
- Sound Setup: `/public/sounds/README.md`

---

**Last Updated**: December 16, 2025

