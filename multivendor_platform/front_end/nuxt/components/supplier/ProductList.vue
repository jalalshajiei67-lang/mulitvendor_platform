<template>
  <div dir="rtl">
    <!-- Header with Add Button -->
    <div class="d-flex align-center justify-space-between mb-4">
      <h3 class="text-h6">محصولات من</h3>
      <v-btn
        color="primary"
        prepend-icon="mdi-plus"
        @click="$emit('add-product')"
        data-tour="add-product-btn"
      >
        افزودن محصول جدید
      </v-btn>
    </div>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-8">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </v-row>

    <!-- Product Upload Request Form (when no products) -->
    <ProductUploadRequestForm v-else-if="products.length === 0" />

    <!-- Products Grid -->
    <div v-else>
      <!-- Stats Summary -->
      <v-row class="mb-4">
        <v-col cols="12" sm="4">
          <v-card elevation="1">
            <v-card-text class="text-center">
              <div class="text-h4 text-primary font-weight-bold">{{ products.length }}</div>
              <div class="text-caption text-grey">کل محصولات</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="4">
          <v-card elevation="1">
            <v-card-text class="text-center">
              <div class="text-h4 text-success font-weight-bold">{{ approvedProductsCount }}</div>
              <div class="text-caption text-grey">تایید شده / فعال</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="4">
          <v-card elevation="1">
            <v-card-text class="text-center">
              <div class="text-h4 text-warning font-weight-bold">{{ pendingProductsCount }}</div>
              <div class="text-caption text-grey">در انتظار تایید ادمین</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-alert
        type="info"
        variant="tonal"
        color="warning"
        class="mb-4"
        border="start"
        elevation="0"
      >
        همه محصولات جدید ابتدا در حالت «در انتظار تایید» قرار می‌گیرند و پس از تایید ادمین فعال می‌شوند. وضعیت هر محصول در ستون «تایید» قابل مشاهده است.
      </v-alert>
    <v-alert
      v-if="hiddenProductsCount > 0"
      type="warning"
      variant="tonal"
      color="error"
      class="mb-4"
      border="start"
      elevation="0"
    >
      <div class="font-weight-bold mb-1">چند محصول از مارکت‌پلیس مخفی شده‌اند</div>
      <div class="text-body-2">
        دلیل نمونه: {{ firstHiddenReason }}
      </div>
      <div class="text-caption mt-1 text-medium-emphasis">
        تصویر و توضیحات را بدون واترمارک یا اطلاعات فروشنده بارگذاری کنید تا دوباره نمایش داده شود.
      </div>
    </v-alert>

      <!-- Products Data Table -->
      <v-card elevation="2">
        <v-card-text>
          <v-data-table
            :headers="headers"
            :items="products"
            :items-per-page="10"
            item-value="id"
            class="elevation-0"
          >
            <template v-slot:item.image="{ item }">
              <v-avatar size="60" rounded="lg" class="ma-2">
                <v-img
                  :src="getProductImage(item)"
                  :alt="item.name"
                  cover
                >
                  <template v-slot:placeholder>
                    <v-icon>mdi-image</v-icon>
                  </template>
                </v-img>
              </v-avatar>
            </template>

            <template v-slot:item.name="{ item }">
              <div>
                <div class="font-weight-bold">{{ item.name }}</div>
                <div class="text-caption text-grey">{{ item.slug }}</div>
              </div>
            </template>

            <template v-slot:item.price="{ item }">
              <span class="font-weight-medium">{{ formatPrice(item.price) }} تومان</span>
            </template>

            <template v-slot:item.stock="{ item }">
              <v-chip
                :color="item.stock > 0 ? 'success' : 'error'"
                size="small"
                variant="flat"
              >
                {{ item.stock }} عدد
              </v-chip>
            </template>

            <template v-slot:item.approval_status="{ item }">
              <v-chip
                :color="approvalChipColor(item.approval_status)"
                size="small"
                variant="flat"
              >
                {{ approvalChipLabel(item.approval_status) }}
              </v-chip>
            </template>

            <template v-slot:item.is_active="{ item }">
              <div class="d-flex flex-column gap-1">
                <v-chip
                  :color="item.is_active ? 'success' : 'grey'"
                  size="small"
                  variant="flat"
                >
                  {{ item.is_active ? 'فعال' : 'غیرفعال' }}
                </v-chip>
                <v-chip
                  v-if="item.is_marketplace_hidden"
                  size="small"
                  color="warning"
                  variant="tonal"
                  prepend-icon="mdi-eye-off-outline"
                >
                  مخفی توسط ادمین
                  <v-tooltip activator="parent" location="top">
                    {{ item.marketplace_hide_reason || 'به دلیل واترمارک یا اطلاعات فروشنده مخفی شده است.' }}
                  </v-tooltip>
                </v-chip>
              </div>
            </template>

            <template v-slot:item.created_at="{ item }">
              <span class="text-caption">{{ formatDate(item.created_at) }}</span>
            </template>

            <template v-slot:item.actions="{ item }">
              <div class="d-flex gap-1">
                <v-btn
                  icon="mdi-eye"
                  size="small"
                  variant="text"
                  color="info"
                  @click="viewProduct(item)"
                >
                  <v-icon>mdi-eye</v-icon>
                  <v-tooltip activator="parent" location="top">مشاهده</v-tooltip>
                </v-btn>
                <v-btn
                  icon="mdi-pencil"
                  size="small"
                  variant="text"
                  color="primary"
                  @click="$emit('edit-product', item)"
                >
                  <v-icon>mdi-pencil</v-icon>
                  <v-tooltip activator="parent" location="top">ویرایش</v-tooltip>
                </v-btn>
                <v-btn
                  icon="mdi-delete"
                  size="small"
                  variant="text"
                  color="error"
                  @click="confirmDelete(item)"
                >
                  <v-icon>mdi-delete</v-icon>
                  <v-tooltip activator="parent" location="top">حذف</v-tooltip>
                </v-btn>
              </div>
            </template>
          </v-data-table>
        </v-card-text>
      </v-card>
    </div>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h6 bg-error text-white">
          <v-icon start>mdi-alert</v-icon>
          تایید حذف
        </v-card-title>
        <v-card-text class="pt-4">
          <p class="text-body-1">آیا از حذف محصول زیر اطمینان دارید؟</p>
          <p class="text-h6 mt-2 font-weight-bold text-primary">{{ productToDelete?.name }}</p>
          <v-alert type="warning" variant="tonal" class="mt-4">
            این عملیات قابل بازگشت نیست!
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="deleteDialog = false" variant="text">انصراف</v-btn>
          <v-btn
            color="error"
            variant="elevated"
            :loading="deleting"
            @click="deleteProduct"
          >
            حذف محصول
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Success Snackbar -->
    <v-snackbar
      v-model="snackbar"
      :color="snackbarColor"
      :timeout="3000"
      location="top"
    >
      {{ snackbarMessage }}
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useProductApi } from '~/composables/useProductApi'
import { useGamificationStore } from '~/stores/gamification'
import EmptyState from '~/components/common/EmptyState.vue'
import ProductUploadRequestForm from '~/components/supplier/ProductUploadRequestForm.vue'

