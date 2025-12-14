<template>
  <v-card
    v-if="task"
    elevation="3"
    rounded="xl"
    class="current-task-card"
    :class="{ 'required-task': task.is_required }"
  >
    <v-card-text class="pa-6 pa-md-8">
      <v-row align="center" class="ma-0">
        <!-- Task Icon -->
        <v-col cols="auto" class="pe-4">
          <v-avatar
            :color="task.is_required ? 'primary' : 'secondary'"
            size="80"
            variant="tonal"
          >
            <v-icon size="40" :color="task.is_required ? 'primary' : 'secondary'">
              {{ task.icon }}
            </v-icon>
          </v-avatar>
        </v-col>

        <!-- Task Content -->
        <v-col>
          <!-- Badge -->
          <v-chip
            v-if="task.is_required"
            size="small"
            color="error"
            variant="flat"
            class="mb-3"
            prepend-icon="mdi-alert-circle"
          >
            <span class="font-weight-bold">ضروری</span>
          </v-chip>
          <v-chip
            v-else
            size="small"
            color="success"
            variant="tonal"
            class="mb-3"
            prepend-icon="mdi-check-circle"
          >
            <span>اختیاری</span>
          </v-chip>

          <!-- Task Title -->
          <h2 class="text-h5 text-md-h4 font-weight-bold mb-3">
            {{ task.title }}
          </h2>

          <!-- Task Description -->
          <p class="text-body-1 text-md-h6 text-medium-emphasis mb-4">
            {{ task.description }}
          </p>

          <!-- Progress Indicator (if applicable) -->
          <div
            v-if="task.current_progress !== undefined && task.target_progress"
            class="mb-4"
          >
            <div class="d-flex justify-space-between align-center mb-2">
              <span class="text-body-2 font-weight-medium">
                پیشرفت: {{ task.current_progress }} از {{ task.target_progress }}
              </span>
              <span class="text-body-2 text-medium-emphasis">
                {{ progressPercentage }}%
              </span>
            </div>
            <v-progress-linear
              :model-value="progressPercentage"
              color="primary"
              height="8"
              rounded
            />
          </div>

          <!-- Action Buttons -->
          <div class="d-flex flex-column flex-sm-row gap-3 align-center">
            <v-btn
              :color="task.is_required ? 'primary' : 'secondary'"
              size="x-large"
              rounded="lg"
              elevation="2"
              class="flex-grow-1 flex-sm-grow-0"
              prepend-icon="mdi-arrow-left"
              @click="handleAction"
            >
              <span class="text-h6 font-weight-bold">شروع کنید</span>
            </v-btn>

            <!-- Points Badge -->
            <v-chip
              size="large"
              :color="task.is_required ? 'primary' : 'secondary'"
              variant="flat"
              class="px-4"
            >
              <v-icon start size="20">mdi-star</v-icon>
              <span class="text-h6 font-weight-bold">
                {{ task.points }} امتیاز
              </span>
            </v-chip>

            <!-- Help Button -->
            <v-btn
              v-if="helpText"
              icon="mdi-help-circle"
              variant="text"
              color="secondary"
              @click="showHelp = !showHelp"
            />
          </div>

          <!-- Help Section -->
          <v-expand-transition>
            <v-alert
              v-if="showHelp && helpText"
              type="info"
              variant="tonal"
              rounded="lg"
              class="mt-4"
              density="comfortable"
            >
              <div class="text-body-1">
                {{ helpText }}
              </div>
            </v-alert>
          </v-expand-transition>
        </v-col>
      </v-row>
    </v-card-text>

    <!-- Decorative Elements -->
    <div class="task-decoration" :class="{ 'required': task.is_required }"></div>
  </v-card>

  <!-- Empty State -->
  <v-card
    v-else
    elevation="2"
    rounded="xl"
    class="current-task-card empty-state"
    variant="tonal"
    color="success"
  >
    <v-card-text class="pa-6 pa-md-8 text-center">
      <v-avatar
        color="success"
        size="100"
        variant="tonal"
        class="mb-4"
      >
        <v-icon size="50" color="success">mdi-check-all</v-icon>
      </v-avatar>
      
      <h2 class="text-h5 text-md-h4 font-weight-bold mb-3">
        عالی! همه کارها انجام شده
      </h2>
      
      <p class="text-body-1 text-md-h6 text-medium-emphasis">
        شما همه مراحل ضروری را تکمیل کرده‌اید. به کار خود ادامه دهید!
      </p>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { CurrentTask } from '~/composables/useGamificationDashboard'

