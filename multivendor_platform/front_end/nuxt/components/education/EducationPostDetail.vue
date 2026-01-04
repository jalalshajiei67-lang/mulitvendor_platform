<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="900"
    scrollable
    fullscreen
    :scrim="false"
    transition="dialog-bottom-transition"
  >
    <v-card dir="rtl" class="education-post-detail">
      <v-card-title class="d-flex align-center justify-space-between pa-4 border-b">
        <h2 class="text-h6">مطالب آموزشی</h2>
        <v-btn
          icon="mdi-close"
          variant="text"
          @click="$emit('update:modelValue', false)"
        ></v-btn>
      </v-card-title>

      <v-card-text class="pa-0">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
          <p class="text-body-2 text-medium-emphasis mt-4">در حال بارگذاری...</p>
        </div>

        <!-- Error State -->
        <v-alert v-else-if="error" type="error" variant="tonal" class="ma-4">
          {{ error }}
        </v-alert>

        <!-- Post Content -->
        <div v-else-if="post" class="post-detail-content">
          <!-- Post Header -->
          <div class="post-header pa-6 border-b">
            <h1 class="text-h5 font-weight-bold mb-4">{{ post.title }}</h1>
            
            <div class="post-meta d-flex align-center flex-wrap gap-3">
              <span class="meta-item">
                <v-icon size="16" class="ml-1">mdi-account</v-icon>
                {{ post.author_name }}
              </span>
              <span class="meta-separator">|</span>
              <span class="meta-item">
                <v-icon size="16" class="ml-1">mdi-calendar</v-icon>
                {{ formatDate(post.created_at) }}
              </span>
              <span class="meta-separator">|</span>
              <span class="meta-item">
                <v-icon size="16" class="ml-1">mdi-eye</v-icon>
                {{ post.view_count }} بازدید
              </span>
              <span v-if="post.comment_count > 0" class="meta-separator">|</span>
              <span v-if="post.comment_count > 0" class="meta-item">
                <v-icon size="16" class="ml-1">mdi-comment-outline</v-icon>
                {{ post.comment_count }} نظر
              </span>
              <span class="meta-separator">|</span>
              <span class="meta-item">
                <v-icon size="16" class="ml-1">mdi-clock-outline</v-icon>
                {{ post.reading_time }} دقیقه مطالعه
              </span>
            </div>
          </div>

          <!-- Post Body -->
          <div class="post-body pa-6">
            <div class="post-content" v-html="post.content"></div>
          </div>

          <!-- Comments Section -->
          <div v-if="post.comments && post.comments.length > 0" class="comments-section pa-6 border-t">
            <h3 class="text-h6 mb-4">نظرات ({{ post.comment_count }})</h3>
            
            <div
              v-for="comment in post.comments"
              :key="comment.id"
              class="comment-item mb-4"
            >
              <div class="comment-header d-flex align-center mb-2">
                <strong class="comment-author">{{ comment.author_name }}</strong>
                <span class="comment-date text-caption text-medium-emphasis mr-2">
                  {{ formatDate(comment.created_at) }}
                </span>
              </div>
              <div class="comment-content text-body-2" v-html="comment.content"></div>
            </div>
          </div>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useEducationApi, type EducationPostDetail } from '~/composables/useEducationApi'

interface Props {
  modelValue: boolean
  postSlug: string | null
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'close': []
}>()

const educationApi = useEducationApi()
const post = ref<EducationPostDetail | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

const fetchPost = async () => {
  if (!props.postSlug) {
    post.value = null
    return
  }

  loading.value = true
  error.value = null

  try {
    post.value = await educationApi.getEducationPost(props.postSlug)
  } catch (err: any) {
    console.error('Error fetching education post:', err)
    error.value = err?.data?.detail || err?.message || 'خطا در بارگذاری مطلب'
    post.value = null
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

watch(() => props.postSlug, (newSlug) => {
  if (newSlug && props.modelValue) {
    fetchPost()
  }
})

watch(() => props.modelValue, (isOpen) => {
  if (isOpen && props.postSlug) {
    fetchPost()
  } else if (!isOpen) {
    emit('close')
  }
})
</script>

<style scoped>
.education-post-detail {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.post-detail-content {
  min-height: 100%;
}

.post-header {
  background-color: rgba(var(--v-theme-surface), 1);
}

.post-meta {
  font-size: 14px;
  color: rgb(var(--v-theme-on-surface-variant));
}

.meta-item {
  display: flex;
  align-items: center;
}

.meta-separator {
  color: rgb(var(--v-theme-on-surface-variant));
  opacity: 0.5;
}

.post-body {
  max-width: 100%;
}

.post-content {
  font-size: 16px;
  line-height: 1.8;
  color: rgb(var(--v-theme-on-surface));
}

.post-content :deep(h1),
.post-content :deep(h2),
.post-content :deep(h3),
.post-content :deep(h4) {
  margin-top: 24px;
  margin-bottom: 12px;
  font-weight: 600;
}

.post-content :deep(p) {
  margin-bottom: 16px;
}

.post-content :deep(ul),
.post-content :deep(ol) {
  margin-bottom: 16px;
  padding-right: 24px;
}

.post-content :deep(li) {
  margin-bottom: 8px;
}

.comments-section {
  background-color: rgba(var(--v-theme-surface), 0.5);
}

.comment-item {
  padding: 16px;
  background-color: rgba(var(--v-theme-surface), 1);
  border-radius: 8px;
}

.comment-author {
  color: rgb(var(--v-theme-primary));
}

.comment-content {
  color: rgb(var(--v-theme-on-surface));
  line-height: 1.6;
}

.border-b {
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

.border-t {
  border-top: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

@media (max-width: 600px) {
  .post-header,
  .post-body,
  .comments-section {
    padding: 16px;
  }
  
  .post-content {
    font-size: 15px;
  }
}
</style>

