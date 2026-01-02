<template>
  <div dir="rtl" class="sms-newsletter-wrapper">
    <v-container fluid class="pa-4">
      <v-card elevation="0" variant="outlined">
        <v-card-title class="d-flex align-center pa-4">
          <v-icon class="ml-2" color="primary">mdi-message-text</v-icon>
          <span>خبرنامه پیامکی فروشندگان</span>
        </v-card-title>

        <v-divider></v-divider>

        <!-- Filter Section -->
        <v-card-text class="pa-4">
          <v-row>
            <v-col cols="12" md="6">
              <v-autocomplete
                v-model="selectedWorkingFields"
                :items="subcategories"
                item-title="name"
                item-value="id"
                label="فیلتر بر اساس حوزه‌های کاری"
                placeholder="حوزه‌های کاری را انتخاب کنید"
                multiple
                chips
                closable-chips
                clearable
                variant="outlined"
                density="comfortable"
                @update:model-value="loadSellers"
              >
                <template v-slot:prepend-inner>
                  <v-icon>mdi-filter</v-icon>
                </template>
              </v-autocomplete>
            </v-col>
            <v-col cols="12" md="6" class="d-flex align-center">
              <v-btn
                color="primary"
                variant="elevated"
                size="large"
                :disabled="!hasSelectedSellers || sendingSms"
                :loading="sendingSms"
                @click="sendSmsToSelected"
                class="ml-auto"
                block
              >
                <v-icon class="ml-2">mdi-send</v-icon>
                ارسال پیامک
                <span v-if="selectedSellers.length > 0" class="mr-2">
                  ({{ selectedSellers.length }})
                </span>
              </v-btn>
            </v-col>
          </v-row>
          <v-alert
            v-if="!hasSelectedSellers && sellers.length > 0"
            type="info"
            variant="tonal"
            density="compact"
            class="mt-4"
          >
            <v-icon class="ml-2">mdi-information</v-icon>
            لطفاً فروشنده‌های مورد نظر را از لیست زیر انتخاب کنید
          </v-alert>
        </v-card-text>

        <v-divider></v-divider>

        <!-- Sellers List -->
        <v-card-text class="pa-4">
          <div v-if="loading" class="text-center py-8">
            <v-progress-circular
              indeterminate
              color="primary"
              size="64"
            ></v-progress-circular>
            <div class="mt-4 text-body-1">در حال بارگذاری...</div>
          </div>

          <div v-else-if="error" class="text-center py-8">
            <v-icon color="error" size="64">mdi-alert-circle</v-icon>
            <div class="mt-4 text-body-1 text-error">{{ error }}</div>
            <v-btn
              color="primary"
              variant="outlined"
              class="mt-4"
              @click="loadSellers"
            >
              تلاش مجدد
            </v-btn>
          </div>

          <div v-else-if="sellers.length === 0" class="text-center py-8">
            <v-icon color="grey" size="64">mdi-information</v-icon>
            <div class="mt-4 text-body-1 text-grey">
              فروشنده‌ای یافت نشد. لطفاً فیلترها را تغییر دهید.
            </div>
          </div>

          <v-table v-else>
            <thead>
              <tr>
                <th class="text-right">
                  <v-checkbox
                    v-model="selectAll"
                    @change="toggleSelectAll"
                    density="compact"
                    hide-details
                  ></v-checkbox>
                </th>
                <th class="text-right">نام فروشنده</th>
                <th class="text-right">نام شرکت</th>
                <th class="text-right">شماره موبایل</th>
                <th class="text-right">تلفن</th>
                <th class="text-right">حوزه‌های کاری</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="seller in sellers"
                :key="seller.id"
                :class="{ 'bg-grey-lighten-4': isSelected(seller.id) }"
              >
                <td>
                  <v-checkbox
                    :model-value="isSelected(seller.id)"
                    @change="toggleSeller(seller.id)"
                    density="compact"
                    hide-details
                  ></v-checkbox>
                </td>
                <td class="font-weight-medium">{{ seller.name }}</td>
                <td>{{ seller.company_name || '-' }}</td>
                <td>
                  <v-chip size="small" color="primary" variant="outlined">
                    {{ seller.mobile_number }}
                  </v-chip>
                </td>
                <td>{{ seller.phone || '-' }}</td>
                <td>
                  <div class="d-flex flex-wrap ga-1">
                    <v-chip
                      v-for="fieldId in seller.working_fields"
                      :key="fieldId"
                      size="x-small"
                      color="info"
                      variant="tonal"
                    >
                      {{ getWorkingFieldName(fieldId) }}
                    </v-chip>
                    <span v-if="seller.working_fields.length === 0" class="text-grey">
                      -
                    </span>
                  </div>
                </td>
              </tr>
            </tbody>
          </v-table>

          <!-- Mobile View -->
          <div v-if="sellers.length > 0" class="d-md-none mt-4">
            <v-card
              v-for="seller in sellers"
              :key="seller.id"
              variant="outlined"
              class="mb-4"
            >
              <v-card-text>
                <div class="d-flex align-center mb-2">
                  <v-checkbox
                    :model-value="isSelected(seller.id)"
                    @change="toggleSeller(seller.id)"
                    density="compact"
                    hide-details
                    class="mr-2"
                  ></v-checkbox>
                  <div class="font-weight-bold text-h6">{{ seller.name }}</div>
                </div>
                <v-divider class="mb-2"></v-divider>
                <div class="text-body-2 mb-1">
                  <strong>شرکت:</strong> {{ seller.company_name || '-' }}
                </div>
                <div class="text-body-2 mb-1">
                  <strong>موبایل:</strong>
                  <v-chip size="small" color="primary" variant="outlined" class="mr-1">
                    {{ seller.mobile_number }}
                  </v-chip>
                </div>
                <div class="text-body-2 mb-1">
                  <strong>تلفن:</strong> {{ seller.phone || '-' }}
                </div>
                <div class="text-body-2">
                  <strong>حوزه‌های کاری:</strong>
                  <div class="d-flex flex-wrap ga-1 mt-1">
                    <v-chip
                      v-for="fieldId in seller.working_fields"
                      :key="fieldId"
                      size="x-small"
                      color="info"
                      variant="tonal"
                    >
                      {{ getWorkingFieldName(fieldId) }}
                    </v-chip>
                    <span v-if="seller.working_fields.length === 0" class="text-grey">
                      -
                    </span>
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </div>
        </v-card-text>
      </v-card>

      <!-- Floating Action Button for Mobile -->
      <v-btn
        v-if="hasSelectedSellers && sellers.length > 0"
        class="sms-fab d-md-none"
        color="primary"
        size="large"
        :disabled="sendingSms"
        :loading="sendingSms"
        @click="sendSmsToSelected"
        icon
        elevation="8"
      >
        <v-badge
          :content="selectedSellers.length > 99 ? '99+' : selectedSellers.length"
          color="error"
          overlap
          floating
        >
          <v-icon size="28">mdi-send</v-icon>
        </v-badge>
      </v-btn>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useSmsNewsletterApi } from '~/composables/useSmsNewsletterApi'