const props = defineProps<{
  task: CurrentTask | null
}>()

const emit = defineEmits<{
  (e: 'action', task: CurrentTask): void
}>()

const showHelp = ref(false)

const progressPercentage = computed(() => {
  if (!props.task?.current_progress || !props.task?.target_progress) return 0
  return Math.round((props.task.current_progress / props.task.target_progress) * 100)
})

const helpText = computed(() => {
  if (!props.task) return null
  
  const helpTexts: Record<string, string> = {
    profile: 'نام و نام خانوادگی، ایمیل و شماره تماس خود را در تب "پروفایل" وارد کنید. این اطلاعات برای ارتباط با مشتریان ضروری است.',
    mini_website: 'در بخش "شرکت من" نام فروشگاه، توضیحات کامل و تصویر بنر جذاب اضافه کنید. این صفحه اولین برداشت مشتری از شما است.',
    products: 'در بخش "محصولات" حداقل ۳ محصول با تصویر واضح، توضیحات کامل و قیمت مشخص اضافه کنید. محصولات با جزئیات بیشتر، فروش بهتری دارند.',
    team: 'در بخش "تیم" حداقل یک نفر از اعضای کلیدی تیم خود را با تصویر و سمت معرفی کنید. این به اعتبار شما کمک می‌کند.',
    portfolio: 'در تب "نمونه کارها" حداقل یک پروژه موفق خود را با تصویر و توضیحات کامل نمایش دهید. نمونه کارها اعتماد مشتریان را جلب می‌کند.',
    insights: 'تجربیات و نکات مفید خود در فروش یا کسب‌وکار را با سایر فروشندگان به اشتراک بگذارید. این به شما امتیاز می‌دهد و به دیگران کمک می‌کند.',
    invite: 'همکاران و فروشندگان دیگری که می‌شناسید را به پلتفرم دعوت کنید. برای هر دعوت موفق امتیاز ویژه دریافت می‌کنید.'
  }
  
  return helpTexts[props.task.type] || null
})

const handleAction = () => {
  if (props.task) {
    emit('action', props.task)
  }
}
</script>

<style scoped>
.current-task-card {
  position: relative;
  overflow: visible;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.current-task-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15) !important;
}

.current-task-card.required-task {
  border: 2px solid rgb(var(--v-theme-primary));
}

.task-decoration {
  position: absolute;
  top: 0;
  right: 0;
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, transparent 50%, rgba(var(--v-theme-secondary), 0.1) 50%);
  border-radius: 0 24px 0 0;
  pointer-events: none;
}

.task-decoration.required {
  background: linear-gradient(135deg, transparent 50%, rgba(var(--v-theme-primary), 0.1) 50%);
}

.empty-state {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Large font sizes for 40+ users */
.text-body-1 {
  font-size: 18px !important;
  line-height: 1.6 !important;
}

.text-h6 {
  font-size: 20px !important;
}

.text-h5 {
  font-size: 24px !important;
}

@media (min-width: 960px) {
  .text-md-h6 {
    font-size: 22px !important;
  }

  .text-md-h4 {
    font-size: 28px !important;
  }
}

@media (max-width: 600px) {
  .current-task-card .v-avatar {
    display: none;
  }

  .current-task-card .pa-6 {
    padding: 16px !important;
  }
}
</style>

