<template>
  <div dir="rtl">
    <!-- Header with Add Button -->
    <div class="d-flex align-center justify-space-between mb-4">
      <h3 class="text-h6">محصولات من</h3>
      <v-btn
        color="primary"
        prepend-icon="mdi-plus"
        @click="$emit('add-product')"
      >
        افزودن محصول جدید
      </v-btn>
    </div>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-8">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </v-row>

    <!-- Empty State -->
    <v-card v-else-if="products.length === 0" elevation="1" class="text-center pa-8">
      <v-icon size="80" color="grey-lighten-1">mdi-package-variant-closed</v-icon>
      <p class="text-h6 mt-4 mb-2">شما هنوز محصولی اضافه نکرده‌اید</p>
      <p class="text-body-2 text-grey mb-4">برای شروع، اولین محصول خود را اضافه کنید</p>
      <v-btn
        color="primary"
        size="large"
        prepend-icon="mdi-plus-circle"
        @click="$emit('add-product')"
      >
        افزودن محصول
      </v-btn>
    </v-card>

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
              <div class="text-h4 text-success font-weight-bold">{{ activeProductsCount }}</div>
              <div class="text-caption text-grey">محصولات فعال</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="4">
          <v-card elevation="1">
            <v-card-text class="text-center">
              <div class="text-h4 text-warning font-weight-bold">{{ inactiveProductsCount }}</div>
              <div class="text-caption text-grey">محصولات غیرفعال</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

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

            <template v-slot:item.is_active="{ item }">
              <v-chip
                :color="item.is_active ? 'success' : 'grey'"
                size="small"
                variant="flat"
              >
                {{ item.is_active ? 'فعال' : 'غیرفعال' }}
              </v-chip>
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

defineEmits(['add-product', 'edit-product'])

const productApi = useProductApi()

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
  { title: 'وضعیت', key: 'is_active' },
  { title: 'تاریخ ایجاد', key: 'created_at' },
  { title: 'عملیات', key: 'actions', sortable: false, align: 'center' }
]

const activeProductsCount = computed(() => {
  return products.value.filter(p => p.is_active).length
})

const inactiveProductsCount = computed(() => {
  return products.value.filter(p => !p.is_active).length
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