import { useCategoryApi } from '~/composables/useCategoryApi'
import { useToast } from '~/composables/useToast'

definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

const smsApi = useSmsNewsletterApi()
const categoryApi = useCategoryApi()
const { showToast } = useToast()

// State
const sellers = ref<Array<{
  id: number
  name: string
  company_name: string | null
  mobile_number: string
  phone: string | null
  working_fields: number[]
  working_fields_display: string
}>>([])
const subcategories = ref<Array<{ id: number; name: string }>>([])
const selectedWorkingFields = ref<number[]>([])
const selectedSellers = ref<number[]>([])
const loading = ref(false)
const sendingSms = ref(false)
const error = ref<string | null>(null)

// Computed
const selectAll = computed({
  get: () => sellers.value.length > 0 && selectedSellers.value.length === sellers.value.length,
  set: (value: boolean) => {
    if (value) {
      selectedSellers.value = sellers.value.map(s => s.id)
    } else {
      selectedSellers.value = []
    }
  }
})

const hasSelectedSellers = computed(() => selectedSellers.value.length > 0)

// Methods
const loadSubcategories = async () => {
  try {
    const response = await categoryApi.getSubcategories({ is_active: true })
    if (response.data?.results) {
      subcategories.value = response.data.results.map((sc: any) => ({
        id: sc.id,
        name: sc.name
      }))
    }
  } catch (err: any) {
    console.error('Failed to load subcategories:', err)
    showToast({
      message: 'خطا در بارگذاری حوزه‌های کاری',
      color: 'error'
    })
  }
}

