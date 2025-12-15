<template>
  <div class="task-list" dir="rtl">
    <v-card elevation="2" rounded="xl">
      <v-card-title class="d-flex align-center justify-space-between">
        <div class="d-flex align-center gap-3">
          <v-icon color="primary">mdi-checkbox-marked-circle-outline</v-icon>
          <span class="text-h6 font-weight-bold">یادآوری‌ها</span>
        </div>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="$emit('create')"
        >
          افزودن یادآوری
        </v-btn>
      </v-card-title>

      <v-card-text>
        <!-- Filters -->
        <div class="d-flex gap-2 mb-4 flex-wrap">
          <v-chip
            v-for="statusOption in statusOptions"
            :key="statusOption.value"
            :color="statusOption.color"
            :variant="filterStatus === statusOption.value ? 'flat' : 'outlined'"
            @click="filterStatus = statusOption.value"
            class="cursor-pointer"
          >
            {{ statusOption.title }}
          </v-chip>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-8">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </div>

        <!-- Tasks List -->
        <v-list v-else-if="filteredTasks.length > 0" lines="three">
          <v-list-item
            v-for="task in filteredTasks"
            :key="task.id"
            class="mb-2 rounded-lg"
            :class="{ 'task-overdue': task.is_overdue }"
          >
            <template v-slot:prepend>
              <v-avatar
                :color="getPriorityColor(task.priority)"
                size="48"
                variant="tonal"
              >
                <v-icon :color="getPriorityColor(task.priority)">
                  {{ getPriorityIcon(task.priority) }}
                </v-icon>
              </v-avatar>
            </template>

            <v-list-item-title class="font-weight-bold">
              {{ task.title }}
            </v-list-item-title>

            <v-list-item-subtitle>
              <div v-if="task.contact_name" class="mb-1">
                <v-icon size="small" class="me-1">mdi-account</v-icon>
                {{ task.contact_name }}
              </div>
              <div v-if="task.description" class="mb-1 text-body-2">
                {{ task.description }}
              </div>
              <div class="text-caption">
                <v-icon size="small" class="me-1">mdi-calendar-clock</v-icon>
                {{ formatDate(task.due_date) }}
              </div>
            </v-list-item-subtitle>

            <template v-slot:append>
              <div class="d-flex flex-column align-end gap-2">
                <v-chip
                  :color="getStatusColor(task.status)"
                  size="small"
                  variant="tonal"
                >
                  {{ task.status_display }}
                </v-chip>
                <v-chip
                  :color="getPriorityColor(task.priority)"
                  size="small"
                  variant="tonal"
                >
                  {{ task.priority_display }}
                </v-chip>
                <v-menu location="bottom end">
                  <template v-slot:activator="{ props }">
                    <v-btn icon="mdi-dots-vertical" variant="text" size="small" v-bind="props"></v-btn>
                  </template>
                  <v-list>
                    <v-list-item v-if="task.status === 'pending'" @click="$emit('complete', task)">
                      <template v-slot:prepend>
                        <v-icon color="success">mdi-check</v-icon>
                      </template>
                      <v-list-item-title>تکمیل</v-list-item-title>
                    </v-list-item>
                    <v-list-item v-if="task.status === 'pending'" @click="$emit('cancel', task)">
                      <template v-slot:prepend>
                        <v-icon color="warning">mdi-close</v-icon>
                      </template>
                      <v-list-item-title>لغو</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="$emit('edit', task)">
                      <template v-slot:prepend>
                        <v-icon>mdi-pencil</v-icon>
                      </template>
                      <v-list-item-title>ویرایش</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="$emit('delete', task)">
                      <template v-slot:prepend>
                        <v-icon color="error">mdi-delete</v-icon>
                      </template>
                      <v-list-item-title>حذف</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </div>
            </template>
          </v-list-item>
        </v-list>

        <!-- Empty State -->
        <div v-else class="text-center py-8">
          <v-icon size="80" color="grey-lighten-2">mdi-checkbox-blank-outline</v-icon>
          <h3 class="text-h6 mt-3">یادآوری وجود ندارد</h3>
          <p class="text-body-2 text-medium-emphasis mb-4">
            برای شروع، یک یادآوری جدید اضافه کنید
          </p>
          <v-btn color="primary" prepend-icon="mdi-plus" @click="$emit('create')">
            افزودن یادآوری
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { ContactTask } from '~/composables/useCrmApi'
import { formatDate } from '~/utils/date'

const emit = defineEmits<{
  create: []
  edit: [task: ContactTask]
  delete: [task: ContactTask]
  complete: [task: ContactTask]
  cancel: [task: ContactTask]
}>()

const filterStatus = ref<string | null>(null)

const statusOptions = [
  { title: 'همه', value: null, color: 'grey' },
  { title: 'در انتظار', value: 'pending', color: 'warning' },
  { title: 'تکمیل شده', value: 'completed', color: 'success' },
  { title: 'لغو شده', value: 'cancelled', color: 'error' }
]

const props = defineProps<{
  tasks: ContactTask[]
  loading?: boolean
}>()

const filteredTasks = computed(() => {
  if (!filterStatus.value) {
    return props.tasks
  }
  return props.tasks.filter(t => t.status === filterStatus.value)
})

const getPriorityColor = (priority: string) => {
  switch (priority) {
    case 'high': return 'error'
    case 'medium': return 'warning'
    case 'low': return 'info'
    default: return 'grey'
  }
}

const getPriorityIcon = (priority: string) => {
  switch (priority) {
    case 'high': return 'mdi-alert'
    case 'medium': return 'mdi-alert-circle'
    case 'low': return 'mdi-information'
    default: return 'mdi-circle'
  }
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'completed': return 'success'
    case 'cancelled': return 'error'
    case 'pending': return 'warning'
    default: return 'grey'
  }
}
</script>

<style scoped>
.task-list {
  width: 100%;
}

.task-overdue {
  border-right: 3px solid rgb(var(--v-theme-error));
}
</style>

