<template>
  <v-container fluid dir="rtl" class="create-auction-page">
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-card elevation="2" rounded="xl">
          <v-card-title class="text-h5 pa-4 pa-md-6">
            <v-icon start>mdi-gavel</v-icon>
            ایجاد مناقصه جدید
          </v-card-title>
          <v-divider></v-divider>

          <v-card-text class="pa-4 pa-md-6">
            <v-alert
              v-if="successMessage"
              type="success"
              variant="tonal"
              class="mb-4"
              closable
              @click:close="successMessage = ''"
            >
              {{ successMessage }}
            </v-alert>

            <v-alert
              v-if="errorMessage"
              type="error"
              variant="tonal"
              class="mb-4"
              closable
              @click:close="errorMessage = ''"
            >
              {{ errorMessage }}
            </v-alert>

            <v-form ref="formRef" v-model="valid">
              <v-text-field
                v-model="formData.title"
                label="عنوان مناقصه"
                :rules="[rules.required]"
                variant="outlined"
                required
                class="mb-4"
              ></v-text-field>

              <div class="mb-4">
                <label class="text-body-2 mb-2 d-block">توضیحات</label>
                <TiptapEditor
                  v-model="formData.description"
                  :placeholder="'توضیحات کامل درخواست را وارد کنید'"
                />
              </div>

              <v-select
                v-model="formData.category"
                :items="categories"
                item-title="name"
                item-value="id"
                label="دسته‌بندی"
                :rules="[rules.required]"
                variant="outlined"
                required
                class="mb-4"
              ></v-select>

              <v-text-field
                v-model.number="formData.starting_price"
                label="قیمت شروع (تومان)"
                type="number"
                :rules="[
                  rules.required,
                  v => !v || v > 0 || 'قیمت باید بیشتر از صفر باشد'
                ]"
                variant="outlined"
                required
                class="mb-4"
                prepend-inner-icon="mdi-currency-usd"
              ></v-text-field>

              <v-text-field
                v-model.number="formData.reserve_price"
                label="قیمت رزرو (اختیاری - تومان)"
                type="number"
                hint="حداقل قیمت پنهان که در صورت پیشنهاد کمتر از آن، قرارداد تضمین می‌شود"
                persistent-hint
                variant="outlined"
                class="mb-4"
                prepend-inner-icon="mdi-lock"
              ></v-text-field>

              <v-text-field
                v-model.number="formData.minimum_decrement"
                label="حداقل کاهش قیمت (تومان)"
                type="number"
                :rules="[
                  rules.required,
                  v => !v || v > 0 || 'مقدار باید بیشتر از صفر باشد'
                ]"
                hint="حداقل مبلغی که هر پیشنهاد باید از پیشنهاد قبلی کمتر باشد"
                persistent-hint
                variant="outlined"
                required
                class="mb-4"
              ></v-text-field>

              <div class="mb-4">
                <label class="text-body-2 mb-2 d-block">مهلت پایان مناقصه</label>
                <PersianDatePicker
                  v-model="deadlineDate"
                  label="تاریخ"
                  :rules="[rules.required, rules.futureDate]"
                  class="mb-2"
                  required
                />
                <v-text-field
                  v-model="deadlineTime"
                  label="ساعت"
                  type="time"
                  :rules="[rules.required, rules.futureTime]"
                  variant="outlined"
                  required
                  prepend-inner-icon="mdi-clock-outline"
                ></v-text-field>
              </div>
            </v-form>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions class="pa-4 pa-md-6">
            <v-spacer></v-spacer>
            <v-btn
              variant="outlined"
              @click="$router.back()"
            >
              انصراف
            </v-btn>
            <v-btn
              color="primary"
              :loading="loading"
              :disabled="!valid"
              @click="submitForm"
            >
              ایجاد مناقصه
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuctionApi } from '~/composables/useAuctionApi'
import { useCategoryApi } from '~/composables/useCategoryApi'
import { useToast } from '~/composables/useToast'
import PersianDatePicker from '~/components/common/PersianDatePicker.vue'

definePageMeta({
  middleware: 'authenticated'
})

const router = useRouter()
const { createAuction } = useAuctionApi()
const { getCategories } = useCategoryApi()
const { showToast } = useToast()