const loadSellers = async () => {
  loading.value = true
  error.value = null
  
  try {
    const workingFieldIds = selectedWorkingFields.value.length > 0
      ? selectedWorkingFields.value
      : undefined
    
    const response = await smsApi.getSellers(workingFieldIds)
    
    if (response.data?.results) {
      sellers.value = response.data.results
      // Clear selection when filters change
      selectedSellers.value = []
    } else {
      sellers.value = []
    }
  } catch (err: any) {
    console.error('Failed to load sellers:', err)
    error.value = err.message || 'خطا در بارگذاری فروشندگان'
    showToast({
      message: 'خطا در بارگذاری فروشندگان',
      color: 'error'
    })
  } finally {
    loading.value = false
  }
}

const toggleSeller = (sellerId: number) => {
  const index = selectedSellers.value.indexOf(sellerId)
  if (index > -1) {
    selectedSellers.value.splice(index, 1)
  } else {
    selectedSellers.value.push(sellerId)
  }
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedSellers.value = []
  } else {
    selectedSellers.value = sellers.value.map(s => s.id)
  }
}

const isSelected = (sellerId: number) => {
  return selectedSellers.value.includes(sellerId)
}

const getWorkingFieldName = (fieldId: number) => {
  const field = subcategories.value.find(sc => sc.id === fieldId)
  return field?.name || `ID: ${fieldId}`
}

const sendSmsToSelected = async () => {
  if (selectedSellers.value.length === 0) {
    showToast({
      message: 'لطفاً حداقل یک فروشنده را انتخاب کنید',
      color: 'warning'
    })
    return
  }

  sendingSms.value = true
  
  try {
    const workingFieldIds = selectedWorkingFields.value.length > 0
      ? selectedWorkingFields.value
      : undefined
    
    const response = await smsApi.sendSms(selectedSellers.value, workingFieldIds)
    
    if (response.data) {
      const { success_count, failure_count, results } = response.data
      
      if (failure_count === 0) {
        showToast({
          message: `پیامک با موفقیت به ${success_count} فروشنده ارسال شد`,
          color: 'success'
        })
        // Clear selection after successful send
        selectedSellers.value = []
      } else {
        const failedSellers = results
          .filter((r: any) => !r.success)
          .map((r: any) => r.seller_name)
          .join(', ')
        
        showToast({
          message: `${success_count} پیامک ارسال شد، ${failure_count} مورد ناموفق. ناموفق: ${failedSellers}`,
          color: 'warning',
          timeout: 6000
        })
      }
    }
  } catch (err: any) {
    console.error('Failed to send SMS:', err)
    showToast({
      message: err.message || 'خطا در ارسال پیامک',
      color: 'error'
    })
  } finally {
    sendingSms.value = false
  }
}

// Watch for filter changes
watch(selectedWorkingFields, () => {
  loadSellers()
})

// Lifecycle
onMounted(async () => {
  await loadSubcategories()
  await loadSellers()
})
</script>

<style scoped>
.sms-newsletter-wrapper {
  min-height: 100vh;
  padding-top: 80px;
}

.sms-fab {
  position: fixed;
  bottom: 80px;
  right: 16px;
  z-index: 1000;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  box-shadow: 0 8px 24px rgba(25, 118, 210, 0.4), 
              0 4px 8px rgba(0, 0, 0, 0.2) !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.sms-fab:hover {
  transform: scale(1.08);
  box-shadow: 0 12px 32px rgba(25, 118, 210, 0.5), 
              0 6px 12px rgba(0, 0, 0, 0.3) !important;
}

.sms-fab:active {
  transform: scale(0.95);
}

@media (max-width: 960px) {
  .sms-newsletter-wrapper {
    padding-top: 72px;
  }
}

@media (max-width: 600px) {
  .sms-newsletter-wrapper {
    padding-top: 72px;
  }
  
  .sms-fab {
    bottom: 16px;
    right: 16px;
  }
}
</style>

