<template>
  <div class="insights-page">
    <!-- Header Section -->
    <v-card elevation="0" rounded="xl" class="insights-header mb-6" color="primary" variant="tonal">
      <div class="d-flex flex-column flex-sm-row align-center justify-space-between gap-4 pa-6">
        <div class="d-flex align-center gap-4">
          <v-avatar color="primary" size="56" class="elevation-2">
            <v-icon size="32" color="white">mdi-lightbulb-on</v-icon>
          </v-avatar>
          <div>
            <div class="text-h5 font-weight-bold mb-1">بینش‌های عمومی فروشندگان</div>
            <div class="text-body-2 text-medium-emphasis">
              تجربه‌ها و نکات خود را به صورت عمومی با خریداران به اشتراک بگذارید
            </div>
          </div>
        </div>
        <v-btn
          color="primary"
          variant="flat"
          prepend-icon="mdi-refresh"
          @click="$emit('refresh')"
          :loading="loading"
          size="large"
          rounded="lg"
          class="refresh-btn"
        >
          به‌روزرسانی
        </v-btn>
      </div>
    </v-card>

    <!-- Error Alert -->
    <v-alert
      v-if="error"
      type="error"
      variant="tonal"
      rounded="lg"
      class="mb-6"
      closable
    >
      {{ error }}
    </v-alert>

    <!-- Create Insight Form -->
    <v-card 
      elevation="2" 
      rounded="xl" 
      class="create-insight-card mb-6"
      :class="{ 'creating': creating }"
    >
      <div class="pa-6">
        <div class="d-flex align-center gap-3 mb-4">
          <v-icon color="primary" size="28">mdi-pencil-outline</v-icon>
          <div class="d-flex flex-column">
            <div class="text-h6 font-weight-bold">ارسال بینش عمومی جدید</div>
            <div class="text-caption text-medium-emphasis">
              این محتوا به صورت عمومی برای خریداران نمایش داده می‌شود
            </div>
          </div>
        </div>
        
        <v-row class="gy-4">
          <v-col cols="12">
            <v-text-field
              v-model="title"
              label="عنوان کوتاه"
              variant="outlined"
              density="comfortable"
              :disabled="creating"
              :rules="[requiredRule]"
              hide-details="auto"
              prepend-inner-icon="mdi-format-title"
              color="primary"
              rounded="lg"
            />
          </v-col>
          <v-col cols="12">
            <div class="d-flex flex-column gap-2">
              <div class="d-flex align-center justify-space-between">
                <label class="text-caption text-medium-emphasis">
                  محتوای بینش (قابل مشاهده برای خریداران)
                </label>
                <v-chip size="x-small" color="info" variant="tonal" class="ms-2">
                  <v-icon start size="12">mdi-eye</v-icon>
                  عمومی
                </v-chip>
              </div>
              <SimpleTiptapEditor
                v-model="content"
                :disabled="creating"
                placeholder="تجربه، نکات و راهنمایی‌های خود را برای خریداران بنویسید..."
                min-height="150px"
              />
              <div v-if="!contentIsValid" class="text-caption text-error">
                محتوای بینش الزامی است
              </div>
            </div>
          </v-col>
          <v-col cols="12">
            <div class="d-flex flex-column flex-sm-row align-center justify-space-between gap-3">
              <div class="d-flex flex-column gap-1">
                <div class="d-flex align-center gap-2 text-caption text-medium-emphasis">
                  <v-icon size="16" color="info">mdi-information-outline</v-icon>
                  <span>محتوای کاربردی و مشخص بنویسید تا برای خریداران مفید باشد</span>
                </div>
                <div class="d-flex align-center gap-2 text-caption text-warning">
                  <v-icon size="14" color="warning">mdi-alert-circle-outline</v-icon>
                  <span>این محتوا به صورت عمومی منتشر می‌شود و برای همه خریداران قابل مشاهده است</span>
                </div>
              </div>
              <v-btn
                color="primary"
                variant="flat"
                prepend-icon="mdi-send"
                :disabled="!canSubmit || creating"
                :loading="creating"
                @click="handleSubmit"
                size="large"
                rounded="lg"
                class="submit-btn"
              >
                انتشار بینش عمومی
              </v-btn>
            </div>
          </v-col>
        </v-row>
      </div>
    </v-card>

    <!-- Loading State -->
    <div v-if="loading" class="insights-loading">
      <v-row class="gy-4">
        <v-col
          v-for="i in 3"
          :key="i"
          cols="12"
        >
          <v-card elevation="1" rounded="xl" class="pa-4">
            <v-skeleton-loader type="list-item-avatar-two-line, actions"></v-skeleton-loader>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Empty State -->
    <v-card
      v-else-if="!insights?.length"
      elevation="0"
      rounded="xl"
      class="empty-state text-center pa-8"
      color="surface-variant"
    >
      <v-icon size="80" color="grey-lighten-1" class="mb-4">mdi-lightbulb-outline</v-icon>
      <div class="text-h6 font-weight-bold mb-2">هنوز بینشی ثبت نشده است</div>
      <div class="text-body-2 text-medium-emphasis mb-3">
        اولین نفر باشید که تجربه و نکات خود را با خریداران به اشتراک می‌گذارد!
      </div>
      <v-chip size="small" color="info" variant="tonal">
        <v-icon start size="14">mdi-eye</v-icon>
        بینش‌های شما به صورت عمومی برای خریداران نمایش داده می‌شود
      </v-chip>
    </v-card>

    <!-- Insights Feed -->
    <div v-else class="insights-feed">
      <v-row class="gy-4">
        <v-col
          v-for="item in insights"
          :key="item.id"
          cols="12"
        >
          <v-card
            elevation="1"
            rounded="xl"
            class="insight-card"
            :class="{ 'liked': item.liked_by_me }"
            hover
          >
            <v-card-text class="pa-6">
              <!-- Insight Header -->
              <div class="d-flex align-start gap-4 mb-4">
                <v-avatar 
                  color="primary" 
                  variant="tonal" 
                  size="48"
                  class="insight-avatar"
                >
                  <v-icon color="primary">mdi-lightbulb-on-outline</v-icon>
                </v-avatar>
                <div class="flex-grow-1">
                  <div class="d-flex flex-column flex-sm-row align-start justify-space-between gap-2 mb-2">
                    <div class="d-flex align-center gap-2 flex-wrap">
                      <div class="text-h6 font-weight-bold insight-title">
                        {{ item.title }}
                      </div>
                      <v-chip size="x-small" color="info" variant="tonal" class="insight-public-badge">
                        <v-icon start size="12">mdi-eye</v-icon>
                        عمومی
                      </v-chip>
                    </div>
                    <div class="d-flex align-center gap-2 text-caption text-medium-emphasis">
                      <v-icon size="14">mdi-clock-outline</v-icon>
                      <span>{{ formatDate(item.created_at) }}</span>
                    </div>
                  </div>
                  <div class="d-flex align-center gap-2 mb-3">
                    <v-icon size="16" color="primary">mdi-account-circle-outline</v-icon>
                    <span class="text-body-2 font-weight-medium">{{ item.author_name || 'فروشنده' }}</span>
                    <v-divider vertical class="mx-2" style="height: 16px;"></v-divider>
                    <span class="text-caption text-medium-emphasis">
                      قابل مشاهده برای خریداران
                    </span>
                  </div>
                </div>
              </div>

              <!-- Insight Content -->
              <div 
                class="insight-content text-body-1 mb-4"
                v-html="item.content"
              ></div>

              <!-- Insight Actions -->
              <div class="d-flex flex-wrap align-center gap-2 pt-4 border-t">
                <v-btn
                  variant="text"
                  :color="item.liked_by_me ? 'primary' : 'grey-darken-1'"
                  :prepend-icon="item.liked_by_me ? 'mdi-thumb-up' : 'mdi-thumb-up-outline'"
                  @click="$emit('like', item.id)"
                  :disabled="creating"
                  size="small"
                  rounded="lg"
                  class="action-btn"
                >
                  <span class="font-weight-medium">{{ item.likes_count || 0 }}</span>
                </v-btn>
                <v-btn
                  variant="text"
                  color="grey-darken-1"
                  prepend-icon="mdi-comment-outline"
                  @click="toggleComments(item.id)"
                  size="small"
                  rounded="lg"
                  class="action-btn"
                >
                  <span class="font-weight-medium">دیدگاه</span>
                  <v-chip
                    v-if="commentsCount(item)"
                    size="x-small"
                    color="primary"
                    variant="flat"
                    class="ms-1"
                  >
                    {{ commentsCount(item) }}
                  </v-chip>
                </v-btn>
              </div>

              <!-- Comments Section -->
              <v-expand-transition>
                <div v-if="expandedComments[item.id]" class="comments-section mt-4 pt-4 border-t">
                  <div class="d-flex align-center justify-space-between mb-4">
                    <div class="d-flex align-center gap-2">
                      <v-icon color="primary" size="20">mdi-comment-multiple-outline</v-icon>
                      <span class="text-subtitle-2 font-weight-bold">دیدگاه‌ها</span>
                    </div>
                    <v-chip size="x-small" color="info" variant="tonal">
                      <v-icon start size="12">mdi-eye</v-icon>
                      عمومی
                    </v-chip>
                  </div>

                  <v-alert
                    v-if="commentsError(item.id)"
                    type="error"
                    variant="tonal"
                    rounded="lg"
                    class="mb-4"
                    density="compact"
                  >
                    {{ commentsError(item.id) }}
                  </v-alert>

                  <template v-else>
                    <v-skeleton-loader
                      v-if="commentsLoading(item.id)"
                      type="list-item-avatar-two-line"
                      class="rounded-lg mb-3"
                    />

                    <div v-else>
                      <div v-if="!commentsFor(item.id).length" class="text-center py-6">
                        <v-icon size="48" color="grey-lighten-1" class="mb-2">mdi-comment-outline</v-icon>
                        <div class="text-body-2 text-medium-emphasis mb-2">
                          هنوز دیدگاهی ثبت نشده است. اولین دیدگاه را شما بنویسید!
                        </div>
                        <div class="text-caption text-medium-emphasis">
                          دیدگاه‌ها به صورت عمومی برای خریداران نمایش داده می‌شود
                        </div>
                      </div>
                      <div v-else class="comments-list mb-4">
                        <v-card
                          v-for="comment in commentsFor(item.id)"
                          :key="comment.id"
                          elevation="0"
                          rounded="lg"
                          class="comment-card mb-3"
                          color="surface-variant"
                        >
                          <v-card-text class="pa-4">
                            <div class="d-flex align-start gap-3">
                              <v-avatar color="secondary" variant="tonal" size="36">
                                <v-icon size="18">mdi-account</v-icon>
                              </v-avatar>
                              <div class="flex-grow-1">
                                <div class="d-flex align-center justify-space-between mb-2">
                                  <span class="text-body-2 font-weight-bold">
                                    {{ comment.author_name || 'فروشنده' }}
                                  </span>
                                  <span class="text-caption text-medium-emphasis">
                                    {{ formatDate(comment.created_at) }}
                                  </span>
                                </div>
                                <div class="text-body-2 text-high-emphasis">
                                  {{ comment.content }}
                                </div>
                              </div>
                            </div>
                          </v-card-text>
                        </v-card>
                      </div>
                    </div>
                  </template>

                  <!-- Add Comment Form -->
                  <v-card elevation="0" rounded="lg" class="add-comment-card" color="surface-variant">
                    <v-card-text class="pa-4">
                      <div class="d-flex align-center gap-2 mb-2">
                        <v-icon size="16" color="info">mdi-information-outline</v-icon>
                        <span class="text-caption text-medium-emphasis">
                          دیدگاه شما به صورت عمومی نمایش داده می‌شود
                        </span>
                      </div>
                      <v-textarea
                        v-model="commentInputs[item.id]"
                        label="نظر خود را بنویسید..."
                        variant="outlined"
                        density="comfortable"
                        rows="2"
                        auto-grow
                        hide-details="auto"
                        color="primary"
                        rounded="lg"
                      />
                      <div class="d-flex justify-end mt-3">
                        <v-btn
                          color="primary"
                          variant="flat"
                          prepend-icon="mdi-send"
                          :disabled="!commentInputs[item.id]?.trim() || commentsLoading(item.id)"
                          @click="handleSubmitComment(item.id)"
                          rounded="lg"
                        >
                          ارسال دیدگاه عمومی
                        </v-btn>
                      </div>
                    </v-card-text>
                  </v-card>
                </div>
              </v-expand-transition>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { SellerInsight } from '~/composables/useGamification'