defineEmits(['add-product', 'edit-product'])

const productApi = useProductApi()
const gamificationStore = useGamificationStore()

const products = ref<any[]>([])
const loading = ref(false)
const deleting = ref(false)
const deleteDialog = ref(false)
const productToDelete = ref<any>(null)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const headers = [
  { title: 'تصویر', key: 'image', sortable: false },
  { title: 'نام محصول', key: 'name' },
  { title: 'قیمت', key: 'price' },
  { title: 'موجودی', key: 'stock' },
  { title: 'تایید', key: 'approval_status' },
  { title: 'وضعیت', key: 'is_active' },
  { title: 'تاریخ ایجاد', key: 'created_at' },
  { title: 'عملیات', key: 'actions', sortable: false, align: 'center' }
]

const approvedProductsCount = computed(() => {
  return products.value.filter(p => p.approval_status === 'approved').length
})

const pendingProductsCount = computed(() => {
  return products.value.filter(p => p.approval_status === 'pending').length
})

const hiddenProductsCount = computed(() => {
  return products.value.filter(p => p.is_marketplace_hidden).length
})

const firstHiddenReason = computed(() => {
  const hidden = products.value.find(p => p.is_marketplace_hidden)
  if (!hidden) return ''
  return hidden.marketplace_hide_reason || 'لطفاً واترمارک و اطلاعات فروشنده را از تصویر/توضیحات حذف کنید.'
})

const productGamificationContext = computed(() => {
  return {
    message: 'افزودن اولین محصول خود را اضافه کنید تا +20 امتیاز دریافت کنید!',
    subtitle: 'محصولات با کیفیت بالا امتیاز بیشتری دریافت می‌کنند',
    color: 'primary',
    points: 20,
  }
})

const loadProducts = async () => {
  loading.value = true
  try {
    const response = await productApi.getMyProducts()
    products.value = response.results || []
  } catch (error) {
    console.error('Error loading products:', error)
    showSnackbar('خطا در بارگذاری محصولات', 'error')
  } finally {
    loading.value = false
  }
}

const getProductImage = (product: any) => {
  if (product.images && product.images.length > 0) {
    return product.images[0].image
  }
  if (product.image) {
    return product.image
  }
  return '/placeholder-product.jpg'
}

const formatPrice = (price: string | number) => {
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  return new Intl.NumberFormat('fa-IR').format(numPrice)
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(date)
}

const approvalChipColor = (status: string) => {
  if (status === 'approved') return 'success'
  if (status === 'rejected') return 'error'
  return 'warning'
}

const approvalChipLabel = (status: string) => {
  if (status === 'approved') return 'تایید شده'
  if (status === 'rejected') return 'رد شده'
  return 'در انتظار تایید'
}

const viewProduct = (product: any) => {
  // Navigate to product detail page
  const slug = product.slug || product.id
  navigateTo(`/products/${slug}`)
}

const confirmDelete = (product: any) => {
  productToDelete.value = product
  deleteDialog.value = true
}

const deleteProduct = async () => {
  if (!productToDelete.value) return

  deleting.value = true
  try {
    await productApi.deleteProduct(productToDelete.value.id)
    showSnackbar('محصول با موفقیت حذف شد', 'success')
    deleteDialog.value = false
    productToDelete.value = null
    await loadProducts()
  } catch (error) {
    console.error('Error deleting product:', error)
    showSnackbar('خطا در حذف محصول', 'error')
  } finally {
    deleting.value = false
  }
}

const showSnackbar = (message: string, color = 'success') => {
  snackbarMessage.value = message
  snackbarColor.value = color
  snackbar.value = true
}

// Expose refresh method for parent component
defineExpose({
  loadProducts
})

onMounted(() => {
  loadProducts()
})
</script>

<style scoped>
.v-data-table {
  direction: rtl;
}
</style>







