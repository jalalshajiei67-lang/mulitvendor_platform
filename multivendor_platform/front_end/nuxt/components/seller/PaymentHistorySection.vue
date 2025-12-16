<template>
  <div class="payment-history-section">
    <!-- Loading State -->
    <div v-if="loading" class="pa-8 text-center">
      <v-progress-circular
        indeterminate
        color="primary"
        size="48"
      />
      <p class="text-subtitle-2 mt-4">در حال بارگذاری...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="payments.length === 0" class="pa-12 text-center">
      <v-icon size="80" color="grey-lighten-1" class="mb-4">
        mdi-cash-clock
      </v-icon>
      <h3 class="text-h6 font-weight-bold mb-2">تاریخچه پرداخت خالی است</h3>
      <p class="text-body-2 text-medium-emphasis mb-4">
        هنوز پرداختی انجام نداده‌اید
      </p>
      <v-btn
        color="amber-darken-2"
        variant="flat"
        prepend-icon="mdi-crown"
        to="/seller/pricing"
      >
        ارتقاء به پریمیوم
      </v-btn>
    </div>

    <!-- Payments List -->
    <v-list v-else bg-color="transparent" class="py-0">
      <template v-for="(payment, index) in payments" :key="payment.id">
        <v-list-item class="payment-item pa-6">
          <template #prepend>
            <v-avatar :color="getStatusColor(payment.status)" size="56">
              <v-icon color="white" size="28">
                {{ getStatusIcon(payment.status) }}
              </v-icon>
            </v-avatar>
          </template>

          <v-list-item-title class="font-weight-bold text-h6 mb-2">
            {{ payment.billing_period_display }}
          </v-list-item-title>

          <v-list-item-subtitle class="d-flex flex-column gap-2">
            <div class="d-flex align-center gap-2">
              <v-chip size="small" :color="getStatusColor(payment.status)" variant="flat">
                {{ payment.status_display }}
              </v-chip>
              <span class="text-caption">{{ formatDate(payment.created_at) }}</span>
            </div>
            
            <div v-if="payment.track_id" class="text-caption d-flex align-center gap-1">
              <v-icon size="16">mdi-identifier</v-icon>
              <span>کد پیگیری: {{ payment.track_id }}</span>
            </div>
            
            <div v-if="payment.ref_number" class="text-caption d-flex align-center gap-1">
              <v-icon size="16">mdi-check-circle-outline</v-icon>
              <span>شماره مرجع: {{ payment.ref_number }}</span>
            </div>

            <div v-if="payment.card_number" class="text-caption d-flex align-center gap-1">
              <v-icon size="16">mdi-credit-card-outline</v-icon>
              <span>کارت: {{ payment.card_number }}</span>
            </div>
          </v-list-item-subtitle>

          <template #append>
            <div class="d-flex flex-column align-end gap-3">
              <div class="text-h6 font-weight-bold text-primary">
                {{ formatCurrency(payment.amount_toman) }} تومان
              </div>
              <v-btn
                v-if="payment.status === 'verified'"
                size="small"
                variant="tonal"
                color="primary"
                prepend-icon="mdi-download"
                @click="downloadInvoice(payment.id)"
              >
                دانلود فاکتور
              </v-btn>
            </div>
          </template>
        </v-list-item>

        <v-divider v-if="index < payments.length - 1" />
      </template>
    </v-list>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pa-4 d-flex justify-center">
      <v-pagination
        v-model="currentPage"
        :length="totalPages"
        :total-visible="7"
        rounded="circle"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { usePaymentApi, type Payment } from '~/composables/usePaymentApi'
import { useToast } from '~/composables/useToast'

const paymentApi = usePaymentApi()
const { showToast } = useToast()

const payments = ref<Payment[]>([])
const loading = ref(true)
const currentPage = ref(1)
const totalPages = ref(1)

async function fetchPayments() {
  loading.value = true
  try {
    const response = await paymentApi.getPaymentHistory({
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
  paymentApi.downloadInvoice(paymentId)
  showToast({
    message: 'در حال دانلود فاکتور...',
    color: 'info',
  })
}

watch(currentPage, () => {
  fetchPayments()
})

onMounted(() => {
  fetchPayments()
})
</script>

<style scoped>
.payment-item {
  transition: background-color 0.2s;
}

.payment-item:hover {
  background-color: rgba(0, 0, 0, 0.02);
}
</style>