import SimpleTiptapEditor from './SimpleTiptapEditor.vue'

interface InsightComment {
  id: number
  content: string
  author_name?: string
  created_at?: string
}

const props = defineProps<{
  insights: SellerInsight[]
  loading?: boolean
  creating?: boolean
  error?: string | null
  comments?: Record<number, InsightComment[]>
  commentsLoading?: Record<number, boolean>
  commentsError?: Record<number, string | null>
}>()

const emit = defineEmits<{
  (e: 'refresh'): void
  (e: 'submit', payload: { title: string; content: string }): void
  (e: 'like', id: number): void
  (e: 'load-comments', id: number): void
  (e: 'submit-comment', payload: { id: number; content: string }): void
}>()

const title = ref('')
const content = ref('')
const pendingReset = ref(false)
const expandedComments = ref<Record<number, boolean>>({})
const commentInputs = ref<Record<number, string>>({})

const requiredRule = (value: string) => !!value?.trim() || 'الزامی'

// Helper function to strip HTML tags and check if there's actual text content
const stripHtmlTags = (html: string): string => {
  if (!html) return ''
  if (process.client) {
    const tmp = document.createElement('div')
    tmp.innerHTML = html
    return tmp.textContent || tmp.innerText || ''
  }
  // SSR fallback: simple regex to remove HTML tags
  return html.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim()
}

