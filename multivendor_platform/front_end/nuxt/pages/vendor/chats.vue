<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">گفتگوهای من</h1>
      </v-col>
    </v-row>

    <v-row>
      <!-- Chat Queue -->
      <v-col cols="12" md="4">
        <v-card height="700">
          <v-card-title class="bg-primary text-white">
            صف گفتگوها
            <v-chip
              v-if="unreadCount > 0"
              size="small"
              class="mr-2"
              color="error"
            >
              {{ unreadCount }} خوانده نشده
            </v-chip>
          </v-card-title>

          <v-card-text class="pa-0" style="height: calc(100% - 64px); overflow-y: auto;">
            <v-list v-if="!loading && rooms.length > 0">
              <v-list-item
                v-for="room in rooms"
                :key="room.room_id"
                @click="selectRoom(room)"
                :class="{
                  'bg-grey-lighten-3': selectedRoom?.room_id === room.room_id,
                  'bg-warning-lighten-5': room.unread_count > 0
                }"
              >
                <template #prepend>
                  <v-avatar color="primary" size="40">
                    {{ getInitials(room.other_participant) }}
                  </v-avatar>
                </template>

                <v-list-item-title>
                  {{ room.other_participant?.username || 'مشتری' }}
                  <v-chip
                    v-if="room.unread_count > 0"
                    size="x-small"
                    color="error"
                    class="mr-2"
                  >
                    {{ room.unread_count }}
                  </v-chip>
                </v-list-item-title>

                <v-list-item-subtitle v-if="room.product_name">
                  <v-icon size="small" class="ml-1">mdi-package-variant</v-icon>
                  {{ room.product_name }}
                </v-list-item-subtitle>

                <v-list-item-subtitle v-if="room.last_message">
                  {{ room.last_message.content.substring(0, 40) }}...
                </v-list-item-subtitle>

                <template #append>
                  <div class="text-caption text-grey">
                    {{ formatTime(room.updated_at) }}
                  </div>
                </template>
              </v-list-item>
            </v-list>

            <div v-else-if="loading" class="text-center pa-4">
              <v-progress-circular indeterminate color="primary" />
            </div>

            <div v-else class="text-center pa-4 text-grey">
              <v-icon size="64" color="grey-lighten-2">mdi-chat-outline</v-icon>
              <p class="mt-2">هنوز گفتگویی ندارید</p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Chat Conversation -->
      <v-col cols="12" md="8">
        <v-card v-if="selectedRoom" height="700">
          <v-card-title class="bg-grey-lighten-3 d-flex justify-space-between align-center">
            <div>
              <div class="font-weight-bold">
                {{ selectedRoom.other_participant?.username || 'مشتری' }}
              </div>
              <div v-if="selectedRoom.product_name" class="text-caption">
                درباره: {{ selectedRoom.product_name }}
              </div>
            </div>
            <div>
              <v-btn
                v-if="selectedRoom.product_id"
                size="small"
                variant="text"
                :to="`/products/${selectedRoom.product_id}`"
              >
                <v-icon class="ml-1">mdi-open-in-new</v-icon>
                مشاهده محصول
              </v-btn>
            </div>
          </v-card-title>

          <v-card-text class="pa-0">
            <ChatRoom :room-id="selectedRoom.room_id" @back="() => {}" />
          </v-card-text>
        </v-card>

        <v-card v-else height="700" class="d-flex align-center justify-center">
          <div class="text-center text-grey">
            <v-icon size="80" color="grey-lighten-2">mdi-chat-outline</v-icon>
            <p class="mt-4">یک گفتگو را انتخاب کنید</p>
            <p class="text-caption">مشتریان شما می‌توانند از صفحه محصول با شما گفتگو کنند</p>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Quick Stats -->
    <v-row class="mt-4">
      <v-col cols="12" md="4">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" color="primary" class="ml-3">mdi-chat</v-icon>
              <div>
                <div class="text-h5">{{ rooms.length }}</div>
                <div class="text-caption text-grey">کل گفتگوها</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" color="warning" class="ml-3">mdi-email-alert</v-icon>
              <div>
                <div class="text-h5">{{ unreadCount }}</div>
                <div class="text-caption text-grey">پیام‌های جدید</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" color="success" class="ml-3">mdi-clock-outline</v-icon>
              <div>
                <div class="text-h5">{{ activeToday }}</div>
                <div class="text-caption text-grey">فعال امروز</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Quick Response Templates (Optional) -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>پاسخ‌های سریع</v-card-title>
          <v-card-text>
            <v-chip-group>
              <v-chip
                v-for="(template, index) in quickResponses"
                :key="index"
                @click="useQuickResponse(template)"
              >
                {{ template }}
              </v-chip>
            </v-chip-group>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

definePageMeta({
  middleware: ['authenticated', 'vendor'],
  layout: 'default',
})

const rooms = ref<any[]>([])
const selectedRoom = ref<any>(null)
const loading = ref(true)

const quickResponses = ref([
  'سلام، چطور می‌تونم کمکتون کنم؟',
  'این محصول موجود هست',
  'زمان ارسال 2-3 روز کاری است',
  'برای اطلاعات بیشتر تماس بگیرید',
  'متشکرم از خریدتون',
])

const unreadCount = computed(() => {
  return rooms.value.reduce((sum, room) => sum + room.unread_count, 0)
})

const activeToday = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return rooms.value.filter(r => new Date(r.updated_at) >= today).length
})

const getInitials = (user: any) => {
  if (!user) return '?'
  const username = user.username || user.first_name || 'U'
  return username.charAt(0).toUpperCase()
}

const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return 'الان'
  if (minutes < 60) return `${minutes} دقیقه پیش`
  if (hours < 24) return `${hours} ساعت پیش`
  if (days < 7) return `${days} روز پیش`
  
  return date.toLocaleDateString('fa-IR')
}

const selectRoom = (room: any) => {
  selectedRoom.value = room
}

const useQuickResponse = (template: string) => {
  // TODO: Insert template into chat input
  console.log('Quick response:', template)
}

const fetchRooms = async () => {
  loading.value = true
  try {
    const data = await useApiFetch<any[]>('chat/vendor/rooms/')
    rooms.value = data
  } catch (error) {
    console.error('Failed to fetch rooms:', error)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchRooms()
  
  // Auto-refresh every 30 seconds
  setInterval(fetchRooms, 30000)
})
</script>

<style scoped>
.v-list-item {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  cursor: pointer;
  transition: background-color 0.2s;
}

.v-list-item:hover {
  background-color: rgba(0, 0, 0, 0.04);
}

.bg-warning-lighten-5 {
  background-color: #fff9c4 !important;
}
</style>

