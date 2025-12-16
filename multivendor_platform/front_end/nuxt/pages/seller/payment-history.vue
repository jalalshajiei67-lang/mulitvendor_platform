<template>
  <v-container class="payment-history-page" dir="rtl">
    <h1 class="text-h5 font-weight-bold mb-6">تاریخچه پرداخت‌ها</h1>

    <!-- Filter Card -->
    <v-card class="mb-4" rounded="lg" elevation="0">
      <v-card-text class="pa-4">
        <v-row align="center">
          <v-col cols="12" md="6">
            <v-select
              v-model="statusFilter"
              label="فیلتر بر اساس وضعیت"
              :items="statusOptions"
              item-title="label"
              item-value="value"
              variant="outlined"
              density="compact"
              hide-details
              clearable
            />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Loading State -->
    <v-card v-if="loading" class="pa-8 text-center" rounded="lg" elevation="0">
      <v-progress-circular
        indeterminate
        color="primary"
        size="48"
      />
      <p class="text-subtitle-2 mt-4">در حال بارگذاری...</p>
    </v-card>

    <!-- Empty State -->
    <v-card v-else-if="payments.length === 0" class="pa-8 text-center" rounded="lg" elevation="0">
      <v-icon size="64" color="grey-lighten-1" class="mb-4">
        mdi-cash-clock
      </v-icon>
      <h3 class="text-h6 font-weight-bold mb-2">تاریخچه پرداخت خالی است</h3>
      <p class="text-body-2 text-medium-emphasis">
        هنوز پرداختی انجام نداده‌اید
      </p>
    </v-card>

    <!-- Payments List -->
    <v-card v-else rounded="lg" elevation="0">
      <v-list bg-color="transparent">
        <template v-for="(payment, index) in payments" :key="payment.id">
          <v-list-item class="payment-item pa-4">
            <template #prepend>
              <v-avatar :color="getStatusColor(payment.status)" size="48">
                <v-icon color="white" size="24">
                  {{ getStatusIcon(payment.status) }}
                </v-icon>
              </v-avatar>
            </template>

            <v-list-item-title class="font-weight-bold mb-1">
              {{ payment.billing_period_display }}
            </v-list-item-title>

            <v-list-item-subtitle class="d-flex flex-column gap-1">
              <div class="d-flex align-center gap-2">
                <v-chip size="x-small" :color="getStatusColor(payment.status)" variant="flat">
                  {{ payment.status_display }}
                </v-chip>
                <span class="text-caption">{{ formatDate(payment.created_at) }}</span>
              </div>
              
              <div v-if="payment.track_id" class="text-caption">
                کد پیگیری: {{ payment.track_id }}
              </div>
              
              <div v-if="payment.ref_number" class="text-caption">
                شماره مرجع: {{ payment.ref_number }}
              </div>
            </v-list-item-subtitle>

            <template #append>
              <div class="d-flex flex-column align-end gap-2">
                <div class="text-subtitle-1 font-weight-bold">
                  {{ formatCurrency(payment.amount_toman) }} تومان
                </div>
                <v-btn
                  v-if="payment.status === 'verified'"
                  size="small"
                  variant="tonal"
                  color="primary"
                  @click="downloadInvoice(payment.id)"
                >
                  <v-icon start size="18">mdi-download</v-icon>
                  دانلود فاکتور
                </v-btn>
              </div>
            </template>
          </v-list-item>

          <v-divider v-if="index < payments.length - 1" />
        </template>
      </v-list>

      <!-- Pagination -->
      <v-divider v-if="totalPages > 1" />
      <div v-if="totalPages > 1" class="pa-4 d-flex justify-center">
        <v-pagination
          v-model="currentPage"
          :length="totalPages"
          :total-visible="5"
          rounded="circle"
        />
      </div>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { usePaymentApi, type Payment } from '~/composables/usePaymentApi'
import { useToast } from '~/composables/useToast'

const paymentApi = usePaymentApi()
const { showToast } = useToast()

const payments = ref<Payment[]>([])
const loading = ref(true)
const statusFilter = ref<string | null>(null)
const currentPage = ref(1)
const totalPages = ref(1)

const statusOptions = [
  { label: 'همه', value: null },
  { label: 'در انتظار', value: 'pending' },
  { label: 'پرداخت شده', value: 'paid' },
  { label: 'تایید شده', value: 'verified' },
  { label: 'ناموفق', value: 'failed' },
  { label: 'لغو شده', value: 'cancelled' },
]

async function fetchPayments() {
  loading.value = true
  try {
    const response = await paymentApi.getPaymentHistory({
      status: statusFilter.value || undefined,
      page: currentPage.value,
      page_size: 10,
    })
    
    payments.value = response.results
    totalPages.value = Math.ceil(response.count / 10)
  } catch (error: any) {
    console.error('Error fetching payments:', error)
    showToast({
      message: 'خطا در بارگذاری تاریخچه پرداخت‌ها',
      color: 'error',
    })
  } finally {
    loading.value = false
  }
}

function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    pending: 'grey',
    paid: 'blue',
    verified: 'green',
    failed: 'red',
    cancelled: 'orange',
  }
  return colors[status] || 'grey'
}

function getStatusIcon(status: string): string {
  const icons: Record<string, string> = {
    pending: 'mdi-clock-outline',
    paid: 'mdi-cash-check',
    verified: 'mdi-check-circle',
    failed: 'mdi-close-circle',
    cancelled: 'mdi-cancel',
  }
  return icons[status] || 'mdi-help-circle'
}

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}

function formatCurrency(amount: number): string {
  return amount.toLocaleString('fa-IR')
}

function downloadInvoice(paymentId: number) {
  // Note: This assumes invoice_id === payment_id
  // In a real app, you might need to fetch the invoice ID from the payment
  paymentApi.downloadInvoice(paymentId)
  showToast({
    message: 'در حال دانلود فاکتور...',
    color: 'info',
  })
}

watch([statusFilter, currentPage], () => {
  fetchPayments()
})

onMounted(() => {
  fetchPayments()
})
</script>

<style scoped>
.payment-history-page {
  max-width: 1000px;
  margin: 0 auto;
}

.payment-item {
  transition: background-color 0.2s;
}

.payment-item:hover {
  background-color: rgba(0, 0, 0, 0.02);
}
</style>

