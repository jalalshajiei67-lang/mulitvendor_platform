<template>
  <v-container fluid class="admin-chats-page">
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">مدیریت گفتگوها</h1>
      </v-col>
    </v-row>

    <v-row>
      <!-- Filters -->
      <v-col cols="12">
        <v-card>
          <v-card-text>
            <v-text-field
              v-model="searchQuery"
              placeholder="جستجو بر اساس نام کاربر یا محصول..."
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              @update:model-value="handleSearch"
            />
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Chat Rooms List -->
      <v-col cols="12" md="4">
        <v-card height="700">
          <v-card-title class="bg-primary text-white">
            لیست گفتگوها
            <v-chip size="small" class="mr-2" color="white" text-color="primary">
              {{ rooms.length }}
            </v-chip>
          </v-card-title>

          <v-card-text class="pa-0" style="height: calc(100% - 64px); overflow-y: auto;">
            <v-list v-if="!loading && rooms.length > 0">
              <v-list-item
                v-for="room in rooms"
                :key="room.room_id"
                @click="selectRoom(room)"
                :class="{ 'bg-grey-lighten-3': selectedRoom?.room_id === room.room_id }"
              >
                <v-list-item-title>
                  <v-chip size="x-small" color="primary" class="ml-2">
                    {{ room.unread_count }}
                  </v-chip>
                  {{ getRoomTitle(room) }}
                </v-list-item-title>

                <v-list-item-subtitle v-if="room.product_name">
                  <v-icon size="small" class="ml-1">mdi-package-variant</v-icon>
                  {{ room.product_name }}
                </v-list-item-subtitle>

                <v-list-item-subtitle v-if="room.last_message">
                  {{ room.last_message.content.substring(0, 50) }}...
                </v-list-item-subtitle>

                <template #append>
                  <div class="text-caption text-grey">
                    {{ formatDate(room.updated_at) }}
                  </div>
                </template>
              </v-list-item>
            </v-list>

            <div v-else-if="loading" class="text-center pa-4">
              <v-progress-circular indeterminate color="primary" />
            </div>

            <div v-else class="text-center pa-4 text-grey">
              گفتگویی یافت نشد
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Selected Chat -->
      <v-col cols="12" md="8">
        <v-card v-if="selectedRoom" height="700">
          <v-card-title class="bg-grey-lighten-3">
            <div>
              <div class="font-weight-bold">{{ getRoomTitle(selectedRoom) }}</div>
              <div v-if="selectedRoom.product_name" class="text-caption">
                محصول: {{ selectedRoom.product_name }}
              </div>
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
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Statistics -->
    <v-row class="mt-4">
      <v-col cols="12" md="3">
        <v-card>
          <v-card-text>
            <div class="text-h4 text-primary">{{ totalRooms }}</div>
            <div class="text-caption text-grey">کل گفتگوها</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card>
          <v-card-text>
            <div class="text-h4 text-warning">{{ totalUnread }}</div>
            <div class="text-caption text-grey">پیام‌های خوانده نشده</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card>
          <v-card-text>
            <div class="text-h4 text-success">{{ activeToday }}</div>
            <div class="text-caption text-grey">فعال امروز</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card>
          <v-card-text>
            <div class="text-h4 text-info">{{ totalMessages }}</div>
            <div class="text-caption text-grey">کل پیام‌ها</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

definePageMeta({
  middleware: ['authenticated', 'admin'],
  layout: 'default',
})

const searchQuery = ref('')
const rooms = ref<any[]>([])
const selectedRoom = ref<any>(null)
const loading = ref(true)

const totalRooms = computed(() => rooms.value.length)
const totalUnread = computed(() => rooms.value.reduce((sum, r) => sum + r.unread_count, 0))
const activeToday = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return rooms.value.filter(r => new Date(r.updated_at) >= today).length
})
const totalMessages = computed(() => {
  return rooms.value.reduce((sum, r) => {
    return sum + (r.last_message ? 1 : 0)
  }, 0)
})

const getRoomTitle = (room: any) => {
  const participants = room.participants_details || []
  return participants.map((p: any) => p.username).join(', ') || 'گفتگو'
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('fa-IR', { month: 'short', day: 'numeric' })
}

const selectRoom = (room: any) => {
  selectedRoom.value = room
}

const handleSearch = async () => {
  await fetchRooms()
}

const fetchRooms = async () => {
  loading.value = true
  try {
    const params = searchQuery.value ? `?search=${searchQuery.value}` : ''
    const data = await useApiFetch<any[]>(`chat/admin/rooms/${params}`)
    rooms.value = data
  } catch (error) {
    console.error('Failed to fetch rooms:', error)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchRooms()
})
</script>

<style scoped>
.admin-chats-page {
  padding-top: 80px;
}

@media (max-width: 960px) {
  .admin-chats-page {
    padding-top: 72px;
  }
}

@media (max-width: 600px) {
  .admin-chats-page {
    padding-top: 72px;
  }
}

.v-list-item {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  cursor: pointer;
}

.v-list-item:hover {
  background-color: rgba(0, 0, 0, 0.04);
}
</style>