const contentIsValid = computed(() => {
  const textContent = stripHtmlTags(content.value)
  return textContent.trim().length > 0
})

const canSubmit = computed(() => {
  return Boolean(title.value.trim() && contentIsValid.value)
})

const commentsFor = (id: number) => props.comments?.[id] || []
const commentsLoading = (id: number) => !!props.commentsLoading?.[id]
const commentsError = (id: number) => props.commentsError?.[id] || null
const commentsCount = (item: SellerInsight) => {
  const fromList = item.comments_count ?? 0
  const loadedCount = commentsFor(item.id).length
  return Math.max(fromList, loadedCount)
}

const toggleComments = (id: number) => {
  expandedComments.value[id] = !expandedComments.value[id]
  if (expandedComments.value[id] && !props.comments?.[id]) {
    emit('load-comments', id)
  }
}

const handleSubmit = () => {
  if (!canSubmit.value) return
  emit('submit', { title: title.value.trim(), content: content.value.trim() })
  pendingReset.value = true
  if (!props.creating) {
    resetForm()
  }
}

const handleSubmitComment = (id: number) => {
  const text = (commentInputs.value[id] || '').trim()
  if (!text) return
  emit('submit-comment', { id, content: text })
  commentInputs.value[id] = ''
}

const resetForm = () => {
  title.value = ''
  content.value = ''
  pendingReset.value = false
}