const formRef = ref()
const valid = ref(false)
const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const categories = ref<any[]>([])
const deadlineDate = ref<string | null>(null)
const deadlineTime = ref('')

const rules = {
  required: (value: any) => !!value || 'این فیلد الزامی است',
  futureDate: (value: string | null) => {
    if (!value) return true // Let required rule handle empty values
    try {
      const [year, month, day] = value.split('-').map(Number)
      const selectedDate = new Date(year, month - 1, day)
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      selectedDate.setHours(0, 0, 0, 0)
      
      if (selectedDate < today) {
        return 'تاریخ باید امروز یا آینده باشد'
      }
      return true
    } catch {
      return true // Let other validation handle invalid format
    }
  },
  futureTime: (value: string) => {
    if (!value) return true // Let required rule handle empty values
    if (!deadlineDate.value) return true // Date validation will handle this
    
    try {
      const [year, month, day] = deadlineDate.value.split('-').map(Number)
      const [hours, minutes] = value.split(':').map(Number)
      const selectedDateTime = new Date(year, month - 1, day, hours, minutes, 0)
      const now = new Date()
      
      if (selectedDateTime <= now) {
        return 'زمان باید در آینده باشد'
      }
      return true
    } catch {
      return true // Let other validation handle invalid format
    }
  }
}

const formData = ref({
  title: '',
  description: '',
  category: null as number | null,
  starting_price: null as number | null,
  reserve_price: null as number | null,
  minimum_decrement: null as number | null
})

const deadline = computed(() => {
  if (!deadlineDate.value || !deadlineTime.value) {
    return null
  }
  
  try {
    // PersianDatePicker returns Gregorian date in format YYYY-MM-DD
    // Combine with time to create ISO datetime string
    // Use local timezone to avoid timezone conversion issues
    const [year, month, day] = deadlineDate.value.split('-').map(Number)
    const [hours, minutes] = deadlineTime.value.split(':').map(Number)
    
    // Create date in local timezone
    const date = new Date(year, month - 1, day, hours, minutes, 0)
    
    // Validate the date is valid
    if (isNaN(date.getTime())) {
      return null
    }
    
    // Return ISO string (will be in UTC, but we preserve the intended local time)
    return date.toISOString()
  } catch (error) {
    console.error('Error parsing deadline:', error)
    return null
  }
})

onMounted(async () => {
  try {
    const response = await getCategories()
    categories.value = response.results || response || []
  } catch (error: any) {
    console.error('Error loading categories:', error)
    errorMessage.value = 'خطا در بارگذاری دسته‌بندی‌ها'
  }
})

const submitForm = async () => {
  // Validate form fields
  const { valid: isValid } = await formRef.value.validate()
  if (!isValid) {
    errorMessage.value = 'لطفا تمام فیلدهای الزامی را پر کنید'
    return
  }

  // Validate date and time separately
  if (!deadlineDate.value) {
    errorMessage.value = 'لطفا تاریخ پایان را انتخاب کنید'
    return
  }

  if (!deadlineTime.value) {
    errorMessage.value = 'لطفا ساعت پایان را وارد کنید'
    return
  }

  // Build deadline datetime
  if (!deadline.value) {
    errorMessage.value = 'تاریخ و ساعت وارد شده معتبر نیست'
    return
  }

  // Check if deadline is in the future
  const now = new Date()
  const deadlineDateObj = new Date(deadline.value)
  if (deadlineDateObj <= now) {
    errorMessage.value = 'مهلت پایان باید در آینده باشد'
    return
  }

  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const data = {
      ...formData.value,
      deadline: deadline.value
    }
    
    const response = await createAuction(data)
    showToast('مناقصه با موفقیت ایجاد شد', 'success')
    router.push(`/buyer/auctions/${response.id}`)
  } catch (error: any) {
    console.error('Error creating auction:', error)
    errorMessage.value = error.data?.error || error.message || 'خطا در ایجاد مناقصه'
    showToast(errorMessage.value, 'error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.create-auction-page {
  min-height: 100vh;
  padding-top: 2rem;
  padding-bottom: 2rem;
}
</style>

