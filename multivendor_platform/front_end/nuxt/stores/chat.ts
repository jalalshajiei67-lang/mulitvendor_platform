import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface ChatMessage {
  id: string
  room_id: string
  sender: number | null
  sender_username: string
  content: string
  is_read: boolean
  created_at: string
}

interface ChatRoom {
  room_id: string
  participants: number[]
  participants_details: any[]
  product?: any
  product_name?: string
  product_id?: number
  guest_session?: string
  is_archived: boolean
  created_at: string
  updated_at: string
  last_message?: ChatMessage
  unread_count: number
  other_participant?: any
}

interface TypingStatus {
  room_id: string
  user_id: number | null
  username: string
  is_typing: boolean
}

export const useChatStore = defineStore('chat', () => {
  // State
  const rooms = ref<ChatRoom[]>([])
  const currentRoomId = ref<string | null>(null)
  const messages = ref<Record<string, ChatMessage[]>>({})
  const typingStatuses = ref<Record<string, TypingStatus[]>>({})
  const isConnected = ref(false)
  const websocket = ref<WebSocket | null>(null)
  const guestSessionId = ref<string | null>(null)
  const reconnectAttempts = ref(0)
  const maxReconnectAttempts = 5
  const reconnectTimeout = ref<NodeJS.Timeout | null>(null)
  const widgetOpen = ref(false)  // Track if chat widget should be open
  
  // Computed
  const currentRoom = computed(() => {
    if (!currentRoomId.value) return null
    return rooms.value.find(r => r.room_id === currentRoomId.value) || null
  })
  
  const currentMessages = computed(() => {
    if (!currentRoomId.value) return []
    return messages.value[currentRoomId.value] || []
  })
  
  const totalUnreadCount = computed(() => {
    return rooms.value.reduce((sum, room) => sum + room.unread_count, 0)
  })
  
  const currentTyping = computed(() => {
    if (!currentRoomId.value) return []
    return typingStatuses.value[currentRoomId.value] || []
  })
  
  // Actions
  const connectWebSocket = async () => {
    const authStore = useAuthStore()
    const config = useRuntimeConfig()
    
    // Debug auth state
    console.log('=== WebSocket Connection Attempt ===')
    console.log('Auth State:', {
      isAuthenticated: authStore.isAuthenticated,
      hasToken: !!authStore.token,
      token: authStore.token ? authStore.token.substring(0, 10) + '...' : null,
      user: authStore.user,
      guestSessionId: guestSessionId.value
    })
    
    // Determine WebSocket URL
    const apiBase = config.public.apiBase || ''
    let wsUrl = ''
    
    if (apiBase) {
      // Convert HTTP URL to WebSocket URL
      wsUrl = apiBase.replace('http://', 'ws://').replace('https://', 'wss://').replace('/api', '')
    } else {
      // Use current host
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      wsUrl = `${protocol}//${window.location.host}`
    }
    
    // Build connection URL with auth
    let connectionUrl = `${wsUrl}/ws/chat/?`
    
    // IMPORTANT: Use token if authenticated, guest session only for anonymous users
    if (authStore.isAuthenticated && authStore.token) {
      connectionUrl += `token=${authStore.token}`
      console.log('✅ Connecting WebSocket with user token')
    } else if (guestSessionId.value) {
      connectionUrl += `guest_session=${guestSessionId.value}`
      console.warn('⚠️ Connecting WebSocket with guest session (not logged in)')
    } else {
      console.error('❌ No authentication token or guest session available')
      return
    }
    
    console.log('WebSocket URL:', connectionUrl.replace(/token=.+/, 'token=***').replace(/guest_session=.+/, 'guest_session=***'))
    
    try {
      websocket.value = new WebSocket(connectionUrl)
      
      websocket.value.onopen = () => {
        console.log('WebSocket connected')
        isConnected.value = true
        reconnectAttempts.value = 0
      }
      
      websocket.value.onmessage = (event) => {
        handleWebSocketMessage(JSON.parse(event.data))
      }
      
      websocket.value.onerror = (error) => {
        console.error('WebSocket error:', error)
      }
      
      websocket.value.onclose = () => {
        console.log('WebSocket disconnected')
        isConnected.value = false
        attemptReconnect()
      }
    } catch (error) {
      console.error('Failed to connect WebSocket:', error)
    }
  }
  
  const disconnectWebSocket = () => {
    if (websocket.value) {
      websocket.value.close()
      websocket.value = null
    }
    isConnected.value = false
    
    if (reconnectTimeout.value) {
      clearTimeout(reconnectTimeout.value)
      reconnectTimeout.value = null
    }
  }
  
  const attemptReconnect = () => {
    if (reconnectAttempts.value >= maxReconnectAttempts) {
      console.error('Max reconnection attempts reached')
      return
    }
    
    reconnectAttempts.value++
    const delay = Math.min(1000 * Math.pow(2, reconnectAttempts.value), 30000)
    
    console.log(`Attempting to reconnect in ${delay}ms...`)
    reconnectTimeout.value = setTimeout(() => {
      connectWebSocket()
    }, delay)
  }
  
  const handleWebSocketMessage = (data: any) => {
    const { type } = data
    
    switch (type) {
      case 'connection_established':
        console.log('Chat connection established:', data)
        if (data.guest_session) {
          guestSessionId.value = data.guest_session
          if (process.client) {
            localStorage.setItem('chatGuestSession', data.guest_session)
          }
        }
        break
        
      case 'room_joined':
        console.log('Joined room:', data.room_id)
        break
        
      case 'message':
        handleIncomingMessage(data)
        break
        
      case 'typing':
        handleTypingStatus(data)
        break
        
      case 'read_receipt':
        handleReadReceipt(data)
        break
        
      case 'error':
        console.error('WebSocket error:', data.message)
        break
    }
  }
  
  const handleIncomingMessage = (data: any) => {
    const message: ChatMessage = {
      id: data.message_id,
      room_id: data.room_id,
      sender: data.sender,
      sender_username: data.sender_username,
      content: data.content,
      is_read: data.is_read,
      created_at: data.created_at,
    }
    
    // Add message to room
    if (!messages.value[data.room_id]) {
      messages.value[data.room_id] = []
    }
    messages.value[data.room_id].push(message)
    
    // Update room's last message
    const room = rooms.value.find(r => r.room_id === data.room_id)
    if (room) {
      room.last_message = message
      room.updated_at = data.created_at
      
      // Increment unread count if message is from someone else
      const authStore = useAuthStore()
      if (data.sender !== authStore.user?.id) {
        room.unread_count++
      }
    }
    
    // Sort rooms by last message time
    rooms.value.sort((a, b) => {
      return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
    })
  }
  
  const handleTypingStatus = (data: any) => {
    const { room_id, user_id, username, is_typing } = data
    
    if (!typingStatuses.value[room_id]) {
      typingStatuses.value[room_id] = []
    }
    
    const existingIndex = typingStatuses.value[room_id].findIndex(
      t => t.user_id === user_id
    )
    
    if (is_typing) {
      const status: TypingStatus = { room_id, user_id, username, is_typing }
      if (existingIndex >= 0) {
        typingStatuses.value[room_id][existingIndex] = status
      } else {
        typingStatuses.value[room_id].push(status)
      }
    } else {
      if (existingIndex >= 0) {
        typingStatuses.value[room_id].splice(existingIndex, 1)
      }
    }
  }
  
  const handleReadReceipt = (data: any) => {
    const { room_id } = data
    const room = rooms.value.find(r => r.room_id === room_id)
    if (room) {
      room.unread_count = 0
    }
  }
  
  const sendMessage = (roomId: string, content: string) => {
    if (!isConnected.value || !websocket.value) {
      console.error('WebSocket not connected')
      return
    }
    
    websocket.value.send(JSON.stringify({
      type: 'send_message',
      room_id: roomId,
      content,
    }))
  }
  
  const joinRoom = (roomId: string) => {
    if (!isConnected.value || !websocket.value) {
      console.error('WebSocket not connected')
      return
    }
    
    currentRoomId.value = roomId
    
    websocket.value.send(JSON.stringify({
      type: 'join_room',
      room_id: roomId,
    }))
  }
  
  const leaveRoom = (roomId: string) => {
    if (!isConnected.value || !websocket.value) {
      return
    }
    
    websocket.value.send(JSON.stringify({
      type: 'leave_room',
      room_id: roomId,
    }))
    
    if (currentRoomId.value === roomId) {
      currentRoomId.value = null
    }
  }
  
  const markAsRead = (roomId: string) => {
    if (!isConnected.value || !websocket.value) {
      return
    }
    
    websocket.value.send(JSON.stringify({
      type: 'mark_read',
      room_id: roomId,
    }))
    
    // Also mark via API
    useApiFetch(`chat/rooms/${roomId}/mark_read/`, {
      method: 'POST',
    }).catch(err => console.error('Failed to mark as read:', err))
  }
  
  const setTyping = (roomId: string, isTyping: boolean) => {
    if (!isConnected.value || !websocket.value) {
      return
    }
    
    websocket.value.send(JSON.stringify({
      type: 'typing',
      room_id: roomId,
      is_typing: isTyping,
    }))
  }
  
  const fetchRooms = async () => {
    try {
      const data = await useApiFetch<ChatRoom[]>('chat/rooms/')
      rooms.value = data
    } catch (error) {
      console.error('Failed to fetch chat rooms:', error)
    }
  }
  
  const fetchMessages = async (roomId: string) => {
    try {
      const data = await useApiFetch<{ results: ChatMessage[] }>(
        `chat/rooms/${roomId}/messages/`
      )
      messages.value[roomId] = data.results || []
    } catch (error) {
      console.error('Failed to fetch messages:', error)
    }
  }
  
  const startChat = async (vendorId: number, productId?: number, initialMessage?: string) => {
    try {
      const payload: any = {
        vendor_id: vendorId,
      }
      
      if (productId) {
        payload.product_id = productId
      }
      
      if (initialMessage) {
        payload.initial_message = initialMessage
      }
      
      // Include guest session if not authenticated
      const authStore = useAuthStore()
      if (!authStore.isAuthenticated && guestSessionId.value) {
        payload.guest_session_id = guestSessionId.value
        payload.identifier = 'web-browser'
      }
      
      console.log('Sending chat start request:', payload)
      
      const room = await useApiFetch<ChatRoom>('chat/start/', {
        method: 'POST',
        body: payload,
      })
      
      console.log('Chat room created/fetched:', room)
      
      // Add room to list if not already there
      const existingIndex = rooms.value.findIndex(r => r.room_id === room.room_id)
      if (existingIndex >= 0) {
        rooms.value[existingIndex] = room
      } else {
        rooms.value.unshift(room)
      }
      
      return room
    } catch (error: any) {
      console.error('Failed to start chat:', error)
      console.error('Error response:', error.data || error.response)
      throw error
    }
  }
  
  const createGuestSession = async () => {
    try {
      const identifier = process.client ? navigator.userAgent : 'unknown'
      const session = await useApiFetch<{ session_id: string }>('chat/guest-session/', {
        method: 'POST',
        body: { identifier },
      })
      
      guestSessionId.value = session.session_id
      if (process.client) {
        localStorage.setItem('chatGuestSession', session.session_id)
      }
      
      return session
    } catch (error) {
      console.error('Failed to create guest session:', error)
      throw error
    }
  }
  
  const linkGuestSession = async () => {
    const authStore = useAuthStore()
    if (!authStore.isAuthenticated || !guestSessionId.value) {
      return
    }
    
    try {
      await useApiFetch('chat/link-guest-session/', {
        method: 'POST',
        body: { guest_session_id: guestSessionId.value },
      })
      
      // Clear guest session after linking
      guestSessionId.value = null
      if (process.client) {
        localStorage.removeItem('chatGuestSession')
      }
      
      // Refresh rooms
      await fetchRooms()
    } catch (error) {
      console.error('Failed to link guest session:', error)
    }
  }
  
  const initializeChat = async () => {
    const authStore = useAuthStore()
    
    // Load guest session from localStorage if exists
    if (process.client && !authStore.isAuthenticated) {
      const storedGuestSession = localStorage.getItem('chatGuestSession')
      if (storedGuestSession) {
        guestSessionId.value = storedGuestSession
      }
    }
    
    // Connect WebSocket if authenticated or has guest session
    if (authStore.isAuthenticated || guestSessionId.value) {
      await connectWebSocket()
      if (authStore.isAuthenticated) {
        await fetchRooms()
      }
    }
  }
  
  const openRoom = (roomId: string) => {
    currentRoomId.value = roomId
    widgetOpen.value = true  // Open the widget
  }
  
  const closeWidget = () => {
    widgetOpen.value = false
    currentRoomId.value = null
  }
  
  const toggleWidget = () => {
    widgetOpen.value = !widgetOpen.value
  }
  
  return {
    // State
    rooms,
    currentRoomId,
    messages,
    typingStatuses,
    isConnected,
    guestSessionId,
    widgetOpen,
    
    // Computed
    currentRoom,
    currentMessages,
    totalUnreadCount,
    currentTyping,
    
    // Actions
    connectWebSocket,
    disconnectWebSocket,
    sendMessage,
    joinRoom,
    leaveRoom,
    markAsRead,
    setTyping,
    fetchRooms,
    fetchMessages,
    startChat,
    createGuestSession,
    linkGuestSession,
    initializeChat,
    openRoom,
    closeWidget,
    toggleWidget,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useChatStore, import.meta.hot))
}