watch(
  () => props.creating,
  (newVal, oldVal) => {
    if (oldVal && !newVal && pendingReset.value) {
      resetForm()
    }
  }
)

const formatDate = (value?: string) => {
  if (!value) return ''
  try {
    return new Intl.DateTimeFormat('fa-IR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    }).format(new Date(value))
  } catch (error) {
    return ''
  }
}
</script>

<style scoped>
.insights-page {
  max-width: 100%;
}

/* Header Styles */
.insights-header {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.1) 0%, rgba(var(--v-theme-primary), 0.05) 100%);
  border: 1px solid rgba(var(--v-theme-primary), 0.2);
}

@media (max-width: 600px) {
  .insights-header {
    padding: 1rem !important;
  }
  
  .insights-header .refresh-btn {
    width: 100%;
  }
}

/* Create Insight Card */
.create-insight-card {
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.create-insight-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.2);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.create-insight-card.creating {
  opacity: 0.7;
  pointer-events: none;
}

@media (max-width: 600px) {
  .create-insight-card {
    padding: 1rem !important;
  }
  
  .create-insight-card .submit-btn {
    width: 100%;
  }
}

/* Empty State */
.empty-state {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* Insights Feed */
.insights-feed {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Insight Card */
.insight-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.insight-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
  border-color: rgba(var(--v-theme-primary), 0.3);
}

.insight-card.liked {
  border-color: rgba(var(--v-theme-primary), 0.4);
  background: linear-gradient(to left, rgba(var(--v-theme-primary), 0.02), transparent);
}

.insight-avatar {
  flex-shrink: 0;
}

.insight-title {
  color: rgba(var(--v-theme-on-surface), 0.9);
  line-height: 1.4;
}

.insight-public-badge {
  flex-shrink: 0;
}

.insight-content {
  color: rgba(var(--v-theme-on-surface), 0.8);
  line-height: 1.7;
  word-wrap: break-word;
}

.insight-content :deep(p) {
  margin: 0.5em 0;
}

.insight-content :deep(ul),
.insight-content :deep(ol) {
  padding-right: 1.5em;
  margin: 0.5em 0;
}

.insight-content :deep(li) {
  margin: 0.25em 0;
}

.insight-content :deep(blockquote) {
  border-right: 3px solid rgba(var(--v-theme-primary), 0.5);
  padding-right: 1em;
  margin: 1em 0;
  font-style: italic;
  color: rgba(var(--v-theme-on-surface), 0.7);
}

.insight-content :deep(h2) {
  font-size: 1.3em;
  font-weight: bold;
  margin: 1em 0 0.5em 0;
  line-height: 1.3;
}

.insight-content :deep(h3) {
  font-size: 1.1em;
  font-weight: bold;
  margin: 0.75em 0 0.5em 0;
  line-height: 1.3;
}

.insight-content :deep(strong) {
  font-weight: bold;
}

.insight-content :deep(em) {
  font-style: italic;
}

.action-btn {
  transition: all 0.2s ease;
}

.action-btn:hover {
  transform: scale(1.05);
}

/* Comments Section */
.comments-section {
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
  }
  to {
    opacity: 1;
    max-height: 1000px;
  }
}

.comment-card {
  transition: all 0.2s ease;
}

.comment-card:hover {
  transform: translateX(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.add-comment-card {
  transition: all 0.2s ease;
}

.add-comment-card:focus-within {
  border-color: rgba(var(--v-theme-primary), 0.3);
  box-shadow: 0 0 0 3px rgba(var(--v-theme-primary), 0.1);
}

/* Loading State */
.insights-loading {
  animation: fadeIn 0.3s ease-in;
}

/* Responsive Adjustments */
@media (max-width: 960px) {
  .insight-card {
    padding: 1rem !important;
  }
  
  .insight-title {
    font-size: 1.1rem;
  }
  
  .insight-content {
    font-size: 0.95rem;
  }
}

@media (max-width: 600px) {
  .insights-page {
    padding: 0;
  }
  
  .insight-card :deep(.v-card-text) {
    padding: 1rem !important;
  }
  
  .insight-card .d-flex.gap-4 {
    gap: 0.75rem !important;
  }
  
  .insight-avatar {
    width: 40px !important;
    height: 40px !important;
  }
  
  .action-btn {
    flex: 1;
    min-width: 0;
  }
  
  .comments-section {
    padding-top: 1rem !important;
  }
  
  .comment-card {
    margin-bottom: 0.75rem !important;
  }
  
  .add-comment-card :deep(.v-btn) {
    width: 100%;
  }
}

/* RTL Specific Adjustments */
[dir="rtl"] .insight-card:hover {
  transform: translateY(-4px) translateX(4px);
}

[dir="rtl"] .comment-card:hover {
  transform: translateX(4px);
}

/* Print Styles */
@media print {
  .create-insight-card,
  .refresh-btn,
  .action-btn,
  .add-comment-card {
    display: none;
  }
  
  .insight-card {
    break-inside: avoid;
    page-break-inside: avoid;
  }
}
</style>


